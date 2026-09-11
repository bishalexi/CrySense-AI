import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import { Camera, Upload, Crosshair } from 'lucide-react';

const BabyFace3D = ({ mood = 'neutral' }) => {
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#07090e',
        overflow: 'hidden',
        zIndex: 1,
      }}
    >
      <img
        src="/video_feed"
        alt="Real-Time Neural Video Feed"
        onError={(e) => {
          e.currentTarget.onerror = null;
          setInterval(() => {
            e.currentTarget.src = '/api/snapshot?t=' + Date.now();
          }, 80);
        }}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          display: 'block',
        }}
      />
    </div>
  );
};

const ScanLine = () => (
  <motion.div
    initial={{ y: '-10%' }}
    animate={{ y: '110%' }}
    transition={{ duration: 2.5, repeat: Infinity, ease: 'linear' }}
    style={{
      position: 'absolute',
      left: 0,
      right: 0,
      height: 2,
      background:
        'linear-gradient(90deg, transparent, #00d4ff 20%, #a855f7 50%, #00d4ff 80%, transparent)',
      boxShadow: '0 0 12px #00d4ff',
      pointerEvents: 'none',
    }}
  />
);

const VideoFeedCard = ({ mood }) => {
  const [fps, setFps] = useState(20.7);
  const [latency, setLatency] = useState(19.5);
  const fileRef = useRef(null);

  useEffect(() => {
    const id = setInterval(() => {
      setFps((f) => +(f + (Math.random() - 0.5) * 1.5).toFixed(1));
      setLatency((l) => +(l + (Math.random() - 0.5) * 2).toFixed(1));
    }, 900);
    return () => clearInterval(id);
  }, []);

  return (
    <Tilt3D intensity={5} className="glass-card">
      <div className="card-header">
        <div className="card-title">
          <span className="dot-cyan" />
          <span>Infant Video Feed &amp; Targeting HUD</span>
        </div>
        <span className="card-subtle mono">Slim 320 SSD (320x240) + FERPlus</span>
      </div>

      <div
        style={{
          position: 'relative',
          height: 380,
          overflow: 'hidden',
          background:
            'radial-gradient(ellipse at center, #0f172a 0%, #020617 80%)',
          borderTop: '1px solid rgba(148,163,184,0.1)',
          borderBottom: '1px solid rgba(148,163,184,0.1)',
        }}
      >
        {/* HUD grid */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'linear-gradient(rgba(0,212,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.07) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        {/* HUD banner top */}
        <div
          style={{
            position: 'absolute',
            top: 12,
            left: 16,
            right: 16,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: '0.7rem',
            color: '#00d4ff',
            letterSpacing: '0.18em',
            textShadow: '0 0 8px rgba(0,212,255,0.65)',
          }}
        >
          <span>◈ ULTRA-LIGHT FACE &amp; EMOTION AI</span>
          <span>FPS: {fps} | LATENCY: {latency}ms | FACES: 1</span>
        </div>

        {/* Baby face */}
        <BabyFace3D mood={mood} />

        {/* Targeting crosshair */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 14, repeat: Infinity, ease: 'linear' }}
          style={{
            position: 'absolute',
            left: '50%',
            top: '52%',
            transform: 'translate(-50%, -50%)',
            color: '#00d4ff',
            opacity: 0.6,
          }}
        >
          <Crosshair size={320} strokeWidth={0.4} />
        </motion.div>

        {/* corner brackets */}
        {[
          { top: 60, left: 60, rot: 0 },
          { top: 60, right: 60, rot: 90 },
          { bottom: 90, left: 60, rot: 270 },
          { bottom: 90, right: 60, rot: 180 },
        ].map((c, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              ...c,
              width: 20,
              height: 20,
              borderTop: '2px solid #00d4ff',
              borderLeft: '2px solid #00d4ff',
              transform: `rotate(${c.rot}deg)`,
              boxShadow: '0 0 8px rgba(0,212,255,0.7)',
            }}
          />
        ))}

        <ScanLine />

        <div
          style={{
            position: 'absolute',
            bottom: 10,
            left: 16,
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: '0.68rem',
            color: '#a855f7',
            letterSpacing: '0.14em',
          }}
        >
          TARGET LOCKED • AFFECT: {mood.toUpperCase()}
        </div>
      </div>

      <div
        style={{
          padding: '12px 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: 14,
          flexWrap: 'wrap',
        }}
      >
        <div style={{ display: 'flex', gap: 20, fontSize: '0.82rem', fontFamily: 'JetBrains Mono, monospace', color: '#94a3b8' }}>
          <span>FPS: <strong style={{ color: '#38bdf8' }}>{fps}</strong></span>
          <span>Faces: <strong style={{ color: '#fff' }}>1</strong></span>
          <span>Facial Affect: <strong style={{ color: '#34d399', textTransform: 'capitalize' }}>{mood}</strong></span>
        </div>
        <button
          onClick={() => fileRef.current?.click()}
          className="btn-mini"
          style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}
        >
          <Upload size={14} /> Upload Face Photo
        </button>
        <input ref={fileRef} type="file" accept="image/*" style={{ display: 'none' }} />
      </div>
    </Tilt3D>
  );
};

export default VideoFeedCard;
