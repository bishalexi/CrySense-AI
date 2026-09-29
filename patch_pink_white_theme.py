import os
import re

# 1. Update frontend/src/components/Starfield.jsx
starfield_source_path = os.path.join("frontend", "src", "components", "Starfield.jsx")

starfield_code = '''import React, { useEffect, useRef } from 'react';

/**
 * BabyPinkWhiteNursery (Replaces generic Starfield)
 * A joyful, adorable White & Pink baby-themed animated background:
 * - Sleepy smiling crescent moon with cute pink nightcap on a fluffy white cloud
 * - Fluffy white clouds with rosy pink blush drifting across the screen
 * - Cute floating baby elements:
 *    • 🍼 Pink & white baby milk bottles with measurement lines and cute hearts
 *    • 🧸 Adorable pink & white teddy bear faces
 *    • 👶 Pastel pink & white pacifiers (soothers)
 *    • 🎀 Sweet baby pink bows / ribbons
 *    • 👣 Cute pink baby footprints
 *    • 🎈 Pastel pink heart balloons
 *    • 🫧 Iridescent pink dream bubbles
 *    • ✦ Twinkling pink, white & gold nursery stars
 * - Interactive pink fairy stardust trail
 */
const Starfield = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
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

    // Fluffy White Clouds with Rosy Cheeks
    const clouds = [
      { x: w * 0.05, y: h * 0.12, scale: 1.2, speed: 0.22, opacity: 0.85 },
      { x: w * 0.45, y: h * 0.06, scale: 0.95, speed: 0.16, opacity: 0.8 },
      { x: w * 0.78, y: h * 0.22, scale: 1.05, speed: 0.26, opacity: 0.85 },
      { x: w * 0.22, y: h * 0.45, scale: 0.85, speed: 0.18, opacity: 0.75 },
      { x: w * 0.65, y: h * 0.62, scale: 1.15, speed: 0.24, opacity: 0.82 },
      { x: -w * 0.12, y: h * 0.78, scale: 1.0, speed: 0.2, opacity: 0.8 }
    ];

    // Twinkling Baby Pink, White & Gold Stars
    const starColors = [
      '#f472b6', // baby pink
      '#ec4899', // rose pink
      '#ffffff', // cloud white
      '#fbbf24', // warm gold
      '#fbcfe8', // soft blush
      '#fda4af'  // peach rose
    ];

    const stars = Array.from({ length: 90 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      size: Math.random() * 4.5 + 2.5,
      color: starColors[Math.floor(Math.random() * starColors.length)],
      twinkleSpeed: Math.random() * 0.035 + 0.018,
      phase: Math.random() * Math.PI * 2,
      rotation: Math.random() * Math.PI,
      rotSpeed: (Math.random() - 0.5) * 0.012,
      isFourPoint: Math.random() > 0.3
    }));

    // Floating Baby Elements in White & Pink (Bottles, Teddies, Pacifiers, Bows, Footprints, Balloons, Bubbles)
    const dreamTypes = ['bottle', 'teddy', 'pacifier', 'bow', 'footprint', 'balloon', 'bubble', 'cloud'];
    const dreamItems = Array.from({ length: 26 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      type: dreamTypes[i % dreamTypes.length],
      scale: Math.random() * 0.35 + 0.75,
      speedY: Math.random() * 0.4 + 0.28,
      wobbleSpeed: Math.random() * 0.02 + 0.012,
      wobbleDist: Math.random() * 25 + 15,
      phase: Math.random() * Math.PI * 2,
      rotation: (Math.random() - 0.5) * 0.35,
      rotSpeed: (Math.random() - 0.5) * 0.008,
      opacity: Math.random() * 0.25 + 0.75, // High, crisp visibility!
      color: starColors[Math.floor(Math.random() * starColors.length)]
    }));

    // Interactive Pink Fairy Stardust Trail
    const stardust = [];
    const handlePointerMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      for (let i = 0; i < 3; i++) {
        stardust.push({
          x: px + (Math.random() - 0.5) * 24,
          y: py + (Math.random() - 0.5) * 24,
          vx: (Math.random() - 0.5) * 1.6,
          vy: Math.random() * -1.8 - 0.6,
          life: 1.0,
          decay: Math.random() * 0.025 + 0.02,
          size: Math.random() * 3.5 + 2,
          color: starColors[Math.floor(Math.random() * starColors.length)]
        });
      }
      if (stardust.length > 60) stardust.splice(0, 15);
    };
    window.addEventListener('pointermove', handlePointerMove, { passive: true });

    let animId;
    let t = 0;

    // --- DRAW PROCEDURAL BABY HELPERS ---
    const drawFourPointStar = (cx, cy, outerRadius, color, alpha) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
      ctx.fillStyle = color;
      ctx.shadowColor = 'rgba(244, 114, 182, 0.6)';
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

    const drawCloud = (cx, cy, scale, opacity, withFace = false) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.scale(scale, scale);
      ctx.globalAlpha = opacity;

      // Puffy White Cloud
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = 'rgba(244, 114, 182, 0.28)';
      ctx.shadowBlur = 18;

      ctx.beginPath();
      ctx.arc(0, 0, 32, 0, Math.PI * 2);
      ctx.arc(26, -12, 26, 0, Math.PI * 2);
      ctx.arc(52, 2, 28, 0, Math.PI * 2);
      ctx.arc(-26, -8, 24, 0, Math.PI * 2);
      ctx.arc(-46, 4, 22, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();

      // Soft Pink Rosy Cheeks & Sweet Smile
      if (withFace) {
        ctx.fillStyle = 'rgba(244, 114, 182, 0.7)';
        ctx.beginPath(); ctx.arc(-14, 4, 5, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(22, 4, 5, 0, Math.PI * 2); ctx.fill();

        ctx.strokeStyle = '#be185d';
        ctx.lineWidth = 1.8;
        ctx.lineCap = 'round';
        // Closed happy eyes
        ctx.beginPath(); ctx.arc(-14, -4, 4, 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke();
        ctx.beginPath(); ctx.arc(22, -4, 4, 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke();
        // Smile
        ctx.beginPath(); ctx.arc(4, 5, 5, 0.1 * Math.PI, 0.9 * Math.PI); ctx.stroke();
      }

      ctx.restore();
    };

    const drawMoon = (cx, cy, time) => {
      ctx.save();
      ctx.translate(cx, cy);

      // Warm Golden-Pink Breathing Halo
      const breathe = Math.sin(time * 0.002) * 10;
      const haloGrad = ctx.createRadialGradient(0, 0, 20, 0, 0, 90 + breathe);
      haloGrad.addColorStop(0, 'rgba(254, 240, 138, 0.45)');
      haloGrad.addColorStop(0.5, 'rgba(251, 113, 133, 0.22)');
      haloGrad.addColorStop(1, 'rgba(254, 240, 138, 0)');
      ctx.fillStyle = haloGrad;
      ctx.beginPath();
      ctx.arc(0, 0, 90 + breathe, 0, Math.PI * 2);
      ctx.fill();

      // Base Little Cloud under Moon
      drawCloud(10, 36, 0.65, 0.95, false);

      // Crescent Moon Body
      ctx.save();
      ctx.beginPath();
      ctx.arc(0, 0, 42, 0, Math.PI * 2, false);
      ctx.arc(16, -12, 38, 0, Math.PI * 2, true);
      ctx.closePath();
      const moonGrad = ctx.createLinearGradient(-35, -35, 25, 35);
      moonGrad.addColorStop(0, '#fffbeb');
      moonGrad.addColorStop(0.5, '#fde047');
      moonGrad.addColorStop(1, '#f59e0b');
      ctx.fillStyle = moonGrad;
      ctx.shadowColor = 'rgba(251, 113, 133, 0.5)';
      ctx.shadowBlur = 16;
      ctx.fill();
      ctx.restore();

      // Sleeping Eyelashes on Moon
      ctx.save();
      ctx.strokeStyle = '#9d174d';
      ctx.lineWidth = 2.0;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.arc(-11, -3, 7, 0.2 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-11, 4); ctx.lineTo(-11, 8);
      ctx.moveTo(-16, 3); ctx.lineTo(-18, 6);
      ctx.moveTo(-6, 3); ctx.lineTo(-4, 6);
      ctx.stroke();

      // Cute Rosy Pink Cheek
      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      ctx.arc(-8, 12, 6.5, 0, Math.PI * 2);
      ctx.fill();

      // Sweet Smile
      ctx.beginPath();
      ctx.arc(-4, 14, 5.0, 0.1 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();

      // Cute Pink & White Nightcap on Moon Horn
      ctx.save();
      ctx.translate(-10, -36);
      ctx.rotate(-0.35 + Math.sin(time * 0.002) * 0.08);

      // Pink Cap Body
      ctx.beginPath();
      ctx.moveTo(-14, 7);
      ctx.quadraticCurveTo(6, -26, 32, -16);
      ctx.quadraticCurveTo(8, 4, 14, 9);
      ctx.closePath();
      ctx.fillStyle = '#f472b6';
      ctx.fill();

      // White Polka Dots on Cap
      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-2, -6, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(10, -8, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(20, -12, 2.5, 0, Math.PI * 2); ctx.fill();

      // White Fluffy Brim
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-16, 5, 30, 8, 4);
      } else {
        ctx.rect(-16, 5, 30, 8);
      }
      ctx.fill();

      // White Pom-pom
      ctx.beginPath();
      ctx.arc(34, -16, 6.5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = '#fbcfe8';
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.restore();

      ctx.restore();
    };

    // 🍼 Baby Element: White & Pink Milk Bottle
    const drawBottle = () => {
      // Bottle Body (White with Pink Border)
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-10, -5, 20, 28, 5);
      } else {
        ctx.rect(-10, -5, 20, 28);
      }
      ctx.fill();
      ctx.stroke();

      // Milk Fill Level (Soft Cream)
      ctx.fillStyle = '#fffbeb';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-8, 3, 16, 18, [0, 0, 4, 4]);
      } else {
        ctx.rect(-8, 3, 16, 18);
      }
      ctx.fill();

      // Cute Pink Heart on Bottle
      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      ctx.arc(-3, 10, 2.5, Math.PI, 0);
      ctx.arc(3, 10, 2.5, Math.PI, 0);
      ctx.lineTo(0, 16);
      ctx.closePath();
      ctx.fill();

      // Measurement Ticks
      ctx.strokeStyle = '#f472b6';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      ctx.moveTo(-6, 2); ctx.lineTo(-1, 2);
      ctx.moveTo(-6, 7); ctx.lineTo(-2, 7);
      ctx.moveTo(-6, 12); ctx.lineTo(-1, 12);
      ctx.stroke();

      // Pink Bottle Collar Cap
      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-8, -10, 16, 5, 2);
      } else {
        ctx.rect(-8, -10, 16, 5);
      }
      ctx.fill();

      // Soft Golden Nipple
      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.arc(0, -12, 4.5, 0, Math.PI * 2);
      ctx.fill();
    };

    // 🧸 Baby Element: Adorable Pink & White Teddy Bear Head
    const drawTeddy = () => {
      // Ears (Pink with White Inners)
      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#db2777';
      ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(-11, -9, 6.0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(11, -9, 6.0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-11, -9, 3.2, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(11, -9, 3.2, 0, Math.PI * 2); ctx.fill();

      // Head (Soft Pink)
      ctx.fillStyle = '#fbcfe8';
      ctx.beginPath();
      ctx.arc(0, 2, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // White Snout Muzzle
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(0, 5, 6.5, 0, Math.PI * 2);
      ctx.fill();

      // Black Shiny Eyes
      ctx.fillStyle = '#831843';
      ctx.beginPath(); ctx.arc(-5, 0, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(5, 0, 1.8, 0, Math.PI * 2); ctx.fill();

      // Cute Pink Nose & Smile
      ctx.fillStyle = '#ec4899';
      ctx.beginPath(); ctx.arc(0, 3.5, 2.2, 0, Math.PI * 2); ctx.fill();

      ctx.strokeStyle = '#be185d';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(-2, 7, 2.5, 0.2 * Math.PI, 0.9 * Math.PI);
      ctx.arc(2, 7, 2.5, 0.1 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();
    };

    // 👶 Baby Element: Pink & White Pacifier (Dummy)
    const drawPacifier = () => {
      // White Circular Handle Ring
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2.4;
      ctx.shadowColor = 'rgba(244, 114, 182, 0.4)';
      ctx.shadowBlur = 6;
      ctx.beginPath();
      ctx.arc(0, 11, 7.5, 0, Math.PI * 2);
      ctx.stroke();

      // Pink Pacifier Shield
      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.ellipse(0, 0, 15, 9.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // White Shield Vent Holes
      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-7, 0, 2.0, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(7, 0, 2.0, 0, Math.PI * 2); ctx.fill();

      // Soft Golden Nipple Bulb
      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.arc(0, -9, 6.0, 0, Math.PI * 2);
      ctx.fill();
    };

    // 🎀 Baby Element: Sweet Pink Ribbon Bow
    const drawBow = () => {
      ctx.fillStyle = '#ec4899';
      ctx.strokeStyle = '#be185d';
      ctx.lineWidth = 1.6;

      // Left Loop
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.quadraticCurveTo(-14, -10, -12, 0);
      ctx.quadraticCurveTo(-14, 10, 0, 0);
      ctx.fill();
      ctx.stroke();

      // Right Loop
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.quadraticCurveTo(14, -10, 12, 0);
      ctx.quadraticCurveTo(14, 10, 0, 0);
      ctx.fill();
      ctx.stroke();

      // Ribbon Tails
      ctx.beginPath();
      ctx.moveTo(-2, 2); ctx.lineTo(-10, 16); ctx.lineTo(-5, 14); ctx.lineTo(0, 4);
      ctx.moveTo(2, 2); ctx.lineTo(10, 16); ctx.lineTo(5, 14); ctx.lineTo(0, 4);
      ctx.fill();

      // Center Knot (Pure White)
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(0, 0, 3.8, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    };

    // 👣 Baby Element: Tiny Pink Baby Footprint Pair
    const drawFootprint = () => {
      ctx.fillStyle = '#f472b6';

      // Left Foot Sole
      ctx.beginPath();
      ctx.ellipse(-6, 3, 4.5, 7.5, 0.15, 0, Math.PI * 2);
      ctx.fill();
      // 5 Toes
      ctx.beginPath(); ctx.arc(-8.5, -7, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-6.0, -8, 1.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-3.8, -8, 1.3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-1.8, -7.5, 1.1, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-0.2, -6.5, 0.9, 0, Math.PI * 2); ctx.fill();

      // Right Foot Sole
      ctx.beginPath();
      ctx.ellipse(6, 0, 4.5, 7.5, -0.15, 0, Math.PI * 2);
      ctx.fill();
      // 5 Toes
      ctx.beginPath(); ctx.arc(8.5, -10, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(6.0, -11, 1.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(3.8, -11, 1.3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(1.8, -10.5, 1.1, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(0.2, -9.5, 0.9, 0, Math.PI * 2); ctx.fill();
    };

    // 🎈 Baby Element: Puffy Pink Heart Balloon
    const drawBalloon = () => {
      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 1.8;

      // Heart Shape
      ctx.beginPath();
      ctx.arc(-5.5, -5.5, 5.5, Math.PI, 0);
      ctx.arc(5.5, -5.5, 5.5, Math.PI, 0);
      ctx.lineTo(0, 9);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Balloon Knot
      ctx.beginPath();
      ctx.moveTo(-2, 9); ctx.lineTo(2, 9); ctx.lineTo(0, 12);
      ctx.fill();

      // Wavy String
      ctx.strokeStyle = '#fda4af';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(0, 12);
      ctx.quadraticCurveTo(6, 18, 0, 24);
      ctx.quadraticCurveTo(-6, 30, 0, 36);
      ctx.stroke();
    };

    // 🫧 Baby Element: Iridescent Dream Bubble
    const drawBubble = () => {
      ctx.strokeStyle = '#f472b6';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.arc(0, 0, 14, 0, Math.PI * 2);
      ctx.stroke();

      // White Glint
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.arc(-5, -5, 8, 1.1 * Math.PI, 1.7 * Math.PI);
      ctx.stroke();
    };

    // --- MAIN ANIMATION LOOP ---
    const render = () => {
      t += 1;
      ctx.clearRect(0, 0, w, h);

      // 1. Draw Smiling Crescent Moon at Top Right
      const moonX = w > 768 ? w * 0.88 : w * 0.82;
      const moonY = h > 600 ? h * 0.14 : 75;
      drawMoon(moonX, moonY, t);

      // 2. Draw & Drift Fluffy White Clouds with Rosy Cheeks
      for (const c of clouds) {
        c.x += c.speed;
        if (c.x - 140 * c.scale > w) {
          c.x = -160 * c.scale;
          c.y = Math.random() * h * 0.75;
        }
        drawCloud(c.x, c.y, c.scale, c.opacity, true);
      }

      // 3. Draw & Twinkle Pink, White & Gold Stars
      for (const s of stars) {
        s.rotation += s.rotSpeed;
        const twinkle = Math.sin(t * s.twinkleSpeed + s.phase);
        const alpha = 0.45 + 0.55 * (twinkle * 0.5 + 0.5);

        if (s.isFourPoint) {
          drawFourPointStar(s.x, s.y, s.size * 2.4, s.color, alpha);
        } else {
          ctx.save();
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.size * 0.8, 0, Math.PI * 2);
          ctx.fillStyle = s.color;
          ctx.globalAlpha = alpha;
          ctx.shadowColor = s.color;
          ctx.shadowBlur = 8;
          ctx.fill();
          ctx.restore();
        }
      }

      // 4. Draw & Float Baby Dream Items (Bottles, Teddies, Pacifiers, Bows, Footprints, Balloons, Bubbles)
      for (const d of dreamItems) {
        d.y -= d.speedY;
        d.rotation += d.rotSpeed;
        const wobbleX = d.x + Math.sin(t * d.wobbleSpeed + d.phase) * d.wobbleDist;

        if (d.y < -50) {
          d.y = h + 50;
          d.x = Math.random() * w;
        }

        ctx.save();
        ctx.translate(wobbleX, d.y);
        ctx.scale(d.scale, d.scale);
        ctx.rotate(d.rotation);
        ctx.globalAlpha = d.opacity;
        ctx.shadowColor = 'rgba(244, 114, 182, 0.4)';
        ctx.shadowBlur = 10;

        switch (d.type) {
          case 'bottle':
            drawBottle();
            break;
          case 'teddy':
            drawTeddy();
            break;
          case 'pacifier':
            drawPacifier();
            break;
          case 'bow':
            drawBow();
            break;
          case 'footprint':
            drawFootprint();
            break;
          case 'balloon':
            drawBalloon();
            break;
          case 'bubble':
            drawBubble();
            break;
          case 'cloud':
            drawCloud(0, 0, 0.45, 0.9, true);
            break;
          default:
            drawBottle();
        }
        ctx.restore();
      }

      // 5. Draw Interactive Pink Fairy Stardust
      for (let i = stardust.length - 1; i >= 0; i--) {
        const p = stardust[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
        if (p.life <= 0) {
          stardust.splice(i, 1);
          continue;
        }
        drawFourPointStar(p.x, p.y, p.size * p.life * 2.0, p.color, p.life * 0.95);
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

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        inset: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 0,
      }}
    />
  );
};

export default Starfield;
'''

with open(starfield_source_path, "w", encoding="utf-8") as f:
    f.write(starfield_code)
print("1. Updated frontend/src/components/Starfield.jsx with White & Pink Baby Nursery code!")

# 2. Patch static/js/bundle.js with the new Starfield and White & Pink CSS
bundle_path = os.path.join("static", "js", "bundle.js")
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

# Compile the component to match bundle's Webpack module format
starfield_old_start = content.find("const Starfield = () => {")
starfield_old_end = content.find("_s(Starfield, \"UJgi7ynoup7eqypjnwyX/s32POg=\");", starfield_old_start)

if starfield_old_start != -1 and starfield_old_end != -1:
    compiled_starfield_js = '''const Starfield = () => {
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

    // Fluffy White Clouds with Rosy Cheeks
    const clouds = [
      { x: w * 0.05, y: h * 0.12, scale: 1.2, speed: 0.22, opacity: 0.85 },
      { x: w * 0.45, y: h * 0.06, scale: 0.95, speed: 0.16, opacity: 0.8 },
      { x: w * 0.78, y: h * 0.22, scale: 1.05, speed: 0.26, opacity: 0.85 },
      { x: w * 0.22, y: h * 0.45, scale: 0.85, speed: 0.18, opacity: 0.75 },
      { x: w * 0.65, y: h * 0.62, scale: 1.15, speed: 0.24, opacity: 0.82 },
      { x: -w * 0.12, y: h * 0.78, scale: 1.0, speed: 0.2, opacity: 0.8 }
    ];

    // Twinkling Baby Pink, White & Gold Stars
    const starColors = [
      '#f472b6', '#ec4899', '#ffffff', '#fbbf24', '#fbcfe8', '#fda4af'
    ];

    const stars = Array.from({ length: 90 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      size: Math.random() * 4.5 + 2.5,
      color: starColors[Math.floor(Math.random() * starColors.length)],
      twinkleSpeed: Math.random() * 0.035 + 0.018,
      phase: Math.random() * Math.PI * 2,
      rotation: Math.random() * Math.PI,
      rotSpeed: (Math.random() - 0.5) * 0.012,
      isFourPoint: Math.random() > 0.3
    }));

    // Floating Baby Elements in White & Pink
    const dreamTypes = ['bottle', 'teddy', 'pacifier', 'bow', 'footprint', 'balloon', 'bubble', 'cloud'];
    const dreamItems = Array.from({ length: 26 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      type: dreamTypes[i % dreamTypes.length],
      scale: Math.random() * 0.35 + 0.75,
      speedY: Math.random() * 0.4 + 0.28,
      wobbleSpeed: Math.random() * 0.02 + 0.012,
      wobbleDist: Math.random() * 25 + 15,
      phase: Math.random() * Math.PI * 2,
      rotation: (Math.random() - 0.5) * 0.35,
      rotSpeed: (Math.random() - 0.5) * 0.008,
      opacity: Math.random() * 0.25 + 0.75,
      color: starColors[Math.floor(Math.random() * starColors.length)]
    }));

    // Interactive Pink Fairy Stardust Trail
    const stardust = [];
    const handlePointerMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const px = e.clientX - rect.left;
      const py = e.clientY - rect.top;
      for (let i = 0; i < 3; i++) {
        stardust.push({
          x: px + (Math.random() - 0.5) * 24,
          y: py + (Math.random() - 0.5) * 24,
          vx: (Math.random() - 0.5) * 1.6,
          vy: Math.random() * -1.8 - 0.6,
          life: 1.0,
          decay: Math.random() * 0.025 + 0.02,
          size: Math.random() * 3.5 + 2,
          color: starColors[Math.floor(Math.random() * starColors.length)]
        });
      }
      if (stardust.length > 60) stardust.splice(0, 15);
    };
    window.addEventListener('pointermove', handlePointerMove, { passive: true });

    let animId;
    let t = 0;

    const drawFourPointStar = (cx, cy, outerRadius, color, alpha) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
      ctx.fillStyle = color;
      ctx.shadowColor = 'rgba(244, 114, 182, 0.6)';
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

    const drawCloud = (cx, cy, scale, opacity, withFace) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.scale(scale, scale);
      ctx.globalAlpha = opacity;
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = 'rgba(244, 114, 182, 0.28)';
      ctx.shadowBlur = 18;

      ctx.beginPath();
      ctx.arc(0, 0, 32, 0, Math.PI * 2);
      ctx.arc(26, -12, 26, 0, Math.PI * 2);
      ctx.arc(52, 2, 28, 0, Math.PI * 2);
      ctx.arc(-26, -8, 24, 0, Math.PI * 2);
      ctx.arc(-46, 4, 22, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();

      if (withFace) {
        ctx.fillStyle = 'rgba(244, 114, 182, 0.7)';
        ctx.beginPath(); ctx.arc(-14, 4, 5, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(22, 4, 5, 0, Math.PI * 2); ctx.fill();

        ctx.strokeStyle = '#be185d';
        ctx.lineWidth = 1.8;
        ctx.lineCap = 'round';
        ctx.beginPath(); ctx.arc(-14, -4, 4, 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke();
        ctx.beginPath(); ctx.arc(22, -4, 4, 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke();
        ctx.beginPath(); ctx.arc(4, 5, 5, 0.1 * Math.PI, 0.9 * Math.PI); ctx.stroke();
      }

      ctx.restore();
    };

    const drawMoon = (cx, cy, time) => {
      ctx.save();
      ctx.translate(cx, cy);

      const breathe = Math.sin(time * 0.002) * 10;
      const haloGrad = ctx.createRadialGradient(0, 0, 20, 0, 0, 90 + breathe);
      haloGrad.addColorStop(0, 'rgba(254, 240, 138, 0.45)');
      haloGrad.addColorStop(0.5, 'rgba(251, 113, 133, 0.22)');
      haloGrad.addColorStop(1, 'rgba(254, 240, 138, 0)');
      ctx.fillStyle = haloGrad;
      ctx.beginPath();
      ctx.arc(0, 0, 90 + breathe, 0, Math.PI * 2);
      ctx.fill();

      drawCloud(10, 36, 0.65, 0.95, false);

      ctx.save();
      ctx.beginPath();
      ctx.arc(0, 0, 42, 0, Math.PI * 2, false);
      ctx.arc(16, -12, 38, 0, Math.PI * 2, true);
      ctx.closePath();
      const moonGrad = ctx.createLinearGradient(-35, -35, 25, 35);
      moonGrad.addColorStop(0, '#fffbeb');
      moonGrad.addColorStop(0.5, '#fde047');
      moonGrad.addColorStop(1, '#f59e0b');
      ctx.fillStyle = moonGrad;
      ctx.shadowColor = 'rgba(251, 113, 133, 0.5)';
      ctx.shadowBlur = 16;
      ctx.fill();
      ctx.restore();

      ctx.save();
      ctx.strokeStyle = '#9d174d';
      ctx.lineWidth = 2.0;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.arc(-11, -3, 7, 0.2 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-11, 4); ctx.lineTo(-11, 8);
      ctx.moveTo(-16, 3); ctx.lineTo(-18, 6);
      ctx.moveTo(-6, 3); ctx.lineTo(-4, 6);
      ctx.stroke();

      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      ctx.arc(-8, 12, 6.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.arc(-4, 14, 5.0, 0.1 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();

      ctx.save();
      ctx.translate(-10, -36);
      ctx.rotate(-0.35 + Math.sin(time * 0.002) * 0.08);

      ctx.beginPath();
      ctx.moveTo(-14, 7);
      ctx.quadraticCurveTo(6, -26, 32, -16);
      ctx.quadraticCurveTo(8, 4, 14, 9);
      ctx.closePath();
      ctx.fillStyle = '#f472b6';
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-2, -6, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(10, -8, 2.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(20, -12, 2.5, 0, Math.PI * 2); ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-16, 5, 30, 8, 4);
      } else {
        ctx.rect(-16, 5, 30, 8);
      }
      ctx.fill();

      ctx.beginPath();
      ctx.arc(34, -16, 6.5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = '#fbcfe8';
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.restore();

      ctx.restore();
    };

    const drawBottle = () => {
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-10, -5, 20, 28, 5);
      } else {
        ctx.rect(-10, -5, 20, 28);
      }
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#fffbeb';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-8, 3, 16, 18, [0, 0, 4, 4]);
      } else {
        ctx.rect(-8, 3, 16, 18);
      }
      ctx.fill();

      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      ctx.arc(-3, 10, 2.5, Math.PI, 0);
      ctx.arc(3, 10, 2.5, Math.PI, 0);
      ctx.lineTo(0, 16);
      ctx.closePath();
      ctx.fill();

      ctx.strokeStyle = '#f472b6';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      ctx.moveTo(-6, 2); ctx.lineTo(-1, 2);
      ctx.moveTo(-6, 7); ctx.lineTo(-2, 7);
      ctx.moveTo(-6, 12); ctx.lineTo(-1, 12);
      ctx.stroke();

      ctx.fillStyle = '#f472b6';
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-8, -10, 16, 5, 2);
      } else {
        ctx.rect(-8, -10, 16, 5);
      }
      ctx.fill();

      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.arc(0, -12, 4.5, 0, Math.PI * 2);
      ctx.fill();
    };

    const drawTeddy = () => {
      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#db2777';
      ctx.lineWidth = 1.8;
      ctx.beginPath(); ctx.arc(-11, -9, 6.0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(11, -9, 6.0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-11, -9, 3.2, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(11, -9, 3.2, 0, Math.PI * 2); ctx.fill();

      ctx.fillStyle = '#fbcfe8';
      ctx.beginPath();
      ctx.arc(0, 2, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(0, 5, 6.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#831843';
      ctx.beginPath(); ctx.arc(-5, 0, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(5, 0, 1.8, 0, Math.PI * 2); ctx.fill();

      ctx.fillStyle = '#ec4899';
      ctx.beginPath(); ctx.arc(0, 3.5, 2.2, 0, Math.PI * 2); ctx.fill();

      ctx.strokeStyle = '#be185d';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(-2, 7, 2.5, 0.2 * Math.PI, 0.9 * Math.PI);
      ctx.arc(2, 7, 2.5, 0.1 * Math.PI, 0.8 * Math.PI);
      ctx.stroke();
    };

    const drawPacifier = () => {
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2.4;
      ctx.shadowColor = 'rgba(244, 114, 182, 0.4)';
      ctx.shadowBlur = 6;
      ctx.beginPath();
      ctx.arc(0, 11, 7.5, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.ellipse(0, 0, 15, 9.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(-7, 0, 2.0, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(7, 0, 2.0, 0, Math.PI * 2); ctx.fill();

      ctx.fillStyle = '#fde047';
      ctx.beginPath();
      ctx.arc(0, -9, 6.0, 0, Math.PI * 2);
      ctx.fill();
    };

    const drawBow = () => {
      ctx.fillStyle = '#ec4899';
      ctx.strokeStyle = '#be185d';
      ctx.lineWidth = 1.6;

      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.quadraticCurveTo(-14, -10, -12, 0);
      ctx.quadraticCurveTo(-14, 10, 0, 0);
      ctx.fill();
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.quadraticCurveTo(14, -10, 12, 0);
      ctx.quadraticCurveTo(14, 10, 0, 0);
      ctx.fill();
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-2, 2); ctx.lineTo(-10, 16); ctx.lineTo(-5, 14); ctx.lineTo(0, 4);
      ctx.moveTo(2, 2); ctx.lineTo(10, 16); ctx.lineTo(5, 14); ctx.lineTo(0, 4);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(0, 0, 3.8, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    };

    const drawFootprint = () => {
      ctx.fillStyle = '#f472b6';

      ctx.beginPath();
      ctx.ellipse(-6, 3, 4.5, 7.5, 0.15, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath(); ctx.arc(-8.5, -7, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-6.0, -8, 1.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-3.8, -8, 1.3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-1.8, -7.5, 1.1, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(-0.2, -6.5, 0.9, 0, Math.PI * 2); ctx.fill();

      ctx.beginPath();
      ctx.ellipse(6, 0, 4.5, 7.5, -0.15, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath(); ctx.arc(8.5, -10, 1.8, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(6.0, -11, 1.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(3.8, -11, 1.3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(1.8, -10.5, 1.1, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(0.2, -9.5, 0.9, 0, Math.PI * 2); ctx.fill();
    };

    const drawBalloon = () => {
      ctx.fillStyle = '#f472b6';
      ctx.strokeStyle = '#ec4899';
      ctx.lineWidth = 1.8;

      ctx.beginPath();
      ctx.arc(-5.5, -5.5, 5.5, Math.PI, 0);
      ctx.arc(5.5, -5.5, 5.5, Math.PI, 0);
      ctx.lineTo(0, 9);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(-2, 9); ctx.lineTo(2, 9); ctx.lineTo(0, 12);
      ctx.fill();

      ctx.strokeStyle = '#fda4af';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(0, 12);
      ctx.quadraticCurveTo(6, 18, 0, 24);
      ctx.quadraticCurveTo(-6, 30, 0, 36);
      ctx.stroke();
    };

    const drawBubble = () => {
      ctx.strokeStyle = '#f472b6';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.arc(0, 0, 14, 0, Math.PI * 2);
      ctx.stroke();

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.arc(-5, -5, 8, 1.1 * Math.PI, 1.7 * Math.PI);
      ctx.stroke();
    };

    const render = () => {
      t += 1;
      ctx.clearRect(0, 0, w, h);

      const moonX = w > 768 ? w * 0.88 : w * 0.82;
      const moonY = h > 600 ? h * 0.14 : 75;
      drawMoon(moonX, moonY, t);

      for (const c of clouds) {
        c.x += c.speed;
        if (c.x - 140 * c.scale > w) {
          c.x = -160 * c.scale;
          c.y = Math.random() * h * 0.75;
        }
        drawCloud(c.x, c.y, c.scale, c.opacity, true);
      }

      for (const s of stars) {
        s.rotation += s.rotSpeed;
        const twinkle = Math.sin(t * s.twinkleSpeed + s.phase);
        const alpha = 0.45 + 0.55 * (twinkle * 0.5 + 0.5);

        if (s.isFourPoint) {
          drawFourPointStar(s.x, s.y, s.size * 2.4, s.color, alpha);
        } else {
          ctx.save();
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.size * 0.8, 0, Math.PI * 2);
          ctx.fillStyle = s.color;
          ctx.globalAlpha = alpha;
          ctx.shadowColor = s.color;
          ctx.shadowBlur = 8;
          ctx.fill();
          ctx.restore();
        }
      }

      for (const d of dreamItems) {
        d.y -= d.speedY;
        d.rotation += d.rotSpeed;
        const wobbleX = d.x + Math.sin(t * d.wobbleSpeed + d.phase) * d.wobbleDist;

        if (d.y < -50) {
          d.y = h + 50;
          d.x = Math.random() * w;
        }

        ctx.save();
        ctx.translate(wobbleX, d.y);
        ctx.scale(d.scale, d.scale);
        ctx.rotate(d.rotation);
        ctx.globalAlpha = d.opacity;
        ctx.shadowColor = 'rgba(244, 114, 182, 0.4)';
        ctx.shadowBlur = 10;

        switch (d.type) {
          case 'bottle':
            drawBottle();
            break;
          case 'teddy':
            drawTeddy();
            break;
          case 'pacifier':
            drawPacifier();
            break;
          case 'bow':
            drawBow();
            break;
          case 'footprint':
            drawFootprint();
            break;
          case 'balloon':
            drawBalloon();
            break;
          case 'bubble':
            drawBubble();
            break;
          case 'cloud':
            drawCloud(0, 0, 0.45, 0.9, true);
            break;
          default:
            drawBottle();
        }
        ctx.restore();
      }

      for (let i = stardust.length - 1; i >= 0; i--) {
        const p = stardust[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
        if (p.life <= 0) {
          stardust.splice(i, 1);
          continue;
        }
        drawFourPointStar(p.x, p.y, p.size * p.life * 2.0, p.color, p.life * 0.95);
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
    content = content[:starfield_old_start] + compiled_starfield_js + content[starfield_old_end:]
    print("2. Replaced Starfield in bundle.js with Baby Pink & White animation!")
else:
    print("[ERROR] Could not find Starfield boundaries in bundle.js")
    exit(1)

# Update .App and card styling in bundle.js
white_pink_app_bg = "background: linear-gradient(135deg, #fff5f8 0%, #fde2ec 28%, #fce7f3 60%, #fff0f5 100%);"
content = re.sub(r'background:\s*radial-gradient\(ellipse at [^;]+;', white_pink_app_bg, content)

white_pink_glass = "background: rgba(255, 255, 255, 0.88); border: 2px solid rgba(244, 114, 182, 0.35); box-shadow: 0 16px 36px rgba(244, 114, 182, 0.16);"
content = re.sub(r'background:\s*linear-gradient\(180deg,\s*rgba\(3[0-9],[^;]+;', white_pink_glass, content)

with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)
print("3. Saved updated bundle.js!")

# 3. Update templates/react_index.html with master CSS overrides for White & Pink theme
react_index_path = os.path.join("templates", "react_index.html")
react_html = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>BabyCry AI — 3D Multimodal Infant Distress Monitor</title>
    <meta name="description" content="AI-Powered Multimodal Infant Distress Monitor combining Face Emotion AI with BabyCry Acoustics." />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
    
    <!-- Global React/react safety shims -->
    <script>
        window.React = window.React || {};
        window.react = window.React;
        window.ReactDOM = window.ReactDOM || {};
        window.reactDom = window.ReactDOM;
        window.addEventListener("error", function(e) {
            if (e.error instanceof DOMException && e.error.name === "DataCloneError" && e.message && e.message.includes("PerformanceServerTiming")) {
                e.stopImmediatePropagation();
                e.preventDefault();
            }
        }, true);
    </script>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --background: 340 100% 98%;
            --foreground: 335 45% 20%;
        }
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: #fff5f8 !important;
            background-image: url('/static/baby_bg.jpg') !important;
            background-repeat: repeat !important;
            background-size: 380px auto !important;
            background-attachment: fixed !important;
            background-position: top center !important;
            color: #1e293b !important;
            font-family: 'Quicksand', 'Inter', system-ui, sans-serif;
            overflow-x: hidden;
            min-height: 100vh;
        }

        .App {
            background-color: transparent !important;
            background-image: url('/static/baby_bg.jpg') !important;
            background-repeat: repeat !important;
            background-size: 380px auto !important;
            background-attachment: fixed !important;
            background-position: top center !important;
            color: #1e293b !important;
            min-height: 100vh;
            position: relative;
        }

        /* Soft ambient canvas so the custom baby illustration wallpaper is crisp and clearly visible */
        canvas {
            z-index: 1 !important;
            pointer-events: none !important;
            opacity: 0.22 !important;
        }

        .content-wrap {
            position: relative;
            z-index: 5 !important;
        }

        /* Sweet White & Pink Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.90) !important;
            border: 2px solid rgba(244, 114, 182, 0.35) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            box-shadow: 0 16px 36px rgba(244, 114, 182, 0.16), 0 2px 10px rgba(0, 0, 0, 0.04) !important;
            color: #1e293b !important;
        }

        .card-header {
            background: linear-gradient(135deg, rgba(253, 242, 248, 0.98), rgba(252, 231, 243, 0.90)) !important;
            border-bottom: 1.5px solid rgba(244, 114, 182, 0.25) !important;
            padding: 14px 20px !important;
        }

        .card-title {
            color: #831843 !important; /* Rich raspberry rose */
            font-weight: 700 !important;
            font-family: 'Quicksand', sans-serif !important;
            font-size: 0.96rem !important;
        }

        .card-subtle {
            color: #be185d !important;
            font-weight: 700 !important;
        }

        /* Top Header Bar in Sweet Pink & Cloud White */
        header {
            background: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: 2.5px solid rgba(244, 114, 182, 0.35) !important;
            box-shadow: 0 6px 24px rgba(244, 114, 182, 0.15) !important;
        }

        /* Buttons in Vibrant Baby Pink */
        .btn-mini {
            background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.7) !important;
            color: #ffffff !important;
            padding: 8px 18px !important;
            border-radius: 14px !important;
            font-size: 0.82rem !important;
            font-weight: 700 !important;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        .btn-mini:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(236, 72, 153, 0.45) !important;
            background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
        }

        /* Footer in Sweet White/Pink */
        .foot {
            background: rgba(255, 255, 255, 0.88) !important;
            border-top: 2px solid rgba(244, 114, 182, 0.25) !important;
            color: #9d174d !important;
            font-weight: 600 !important;
        }
        .foot strong {
            color: #831843 !important;
        }

        /* Custom gentle baby pink scrollbar */
        ::-webkit-scrollbar {
            width: 9px;
        }
        ::-webkit-scrollbar-track {
            background: #fdf2f8;
        }
        ::-webkit-scrollbar-thumb {
            background: #f472b6;
            border-radius: 6px;
            border: 2px solid #fdf2f8;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #ec4899;
        }
    </style>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <script defer src="/static/js/bundle.js?v=12.0"></script>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
"""

with open(react_index_path, "w", encoding="utf-8") as f:
    f.write(react_html)
print("4. Updated templates/react_index.html with master White & Pink theme and bundle.js?v=12.0!")

# 4. Update templates/index.html (classic dashboard)
classic_index_path = os.path.join("templates", "index.html")
with open(classic_index_path, "r", encoding="utf-8") as f:
    classic_content = f.read()

classic_old_bg = "background-color: #090c18;"
classic_new_bg = "background-color: #fff5f8;"
classic_content = classic_content.replace(classic_old_bg, classic_new_bg)
classic_content = classic_content.replace("--bg-primary: #090c18;", "--bg-primary: #fff5f8;")
classic_content = classic_content.replace("--bg-secondary: #12182e;", "--bg-secondary: #fdf2f8;")
classic_content = classic_content.replace("--bg-card: rgba(22, 30, 56, 0.75);", "--bg-card: rgba(255, 255, 255, 0.90);")
classic_content = classic_content.replace("--text-main: #f1f5f9;", "--text-main: #1e293b;")

with open(classic_index_path, "w", encoding="utf-8") as f:
    f.write(classic_content)
print("5. Updated templates/index.html with White & Pink palette!")

print("\n[SUCCESS] Master White & Pink Baby Nursery theme applied across all files!")
