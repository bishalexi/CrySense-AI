import React from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';

const EmotionSpectrumCard = ({ classes }) => {
  return (
    <Tilt3D intensity={4} className="glass-card" style={{ padding: '18px 20px' }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 14,
        }}
      >
        <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#e2e8f0' }}>
          Facial Emotion Spectrum <span style={{ color: '#64748b', fontWeight: 400 }}>(Visual Tension)</span>
        </div>
        <span className="card-subtle mono">FERPLUS (8 CLASSES)</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {classes.map((c, idx) => (
          <div key={c.key}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '0.82rem',
                color: '#cbd5e1',
                marginBottom: 4,
              }}
            >
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                <span style={{ fontSize: '1rem' }}>{c.emoji}</span>
                {c.label}
              </span>
              <span className="mono" style={{ color: '#94a3b8' }}>
                {c.value.toFixed(1)}%
              </span>
            </div>
            <div
              style={{
                height: 10,
                borderRadius: 6,
                background: 'rgba(15, 23, 42, 0.8)',
                overflow: 'hidden',
                position: 'relative',
                boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.5), inset 0 -1px 0 rgba(255,255,255,0.05)',
              }}
            >
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${c.value}%` }}
                transition={{ duration: 1.1, delay: idx * 0.05, ease: 'easeOut' }}
                style={{
                  height: '100%',
                  background: `linear-gradient(90deg, ${c.color}aa, ${c.color})`,
                  boxShadow: `0 0 12px ${c.color}88, inset 0 1px 0 rgba(255,255,255,0.35)`,
                  borderRadius: 6,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </Tilt3D>
  );
};

export default EmotionSpectrumCard;
