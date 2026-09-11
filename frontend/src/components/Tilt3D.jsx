import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';

const Tilt3D = ({ children, className = '', intensity = 10, glare = true, style = {} }) => {
  const ref = useRef(null);
  const [t, setT] = useState({ rx: 0, ry: 0, gx: 50, gy: 50, active: false });

  const handleMove = (e) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width;
    const py = (e.clientY - rect.top) / rect.height;
    const ry = (px - 0.5) * intensity * 2;
    const rx = -(py - 0.5) * intensity * 2;
    setT({ rx, ry, gx: px * 100, gy: py * 100, active: true });
  };

  const handleLeave = () => setT({ rx: 0, ry: 0, gx: 50, gy: 50, active: false });

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      className={className}
      style={{
        transformStyle: 'preserve-3d',
        transform: `perspective(1200px) rotateX(${t.rx}deg) rotateY(${t.ry}deg)`,
        transition: t.active ? 'transform 0.05s linear' : 'transform 0.6s cubic-bezier(.2,.9,.3,1.4)',
        position: 'relative',
        ...style,
      }}
    >
      <div style={{ transformStyle: 'preserve-3d', position: 'relative' }}>
        {children}
        {glare && (
          <div
            style={{
              pointerEvents: 'none',
              position: 'absolute',
              inset: 0,
              borderRadius: 'inherit',
              background: `radial-gradient(circle at ${t.gx}% ${t.gy}%, rgba(120, 180, 255, 0.18), transparent 55%)`,
              opacity: t.active ? 1 : 0,
              transition: 'opacity 0.3s ease',
              mixBlendMode: 'screen',
            }}
          />
        )}
      </div>
    </motion.div>
  );
};

export default Tilt3D;
