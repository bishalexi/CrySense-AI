"""Visualizer & HUD Rendering Module.
Provides high-tech, futuristic HUD overlays for real-time face and emotion recognition.
Includes corner brackets, dynamic color themes, emotion probability meters, and performance telemetry.
"""

import cv2
import numpy as np


class EmotionVisualizer:
    def __init__(self, show_bars: bool = True, show_telemetry: bool = True):
        self.show_bars = show_bars
        self.show_telemetry = show_telemetry
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def _draw_corner_brackets(self, img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple, length: int = 15, thickness: int = 2):
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Ensure bracket length doesn't exceed half box dimension
        length = min(length, (x2 - x1) // 3, (y2 - y1) // 3)
        if length < 4:
            length = 4
            
        # Top-Left
        cv2.line(img, (x1, y1), (x1 + length, y1), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x1, y1), (x1, y1 + length), color, thickness, cv2.LINE_AA)
        
        # Top-Right
        cv2.line(img, (x2, y1), (x2 - length, y1), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x2, y1), (x2, y1 + length), color, thickness, cv2.LINE_AA)
        
        # Bottom-Left
        cv2.line(img, (x1, y2), (x1 + length, y2), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x1, y2), (x1, y2 - length), color, thickness, cv2.LINE_AA)
        
        # Bottom-Right
        cv2.line(img, (x2, y2), (x2 - length, y2), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x2, y2), (x2, y2 - length), color, thickness, cv2.LINE_AA)

    def draw_detections(self, frame: np.ndarray, results: list, fps: float = 0.0, latency_ms: float = 0.0) -> np.ndarray:
        """Renders detections, emotion tags, and probability bars onto frame."""
        canvas = frame.copy()
        h, w = canvas.shape[:2]
        
        for item in results:
            box = item["box"]
            x1, y1, x2, y2 = box
            emotion_data = item.get("emotion", {})
            dom_emotion = emotion_data.get("dominant_emotion", "Neutral")
            conf = emotion_data.get("confidence", 0.0)
            color = emotion_data.get("color", (180, 180, 180))
            probs = emotion_data.get("probabilities", {})
            
            # 1. Subtle bounding box with glowing corners
            # Semi-transparent inner tint
            overlay = canvas.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 1)
            cv2.addWeighted(overlay, 0.4, canvas, 0.6, 0, canvas)
            
            # Corner targeting brackets
            self._draw_corner_brackets(canvas, (x1, y1), (x2, y2), color, length=20, thickness=2)
            
            # 2. Emotion Badge Header
            badge_text = f"{dom_emotion.upper()} {int(conf * 100)}%"
            (tw, th), _ = cv2.getTextSize(badge_text, self.font, 0.55, 1)
            
            badge_y1 = max(0, y1 - th - 12)
            badge_y2 = max(th + 12, y1)
            badge_x1 = x1
            badge_x2 = min(w, x1 + tw + 18)
            
            # Dark pill background for text
            pill_overlay = canvas.copy()
            cv2.rectangle(pill_overlay, (badge_x1, badge_y1), (badge_x2, badge_y2), (20, 20, 25), -1)
            cv2.addWeighted(pill_overlay, 0.75, canvas, 0.25, 0, canvas)
            
            # Accent line on left of badge
            cv2.rectangle(canvas, (badge_x1, badge_y1), (badge_x1 + 3, badge_y2), color, -1)
            
            # Text inside badge
            cv2.putText(canvas, badge_text, (badge_x1 + 10, badge_y2 - 6),
                        self.font, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
            
            # 3. Floating Probability Bars (if enabled and space permits)
            if self.show_bars and probs:
                bar_w = 110
                bar_h = 10
                bar_gap = 4
                num_items = len(probs)
                total_panel_h = num_items * (bar_h + bar_gap) + 12
                
                # Position beside box if fits, else below
                if x2 + bar_w + 30 < w:
                    px = x2 + 10
                    py = max(10, y1)
                elif x1 - bar_w - 30 > 0:
                    px = x1 - bar_w - 20
                    py = max(10, y1)
                else:
                    px = x1
                    py = min(h - total_panel_h, y2 + 10)
                    
                panel_overlay = canvas.copy()
                cv2.rectangle(panel_overlay, (px - 5, py - 5), (px + bar_w + 55, py + total_panel_h), (15, 15, 20), -1)
                cv2.addWeighted(panel_overlay, 0.7, canvas, 0.3, 0, canvas)
                
                for idx, (emo, p) in enumerate(probs.items()):
                    item_y = py + idx * (bar_h + bar_gap) + 8
                    emo_color = emotion_data.get("color_map", {}).get(emo, (150, 150, 150))
                    
                    # Label abbreviation
                    cv2.putText(canvas, emo[:4], (px, item_y + bar_h - 2),
                                self.font, 0.32, (200, 200, 200), 1, cv2.LINE_AA)
                    
                    # Background slot
                    bx = px + 32
                    cv2.rectangle(canvas, (bx, item_y), (bx + bar_w, item_y + bar_h), (45, 45, 55), -1)
                    
                    # Fill slot
                    fill_len = int(bar_w * np.clip(p, 0.0, 1.0))
                    if fill_len > 0:
                        cv2.rectangle(canvas, (bx, item_y), (bx + fill_len, item_y + bar_h), emo_color, -1)
                        
                    # Percent text
                    p_str = f"{int(p * 100)}%"
                    cv2.putText(canvas, p_str, (bx + bar_w + 4, item_y + bar_h - 2),
                                self.font, 0.30, (220, 220, 220), 1, cv2.LINE_AA)

        # 4. Top Telemetry Banner
        if self.show_telemetry:
            header_overlay = canvas.copy()
            cv2.rectangle(header_overlay, (0, 0), (w, 36), (12, 14, 18), -1)
            cv2.addWeighted(header_overlay, 0.85, canvas, 0.15, 0, canvas)
            
            # Title
            cv2.putText(canvas, "ULTRA-LIGHT FACE & EMOTION AI", (14, 23),
                        self.font, 0.55, (0, 220, 255), 1, cv2.LINE_AA)
                        
            # System Metrics on the right
            metrics_str = f"FPS: {fps:4.1f} | Latency: {latency_ms:4.1f}ms | Faces: {len(results)}"
            (mw, _), _ = cv2.getTextSize(metrics_str, self.font, 0.45, 1)
            cv2.putText(canvas, metrics_str, (w - mw - 15, 23),
                        self.font, 0.45, (160, 220, 160), 1, cv2.LINE_AA)
                        
            # Accent bottom border for banner
            cv2.line(canvas, (0, 36), (w, 36), (0, 180, 230), 1)

        return canvas
