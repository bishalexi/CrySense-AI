"""Flask Web Application for Multimodal Infant Distress Monitoring.
Combines Real-Time Facial Emotion AI (Slim 320) with BabyCry Acoustic Classification.
Provides live camera streaming, microphone/sample audio classification, and cross-modal telemetry.
"""

import io
import os
import threading
import time
import cv2
import numpy as np
from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

from pipeline import EmotionPipeline
from baby_cry_classifier import BabyCryClassifier
from multimodal_fusion import MultimodalDistressFusion

app = Flask(__name__)
CORS(app)
pipeline = EmotionPipeline()
baby_cry_classifier = BabyCryClassifier()
fusion_engine = MultimodalDistressFusion()

# Global state
frame_lock = threading.Lock()
latest_frame_jpeg = None

latest_visual_telemetry = {
    "fps": 0.0,
    "latency_ms": 0.0,
    "faces_count": 0,
    "dominant_emotion": "Neutral",
    "confidence": 0.0,
    "probabilities": {e: 0.0 for e in pipeline.classifier.EMOTIONS}
}

latest_audio_telemetry = None
latest_fused_assessment = None


active_source = "camera"  # 'camera' or 'sample'


def camera_background_worker():
    """Dedicated background thread capturing and analyzing frames at 30 FPS.
    Prevents lock contention, handles DirectShow on Windows, and falls back to sample.jpg seamlessly.
    """
    global latest_frame_jpeg, latest_visual_telemetry, latest_fused_assessment
    
    # Try DirectShow first on Windows to avoid MSMF 8-second hang
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)
        
    print(f"[CAMERA] Initialized. Hardware camera opened: {camera.isOpened()}")
        
    while True:
        frame = None
        success = False
        if active_source == "camera" and camera.isOpened():
            success, frame = camera.read()
            
        if not success or frame is None:
            if os.path.exists("sample.jpg"):
                frame = cv2.imread("sample.jpg")
            else:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "BabyCry AI: Neural Feed Active", (120, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 212, 255), 2)
            time.sleep(0.033)

        try:
            annotated, results, latency = pipeline.process_frame(frame)
            
            if results:
                top_face = max(results, key=lambda x: x["det_score"])
                latest_visual_telemetry = {
                    "fps": round(pipeline.fps, 1),
                    "latency_ms": round(latency, 1),
                    "faces_count": len(results),
                    "dominant_emotion": top_face["emotion"]["dominant_emotion"],
                    "confidence": round(top_face["emotion"]["confidence"] * 100, 1),
                    "probabilities": {k: round(v * 100, 1) for k, v in top_face["emotion"]["probabilities"].items()}
                }
            else:
                latest_visual_telemetry = {
                    "fps": round(pipeline.fps, 1),
                    "latency_ms": round(latency, 1),
                    "faces_count": 0,
                    "dominant_emotion": "Neutral",
                    "confidence": 0.0,
                    "probabilities": {e: 0.0 for e in pipeline.classifier.EMOTIONS}
                }
                
            latest_fused_assessment = fusion_engine.fuse(
                visual_data=latest_visual_telemetry,
                audio_data=latest_audio_telemetry
            )
                
            ret, buffer = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                with frame_lock:
                    latest_frame_jpeg = buffer.tobytes()
        except Exception as e:
            print(f"[CAMERA ERROR] {e}")
            time.sleep(0.05)
            
        time.sleep(0.01)


# Launch camera background worker daemon
camera_thread = threading.Thread(target=camera_background_worker, daemon=True)
camera_thread.start()


def generate_frames():
    """Streams MJPEG frames from the background worker without lock contention."""
    while True:
        with frame_lock:
            frame_bytes = latest_frame_jpeg
            
        if frame_bytes is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)


@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    return render_template('react_index.html')


@app.route('/classic')
def classic():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/snapshot')
def api_snapshot():
    """Returns the latest single JPEG frame instantly for high-reliability fallback."""
    with frame_lock:
        frame_bytes = latest_frame_jpeg
        
    if frame_bytes is not None:
        return Response(frame_bytes, mimetype='image/jpeg')
    return Response(b'', status=503)


@app.route('/api/set_source', methods=['POST', 'GET'])
def set_source():
    global active_source
    src = request.args.get('source') or (request.json and request.json.get('source')) or 'camera'
    active_source = src
    return jsonify({"status": "ok", "active_source": active_source})


@app.route('/api/upload_face', methods=['POST'])
def upload_face():
    global active_source
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    f.save("sample.jpg")
    active_source = "sample"
    return jsonify({"status": "ok", "active_source": "sample"})


@app.route('/audio_samples/<filename>')
def serve_audio_sample(filename):
    samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_samples")
    return send_from_directory(samples_dir, filename)


@app.route('/api/telemetry')
def api_telemetry():
    global latest_fused_assessment
    if latest_fused_assessment is None:
        latest_fused_assessment = fusion_engine.fuse(latest_visual_telemetry, latest_audio_telemetry)
        
    return jsonify({
        "visual": latest_visual_telemetry,
        "audio": latest_audio_telemetry,
        "fused": latest_fused_assessment
    })


@app.route('/api/sample_audios')
def api_sample_audios():
    samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_samples")
    samples = []
    
    sample_meta = {
        "sample_hungry.wav": {"name": "Hunger Cry", "category": "hungry", "icon": "🍼"},
        "sample_belly_pain.wav": {"name": "Belly Pain (Colic)", "category": "belly_pain", "icon": "🩹"},
        "sample_burping.wav": {"name": "Burping Needed", "category": "burping", "icon": "💨"},
        "sample_tired.wav": {"name": "Tired Cry", "category": "tired", "icon": "😴"},
        "sample_tone.wav": {"name": "Discomfort Cry", "category": "discomfort", "icon": "👶"}
    }
    
    if os.path.exists(samples_dir):
        for f in sorted(os.listdir(samples_dir)):
            if f.endswith(".wav"):
                meta = sample_meta.get(f, {"name": f, "category": "cry", "icon": "🎵"})
                samples.append({
                    "id": f,
                    "filename": f,
                    "name": meta["name"],
                    "category": meta["category"],
                    "icon": meta["icon"],
                    "url": f"/audio_samples/{f}"
                })
    return jsonify(samples)


@app.route('/api/audio_classify', methods=['POST'])
def api_audio_classify():
    global latest_audio_telemetry, latest_fused_assessment
    
    audio_data = None
    
    # Check if a preset sample was requested
    sample_name = request.args.get('sample')
    if sample_name:
        sample_path = os.path.join("audio_samples", sample_name)
        if os.path.exists(sample_path):
            audio_data = sample_path
            
    # Or check if an audio file was uploaded (from mic or file input)
    if audio_data is None and 'file' in request.files:
        uploaded = request.files['file']
        audio_data = uploaded.read()
        
    if audio_data is None:
        return jsonify({"error": "No audio data provided"}), 400
        
    try:
        audio_result = baby_cry_classifier.predict(audio_data)
        latest_audio_telemetry = audio_result
        
        # Calculate updated multimodal fusion
        latest_fused_assessment = fusion_engine.fuse(
            visual_data=latest_visual_telemetry,
            audio_data=latest_audio_telemetry
        )
        
        return jsonify({
            "audio": audio_result,
            "fused": latest_fused_assessment
        })
    except Exception as e:
        return jsonify({"error": f"Audio processing failed: {str(e)}"}), 500


@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
        
    in_memory = file.read()
    nparr = np.frombuffer(in_memory, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({"error": "Could not decode image"}), 400
        
    annotated, results, latency = pipeline.process_frame(img)
    _, buffer = cv2.imencode('.jpg', annotated)
    return Response(buffer.tobytes(), mimetype='image/jpeg')


def run_server(host='0.0.0.0', port=5000):
    print(f"\n[WEB] Launching Multimodal Infant Distress Monitor...")
    print(f"[WEB] Open your browser at: http://localhost:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == '__main__':
    run_server()
