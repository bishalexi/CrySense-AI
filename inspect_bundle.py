import urllib.request
import re

url = "https://beat-maker-portal-2.preview.emergentagent.com/static/js/bundle.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
content = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")

# Find all fetch or axios occurrences
fetches = re.findall(r"fetch\([^)]+\)", content)
print("[Fetch Calls Found in Frontend]:")
for f in set(fetches):
    print(" ->", f[:150])

# Find all input placeholders or labels related to URL, backend, connect
inputs = re.findall(r"placeholder\s*:\s*[\"']([^\"']+)[\"']", content)
print("\n[Input Placeholders in Frontend]:")
for p in set(inputs):
    print(" *", p)

# Find texts near 'backend' or 'connect'
contexts = re.findall(r".{0,50}(?:backend|tunnel|ngrok|trycloudflare|server url|api url).{0,50}", content, re.IGNORECASE)
print("\n[Backend References]:")
for c in set(contexts[:15]):
    print(" -", c.strip().replace("\n", " "))
