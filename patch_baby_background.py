import os
import re

bundle_path = os.path.join("static", "js", "bundle.js")
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read bundle.js: {len(content)} bytes")

# 1. New Baby Nursery Background Component
starfield_old_start = content.find("const Starfield = () => {")
starfield_old_end = content.find("_s(Starfield, \"UJgi7ynoup7eqypjnwyX/s32POg=\");", starfield_old_start)

if starfield_old_start == -1 or starfield_old_end == -1:
    print("[ERROR] Could not find Starfield boundaries in bundle.js")
    exit(1)

new_starfield_js = '''const Starfield = () => {
  _s();
  const canvasRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);

  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const handleResize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Nursery Clouds
    const clouds = [
      { x: w * 0.08, y: h * 0.16, scale: 1.15, speed: 0.18, opacity: 0.18 },
      { x: w * 0.52, y: h * 0.07, scale: 0.85, speed: 0.12, opacity: 0.15 },
      { x: w * 0.82, y: h * 0.26, scale: 0.95, speed: 0.22, opacity: 0.16 },
      { x: w * 0.28, y: h * 0.45, scale: 0.75, speed: 0.15, opacity: 0.13 },
      { x: w * 0.68, y: h * 0.62, scale: 1.05, speed: 0.2, opacity: 0.17 },
      { x: -w * 0.15, y: h * 0.78, scale: 0.9, speed: 0.16, opacity: 0.14 }
    ];

    // Twinkling Nursery 4-pointed Stars & Pastel Palette
    const starColors = [
      '#fef08a', // lullaby gold
      '#bae6fd', // baby sky blue
      '#fbcfe8', // soft blossom pink
      '#e9d5ff', // gentle lavender
      '#bbf7d0'  // pastel mint
    ];

    const stars = Array.from({ length: 85 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      size: Math.random() * 4 + 2,
      color: starColors[Math.floor(Math.random() * starColors.length)],
      twinkleSpeed: Math.random() * 0.03 + 0.015,
      phase: Math.random() * Math.PI * 2,
      rotation: Math.random() * Math.PI,
      rotSpeed: (Math.random() - 0.5) * 0.01,
      isFourPoint: Math.random() > 0.35
    }));

    // Floating Baby Dream Shapes (Bottles, Teddies, Pacifiers, Notes, Bubbles)
    const dreamTypes = ['bottle', 'teddy', 'pacifier', 'note', 'cloud', 'bubble'];
    const dreamItems = Array.from({ length: 22 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      type: dreamTypes[i % dreamTypes.length],
      scale: Math.random() * 0.35 + 0.7,
      speedY: Math.random() * 0.35 + 0.22,
      wobbleSpeed: Math.random() * 0.02 + 0.01,
      wobbleDist: Math.random() * 25 + 15,
      phase: Math.random() * Math.PI * 2,
      rotation: (Math.random() - 0.5) * 0.3,
      rotSpeed: (Math.random() - 0.5) * 0.006,
      opacity: Math.random() * 0.28 + 0.22,
      color: starColors[Math.floor(Math.random() * starColors.length)]
    }));

    // Interactive Stardust
    const stardust = [];
    const handlePointerMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      for (let i = 0; i < 2; i++) {
        stardust.push({
          x: px + (Math.random() - 0.5) * 20,
          y: py + (Math.random() - 0.5) * 20,
          vx: (Math.random() - 0.5) * 1.2,
          vy: Math.random() * -1.5 - 0.5,
          life: 1.0,
          decay: Math.random() * 0.02 + 0.02,
          size: Math.random() * 3 + 1.5,
          color: starColors[Math.floor(Math.random() * starColors.length)]
        });
      }
      if (stardust.length > 50) stardust.splice(0, 10);
    };
    window.addEventListener('pointermove', handlePointerMove, { passive: true });

    let animId;
    let t = 0;

    // --- DRAW PROCEDURAL HELPERS ---
    const drawFourPointStar = (cx, cy, outerRadius, color, alpha) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      const r = outerRadius;
      ctx.moveTo(0, -r);
      ctx.quadraticCurveTo(0, 0, r, 0);
      ctx.quadraticCurveTo(0, 0, 0, r);
      ctx.quadraticCurveTo(0, 0, -r, 0);
      ctx.quadraticCurveTo(0, 0, 0, -r);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    };

    const drawCloud = (cx, cy, scale, opacity) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.scale(scale, scale);
      ctx.globalAlpha = opacity;
      ctx.fillStyle = '#e2e8f0';
      ctx.shadowColor = 'rgba(216, 180, 254, 0.4)';
      ctx.shadowBlur = 15;

      ctx.beginPath();
      ctx.arc(0, 0, 28, 0, Math.PI * 2);
      ctx.arc(22, -10, 22, 0, Math.PI * 2);
      ctx.arc(44, 2, 24, 0, Math.PI * 2);
      ctx.arc(-22, -6, 20, 0, Math.PI * 2);
      ctx.arc(-38, 4, 18, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    };

    const drawMoon = (cx, cy, time) => {
      ctx.save();
      ctx.translate(cx, cy);

      // Breathing halo glow
      const breathe = Math.sin(time * 0.002) * 8;
      const haloGrad = ctx.createRadialGradient(0, 0, 20, 0, 0, 80 + breathe);
      haloGrad.addColorStop(0, 'rgba(253, 224, 71, 0.28)');
      haloGrad.addColorStop(0.5, 'rgba(253, 186, 116, 0.12)');
      haloGrad.addColorStop(1, 'rgba(253, 224, 71, 0)');
      ctx.fillStyle = haloGrad;
      ctx.beginPath();
      ctx.arc(0, 0, 80 + breathe, 0, Math.PI * 2);
      ctx.fill();

      // Crescent Moon Body
      ctx.save();
      ctx.beginPath();
      ctx.arc(0, 0, 36, 0, Math.PI * 2, false);
      ctx.arc(14, -10, 32, 0, Math.PI * 2, true);
      ctx.closePath();
      const moonGrad = ctx.createLinearGradient(-30, -30, 20, 30);
      moonGrad.addColorStop(0, '#fef9c3');
      moonGrad.addColorStop(0.6, '#fde047');
      moonGrad.addColorStop(1, '#f59e0b');
      ctx.fillStyle = moonGrad;
      ctx.shadowColor = 'rgba(254, 240, 138, 0.8)';
      ctx.shadowBlur = 14;
      ctx.fill();
      ctx.restore();

      // Sleeping Eyelashes on Moon
      ctx.save();
      ctx.strokeStyle = '#92400e';
      ctx.lineWidth = 1.8;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.arc(-10, -2, 6, 0.2 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-10, 4);
      ctx.lineTo(-10, 7);
      ctx.moveTo(-14, 3);
      ctx.lineTo(-16, 5);
      ctx.moveTo(-6, 3);
      ctx.lineTo(-4, 5);
      ctx.stroke();

      // Rosy Cheek
      ctx.fillStyle = 'rgba(244, 114, 182, 0.55)';
      ctx.beginPath();
      ctx.arc(-7, 10, 5.5, 0, Math.PI * 2);
      ctx.fill();

      // Cute Smile
      ctx.beginPath();
      ctx.arc(-4, 12, 4.5, 0.1 * Math.PI, 0.7 * Math.PI);
      ctx.stroke();

      // Cute Nightcap on Moon Horn
      ctx.save();
      ctx.translate(-8, -32);
      ctx.rotate(-0.35 + Math.sin(time * 0.002) * 0.08);
      ctx.beginPath();
      ctx.moveTo(-12, 6);
      ctx.quadraticCurveTo(6, -22, 28, -14);
      ctx.quadraticCurveTo(8, 4, 12, 8);
      ctx.closePath();
      ctx.fillStyle = '#60a5fa';
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-14, 4, 26, 7, 3);
      } else {
        ctx.rect(-14, 4, 26, 7);
      }
      ctx.fill();

      ctx.beginPath();
      ctx.arc(30, -14, 5.5, 0, Math.PI * 2);
      ctx.fillStyle = '#fef08a';
      ctx.shadowColor = '#fef08a';
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.restore();

      ctx.restore();
    };

    // Draw Dream Item: Baby Milk Bottle
    const drawBottle = (color) => {
      ctx.fillStyle = color;
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-8, -4, 16, 22, 4);
      } else {
        ctx.rect(-8, -4, 16, 22);
      }
      ctx.stroke();

      ctx.globalAlpha *= 0.5;
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-7, 2, 14, 15, [0, 0, 3, 3]);
      } else {
        ctx.rect(-7, 2, 14, 15);
      }
      ctx.fill();
      ctx.globalAlpha /= 0.5;

      ctx.beginPath();
      ctx.moveTo(-4, 5); ctx.lineTo(0, 5);
      ctx.moveTo(-4, 9); ctx.lineTo(0, 9);
      ctx.moveTo(-4, 13); ctx.lineTo(0, 13);
      ctx.stroke();

      ctx.beginPath();
      ctx.rect(-6, -8, 12, 4);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, -10, 3.5, 0, Math.PI * 2);
      ctx.fill();
    };

    // Draw Dream Item: Teddy Bear
    const drawTeddy = (color) => {
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(0, 2, 11, 0, Math.PI * 2);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(-8, -7, 4.5, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(8, -7, 4.5, 0, Math.PI * 2);
      ctx.stroke();

      ctx.globalAlpha *= 0.5;
      ctx.beginPath(); ctx.arc(-8, -7, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(8, -7, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha /= 0.5;

      ctx.beginPath();
      ctx.arc(0, 4, 4.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#0f172a';
      ctx.beginPath(); ctx.arc(-3.5, 0, 1.2, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(3.5, 0, 1.2, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(0, 3, 1, 0, Math.PI * 2); ctx.fill();
    };

    // Draw Dream Item: Pacifier
    const drawPacifier = (color) => {
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = 1.3;
      ctx.beginPath();
      ctx.arc(0, 8, 5.5, 0, Math.PI * 2);
      ctx.stroke();

      ctx.beginPath();
      ctx.ellipse(0, 0, 11, 6.5, 0, 0, Math.PI * 2);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(0, -7, 4.5, 0, Math.PI * 2);
      ctx.globalAlpha *= 0.6;
      ctx.fill();
      ctx.globalAlpha /= 0.6;
    };

    // Draw Dream Item: Music Note
    const drawMusicNote = (color) => {
      ctx.fillStyle = color;
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.ellipse(-5, 5, 4, 3, -0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(6, 2, 4, 3, -0.3, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.moveTo(-2, 5); ctx.lineTo(-2, -7);
      ctx.moveTo(9, 2); ctx.lineTo(9, -10);
      ctx.lineTo(-2, -7);
      ctx.stroke();
    };

    // Draw Dream Item: Iridescent Bubble
    const drawBubble = (color) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.arc(0, 0, 12, 0, Math.PI * 2);
      ctx.stroke();

      ctx.strokeStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(-4, -4, 7, 1.1 * Math.PI, 1.7 * Math.PI);
      ctx.stroke();
    };

    // --- MAIN ANIMATION LOOP ---
    const render = () => {
      t += 1;
      ctx.clearRect(0, 0, w, h);

      // 1. Draw Moon in Top Right
      const moonX = w > 768 ? w * 0.88 : w * 0.82;
      const moonY = h > 600 ? h * 0.14 : 70;
      drawMoon(moonX, moonY, t);

      // 2. Draw & Drift Clouds
      for (const c of clouds) {
        c.x += c.speed;
        if (c.x - 120 * c.scale > w) {
          c.x = -150 * c.scale;
          c.y = Math.random() * h * 0.75;
        }
        drawCloud(c.x, c.y, c.scale, c.opacity);
      }

      // 3. Draw & Twinkle Stars
      for (const s of stars) {
        s.rotation += s.rotSpeed;
        const twinkle = Math.sin(t * s.twinkleSpeed + s.phase);
        const alpha = 0.25 + 0.65 * (twinkle * 0.5 + 0.5);

        if (s.isFourPoint) {
          drawFourPointStar(s.x, s.y, s.size * 2.2, s.color, alpha);
        } else {
          ctx.save();
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.size * 0.7, 0, Math.PI * 2);
          ctx.fillStyle = s.color;
          ctx.globalAlpha = alpha;
          ctx.shadowColor = s.color;
          ctx.shadowBlur = 6;
          ctx.fill();
          ctx.restore();
        }
      }

      // 4. Draw & Float Baby Dream Items
      for (const d of dreamItems) {
        d.y -= d.speedY;
        d.rotation += d.rotSpeed;
        const wobbleX = d.x + Math.sin(t * d.wobbleSpeed + d.phase) * d.wobbleDist;

        if (d.y < -40) {
          d.y = h + 40;
          d.x = Math.random() * w;
        }

        ctx.save();
        ctx.translate(wobbleX, d.y);
        ctx.scale(d.scale, d.scale);
        ctx.rotate(d.rotation);
        ctx.globalAlpha = d.opacity;
        ctx.shadowColor = d.color;
        ctx.shadowBlur = 8;

        switch (d.type) {
          case 'bottle':
            drawBottle(d.color);
            break;
          case 'teddy':
            drawTeddy(d.color);
            break;
          case 'pacifier':
            drawPacifier(d.color);
            break;
          case 'note':
            drawMusicNote(d.color);
            break;
          case 'cloud':
            drawCloud(0, 0, 0.45, 0.4);
            break;
          case 'bubble':
            drawBubble(d.color);
            break;
          default:
            drawBottle(d.color);
        }
        ctx.restore();
      }

      // 5. Draw Interactive Stardust
      for (let i = stardust.length - 1; i >= 0; i--) {
        const p = stardust[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
        if (p.life <= 0) {
          stardust.splice(i, 1);
          continue;
        }
        drawFourPointStar(p.x, p.y, p.size * p.life * 1.8, p.color, p.life * 0.9);
      }

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('pointermove', handlePointerMove);
    };
  }, []);

  return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_1__.jsxDEV)("canvas", {
    ref: canvasRef,
    style: {
      position: 'fixed',
      inset: 0,
      width: '100vw',
      height: '100vh',
      pointerEvents: 'none',
      zIndex: 0
    },
    "x-file-name": "Starfield",
    "x-line-number": "50",
    "x-column": "4",
    "x-component": "canvas",
    "x-id": "Starfield_50_4",
    "x-dynamic": "false"
  }, void 0, false, {
    fileName: _jsxFileName,
    lineNumber: 50,
    columnNumber: 5
  }, undefined);
};
'''

content = content[:starfield_old_start] + new_starfield_js + content[starfield_old_end:]
print("[1] Successfully replaced Starfield with BabyNurseryBackground in bundle.js!")

# 2. Update .App background gradient to soothing twilight nursery palette
old_app_bg = "background: radial-gradient(ellipse at top, #1e1b4b 0%, #020617 55%, #000000 100%);"
new_app_bg = "background: radial-gradient(ellipse at 50% -10%, #2e2659 0%, #1a1e42 35%, #0f1429 70%, #090c18 100%);"

if old_app_bg in content:
    content = content.replace(old_app_bg, new_app_bg)
    print("[2] Successfully updated .App background gradient!")
else:
    print("[WARN] old_app_bg not found, checking with regex")
    content = re.sub(r'background:\s*radial-gradient\(ellipse at top[^;]+;', new_app_bg, content)

# 3. Enhance card glassmorphism with warmer nursery tint
old_glass = "background: linear-gradient(180deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.65));"
new_glass = "background: linear-gradient(180deg, rgba(34, 44, 76, 0.62), rgba(17, 23, 48, 0.72));"
if old_glass in content:
    content = content.replace(old_glass, new_glass)
    print("[3] Successfully updated glass-card background styling!")

# Save patched bundle
with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved updated bundle.js: {len(content)} bytes.")
