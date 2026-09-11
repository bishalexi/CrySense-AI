"""Ultra-Lightweight Face Detection (Slim 320) Inference Module.
Uses OpenCV DNN (or ONNX Runtime) with anchor decoding and Non-Maximum Suppression.
Optimized for high-speed edge computing and real-time webcam streams.
"""

from math import ceil
import os
import cv2
import numpy as np


class UltraLightFaceDetector:
    def __init__(self, model_path: str = None, conf_threshold: float = 0.7, iou_threshold: float = 0.3):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "version-slim-320.onnx")
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}. Run download_models.py first.")
            
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.input_size = (320, 240)  # (width, height)
        
        # Load model using OpenCV DNN
        self.net = cv2.dnn.readNetFromONNX(model_path)
        self.out_names = ["scores", "boxes"]
        
        # Hyperparameters for SSD prior anchor generation
        self.strides = [8.0, 16.0, 32.0, 64.0]
        self.min_boxes = [
            [10.0, 16.0, 24.0],
            [32.0, 48.0],
            [64.0, 96.0],
            [128.0, 192.0, 256.0]
        ]
        self.center_variance = 0.1
        self.size_variance = 0.2
        self.image_mean = (127, 127, 127)
        self.image_scale = 1.0 / 128.0
        
        # Precompute priors for 320x240
        self.priors = self._generate_priors()

    def _generate_priors(self) -> np.ndarray:
        w, h = self.input_size
        feature_map_w = [int(ceil(w / stride)) for stride in self.strides]
        feature_map_h = [int(ceil(h / stride)) for stride in self.strides]
        
        priors = []
        for level in range(len(self.strides)):
            scale_w = w / self.strides[level]
            scale_h = h / self.strides[level]
            
            for j in range(feature_map_h[level]):
                for i in range(feature_map_w[level]):
                    cx = (i + 0.5) / scale_w
                    cy = (j + 0.5) / scale_h
                    
                    for min_box in self.min_boxes[level]:
                        bw = min_box / w
                        bh = min_box / h
                        priors.append([cx, cy, bw, bh])
                        
        priors = np.array(priors, dtype=np.float32)
        # Shape: (4420, 4)
        return priors

    def _decode_boxes(self, raw_boxes: np.ndarray) -> np.ndarray:
        # raw_boxes shape: (N, 4)
        cx = self.priors[:, 0] + raw_boxes[:, 0] * self.center_variance * self.priors[:, 2]
        cy = self.priors[:, 1] + raw_boxes[:, 1] * self.center_variance * self.priors[:, 3]
        bw = self.priors[:, 2] * np.exp(raw_boxes[:, 2] * self.size_variance)
        bh = self.priors[:, 3] * np.exp(raw_boxes[:, 3] * self.size_variance)
        
        x1 = cx - bw / 2.0
        y1 = cy - bh / 2.0
        x2 = cx + bw / 2.0
        y2 = cy + bh / 2.0
        
        decoded = np.stack([x1, y1, x2, y2], axis=-1)
        return np.clip(decoded, 0.0, 1.0)

    def _hard_nms(self, boxes: np.ndarray, scores: np.ndarray) -> list:
        if len(boxes) == 0:
            return []
            
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        
        order = scores.argsort()[::-1]
        keep = []
        
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            
            ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
            inds = np.where(ovr <= self.iou_threshold)[0]
            order = order[inds + 1]
            
        return keep

    def detect(self, frame: np.ndarray):
        """Runs face detection on an OpenCV BGR frame.
        
        Returns:
            list of dict: [
                {
                    "box": [x1, y1, x2, y2],  # Pixel coordinates in original frame
                    "norm_box": [nx1, ny1, nx2, ny2],  # Normalized [0, 1]
                    "score": float  # Confidence score
                }
            ]
        """
        orig_h, orig_w = frame.shape[:2]
        
        # Preprocess input using OpenCV DNN blobFromImage (RGB format, mean subtraction, scaling)
        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=self.image_scale,
            size=self.input_size,
            mean=self.image_mean,
            swapRB=True,
            crop=False
        )
        
        self.net.setInput(blob)
        scores, raw_boxes = self.net.forward(self.out_names)
        
        scores = scores[0]  # (4420, 2)
        raw_boxes = raw_boxes[0]  # (4420, 4)
        
        face_scores = scores[:, 1]
        mask = face_scores > self.conf_threshold
        
        if not np.any(mask):
            return []
            
        decoded_boxes = self._decode_boxes(raw_boxes)
        filtered_boxes = decoded_boxes[mask]
        filtered_scores = face_scores[mask]
        
        keep_indices = self._hard_nms(filtered_boxes, filtered_scores)
        
        detections = []
        for idx in keep_indices:
            box = filtered_boxes[idx]
            score = float(filtered_scores[idx])
            
            px1 = int(max(0, box[0] * orig_w))
            py1 = int(max(0, box[1] * orig_h))
            px2 = int(min(orig_w, box[2] * orig_w))
            py2 = int(min(orig_h, box[3] * orig_h))
            
            if px2 - px1 > 4 and py2 - py1 > 4:
                detections.append({
                    "box": [px1, py1, px2, py2],
                    "norm_box": [float(box[0]), float(box[1]), float(box[2]), float(box[3])],
                    "score": score
                })
                
        return detections
