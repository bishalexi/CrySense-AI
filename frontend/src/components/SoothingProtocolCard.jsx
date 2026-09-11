import React from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import { Sparkles, Check } from 'lucide-react';

const SoothingProtocolCard = ({ items }) => {
  return (
    <Tilt3D intensity={4} className="glass-card" style={{ padding: '18px 20px' }}>
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 8,
          fontSize: '0.92rem',
          fontWeight: 700,
          color: '#e2e8f0',
          marginBottom: 14,
        }}
      >
        <Sparkles size={16} color="#38bdf8" /> Pediatric Caregiver Soothing Protocol
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {items.map((it, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08, duration: 0.5 }}
            whileHover={{ x: 4, scale: 1.01 }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '10px 12px',
              background: 'rgba(15, 23, 42, 0.55)',
              border: '1px solid rgba(56, 189, 248, 0.15)',
              borderLeft: '3px solid #38bdf8',
              borderRadius: 8,
              fontSize: '0.85rem',
              color: '#e2e8f0',
              cursor: 'default',
            }}
          >
            <span
              style={{
                width: 22,
                height: 22,
                borderRadius: '50%',
                background: 'rgba(56, 189, 248, 0.15)',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#38bdf8',
                flexShrink: 0,
              }}
            >
              <Check size={13} />
            </span>
            {it}
          </motion.div>
        ))}
      </div>
    </Tilt3D>
  );
};

export default SoothingProtocolCard;
