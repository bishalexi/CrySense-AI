import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import { Camera, Upload, Video, RefreshCw, AlertCircle, CheckCircle2 } from 'lucide-react';

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
      zIndex: 5,
    }}
  />
);

const VideoFeedCard = ({ mood = 'Neutral' }) => {
  const [cameraMode, setCameraMode] = useState('host'); // 'host', 'browser', 'sample'
  const [fps, setFps] = useState(30.0);
  const [latency, setLatency] = useState(14.5);
  const [facesCount, setFacesCount] = useState(1);
  const [dominantEmotion, setDominantEmotion] = useState(mood || 'Neutral');
  const [streamError, setStreamError] = useState(null);
  const [feedUrl, setFeedUrl] = useState('/video_feed');
  const [browserActive, setBrowserActive] = useState(false);

  const fileRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const browserStreamRef = useRef(null);
  const frameIntervalRef = useRef(null);

  // Poll backend telemetry for real camera speed & detections
  useEffect(() => {
    const pollId = setInterval(async () => {
      try {
        const res = await fetch('/api/telemetry');
        if (!res.ok) return;
        const data = await res.json();
        if (data.visual) {
          if (data.visual.fps !== undefined) setFps(data.visual.fps);
          if (data.visual.latency_ms !== undefined) setLatency(data.visual.latency_ms);
          if (data.visual.faces_count !== undefined) setFacesCount(data.visual.faces_count);
          if (data.visual.dominant_emotion) setDominantEmotion(data.visual.dominant_emotion);
        }
      } catch (e) {}
    }, 500);

    return () => clearInterval(pollId);
  }, []);

  // Stop browser stream helper
  const stopBrowserStream = () => {
    if (frameIntervalRef.current) {
      clearInterval(frameIntervalRef.current);
      frameIntervalRef.current = null;
    }
    if (browserStreamRef.current) {
      browserStreamRef.current.getTracks().forEach((t) => t.stop());
      browserStreamRef.current = null;
    }
    setBrowserActive(false);
  };

  // Switch to Host Camera
  const handleSelectHostCamera = async () => {
    stopBrowserStream();
    setCameraMode('host');
    setStreamError(null);
    setFeedUrl('/video_feed?t=' + Date.now());
    try {
      await fetch('/api/set_source?source=camera');
    } catch (e) {}
  };

  // Switch to Browser Camera (getUserMedia)
  const handleSelectBrowserCamera = async () => {
    try {
      setStreamError(null);
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setStreamError('Browser camera API is not supported on this browser/connection.');
        return;
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
        audio: false,
      });

      browserStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(() => {});
      }
      setCameraMode('browser');
      setBrowserActive(true);

      // Start frame capture loop sending frames to Python AI backend
      frameIntervalRef.current = setInterval(async () => {
        if (!videoRef.current || !canvasRef.current) return;
        const v = videoRef.current;
        if (v.readyState < 2) return;

        const c = canvasRef.current;
        c.width = 640;
        c.height = 480;
        const ctx = c.getContext('2d');
        ctx.drawImage(v, 0, 0, 640, 480);

        try {
          const b64 = c.toDataURL('image/jpeg', 0.8);
          const res = await fetch('/api/upload_frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: b64 }),
          });
          if (res.ok) {
            const resData = await res.json();
            if (resData.faces_count !== undefined) setFacesCount(resData.faces_count);
            if (resData.dominant_emotion) setDominantEmotion(resData.dominant_emotion);
            if (resData.fps !== undefined) setFps(resData.fps);
            if (resData.latency_ms !== undefined) setLatency(resData.latency_ms);
          }
        } catch (err) {}
      }, 180);
    } catch (err) {
      setStreamError('Could not access device camera: ' + err.message);
      setCameraMode('host');
    }
  };

  // Handle Photo Upload
  const handleUploadPhoto = async (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    stopBrowserStream();
    setCameraMode('sample');
    setStreamError(null);

    const fd = new FormData();
    fd.append('file', f);
    try {
      const res = await fetch('/api/upload_face', { method: 'POST', body: fd });
      if (res.ok) {
        setFeedUrl('/api/snapshot?t=' + Date.now());
      }
    } catch (err) {
      setStreamError('Upload failed: ' + err.message);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopBrowserStream();
    };
  }, []);

  const emotionColors = {
    Happy: '#10b981',
    Sad: '#3b82f6',
    Angry: '#ef4444',
    Surprise: '#f59e0b',
    Fear: '#ec4899',
    Disgust: '#8b5cf6',
    Contempt: '#64748b',
    Neutral: '#00d4ff',
  };
  const currentEmotionColor = emotionColors[dominantEmotion] || '#00d4ff';

  return (
    <Tilt3D intensity={5} className="glass-card">
      {/* Card Header */}
      <div className="card-header">
        <div className="card-title">
          <span className="dot-cyan" />
          <span>Infant Video Feed &amp; Targeting HUD</span>
        </div>
        <span className="card-subtle mono">Slim 320 SSD (320x240) + FERPlus</span>
      </div>

      {/* Video Viewport Container */}
      <div
        style={{
          position: 'relative',
          height: 380,
          overflow: 'hidden',
          background: 'radial-gradient(ellipse at center, #0f172a 0%, #020617 80%)',
          borderTop: '1px solid rgba(148,163,184,0.1)',
          borderBottom: '1px solid rgba(148,163,184,0.1)',
        }}
      >
        {/* HUD grid background */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'linear-gradient(rgba(0,212,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.07) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
            pointerEvents: 'none',
            zIndex: 2,
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
            zIndex: 10,
          }}
        >
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: '50%',
                background: cameraMode === 'browser' ? '#a855f7' : '#10b981',
                boxShadow: `0 0 8px ${cameraMode === 'browser' ? '#a855f7' : '#10b981'}`,
              }}
            />
            {cameraMode === 'browser'
              ? '◈ BROWSER WEBCAM ACTIVE'
              : cameraMode === 'sample'
              ? '◈ PHOTO ARCHETYPE'
              : '◈ LIVE HARDWARE WEBCAM'}
          </span>
          <span>
            FPS: {fps} | LATENCY: {latency}ms | FACES: {facesCount}
          </span>
        </div>

        {/* Video stream rendering: Host / Sample or Browser */}
        {cameraMode === 'browser' ? (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: '#07090e',
              zIndex: 1,
            }}
          >
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
                transform: 'scaleX(-1)', // Mirror browser webcam
              }}
            />
          </div>
        ) : (
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
              key={feedUrl}
              src={feedUrl}
              alt="Real-Time Neural Video Feed"
              onError={(e) => {
                // If multipart stream stalls, smoothly fallback to snapshot poller
                e.currentTarget.onerror = null;
                const poller = setInterval(() => {
                  if (cameraMode !== 'browser') {
                    e.currentTarget.src = '/api/snapshot?t=' + Date.now();
                  }
                }, 100);
                return () => clearInterval(poller);
              }}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
                display: 'block',
              }}
            />
          </div>
        )}

        {/* Hidden Canvas for browser frame encoding */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />

        {/* Scanning laser line */}
        <ScanLine />

        {/* Corner HUD brackets */}
        {[
          { top: 50, left: 50, rot: 0 },
          { top: 50, right: 50, rot: 90 },
          { bottom: 50, left: 50, rot: 270 },
          { bottom: 50, right: 50, rot: 180 },
        ].map((c, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              ...c,
              width: 22,
              height: 22,
              borderTop: `2px solid ${currentEmotionColor}`,
              borderLeft: `2px solid ${currentEmotionColor}`,
              transform: `rotate(${c.rot}deg)`,
              boxShadow: `0 0 8px ${currentEmotionColor}`,
              pointerEvents: 'none',
              zIndex: 6,
            }}
          />
        ))}

        {/* HUD bottom status overlay */}
        <div
          style={{
            position: 'absolute',
            bottom: 10,
            left: 16,
            right: 16,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: '0.68rem',
            color: currentEmotionColor,
            letterSpacing: '0.14em',
            zIndex: 10,
            textShadow: `0 0 8px ${currentEmotionColor}aa`,
          }}
        >
          <span>
            {facesCount > 0
              ? `TARGET LOCKED • ${facesCount} FACE • AFFECT: ${dominantEmotion.toUpperCase()}`
              : 'SEARCHING TARGET • NEURAL SCAN ACTIVE'}
          </span>
          <span style={{ color: '#94a3b8', fontSize: '0.62rem' }}>
            {cameraMode === 'browser' ? 'CLIENT WEBCAM' : 'OPENCV DSHOW'}
          </span>
        </div>
      </div>

      {/* Error alert if any */}
      {streamError && (
        <div
          style={{
            padding: '8px 16px',
            background: 'rgba(239, 68, 68, 0.15)',
            borderBottom: '1px solid rgba(239, 68, 68, 0.3)',
            color: '#f87171',
            fontSize: '0.75rem',
            fontFamily: 'JetBrains Mono, monospace',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
          }}
        >
          <AlertCircle size={14} />
          <span>{streamError}</span>
        </div>
      )}

      {/* Bottom Controls Bar */}
      <div
        style={{
          padding: '12px 18px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: 12,
          flexWrap: 'wrap',
          background: 'rgba(7, 9, 14, 0.6)',
        }}
      >
        {/* Real-time telemetry badges */}
        <div style={{ display: 'flex', gap: 16, fontSize: '0.82rem', fontFamily: 'JetBrains Mono, monospace', color: '#94a3b8' }}>
          <span>
            FPS: <strong style={{ color: '#38bdf8' }}>{fps}</strong>
          </span>
          <span>
            Faces: <strong style={{ color: facesCount > 0 ? '#10b981' : '#f59e0b' }}>{facesCount}</strong>
          </span>
          <span>
            Affect:{' '}
            <strong style={{ color: currentEmotionColor, textTransform: 'capitalize' }}>
              {dominantEmotion}
            </strong>
          </span>
        </div>

        {/* Camera mode buttons */}
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <button
            onClick={handleSelectHostCamera}
            className={`btn-mini ${cameraMode === 'host' ? 'btn-active' : ''}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              background: cameraMode === 'host' ? 'rgba(56, 189, 248, 0.2)' : 'rgba(15, 23, 42, 0.6)',
              border: `1px solid ${cameraMode === 'host' ? '#38bdf8' : 'rgba(148, 163, 184, 0.2)'}`,
              color: cameraMode === 'host' ? '#38bdf8' : '#cbd5e1',
              padding: '6px 12px',
              borderRadius: 6,
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            <Camera size={13} /> Live Camera
          </button>

          <button
            onClick={handleSelectBrowserCamera}
            className={`btn-mini ${cameraMode === 'browser' ? 'btn-active' : ''}`}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              background: cameraMode === 'browser' ? 'rgba(168, 85, 247, 0.2)' : 'rgba(15, 23, 42, 0.6)',
              border: `1px solid ${cameraMode === 'browser' ? '#a855f7' : 'rgba(148, 163, 184, 0.2)'}`,
              color: cameraMode === 'browser' ? '#c084fc' : '#cbd5e1',
              padding: '6px 12px',
              borderRadius: 6,
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            <Video size={13} /> Device Webcam
          </button>

          <button
            onClick={() => fileRef.current?.click()}
            className="btn-mini"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              background: cameraMode === 'sample' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(15, 23, 42, 0.6)',
              border: `1px solid ${cameraMode === 'sample' ? '#10b981' : 'rgba(148, 163, 184, 0.2)'}`,
              color: cameraMode === 'sample' ? '#34d399' : '#cbd5e1',
              padding: '6px 12px',
              borderRadius: 6,
              fontSize: '0.75rem',
              cursor: 'pointer',
            }}
          >
            <Upload size={13} /> Upload Face
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={handleUploadPhoto}
          />
        </div>
      </div>
    </Tilt3D>
  );
};

export default VideoFeedCard;
