const fs = require('fs');
const path = require('path');

const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// Copy templates/react_index.html to dist/index.html
const templatePath = path.join(__dirname, '..', 'templates', 'react_index.html');
if (fs.existsSync(templatePath)) {
  const html = fs.readFileSync(templatePath, 'utf8');
  fs.writeFileSync(path.join(distDir, 'index.html'), html);
}

// Copy static directory to dist/static
const staticSrc = path.join(__dirname, '..', 'static');
const staticDst = path.join(distDir, 'static');

function copyDir(src, dst) {
  if (!fs.existsSync(dst)) fs.mkdirSync(dst, { recursive: true });
  for (const file of fs.readdirSync(src)) {
    const s = path.join(src, file);
    const d = path.join(dst, file);
    if (fs.statSync(s).isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

if (fs.existsSync(staticSrc)) {
  copyDir(staticSrc, staticDst);
}

console.log('Build completed successfully! Static dist generated at:', distDir);
