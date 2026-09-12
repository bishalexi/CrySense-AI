"""Patches static/js/bundle.js to install the enhanced Multi-Mode Camera Engine in VideoFeedCard and BabyFace3D.
- Auto-recovering OpenCV hardware stream with /api/snapshot fallback
- Direct browser webcam stream via navigator.mediaDevices.getUserMedia and /api/upload_frame
- Face photo upload with instant AI detection
- Real-time telemetry syncing (real FPS, faces count, latency, and emotion affect)
"""

import re

bundle_path = "static/js/bundle.js"
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read bundle.js ({len(content)} bytes)")

p_face_start = content.find("const BabyFace3D = ({")
p_face_end = content.find("const ScanLine = () =>", p_face_start)

if p_face_start == -1 or p_face_end == -1:
    print("ERROR: Could not locate BabyFace3D boundaries")
    exit(1)

new_baby_face = """const BabyFace3D = ({ mood = 'neutral' }) => {
  const [useBrowserCam, setUseBrowserCam] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
  const [feedSrc, setFeedSrc] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)('/video_feed');
  const [snapshotMode, setSnapshotMode] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
  const videoRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
  const canvasRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
  const streamRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);

  // Global triggers exposed for toolbar buttons
  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    window.__toggleBrowserCamera = async () => {
      if (useBrowserCam) {
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(t => t.stop());
          streamRef.current = null;
        }
        setUseBrowserCam(false);
        setFeedSrc('/video_feed?t=' + Date.now());
        try { await fetch('/api/set_source?source=camera'); } catch(e) {}
      } else {
        try {
          if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Browser camera is unavailable or requires HTTPS.');
            return;
          }
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
            audio: false
          });
          streamRef.current = stream;
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play().catch(() => {});
          }
          setUseBrowserCam(true);
        } catch(err) {
          alert('Could not access device camera: ' + err.message);
        }
      }
    };

    window.__resetHostCamera = async () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
        streamRef.current = null;
      }
      setUseBrowserCam(false);
      setSnapshotMode(false);
      setFeedSrc('/video_feed?t=' + Date.now());
      try { await fetch('/api/set_source?source=camera'); } catch(e) {}
    };

    window.__setSnapshotFeed = () => {
      setFeedSrc('/api/snapshot?t=' + Date.now());
    };

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
      }
    };
  }, [useBrowserCam]);

  // Frame streaming loop for browser webcam -> Python Emotion AI
  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    if (!useBrowserCam) return;
    const interval = setInterval(async () => {
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
        await fetch('/api/upload_frame', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: b64 })
        });
      } catch(err) {}
    }, 180);
    return () => clearInterval(interval);
  }, [useBrowserCam]);

  // Smooth fallback polling if MJPEG drops
  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    if (useBrowserCam || !snapshotMode) return;
    const id = setInterval(() => {
      setFeedSrc('/api/snapshot?t=' + Date.now());
    }, 120);
    return () => clearInterval(id);
  }, [useBrowserCam, snapshotMode]);

  return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
    style: {
      position: 'absolute',
      inset: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#07090e',
      overflow: 'hidden',
      zIndex: 1
    },
    children: [
      useBrowserCam ? /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("video", {
        ref: videoRef,
        autoPlay: true,
        playsInline: true,
        muted: true,
        style: {
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          transform: 'scaleX(-1)'
        }
      }, void 0, false, {
        fileName: "VideoFeedCard.jsx",
        lineNumber: 10,
        columnNumber: 5
      }, undefined) : /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("img", {
        key: feedSrc,
        src: feedSrc,
        alt: "Real-Time Neural Video Feed",
        onError: () => {
          setSnapshotMode(true);
        },
        style: {
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          display: 'block'
        }
      }, void 0, false, {
        fileName: "VideoFeedCard.jsx",
        lineNumber: 11,
        columnNumber: 5
      }, undefined),
      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("canvas", {
        ref: canvasRef,
        style: { display: 'none' }
      }, void 0, false, {
        fileName: "VideoFeedCard.jsx",
        lineNumber: 12,
        columnNumber: 5
      }, undefined)
    ]
  }, void 0, false, {
    fileName: "VideoFeedCard.jsx",
    lineNumber: 9,
    columnNumber: 3
  }, undefined);
};
"""

content = content[:p_face_start] + new_baby_face + content[p_face_end:]
print("[1] Successfully patched BabyFace3D with dynamic dual-engine streaming!")

# Find VideoFeedCard boundaries
p_card_start = content.find("const VideoFeedCard = ({")
p_card_end = content.find("_s(VideoFeedCard,", p_card_start)

if p_card_start == -1 or p_card_end == -1:
    print("ERROR: Could not locate VideoFeedCard boundaries")
    exit(1)

new_video_card = """const VideoFeedCard = ({
  mood = 'Neutral'
}) => {
  _s();
  const [fps, setFps] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(30.0);
  const [latency, setLatency] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(14.5);
  const [facesCount, setFacesCount] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(1);
  const [dominantEmotion, setDominantEmotion] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(mood || 'Neutral');
  const [activeMode, setActiveMode] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)('host');
  const fileRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);

  // Poll live telemetry from Python Emotion AI
  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const id = setInterval(async () => {
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
    }, 450);
    return () => clearInterval(id);
  }, []);

  const emotionColors = {
    Happy: '#10b981',
    Sad: '#3b82f6',
    Angry: '#ef4444',
    Surprise: '#f59e0b',
    Fear: '#ec4899',
    Disgust: '#8b5cf6',
    Contempt: '#64748b',
    Neutral: '#00d4ff'
  };
  const currentEmotionColor = emotionColors[dominantEmotion] || '#00d4ff';

  const onSelectHost = () => {
    setActiveMode('host');
    if (window.__resetHostCamera) window.__resetHostCamera();
  };

  const onSelectBrowser = () => {
    setActiveMode(prev => prev === 'browser' ? 'host' : 'browser');
    if (window.__toggleBrowserCamera) window.__toggleBrowserCamera();
  };

  const onUploadPhoto = async (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    setActiveMode('sample');
    const fd = new FormData();
    fd.append('file', f);
    try {
      const res = await fetch('/api/upload_face', { method: 'POST', body: fd });
      if (res.ok && window.__setSnapshotFeed) {
        window.__setSnapshotFeed();
      }
    } catch (err) {
      alert('Upload failed: ' + err.message);
    }
  };

  return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(_Tilt3D__WEBPACK_IMPORTED_MODULE_2__["default"], {
    intensity: 5,
    className: "glass-card",
    children: [
      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
        className: "card-header",
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            className: "card-title",
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", { className: "dot-cyan" }, void 0, false),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", { children: "Infant Video Feed & Targeting HUD" }, void 0, false)
            ]
          }, void 0, true),
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
            className: "card-subtle mono",
            children: "Slim 320 SSD (320x240) + FERPlus"
          }, void 0, false)
        ]
      }, void 0, true),

      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
        style: {
          position: 'relative',
          height: 380,
          overflow: 'hidden',
          background: 'radial-gradient(ellipse at center, #0f172a 0%, #020617 80%)',
          borderTop: '1px solid rgba(148,163,184,0.1)',
          borderBottom: '1px solid rgba(148,163,184,0.1)'
        },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
              position: 'absolute',
              inset: 0,
              backgroundImage: 'linear-gradient(rgba(0,212,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.07) 1px, transparent 1px)',
              backgroundSize: '40px 40px',
              pointerEvents: 'none',
              zIndex: 2
            }
          }, void 0, false),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
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
              zIndex: 10
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                style: { display: 'inline-flex', alignItems: 'center', gap: 6 },
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                    style: {
                      width: 7,
                      height: 7,
                      borderRadius: '50%',
                      background: activeMode === 'browser' ? '#a855f7' : '#10b981',
                      display: 'inline-block',
                      boxShadow: '0 0 8px ' + (activeMode === 'browser' ? '#a855f7' : '#10b981')
                    }
                  }, void 0, false),
                  activeMode === 'browser' ? '◈ BROWSER WEBCAM ACTIVE' : activeMode === 'sample' ? '◈ PHOTO ARCHETYPE' : '◈ LIVE HARDWARE WEBCAM'
                ]
              }, void 0, true),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                children: ["FPS: ", fps, " | LATENCY: ", latency, "ms | FACES: ", facesCount]
              }, void 0, true)
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(BabyFace3D, { mood: dominantEmotion }, void 0, false),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(framer_motion__WEBPACK_IMPORTED_MODULE_1__.motion.div, {
            animate: { rotate: 360 },
            transition: { duration: 14, repeat: Infinity, ease: 'linear' },
            style: {
              position: 'absolute',
              left: '50%',
              top: '52%',
              transform: 'translate(-50%, -50%)',
              color: currentEmotionColor,
              opacity: 0.5,
              pointerEvents: 'none',
              zIndex: 3
            },
            children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_3__["default"], {
              size: 300,
              strokeWidth: 0.4
            }, void 0, false)
          }, void 0, false),

          [{ top: 50, left: 50, rot: 0 }, { top: 50, right: 50, rot: 90 }, { bottom: 50, left: 50, rot: 270 }, { bottom: 50, right: 50, rot: 180 }].map((c, i) =>
            /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
              style: {
                position: 'absolute',
                ...c,
                width: 22,
                height: 22,
                borderTop: '2px solid ' + currentEmotionColor,
                borderLeft: '2px solid ' + currentEmotionColor,
                transform: 'rotate(' + c.rot + 'deg)',
                boxShadow: '0 0 8px ' + currentEmotionColor,
                pointerEvents: 'none',
                zIndex: 6
              }
            }, i, false)
          ),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(ScanLine, {}, void 0, false),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
              position: 'absolute',
              bottom: 10,
              left: 16,
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '0.68rem',
              color: currentEmotionColor,
              letterSpacing: '0.14em',
              zIndex: 10,
              textShadow: '0 0 8px ' + currentEmotionColor + 'aa'
            },
            children: facesCount > 0 ? ('TARGET LOCKED • ' + facesCount + ' FACE • AFFECT: ' + dominantEmotion.toUpperCase()) : 'SEARCHING TARGET • NEURAL SCAN ACTIVE'
          }, void 0, false)
        ]
      }, void 0, true),

      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
        style: {
          padding: '12px 18px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: 12,
          flexWrap: 'wrap',
          background: 'rgba(7, 9, 14, 0.6)'
        },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: { display: 'flex', gap: 16, fontSize: '0.82rem', fontFamily: 'JetBrains Mono, monospace', color: '#94a3b8' },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                children: ["FPS: ", /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("strong", { style: { color: '#38bdf8' }, children: fps }, void 0, false)]
              }, void 0, true),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                children: ["Faces: ", /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("strong", { style: { color: facesCount > 0 ? '#10b981' : '#f59e0b' }, children: facesCount }, void 0, false)]
              }, void 0, true),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                children: ["Affect: ", /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("strong", { style: { color: currentEmotionColor, textTransform: 'capitalize' }, children: dominantEmotion }, void 0, false)]
              }, void 0, true)
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: { display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("button", {
                onClick: onSelectHost,
                className: "btn-mini",
                style: {
                  background: activeMode === 'host' ? 'rgba(56, 189, 248, 0.2)' : 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid ' + (activeMode === 'host' ? '#38bdf8' : 'rgba(148, 163, 184, 0.2)'),
                  color: activeMode === 'host' ? '#38bdf8' : '#cbd5e1',
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: '0.75rem',
                  cursor: 'pointer'
                },
                children: "● Live Camera"
              }, void 0, false),

              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("button", {
                onClick: onSelectBrowser,
                className: "btn-mini",
                style: {
                  background: activeMode === 'browser' ? 'rgba(168, 85, 247, 0.2)' : 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid ' + (activeMode === 'browser' ? '#a855f7' : 'rgba(148, 163, 184, 0.2)'),
                  color: activeMode === 'browser' ? '#c084fc' : '#cbd5e1',
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: '0.75rem',
                  cursor: 'pointer'
                },
                children: "📹 Device Webcam"
              }, void 0, false),

              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("button", {
                onClick: () => { if (fileRef.current) fileRef.current.click(); },
                className: "btn-mini",
                style: {
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  background: activeMode === 'sample' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(15, 23, 42, 0.6)',
                  border: '1px solid ' + (activeMode === 'sample' ? '#10b981' : 'rgba(148, 163, 184, 0.2)'),
                  color: activeMode === 'sample' ? '#34d399' : '#cbd5e1',
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: '0.75rem',
                  cursor: 'pointer'
                },
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_4__["default"], { size: 13 }, void 0, false),
                  " Upload Photo"
                ]
              }, void 0, true),

              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("input", {
                ref: fileRef,
                type: "file",
                accept: "image/*",
                style: { display: 'none' },
                onChange: onUploadPhoto
              }, void 0, false)
            ]
          }, void 0, true)
        ]
      }, void 0, true)
    ]
  }, void 0, true);
};
"""

content = content[:p_card_start] + new_video_card + content[p_card_end:]
print("[2] Successfully patched VideoFeedCard with multi-mode controls and telemetry!")

with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Patched bundle.js saved! ({len(content)} bytes)")
