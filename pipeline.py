"""Integrated Real-Time Face Detection & Emotion Recognition Pipeline.
Combines Ultra-Light-Fast Face Detector (Slim 320) with Emotion-FERPlus Classifier.
"""

import time
import cv2
import numpy as np

from face_detector import UltraLightFaceDetector
from emotion_classifier import EmotionClassifier
from visualizer import EmotionVisualizer


class EmotionPipeline:
    def __init__(
        self,
        face_model_path: str = None,
        emotion_model_path: str = None,
        conf_threshold: float = 0.7,
        iou_threshold: float = 0.3,
        smoothing_alpha: float = 0.6,
        padding_ratio: float = 0.15,
        show_bars: bool = True,
        show_telemetry: bool = True
    ):
        self.detector = UltraLightFaceDetector(
            model_path=face_model_path,
            conf_threshold=conf_threshold,
            iou_threshold=iou_threshold
        )
        self.classifier = EmotionClassifier(
            model_path=emotion_model_path,
            smoothing_alpha=smoothing_alpha
        )
        self.visualizer = EmotionVisualizer(
            show_bars=show_bars,
            show_telemetry=show_telemetry
        )
        self.padding_ratio = padding_ratio
        
        # FPS tracker
        self.prev_time = time.time()
        self.fps = 0.0

    def _crop_face_with_padding(self, frame: np.ndarray, box: list) -> np.ndarray:
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = box
        bw = x2 - x1
        bh = y2 - y1
        
        pad_x = int(bw * self.padding_ratio)
        pad_y = int(bh * self.padding_ratio)
        
        cx1 = max(0, x1 - pad_x)
        cy1 = max(0, y1 - pad_y)
        cx2 = min(w, x2 + pad_x)
        cy2 = min(h, y2 + pad_y)
        
        crop = frame[cy1:cy2, cx1:cx2]
        return crop

    def process_frame(self, frame: np.ndarray, annotate: bool = True):
        """Processes a single BGR frame.
        
        Returns:
            annotated_frame (np.ndarray): The rendered frame with HUD (if annotate=True)
            results (list): List of detection and emotion records
            latency_ms (float): Inference execution time in milliseconds
        """
        start_time = time.time()
        
        # 1. Face Detection
        detections = self.detector.detect(frame)
        
        # 2. Emotion Recognition on each face crop
        results = []
        for det in detections:
            box = det["box"]
            face_crop = self._crop_face_with_padding(frame, box)
            
            emotion_res = self.classifier.predict(face_crop)
            emotion_res["color_map"] = self.classifier.EMOTION_COLORS
            
            results.append({
                "box": box,
                "norm_box": det["norm_box"],
                "det_score": det["score"],
                "emotion": emotion_res
            })
            
        latency_ms = (time.time() - start_time) * 1000.0
        
        # Calculate smoothed FPS
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        current_fps = (1.0 / dt) if dt > 0 else 0.0
        self.fps = 0.9 * self.fps + 0.1 * current_fps if self.fps > 0 else current_fps
        
        # 3. Visualization
        if annotate:
            annotated_frame = self.visualizer.draw_detections(
                frame, results, fps=self.fps, latency_ms=latency_ms
            )
        else:
            annotated_frame = frame
            
        return annotated_frame, results, latency_ms
