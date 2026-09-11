import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';

const Button3D = ({
  children,
  onClick,
  color = '#38bdf8',
  shadow = '#0ea5e9',
  size = 'md',
  wide = false,
  active = false,
  icon = null,
}) => {
  const [pressed, setPressed] = useState(false);
  const [hover, setHover] = useState(false);
  const ref = useRef(null);
  const [tilt, setTilt] = useState({ rx: 0, ry: 0 });

  const handleMove = (e) => {
    const el = ref.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - 0.5;
    const py = (e.clientY - r.top) / r.height - 0.5;
    setTilt({ rx: -py * 14, ry: px * 14 });
  };
  const reset = () => {
    setTilt({ rx: 0, ry: 0 });
    setHover(false);
  };

  const paddings = {
    sm: '8px 14px',
    md: '12px 18px',
    lg: '16px 26px',
  };

  return (
    <div
      ref={ref}
      onMouseEnter={() => setHover(true)}
      onMouseMove={handleMove}
      onMouseLeave={reset}
      style={{
        perspective: '800px',
        display: wide ? 'block' : 'inline-block',
        width: wide ? '100%' : 'auto',
      }}
    >
      <motion.button
        onMouseDown={() => setPressed(true)}
        onMouseUp={() => setPressed(false)}
        onClick={onClick}
        animate={{
          rotateX: tilt.rx,
          rotateY: tilt.ry,
          translateZ: pressed ? -4 : hover ? 6 : 0,
          scale: pressed ? 0.97 : 1,
        }}
        transition={{ type: 'spring', stiffness: 260, damping: 18 }}
        style={{
          border: 'none',
          cursor: 'pointer',
          padding: paddings[size],
          borderRadius: '14px',
          background: active
            ? `linear-gradient(135deg, ${color}, ${shadow})`
            : `linear-gradient(180deg, ${color} 0%, ${shadow} 100%)`,
          color: '#fff',
          fontWeight: 600,
          fontSize: size === 'lg' ? '1rem' : '0.88rem',
          letterSpacing: '0.02em',
          transformStyle: 'preserve-3d',
          width: wide ? '100%' : 'auto',
          boxShadow: pressed
            ? `0 2px 0 ${shadow}, 0 4px 10px rgba(0,0,0,0.35)`
            : `0 6px 0 ${shadow}, 0 12px 24px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.35)`,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '10px',
          transition: 'box-shadow 0.15s ease',
          textShadow: '0 1px 2px rgba(0,0,0,0.35)',
        }}
      >
        {icon}
        <span style={{ position: 'relative', zIndex: 1 }}>{children}</span>
        <span
          style={{
            position: 'absolute',
            inset: 0,
            borderRadius: 'inherit',
            background:
              'linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0) 50%)',
            pointerEvents: 'none',
          }}
        />
      </motion.button>
    </div>
  );
};

export default Button3D;
