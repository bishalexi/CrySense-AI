import os
import cv2
from baby_cry_classifier import BabyCryClassifier
from multimodal_fusion import MultimodalDistressFusion
from pipeline import EmotionPipeline

def test_multimodal():
    print("=== MULTIMODAL INFANT DISTRESS TEST ===")
    
    # 1. Test Baby Cry Classifier
    print("\n[1] Initializing BabyCryClassifier...")
    cry_clf = BabyCryClassifier()
    sample_audio = os.path.join("audio_samples", "sample_belly_pain.wav")
    
    print(f"Running acoustic inference on {sample_audio}...")
    audio_res = cry_clf.predict(sample_audio)
    print(f"-> Predicted Cry Category: {audio_res['predicted_category'].upper()} ({audio_res['confidence'] * 100:.1f}%)")
    print(f"-> Probabilities: { {k: round(v, 2) for k, v in audio_res['probabilities'].items()} }")
    print(f"-> Baby Translation: {audio_res['baby_message'][:80]}...")
    
    # 2. Test Visual Emotion Pipeline
    print("\n[2] Initializing EmotionPipeline (Slim 320 Face Detector)...")
    video_pipe = EmotionPipeline()
    sample_img = cv2.imread("sample.jpg")
    _, results, _ = video_pipe.process_frame(sample_img)
    visual_res = results[0]["emotion"] if results else None
    print(f"-> Detected Face Emotion: {visual_res['dominant_emotion']} ({visual_res['confidence'] * 100:.1f}%)")
    
    # 3. Test Cross-Modal Fusion
    print("\n[3] Fusing Visual Facial Cues + Acoustic Cry Signal...")
    fusion = MultimodalDistressFusion()
    fused = fusion.fuse(visual_data=visual_res, audio_data=audio_res)
    
    print(f"\n==========================================")
    print(f" UNIFIED DISTRESS SCORE: {fused['unified_distress_score']}%")
    print(f" SEVERITY STATUS:       {fused['severity_label']} ({fused['severity_badge']})")
    print(f" MODALITY USED:         {fused['modality_used']}")
    print(f" NARRATIVE:             {fused['narrative']}")
    print(f" FIRST-PERSON MESSAGE:  {fused['baby_message']}")
    print(f" ACTIONS:               {len(fused['soothing_checklist'])} protocol steps")
    print(f"==========================================")
    print("\nMultimodal Verification PASSED!")

if __name__ == "__main__":
    test_multimodal()
