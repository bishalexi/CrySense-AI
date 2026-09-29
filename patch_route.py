with open('static/js/bundle.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('path: "/"')
if idx != -1:
    text = text[:idx] + 'path: "*"' + text[idx + len('path: "/"'):]
    with open('static/js/bundle.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully changed Route path to '*' in bundle.js!")
else:
    print("path: \"/\" not found in bundle.js, checking if already '*'")
    if 'path: "*"' in text:
        print("Already set to '*'!")
