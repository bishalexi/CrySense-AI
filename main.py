"""Main Application Entry Point for Real-Time Facial Emotion Recognition.
Supports Webcam Live Stream, Static Image Processing, and Video File Inference.
"""

import argparse
import os
import sys
import time
import cv2

from pipeline import EmotionPipeline


def run_webcam(pipeline: EmotionPipeline, camera_id: int = 0):
    print(f"\n[CAMERA] Attempting to open camera index {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    
    # Try DSHOW backend on Windows if default takes long or fails
    if not cap.isOpened():
        print("[CAMERA] Default backend failed, attempting DirectShow (cv2.CAP_DSHOW)...")
        cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        
    if not cap.isOpened():
        print(f"[ERROR] Could not open video device {camera_id}.")
        print("Tip: If you don't have a webcam connected, you can run on an image or video:")
        print("     python main.py --mode image --input sample.jpg")
        return
        
    # Configure camera capture properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    window_name = "Real-Time Facial Emotion AI (Slim 320)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    
    print("\n" + "=" * 55)
    print(" LIVE WEBCAM INFERENCE ACTIVE")
    print(" Controls:")
    print("   [Q] or [ESC] : Quit application")
    print("   [S]          : Save high-res snapshot")
    print("   [B]          : Toggle emotion probability bars")
    print("   [T]          : Toggle top telemetry banner")
    print("=" * 55 + "\n")
    
    snap_count = 0
    show_bars = True
    show_telemetry = True
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[WARN] Failed to grab frame from camera. Retrying...")
                time.sleep(0.05)
                continue
                
            annotated_frame, results, latency = pipeline.process_frame(frame)
            
            cv2.imshow(window_name, annotated_frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key in [27, ord('q'), ord('Q')]:
                print("\n[EXIT] Exiting webcam loop...")
                break
            elif key in [ord('s'), ord('S')]:
                snap_count += 1
                filename = f"snapshot_{snap_count:03d}_{int(time.time())}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"[SNAPSHOT] Saved: {filename}")
            elif key in [ord('b'), ord('B')]:
                show_bars = not show_bars
                pipeline.visualizer.show_bars = show_bars
                print(f"[UI] Probability bars: {'ON' if show_bars else 'OFF'}")
            elif key in [ord('t'), ord('T')]:
                show_telemetry = not show_telemetry
                pipeline.visualizer.show_telemetry = show_telemetry
                print(f"[UI] Telemetry banner: {'ON' if show_telemetry else 'OFF'}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def run_image(pipeline: EmotionPipeline, input_path: str, output_path: str = None):
    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        return
        
    print(f"\n[IMAGE] Loading: {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        print(f"[ERROR] Unable to decode image: {input_path}")
        return
        
    annotated, results, latency = pipeline.process_frame(img)
    print(f"[IMAGE] Processed in {latency:.2f} ms | Found {len(results)} face(s)")
    
    for idx, r in enumerate(results):
        emo = r["emotion"]["dominant_emotion"]
        conf = r["emotion"]["confidence"]
        box = r["box"]
        print(f"  Face #{idx + 1}: {emo.upper()} ({conf * 100:.1f}%) at {box}")
        
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_analyzed{ext}"
        
    cv2.imwrite(output_path, annotated)
    print(f"[IMAGE] Saved annotated result to: {output_path}")


def run_video(pipeline: EmotionPipeline, input_path: str, output_path: str = None):
    if not os.path.exists(input_path):
        print(f"[ERROR] Video file not found: {input_path}")
        return
        
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video file: {input_path}")
        return
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_analyzed.mp4"
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    
    print(f"\n[VIDEO] Processing {input_path} ({total_frames} frames @ {fps:.1f} FPS)...")
    frame_idx = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                break
                
            frame_idx += 1
            annotated, _, _ = pipeline.process_frame(frame)
            writer.write(annotated)
            
            if frame_idx % 30 == 0 or frame_idx == total_frames:
                percent = (frame_idx / total_frames) * 100 if total_frames > 0 else 0
                elapsed = time.time() - start_time
                est_fps = frame_idx / elapsed if elapsed > 0 else 0
                print(f"\rProgress: {frame_idx}/{total_frames} frames ({percent:.1f}%) - {est_fps:.1f} FPS", end="", flush=True)
        print()
    finally:
        cap.release()
        writer.release()
        
    print(f"[VIDEO] Processing finished! Output saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Real-Time Facial Emotion Recognition Pipeline (Slim 320)")
    parser.add_argument("--mode", type=str, default="webcam", choices=["webcam", "image", "video", "web"],
                        help="Operating mode: webcam, image, video, or web")
    parser.add_argument("--input", type=str, default="sample.jpg", help="Path to input image or video file")
    parser.add_argument("--output", type=str, default=None, help="Path to save processed image or video")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device ID (default: 0)")
    parser.add_argument("--conf", type=float, default=0.7, help="Face detection confidence threshold")
    parser.add_argument("--no-bars", action="store_true", help="Disable emotion probability distribution bars")
    parser.add_argument("--no-telemetry", action="store_true", help="Disable top telemetry banner")
    parser.add_argument("--port", type=int, default=5000, help="Port for web dashboard")
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = EmotionPipeline(
        conf_threshold=args.conf,
        show_bars=not args.no_bars,
        show_telemetry=not args.no_telemetry
    )
    
    if args.mode == "webcam":
        run_webcam(pipeline, camera_id=args.camera)
    elif args.mode == "image":
        run_image(pipeline, input_path=args.input, output_path=args.output)
    elif args.mode == "video":
        run_video(pipeline, input_path=args.input, output_path=args.output)
    elif args.mode == "web":
        from web_app import run_server
        run_server(port=args.port)


if __name__ == "__main__":
    main()
