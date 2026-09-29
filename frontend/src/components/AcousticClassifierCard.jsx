import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const archetypeItems = [
  {
    id: 'hungry',
    label: 'Baby Hungry',
    sample: 'sample_hungry.wav',
    bg: '#fdecf2',
    borderColor: '#fbcfe8',
    img: '/static/images/cry_archetypes/hungry.png',
  },
  {
    id: 'belly_pain',
    label: 'Baby Belly Pain',
    sample: 'sample_belly_pain.wav',
    bg: '#fae9fb',
    borderColor: '#e9d5ff',
    img: '/static/images/cry_archetypes/belly_pain.png',
  },
  {
    id: 'burping',
    label: 'Burping Needed',
    sample: 'sample_burping.wav',
    bg: '#e7f1fd',
    borderColor: '#bae6fd',
    img: '/static/images/cry_archetypes/burping.png',
  },
  {
    id: 'discomfort',
    label: 'Baby Discomfort',
    sample: 'sample_tone.wav',
    bg: '#fff6e7',
    borderColor: '#fef08a',
    img: '/static/images/cry_archetypes/discomfort.png',
  },
  {
    id: 'tired',
    label: 'Tired Cry',
    sample: 'sample_tired.wav',
    bg: '#edf8f2',
    borderColor: '#bbf7d0',
    img: '/static/images/cry_archetypes/tired.png',
  },
  {
    id: 'hunger_cry',
    label: 'Hunger Cry',
    sample: 'sample_hungry.wav',
    bg: '#f2ebfd',
    borderColor: '#ddd6fe',
    img: '/static/images/cry_archetypes/hunger_cry.png',
  },
  {
    id: 'other',
    label: 'Other Cry',
    sample: 'demo_hungry.wav',
    bg: '#fee7ed',
    borderColor: '#fecdd3',
    img: '/static/images/cry_archetypes/other.png',
  },
  {
    id: 'calm',
    label: 'Calm / Sleeping',
    sample: 'sample_tone.wav',
    bg: '#ebf5fe',
    borderColor: '#ccfbf1',
    img: '/static/images/cry_archetypes/calm.png',
  },
];

const AcousticClassifierCard = ({ onRecord, onSample, onUpload, recording, selectedSample }) => {
  const [countdown, setCountdown] = useState(0);
  const [activeId, setActiveId] = useState(null);

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

  const handleUploadClick = () => {
    const inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = 'audio/*';
    inp.onchange = (e) => {
      const f = e.target.files && e.target.files[0];
      if (f && onUpload) onUpload(f);
    };
    inp.click();
  };

  const handleCardClick = async (item) => {
    setActiveId(item.id);
    try {
      const audio = new Audio('/audio_samples/' + item.sample);
      audio.play().catch(() => {});
    } catch (e) {}

    try {
      const res = await fetch('/api/audio_classify?sample=' + item.sample, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        onSample && onSample({ id: item.id, label: item.label, data });
      } else {
        onSample && onSample(item);
      }
    } catch (err) {
      onSample && onSample(item);
    }

    setTimeout(() => {
      setActiveId(null);
    }, 3000);
  };

  return (
    <div
      className="glass-card"
      style={{
        background: 'rgba(255, 255, 255, 0.94)',
        borderRadius: 24,
        padding: '24px 28px',
        border: '2px solid rgba(244, 114, 182, 0.35)',
        boxShadow: '0 20px 40px rgba(244, 114, 182, 0.16), 0 2px 10px rgba(0, 0, 0, 0.04)',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            fontSize: '1.25rem',
            fontWeight: 800,
            color: '#334155',
            fontFamily: "'Quicksand', 'Outfit', sans-serif",
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
            <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
            <path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
          </svg>
          <span>Acoustic Baby Cry Classifier</span>
        </div>
        <span
          style={{
            fontSize: '0.84rem',
            fontWeight: 800,
            color: '#f43f5e',
            letterSpacing: '0.12em',
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          194-DIM ACOUSTIC SVC
        </span>
      </div>

      {/* Top Action Buttons */}
      <div style={{ display: 'flex', gap: 16, marginBottom: 22, alignItems: 'stretch' }}>
        {/* Record Button */}
        <motion.div
          whileHover={{ y: -2, scale: 1.01 }}
          whileTap={{ scale: 0.98 }}
          onClick={startRecord}
          style={{
            flex: 1.85,
            background: recording
              ? 'linear-gradient(135deg, #e11d48 0%, #be123c 100%)'
              : 'linear-gradient(135deg, #fb7185 0%, #f43f5e 48%, #e11d48 100%)',
            borderRadius: 22,
            padding: '12px 20px 12px 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: recording
              ? '0 10px 28px rgba(225, 29, 72, 0.55), inset 0 2px 4px rgba(0,0,0,0.1)'
              : '0 10px 24px rgba(244, 63, 94, 0.32), 0 2px 6px rgba(0,0,0,0.04)',
            userSelect: 'none',
            border: '1.5px solid rgba(255, 255, 255, 0.65)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div
              style={{
                width: 44,
                height: 44,
                borderRadius: '50%',
                background: 'rgba(255, 255, 255, 0.24)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
            </div>
            <span
              style={{
                color: '#ffffff',
                fontSize: '1.12rem',
                fontWeight: 800,
                fontFamily: "'Quicksand', 'Inter', sans-serif",
              }}
            >
              {recording ? 'Recording Cry...' : countdown > 0 ? `Starting in ${countdown}...` : 'Record Cry via Mic (3s)'}
            </span>
          </div>
          <img
            src="/static/images/cry_archetypes/btn_record_baby_alpha.png"
            alt="Crying baby"
            style={{
              height: 68,
              width: 'auto',
              objectFit: 'contain',
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.12))',
            }}
          />
        </motion.div>

        {/* Upload Audio Button */}
        <motion.div
          whileHover={{ y: -2, scale: 1.01 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleUploadClick}
          style={{
            flex: 1.15,
            background: 'linear-gradient(135deg, #818cf8 0%, #6366f1 100%)',
            borderRadius: 22,
            padding: '12px 18px 12px 22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: '0 10px 24px rgba(99, 102, 241, 0.32), 0 2px 6px rgba(0,0,0,0.04)',
            userSelect: 'none',
            border: '1.5px solid rgba(255, 255, 255, 0.65)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div
              style={{
                width: 44,
                height: 44,
                borderRadius: '50%',
                background: 'rgba(255, 255, 255, 0.24)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" />
                <path d="M12 12v9" />
                <path d="m16 16-4-4-4 4" />
              </svg>
            </div>
            <div
              style={{
                color: '#ffffff',
                fontSize: '1.08rem',
                fontWeight: 800,
                lineHeight: 1.18,
                fontFamily: "'Quicksand', 'Inter', sans-serif",
              }}
            >
              Upload<br />Audio
            </div>
          </div>
          <img
            src="/static/images/cry_archetypes/btn_upload_baby_alpha.png"
            alt="Headphone baby"
            style={{
              height: 68,
              width: 'auto',
              objectFit: 'contain',
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.12))',
            }}
          />
        </motion.div>
      </div>

      {/* Subheader */}
      <div style={{ marginBottom: 16 }}>
        <div
          style={{
            fontSize: '0.84rem',
            fontWeight: 800,
            color: '#64748b',
            letterSpacing: '0.14em',
            fontFamily: "'JetBrains Mono', monospace",
            display: 'inline-block',
            position: 'relative',
          }}
        >
          TEST ARCHETYPE CRY SAMPLES:
          <div
            style={{
              width: 42,
              height: 3.5,
              background: '#f472b6',
              borderRadius: 2,
              marginTop: 5,
            }}
          />
        </div>
      </div>

      {/* 8 Archetype Cards Grid (2 rows x 4 columns) */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 14,
        }}
      >
        {archetypeItems.map((item) => {
          const isSelected = activeId === item.id || selectedSample === item.id;
          return (
            <motion.div
              key={item.id}
              whileHover={{ y: -4, scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              onClick={() => handleCardClick(item)}
              style={{
                background: item.bg,
                border: isSelected ? '2.5px solid #f43f5e' : `2px solid ${item.borderColor}`,
                borderRadius: 20,
                padding: '12px 10px 14px 10px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'space-between',
                cursor: 'pointer',
                boxShadow: isSelected
                  ? '0 12px 28px rgba(244, 63, 94, 0.32), 0 0 0 3px rgba(244, 114, 182, 0.25)'
                  : '0 6px 16px rgba(0, 0, 0, 0.03)',
                transform: isSelected ? 'translateY(-4px)' : 'none',
                transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              <img
                src={item.img}
                alt={item.label}
                style={{
                  width: '100%',
                  height: 94,
                  objectFit: 'contain',
                  marginBottom: 8,
                  transition: 'transform 0.2s ease',
                }}
              />
              <div
                style={{
                  fontSize: '0.94rem',
                  fontWeight: 700,
                  color: '#334155',
                  textAlign: 'center',
                  fontFamily: "'Quicksand', 'Outfit', sans-serif",
                }}
              >
                {item.label}
              </div>

              {isSelected && (
                <div style={{ display: 'flex', gap: 3, alignItems: 'center', marginTop: 4 }}>
                  <span style={{ width: 3, height: 10, background: '#f43f5e', borderRadius: 2 }} />
                  <span style={{ width: 3, height: 16, background: '#f43f5e', borderRadius: 2 }} />
                  <span style={{ width: 3, height: 8, background: '#f43f5e', borderRadius: 2 }} />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      <AnimatePresence>
        {activeId && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{ overflow: 'hidden', marginTop: 14 }}
          >
            <div
              style={{
                padding: '10px 14px',
                background: 'rgba(244, 114, 182, 0.1)',
                border: '1.5px solid rgba(244, 114, 182, 0.35)',
                borderRadius: 12,
                fontSize: '0.82rem',
                color: '#be185d',
                fontFamily: "'JetBrains Mono', monospace",
                display: 'flex',
                alignItems: 'center',
                gap: 8,
              }}
            >
              <span>◈</span> Analyzing Archetype Cry & Fusing with Face Telemetry...
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AcousticClassifierCard;
