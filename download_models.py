import os
import sys
import requests

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

MODEL_SOURCES = {
    "version-slim-320.onnx": [
        "https://raw.githubusercontent.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB/master/models/onnx/version-slim-320_without_postprocessing.onnx",
        "https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB/raw/master/models/onnx/version-slim-320.onnx",
    ],
    "emotion-ferplus-8.onnx": [
        "https://huggingface.co/onnxmodelzoo/emotion-ferplus-8/resolve/main/emotion-ferplus-8.onnx",
        "https://github.com/onnx/models/raw/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx",
    ]
}


def download_file(url: str, dest_path: str) -> bool:
    try:
        print(f"Downloading from: {url}")
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        
        total_size = int(resp.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 64 * 1024
        
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB ({percent:.1f}%)", end="", flush=True)
                    else:
                        print(f"\rDownloaded: {downloaded / 1024 / 1024:.2f} MB", end="", flush=True)
        print()
        
        # Sanity check: Ensure file size > 50KB to avoid error HTML pages
        if os.path.getsize(dest_path) < 50 * 1024:
            print(f"Warning: File {dest_path} is suspiciously small ({os.path.getsize(dest_path)} bytes).")
            os.remove(dest_path)
            return False
            
        return True
    except Exception as e:
        print(f"\nDownload error: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False


def ensure_models():
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    for filename, urls in MODEL_SOURCES.items():
        dest_path = os.path.join(MODELS_DIR, filename)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100 * 1024:
            print(f"[OK] Model already exists: {filename} ({os.path.getsize(dest_path) / 1024 / 1024:.2f} MB)")
            continue
            
        print(f"\n[FETCH] Obtaining model: {filename}...")
        success = False
        for url in urls:
            if download_file(url, dest_path):
                print(f"[SUCCESS] Successfully downloaded: {filename}")
                success = True
                break
                
        if not success:
            print(f"[ERROR] Failed to download {filename} from all available sources.")
            return False
            
    print("\nAll models ready in:", MODELS_DIR)
    return True


if __name__ == "__main__":
    success = ensure_models()
    sys.exit(0 if success else 1)
