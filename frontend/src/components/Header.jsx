import React from 'react';
import { motion } from 'framer-motion';
import { Baby, Activity, Radio } from 'lucide-react';

const Pulse = ({ color }) => (
  <motion.span
    animate={{ scale: [1, 1.4, 1], opacity: [0.9, 0.4, 0.9] }}
    transition={{ duration: 1.6, repeat: Infinity }}
    style={{
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: color,
      display: 'inline-block',
      boxShadow: `0 0 12px ${color}`,
    }}
  />
);

const Header = () => {
  return (
    <header
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '18px 32px',
        position: 'relative',
        zIndex: 5,
        borderBottom: '1px solid rgba(148, 163, 184, 0.12)',
        background: 'rgba(10, 14, 24, 0.55)',
        backdropFilter: 'blur(14px)',
      }}
    >
      <motion.div
        initial={{ opacity: 0, x: -18 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        style={{ display: 'flex', alignItems: 'center', gap: 14 }}
      >
        <motion.div
          animate={{ rotateY: [0, 360] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
          style={{
            width: 48,
            height: 48,
            borderRadius: 14,
            background:
              'linear-gradient(135deg, #f472b6 0%, #a855f7 50%, #38bdf8 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow:
              '0 10px 30px rgba(168, 85, 247, 0.35), inset 0 1px 0 rgba(255,255,255,0.35)',
            transformStyle: 'preserve-3d',
          }}
        >
          <Baby size={26} color="#fff" strokeWidth={2.2} />
        </motion.div>
        <div>
          <div
            style={{
              fontSize: '1.15rem',
              fontWeight: 700,
              color: '#fff',
              letterSpacing: '-0.01em',
            }}
          >
            <span style={{ color: '#c4b5fd' }}>Multimodal</span> Infant Distress Monitor
          </div>
          <div
            style={{
              fontSize: '0.7rem',
              color: '#94a3b8',
              letterSpacing: '0.15em',
              fontFamily: 'JetBrains Mono, monospace',
              marginTop: 2,
            }}
          >
            FACE EMOTION AI (SLIM 320) + BABYCRY AI ACOUSTICS
          </div>
        </div>
      </motion.div>

      <div style={{ display: 'flex', gap: 12 }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 14px',
            borderRadius: 10,
            background: 'rgba(56, 189, 248, 0.10)',
            border: '1px solid rgba(56, 189, 248, 0.30)',
            color: '#38bdf8',
            fontSize: '0.72rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          <Pulse color="#38bdf8" />
          <Activity size={12} /> VISION ACTIVE
        </div>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 14px',
            borderRadius: 10,
            background: 'rgba(244, 63, 94, 0.10)',
            border: '1px solid rgba(244, 63, 94, 0.30)',
            color: '#fb7185',
            fontSize: '0.72rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          <Pulse color="#fb7185" />
          <Radio size={12} /> ACOUSTIC ACTIVE
        </div>
      </div>
    </header>
  );
};

export default Header;
