import os
import json
import urllib.request

url = "https://beat-maker-portal-2.preview.emergentagent.com/static/js/bundle.js.map"
print("Downloading full source map from:", url)

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
resp = urllib.request.urlopen(req, timeout=30)
data = json.loads(resp.read().decode("utf-8"))

sources = data.get("sources", [])
contents = data.get("sourcesContent", [])

print(f"Total sources: {len(sources)}")

extracted_count = 0
for src_path, src_content in zip(sources, contents):
    if not src_content:
        continue
        
    # We only care about /app/frontend/src/ or src/
    if "/app/frontend/" in src_path or src_path.startswith("src/"):
        clean_path = src_path.replace("/app/frontend/", "").replace("src/", "src/")
        # Remove webpack query strings if any
        clean_path = clean_path.split("?")[0]
        
        dest_file = os.path.join("frontend", clean_path)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(src_content)
        extracted_count += 1
        print(f"Saved: {clean_path}")

print(f"\nSuccessfully extracted {extracted_count} frontend source files into ./frontend/")
