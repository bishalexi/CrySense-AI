"""Flask Web Application for Multimodal Infant Distress Monitoring.
Combines Real-Time Facial Emotion AI (Slim 320) with BabyCry Acoustic Classification.
Provides live camera streaming, microphone/sample audio classification, and cross-modal telemetry.
"""

import base64
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)
pipeline = EmotionPipeline()
baby_cry_classifier = BabyCryClassifier()
fusion_engine = MultimodalDistressFusion()

# Global state
frame_lock = threading.Lock()
latest_frame_jpeg = None
camera_hardware_active = False

latest_visual_telemetry = {
    "fps": 30.0,
    "latency_ms": 14.5,
    "faces_count": 0,
    "dominant_emotion": "Neutral",
    "confidence": 0.0,
    "probabilities": {e: 0.0 for e in pipeline.classifier.EMOTIONS}
}

latest_audio_telemetry = None
latest_fused_assessment = None

active_source = "camera"  # 'camera', 'browser', or 'sample'
reconnect_requested = False


def open_hardware_camera():
    """Attempts opening camera with DirectShow first (fast on Windows), then fallback."""
    for idx in (0, 1):
        try:
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                print(f"[CAMERA] Successfully opened hardware camera on index {idx} with DirectShow.")
                return cap
            cap.release()
        except Exception:
            pass

    for idx in (0, 1):
        try:
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                print(f"[CAMERA] Successfully opened hardware camera on index {idx} with default backend.")
                return cap
            cap.release()
        except Exception:
            pass

    return None


def camera_background_worker():
    """Dedicated background thread capturing and analyzing frames at up to 30 FPS.
    Self-healing: automatically reconnects to physical webcam when disconnected or idle.
    """
    global latest_frame_jpeg, latest_visual_telemetry, latest_fused_assessment
    global camera_hardware_active, reconnect_requested
    
    camera = None
    last_reconnect_time = 0
    anim_step = 0

    while True:
        now = time.time()
        frame = None
        success = False

        if reconnect_requested:
            if camera is not None:
                try:
                    camera.release()
                except Exception:
                    pass
                camera = None
            reconnect_requested = False
            last_reconnect_time = 0

        if active_source == "camera":
            # Attempt to acquire/reconnect camera every 1.5 seconds if not open
            if camera is None or not camera.isOpened():
                if now - last_reconnect_time >= 1.5:
                    last_reconnect_time = now
                    camera = open_hardware_camera()
                    camera_hardware_active = (camera is not None and camera.isOpened())

            if camera is not None and camera.isOpened():
                try:
                    success, frame = camera.read()
                    if not success or frame is None:
                        print("[CAMERA WARNING] Hardware camera read dropped frame. Releasing for reconnect...")
                        try:
                            camera.release()
                        except Exception:
                            pass
                        camera = None
                        camera_hardware_active = False
                    else:
                        camera_hardware_active = True
                except Exception as e:
                    print(f"[CAMERA EXCEPTION] {e}")
                    camera = None
                    camera_hardware_active = False

        elif active_source == "sample":
            sample_file = os.path.join(BASE_DIR, "sample.jpg")
            if os.path.exists(sample_file):
                frame = cv2.imread(sample_file)
                if frame is not None:
                    success = True
            time.sleep(0.033)

        elif active_source == "browser":
            # Client browser pushes frames via /api/upload_frame
            time.sleep(0.02)
            continue

        # If camera not connected or frame not read, fallback to realistic infant sample or neural pattern
        if not success or frame is None:
            sample_file = os.path.join(BASE_DIR, "sample.jpg")
            if os.path.exists(sample_file):
                frame = cv2.imread(sample_file)
            
            if frame is None:
                anim_step = (anim_step + 3) % 480
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.circle(frame, (320, 240), 90, (0, 212, 255), 1)
                cv2.line(frame, (320, 100), (320, 380), (0, 212, 255), 1)
                cv2.line(frame, (180, 240), (460, 240), (0, 212, 255), 1)
                cv2.line(frame, (0, anim_step), (640, anim_step), (168, 85, 247), 2)
                cv2.putText(frame, "BabyCry AI: Neural Optical Scan Active", (110, 220),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 212, 255), 2)
                cv2.putText(frame, "Awaiting Camera / Upload Face Photo", (130, 260),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (148, 163, 184), 1)
            time.sleep(0.033)

        # Run through inference pipeline
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
                    "fps": round(pipeline.fps, 1) if pipeline.fps > 0 else 30.0,
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
            print(f"[CAMERA PIPELINE ERROR] {e}")
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
    response.headers['Access-Control-Allow-Origin'] = '*'
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
    """Returns the latest single JPEG frame instantly with no caching."""
    global latest_frame_jpeg
    with frame_lock:
        frame_bytes = latest_frame_jpeg
        
    if frame_bytes is None:
        sample_file = os.path.join(BASE_DIR, "sample.jpg")
        if os.path.exists(sample_file):
            img = cv2.imread(sample_file)
            if img is not None:
                ret, buf = cv2.imencode('.jpg', img)
                if ret:
                    frame_bytes = buf.tobytes()
                    with frame_lock:
                        latest_frame_jpeg = frame_bytes

    if frame_bytes is not None:
        resp = Response(frame_bytes, mimetype='image/jpeg')
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
    return Response(b'', status=503)


@app.route('/api/camera_status')
def api_camera_status():
    return jsonify({
        "hardware_active": camera_hardware_active,
        "active_source": active_source,
        "fps": latest_visual_telemetry["fps"],
        "faces_count": latest_visual_telemetry["faces_count"],
        "dominant_emotion": latest_visual_telemetry["dominant_emotion"]
    })


@app.route('/api/upload_frame', methods=['POST'])
@app.route('/api/process_frame', methods=['POST'])
def api_upload_frame():
    """Receives a video frame from the client browser webcam (blob or base64).
    Processes frame through EmotionPipeline, updates visual telemetry, and returns detection results.
    """
    global latest_frame_jpeg, latest_visual_telemetry, latest_fused_assessment, active_source
    img = None
    
    if 'file' in request.files:
        f = request.files['file']
        nparr = np.frombuffer(f.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif request.is_json:
        data = request.get_json(silent=True) or {}
        img_b64 = data.get('image', '')
        if ',' in img_b64:
            img_b64 = img_b64.split(',', 1)[1]
        if img_b64:
            try:
                raw_bytes = base64.b64decode(img_b64)
                nparr = np.frombuffer(raw_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                return jsonify({"error": f"Base64 decode failed: {str(e)}"}), 400
                
    if img is None:
        return jsonify({"error": "No image frame provided"}), 400
        
    try:
        annotated, results, latency = pipeline.process_frame(img)
        active_source = "browser"
        
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
                "fps": round(pipeline.fps, 1) if pipeline.fps > 0 else 30.0,
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
        annotated_b64 = ""
        if ret:
            with frame_lock:
                latest_frame_jpeg = buffer.tobytes()
            annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
            
        return jsonify({
            "status": "ok",
            "faces_count": latest_visual_telemetry["faces_count"],
            "dominant_emotion": latest_visual_telemetry["dominant_emotion"],
            "confidence": latest_visual_telemetry["confidence"],
            "probabilities": latest_visual_telemetry["probabilities"],
            "fps": latest_visual_telemetry["fps"],
            "latency_ms": latest_visual_telemetry["latency_ms"],
            "annotated_frame": annotated_b64,
            "fused": latest_fused_assessment
        })
    except Exception as e:
        return jsonify({"error": f"Frame processing error: {str(e)}"}), 500


@app.route('/api/set_source', methods=['POST', 'GET'])
def set_source():
    global active_source, reconnect_requested
    src = request.args.get('source')
    if not src and request.is_json:
        data = request.get_json(silent=True) or {}
        src = data.get('source')
    active_source = src or 'camera'
    if active_source == 'camera':
        reconnect_requested = True
    return jsonify({
        "status": "ok",
        "active_source": active_source,
        "hardware_camera": camera_hardware_active
    })


@app.route('/api/upload_face', methods=['POST'])
@app.route('/api/upload', methods=['POST'])
def upload_face():
    global active_source, latest_visual_telemetry, latest_fused_assessment
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({"error": "Empty filename"}), 400
        
    sample_dest = os.path.join(BASE_DIR, "sample.jpg")
    f.save(sample_dest)
    active_source = "sample"
    
    # Process immediately
    img = cv2.imread(sample_dest)
    if img is not None:
        try:
            annotated, results, latency = pipeline.process_frame(img)
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
            ret, buffer = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                with frame_lock:
                    latest_frame_jpeg = buffer.tobytes()
        except Exception as e:
            print(f"[UPLOAD PROCESS ERROR] {e}")

    return jsonify({"status": "ok", "active_source": "sample"})


@app.route('/audio_samples/<filename>')
def serve_audio_sample(filename):
    samples_dir = os.path.join(BASE_DIR, "audio_samples")
    return send_from_directory(samples_dir, filename)


@app.route('/api/telemetry')
def api_telemetry():
    global latest_fused_assessment
    if latest_fused_assessment is None:
        latest_fused_assessment = fusion_engine.fuse(latest_visual_telemetry, latest_audio_telemetry)
        
    return jsonify({
        "visual": latest_visual_telemetry,
        "audio": latest_audio_telemetry,
        "fused": latest_fused_assessment,
        "camera_hardware": camera_hardware_active,
        "active_source": active_source
    })


@app.route('/api/sample_audios')
def api_sample_audios():
    samples_dir = os.path.join(BASE_DIR, "audio_samples")
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
        sample_path = os.path.join(BASE_DIR, "audio_samples", sample_name)
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


def run_server(host='0.0.0.0', port=5000):
    print(f"\n[WEB] Launching Multimodal Infant Distress Monitor...")
    print(f"[WEB] Open your browser at: http://localhost:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    run_server(port=port)
