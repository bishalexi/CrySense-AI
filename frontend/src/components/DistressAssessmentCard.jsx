import React from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import { distressLevels } from '../mock';

const DistressAssessmentCard = ({ percentage, level, visualStrain, acousticSeverity, primaryAffect }) => {
  const info = distressLevels[level] || distressLevels.mild;
  const radius = 62;
  const circ = 2 * Math.PI * radius;
  const dash = (percentage / 100) * circ;

  return (
    <Tilt3D intensity={5} className="glass-card" style={{ padding: '20px 22px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
        <div style={{ fontSize: '0.78rem', fontWeight: 700, letterSpacing: '0.15em', color: '#cbd5e1' }}>
          MULTIMODAL DISTRESS ASSESSMENT
        </div>
        <motion.span
          animate={{ boxShadow: [`0 0 0 ${info.color}55`, `0 0 22px ${info.color}55`, `0 0 0 ${info.color}55`] }}
          transition={{ duration: 2, repeat: Infinity }}
          style={{
            padding: '5px 10px',
            borderRadius: 6,
            fontSize: '0.68rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            background: `${info.color}22`,
            color: info.color,
            border: `1px solid ${info.color}55`,
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          {info.badge}
        </motion.span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginBottom: 16 }}>
        {/* 3D dial */}
        <div style={{ position: 'relative', width: 150, height: 150, perspective: 800 }}>
          <motion.svg
            width="150"
            height="150"
            viewBox="0 0 150 150"
            animate={{ rotateY: [0, 12, 0, -12, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
            style={{ transformStyle: 'preserve-3d', filter: `drop-shadow(0 8px 20px ${info.color}55)` }}
          >
            <defs>
              <linearGradient id="dialGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#10b981" />
                <stop offset="40%" stopColor="#f59e0b" />
                <stop offset="75%" stopColor="#f43f5e" />
              </linearGradient>
            </defs>
            <circle cx="75" cy="75" r={radius} stroke="rgba(148,163,184,0.15)" strokeWidth="10" fill="none" />
            <motion.circle
              cx="75"
              cy="75"
              r={radius}
              stroke="url(#dialGrad)"
              strokeWidth="10"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circ}
              initial={{ strokeDashoffset: circ }}
              animate={{ strokeDashoffset: circ - dash }}
              transition={{ duration: 1.6, ease: 'easeOut' }}
              transform="rotate(-90 75 75)"
            />
          </motion.svg>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
            }}
          >
            <motion.div
              key={percentage}
              initial={{ scale: 0.6, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 14 }}
              className="mono"
              style={{ fontSize: '1.9rem', fontWeight: 700, letterSpacing: '-0.02em', color: info.color }}
            >
              {percentage.toFixed(1)}%
            </motion.div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', letterSpacing: '0.15em', fontFamily: 'JetBrains Mono, monospace' }}>
              DISTRESS
            </div>
          </div>
        </div>

        <div style={{ flex: 1 }}>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff', marginBottom: 4 }}>{info.label}</div>
          <div style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
            {acousticSeverity > 5 ? 'Facial Strain + Acoustic Signal' : 'Facial Strain Only'}
          </div>
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 12,
          padding: '12px 14px',
          background: 'rgba(15, 23, 42, 0.6)',
          borderRadius: 10,
          border: '1px solid rgba(148,163,184,0.1)',
        }}
      >
        <div>
          <div style={{ fontSize: '0.65rem', color: '#64748b', letterSpacing: '0.14em', marginBottom: 4 }}>
            VISUAL STRAIN (FACE)
          </div>
          <div className="mono" style={{ fontSize: '1.05rem', fontWeight: 700, color: '#e2e8f0' }}>
            {visualStrain.toFixed(1)}%
          </div>
        </div>
        <div>
          <div style={{ fontSize: '0.65rem', color: '#64748b', letterSpacing: '0.14em', marginBottom: 4 }}>
            ACOUSTIC CRY SEVERITY
          </div>
          <div className="mono" style={{ fontSize: '1.05rem', fontWeight: 700, color: '#e2e8f0' }}>
            {acousticSeverity.toFixed(1)}%
          </div>
        </div>
      </div>

      <div style={{ marginTop: 12, fontSize: '0.8rem', color: '#94a3b8' }}>
        Visual facial detector observing primary affect: <span style={{ color: '#e2e8f0', fontWeight: 600 }}>‘{primaryAffect}’</span>.
      </div>
    </Tilt3D>
  );
};

export default DistressAssessmentCard;
