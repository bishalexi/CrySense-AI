import React, { useEffect, useRef } from 'react';

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
