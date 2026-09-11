"""Facial Emotion Recognition Classifier Module.
Uses OpenCV DNN engine running the ONNX Model Zoo Emotion-FERPlus-8 model.
Recognizes: Neutral, Happiness, Surprise, Sadness, Anger, Disgust, Fear, Contempt.
Includes temporal probability smoothing for flicker-free real-time video inference.
"""

import os
import cv2
import numpy as np


class EmotionClassifier:
    EMOTIONS = [
        "Neutral",
        "Happy",
        "Surprise",
        "Sad",
        "Angry",
        "Disgust",
        "Fear",
        "Contempt"
    ]
    
    EMOTION_COLORS = {
        "Neutral": (180, 180, 180),    # Soft Slate Gray
        "Happy": (80, 220, 100),       # Vibrant Emerald Green
        "Surprise": (40, 200, 255),    # Electric Amber/Orange
        "Sad": (230, 140, 60),         # Steel Blue (BGR)
        "Angry": (60, 60, 240),        # Vivid Crimson Red
        "Disgust": (60, 180, 140),     # Muted Olive / Sea Green
        "Fear": (200, 100, 180),       # Mystic Violet / Purple
        "Contempt": (140, 100, 230)    # Coral Pink
    }

    def __init__(self, model_path: str = None, smoothing_alpha: float = 0.6):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "emotion-ferplus-8.onnx")
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}. Run download_models.py first.")
            
        # Initialize OpenCV DNN network
        self.net = cv2.dnn.readNetFromONNX(model_path)
        self.out_name = self.net.getUnconnectedOutLayersNames()[0]
        
        # Temporal smoothing coefficient (1.0 = no smoothing, lower = smoother)
        self.smoothing_alpha = smoothing_alpha
        self.prev_probs = None

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x - np.max(x))
        return e_x / (e_x.sum(axis=-1, keepdims=True) + 1e-7)

    def _preprocess(self, face_bgr: np.ndarray) -> np.ndarray:
        if len(face_bgr.shape) == 3 and face_bgr.shape[2] == 3:
            gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        else:
            gray = face_bgr
            
        # Use blobFromImage for 64x64 grayscale
        blob = cv2.dnn.blobFromImage(
            gray,
            scalefactor=1.0,
            size=(64, 64),
            mean=0.0,
            swapRB=False,
            crop=False
        )
        return blob

    def predict(self, face_bgr: np.ndarray) -> dict:
        """Predicts emotion probabilities for a face crop.
        
        Returns:
            dict containing:
                - dominant_emotion: str (e.g. 'Happy')
                - confidence: float (0.0 to 1.0)
                - probabilities: dict of {emotion_name: probability}
                - color: tuple (B, G, R)
        """
        if face_bgr.size == 0 or face_bgr.shape[0] < 8 or face_bgr.shape[1] < 8:
            return {
                "dominant_emotion": "Neutral",
                "confidence": 0.0,
                "probabilities": {e: 1.0 / len(self.EMOTIONS) for e in self.EMOTIONS},
                "color": self.EMOTION_COLORS["Neutral"]
            }
            
        blob = self._preprocess(face_bgr)
        self.net.setInput(blob)
        raw_output = self.net.forward(self.out_name)
        
        # Softmax over logits
        probs = self._softmax(raw_output)[0]
        
        # Temporal smoothing
        if self.prev_probs is not None:
            probs = self.smoothing_alpha * probs + (1.0 - self.smoothing_alpha) * self.prev_probs
        self.prev_probs = probs
        
        top_idx = int(np.argmax(probs))
        dominant_emotion = self.EMOTIONS[top_idx]
        confidence = float(probs[top_idx])
        
        prob_dict = {self.EMOTIONS[i]: float(probs[i]) for i in range(len(self.EMOTIONS))}
        
        return {
            "dominant_emotion": dominant_emotion,
            "confidence": confidence,
            "probabilities": prob_dict,
            "color": self.EMOTION_COLORS.get(dominant_emotion, (200, 200, 200))
        }

    def reset_smoothing(self):
        self.prev_probs = None
