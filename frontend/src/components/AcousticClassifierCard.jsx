import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Tilt3D from './Tilt3D';
import Button3D from './Button3D';
import { Mic, Upload, Waves, Music2, Bandage, Wind, Milk, Moon, AlertCircle } from 'lucide-react';
import { archetypeCries } from '../mock';

const iconMap = { Music2, Bandage, Wind, Milk, Moon, AlertCircle };

const WaveBars = ({ active }) => (
  <div style={{ display: 'inline-flex', gap: 3, alignItems: 'flex-end', height: 18 }}>
    {[0, 1, 2, 3, 4].map((i) => (
      <motion.span
        key={i}
        animate={{ height: active ? [4, 16, 6, 14, 4] : 4 }}
        transition={{ duration: 0.8, repeat: active ? Infinity : 0, delay: i * 0.08 }}
        style={{ width: 3, borderRadius: 2, background: '#fff', display: 'inline-block' }}
      />
    ))}
  </div>
);

const AcousticClassifierCard = ({ onRecord, onSample, onUpload, recording, selectedSample }) => {
  const [countdown, setCountdown] = useState(0);

  const startRecord = () => {
    if (recording) return;
    setCountdown(3);
    const iv = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) {
          clearInterval(iv);
          onRecord && onRecord();
          return 0;
        }
        return c - 1;
      });
    }, 1000);
  };

  return (
    <Tilt3D intensity={4} className="glass-card" style={{ padding: '18px 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            fontSize: '0.92rem',
            fontWeight: 700,
            color: '#e2e8f0',
          }}
        >
          <Waves size={16} color="#a855f7" /> Acoustic Baby Cry Classifier
        </div>
        <span className="card-subtle mono">194-DIM ACOUSTIC SVC</span>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 18 }}>
        <div style={{ flex: 2 }}>
          <Button3D
            wide
            size="lg"
            onClick={startRecord}
            color={recording ? '#f43f5e' : '#ef4444'}
            shadow={recording ? '#9f1239' : '#b91c1c'}
            icon={recording ? <WaveBars active /> : <Mic size={18} />}
          >
            {recording ? 'Recording...' : countdown > 0 ? `Starting in ${countdown}...` : 'Record Cry via Mic (3s)'}
          </Button3D>
        </div>
        <div style={{ flex: 1 }}>
          <Button3D
            wide
            size="lg"
            color="#8b5cf6"
            shadow="#6d28d9"
            icon={<Upload size={16} />}
            onClick={() => {
              const inp = document.createElement('input');
              inp.type = 'file';
              inp.accept = 'audio/*';
              inp.onchange = (e) => {
                const f = e.target.files && e.target.files[0];
                if (f && onUpload) onUpload(f);
              };
              inp.click();
            }}
          >
            Upload Audio
          </Button3D>
        </div>
      </div>

      <div style={{ fontSize: '0.7rem', color: '#94a3b8', letterSpacing: '0.15em', marginBottom: 12, fontFamily: 'JetBrains Mono, monospace' }}>
        TEST ARCHETYPE CRY SAMPLES:
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: 10,
        }}
      >
        {archetypeCries.map((s) => {
          const Icon = iconMap[s.icon] || Music2;
          const active = selectedSample === s.id;
          return (
            <motion.button
              key={s.id}
              whileHover={{ y: -4, rotateX: -6, rotateY: 4, scale: 1.03 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => onSample && onSample(s)}
              style={{
                background: active
                  ? `linear-gradient(135deg, ${s.tone}55, ${s.tone}22)`
                  : 'rgba(15, 23, 42, 0.6)',
                border: `1px solid ${active ? s.tone : 'rgba(148,163,184,0.15)'}`,
                borderRadius: 12,
                padding: '14px 8px',
                color: '#e2e8f0',
                fontSize: '0.78rem',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 6,
                transformStyle: 'preserve-3d',
                boxShadow: active
                  ? `0 8px 18px ${s.tone}55, inset 0 1px 0 rgba(255,255,255,0.1)`
                  : '0 4px 10px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05)',
              }}
            >
              <motion.span
                animate={active ? { y: [0, -3, 0] } : {}}
                transition={{ duration: 1.2, repeat: Infinity }}
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 8,
                  background: `${s.tone}22`,
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: s.tone,
                }}
              >
                <Icon size={18} />
              </motion.span>
              {s.label}
            </motion.button>
          );
        })}
      </div>

      <AnimatePresence>
        {selectedSample && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{ overflow: 'hidden', marginTop: 12 }}
          >
            <div
              style={{
                padding: '10px 12px',
                background: 'rgba(56, 189, 248, 0.08)',
                border: '1px solid rgba(56, 189, 248, 0.25)',
                borderRadius: 8,
                fontSize: '0.78rem',
                color: '#7dd3fc',
                fontFamily: 'JetBrains Mono, monospace',
              }}
            >
              ◈ Analyzing sample: {selectedSample}...
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Tilt3D>
  );
};

export default AcousticClassifierCard;
