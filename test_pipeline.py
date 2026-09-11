import cv2
from pipeline import EmotionPipeline

def main():
    print("Loading EmotionPipeline...")
    pipeline = EmotionPipeline()
    
    img_path = "sample.jpg"
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Could not read {img_path}")
        return
        
    print(f"Processing image {img_path} ({img.shape[1]}x{img.shape[0]})...")
    annotated, results, latency = pipeline.process_frame(img)
    
    print(f"\nDetection complete in {latency:.2f} ms!")
    print(f"Detected {len(results)} face(s):")
    
    for idx, r in enumerate(results):
        box = r["box"]
        score = r["det_score"]
        emo = r["emotion"]["dominant_emotion"]
        conf = r["emotion"]["confidence"]
        probs = r["emotion"]["probabilities"]
        
        print(f"\n--- Face #{idx + 1} ---")
        print(f"Bounding Box: [x1={box[0]}, y1={box[1]}, x2={box[2]}, y2={box[3]}] (Score: {score:.3f})")
        print(f"Dominant Emotion: {emo} ({conf * 100:.2f}%)")
        print("Emotion Probabilities:")
        for e_name, p in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            bar = "#" * int(p * 30)
            print(f"  {e_name:<10}: {p * 100:5.1f}% | {bar}")
            
    out_path = "annotated_sample.jpg"
    cv2.imwrite(out_path, annotated)
    print(f"\nSaved annotated result to: {out_path}")

if __name__ == "__main__":
    main()
