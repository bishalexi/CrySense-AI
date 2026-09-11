"""Baby Cry Acoustic Classifier Module.
Extracts 194-dimension spectral features (MFCC, Chroma, Mel, Spectral Contrast, Tonnetz)
and predicts the underlying infant distress cause with calibrated probabilities.
Includes pediatric caregiver guidance and first-person empathetic baby messages.
"""

import os
import io
import warnings
import numpy as np
import soundfile as sf
import joblib

warnings.filterwarnings("ignore", category=UserWarning)


def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    e_x = np.exp((x - np.max(x)) / temperature)
    return e_x / np.sum(e_x)


ADVICE_DATABASE = {
    "hungry": {
        "title": "Hunger Cry (Feeding Needed)",
        "icon": "🍼",
        "color": "#f59e0b",
        "baby_message": "Mommy & Daddy, my little tummy feels so empty and rumbling! I am growing every single day and my body is asking for milk right now. Please hold me close and let me nurse or enjoy a warm bottle.",
        "soothing_checklist": [
            "Check time since last feed (newborns feed every 2 to 3 hours).",
            "Offer breast milk or warm formula in a calm, low-light environment.",
            "Ensure proper latch or bottle angle to minimize swallowed air.",
            "Burp midway through and at the end of feeding."
        ]
    },
    "burping": {
        "title": "Burping Needed (Upper Gas Bubble)",
        "icon": "💨",
        "color": "#06b6d4",
        "baby_message": "There is a sneaky air bubble trapped in my chest after drinking my milk! It feels uncomfortable whenever I lie down flat. Please hold me upright over your shoulder and gently pat my back so I can let out that big burp!",
        "soothing_checklist": [
            "Over-the-shoulder hold: Place baby upright on your chest, gently patting the upper back.",
            "Sitting on lap: Support baby's chin/chest leaning slightly forward with rhythmic upward back rubs.",
            "Keep upright for 15-20 minutes post-feed to encourage natural air release."
        ]
    },
    "belly_pain": {
        "title": "Belly Pain (Colic & Lower Gas)",
        "icon": "🩹",
        "color": "#ef4444",
        "baby_message": "My little tummy really cramps and hurts inside! I have stubborn gas bubbles that I cannot push out on my own. Please tuck my knees up, bicycle my legs gently, and warm my tummy with gentle clockwise rubs.",
        "soothing_checklist": [
            "Bicycle kicks: Gently pump baby's legs in a pedaling motion toward the belly to release gas.",
            "Clockwise abdominal massage ('I Love You' stroke) to follow the colon path.",
            "Colic carry: Hold baby face-down resting across your forearm with gentle pressure on the abdomen.",
            "Warm compress or relaxing warm bath to ease abdominal cramping."
        ]
    },
    "discomfort": {
        "title": "Discomfort (Diaper / Temperature / Clothes)",
        "icon": "👶",
        "color": "#8b5cf6",
        "baby_message": "Something is tickling, pinching, or bothering my sensitive skin! Maybe my diaper is wet, or my clothes are feeling too warm, tight, or scratchy. Please check on me and make me snug and cozy again.",
        "soothing_checklist": [
            "Diaper inspection: Check for wetness, redness, or diaper tape pinching skin.",
            "Temperature check: Feel the back of baby's neck. If sweaty, shed a layer; if cool, add a swaddle.",
            "Inspect clothing for scratchy tags, tight elastic bands, or hair tourniquets."
        ]
    },
    "tired": {
        "title": "Tiredness (Sleepiness & Overstimulation)",
        "icon": "😴",
        "color": "#3b82f6",
        "baby_message": "My eyes are heavy and everything around me is too bright and loud! I am overtired and I do not know how to switch off all the sights and sounds by myself. Please wrap me snugly, dim the lights, and softly shush me to sleep.",
        "soothing_checklist": [
            "Move to a quiet, dimly lit room to reduce sensory stimulation.",
            "Wrap in a snug swaddle or sleep sack to suppress startling Moro reflex.",
            "Use rhythmic white noise (womb sounds, fan, shushing) and gentle rocking."
        ]
    }
}


class BabyCryClassifier:
    EXPECTED_FEATURES = 194
    SAMPLE_RATE = 16000

    def __init__(self, model_path: str = None, label_path: str = None):
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        self.model_path = model_path or os.path.join(base_dir, "babycry_model.joblib")
        self.label_path = label_path or os.path.join(base_dir, "babycry_label.joblib")
        
        self.model = None
        self.label_encoder = None
        self.classes_ = []
        self._load_models()

    def _load_models(self):
        if not os.path.exists(self.model_path) or not os.path.exists(self.label_path):
            raise FileNotFoundError(f"BabyCry model files missing at: {self.model_path}")
            
        self.model = joblib.load(self.model_path)
        self.label_encoder = joblib.load(self.label_path)
        self.classes_ = list(self.label_encoder.classes_)

    def extract_features(self, y: np.ndarray, sr: int = 16000) -> np.ndarray:
        import librosa
        
        # Ensure audio length >= 0.5s
        min_len = int(sr * 0.5)
        if len(y) < min_len:
            y = np.pad(y, (0, min_len - len(y)), mode="reflect")
            
        # 1. 40 MFCCs
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        
        # 2. 12 Chroma STFT
        stft = np.abs(librosa.stft(y))
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, y=y, sr=sr).T, axis=0)
        
        # 3. 128 Mel Spectrogram
        mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128).T, axis=0)
        
        # 4. 8 Spectral Contrast
        contrast = np.mean(
            librosa.feature.spectral_contrast(S=stft, y=y, sr=sr, n_bands=7, fmin=50).T,
            axis=0
        )
        
        # 5. 6 Tonnetz
        tonnetz = np.mean(librosa.feature.tonnetz(y=y, sr=sr).T, axis=0)
        
        features = np.concatenate((mfcc, chroma, mel, contrast, tonnetz)).astype(np.float32)
        return features

    def load_audio_data(self, audio_source) -> np.ndarray:
        import librosa
        
        if isinstance(audio_source, str):
            y, _ = librosa.load(audio_source, sr=self.SAMPLE_RATE, mono=True)
            return y
        elif isinstance(audio_source, bytes):
            # In-memory audio bytes
            try:
                bio = io.BytesIO(audio_source)
                y, sr = sf.read(bio)
            except Exception:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
                    tf.write(audio_source)
                    tmp_name = tf.name
                try:
                    y, sr = librosa.load(tmp_name, sr=self.SAMPLE_RATE, mono=True)
                finally:
                    if os.path.exists(tmp_name):
                        try:
                            os.remove(tmp_name)
                        except Exception:
                            pass
            if len(y.shape) > 1:
                y = np.mean(y, axis=1)
            if sr != self.SAMPLE_RATE:
                y = librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=self.SAMPLE_RATE)
            return y
        elif isinstance(audio_source, np.ndarray):
            return audio_source.astype(np.float32)
        else:
            raise ValueError("Unsupported audio source format")

    def predict(self, audio_source) -> dict:
        """Classifies a baby cry audio signal into distress categories."""
        y = self.load_audio_data(audio_source)
        feats = self.extract_features(y, sr=self.SAMPLE_RATE)
        feats = feats.reshape(1, -1)
        
        # Decision function -> calibrated softmax probabilities
        if hasattr(self.model, "decision_function"):
            decision_scores = self.model.decision_function(feats)[0]
            probs = softmax(decision_scores, temperature=1.2)
        elif hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(feats)[0]
        else:
            pred_idx = self.model.predict(feats)[0]
            probs = np.zeros(len(self.classes_))
            probs[pred_idx] = 1.0
            
        top_idx = int(np.argmax(probs))
        predicted_category = self.classes_[top_idx]
        confidence = float(probs[top_idx])
        
        prob_dict = {
            self.classes_[i]: float(probs[i])
            for i in range(len(self.classes_))
        }
        
        advice_info = ADVICE_DATABASE.get(predicted_category, {})
        
        return {
            "predicted_category": predicted_category,
            "confidence": confidence,
            "probabilities": prob_dict,
            "title": advice_info.get("title", predicted_category.capitalize()),
            "icon": advice_info.get("icon", "👶"),
            "color": advice_info.get("color", "#00d4ff"),
            "baby_message": advice_info.get("baby_message", ""),
            "soothing_checklist": advice_info.get("soothing_checklist", [])
        }
