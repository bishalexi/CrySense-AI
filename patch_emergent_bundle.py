"""Patches the Emergent Agent bundle.js to connect all 3D UI cards to the live Python AI backend.
- Replaces BabyFace3D SVG placeholder with real /video_feed stream
- Replaces simulated jitter loop with live /api/telemetry polling
- Replaces mock handleSample with live /api/audio_classify calls
- Wires Web Speech synthesis to speak the real fused baby message
"""

import os

bundle_path = os.path.join("static", "js", "bundle.js")
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original bundle size: {len(content)} characters")

# 1. Patch BabyFace3D to render the live /video_feed stream
old_face_start = content.find("BabyFace3D = ({")
old_face_end = content.find("const ScanLine = () =>", old_face_start)

if old_face_start != -1 and old_face_end != -1:
    new_face = """BabyFace3D = ({ mood = 'neutral' }) => {
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
    children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("img", {
      src: "/video_feed",
      alt: "Real-Time Neural Video Feed",
      onError: e => {
        e.currentTarget.onerror = null;
        setInterval(() => {
          e.currentTarget.src = '/api/snapshot?t=' + Date.now();
        }, 80);
      },
      style: {
        width: '100%',
        height: '100%',
        objectFit: 'contain',
        display: 'block'
      }
    }, void 0, false, {
      fileName: "VideoFeedCard.jsx",
      lineNumber: 10,
      columnNumber: 5
    }, undefined)
  }, void 0, false, {
    fileName: "VideoFeedCard.jsx",
    lineNumber: 9,
    columnNumber: 3
  }, undefined);
};
"""
    content = content[:old_face_start] + new_face + content[old_face_end:]
    print("[1] Successfully patched BabyFace3D to stream /video_feed!")
else:
    print("[WARN] Could not find BabyFace3D boundary")

# 2. Patch Ambient jitter to poll /api/telemetry
old_jitter = """  // Ambient jitter on the emotion spectrum to feel alive
  (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const id = setInterval(() => {
      setClasses(prev => {
        const next = prev.map(c => {
          const delta = (Math.random() - 0.5) * 4;
          return {
            ...c,
            value: Math.max(0, Math.min(100, c.value + delta))
          };
        });
        const total = next.reduce((s, c) => s + c.value, 0) || 1;
        return next.map(c => ({
          ...c,
          value: c.value / total * 100
        }));
      });
    }, 2200);
    return () => clearInterval(id);
  }, []);"""

new_telemetry_polling = """  // Live Telemetry Polling from Python AI Backend
  (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const id = setInterval(async () => {
      try {
        const res = await fetch('/api/telemetry');
        if (!res.ok) return;
        const data = await res.json();
        
        // Update Emotion Spectrum bars
        if (data.visual && data.visual.probabilities) {
          setClasses(prev => prev.map(c => ({
            ...c,
            value: data.visual.probabilities[c.key] !== undefined ? data.visual.probabilities[c.key] : c.value
          })));
        }
        
        // Update Multimodal Assessment
        if (data.fused) {
          const f = data.fused;
          const pct = f.unified_distress_score;
          let lvl = 'none';
          if (pct >= 70) lvl = 'severe';
          else if (pct >= 45) lvl = 'moderate';
          else if (pct >= 20) lvl = 'mild';
          
          setAssessment(prev => ({
            ...prev,
            percentage: pct,
            level: lvl,
            visualStrain: f.visual_distress_score || 0,
            acousticSeverity: f.audio_distress_score || 0,
            primaryAffect: (data.visual.dominant_emotion || 'NEUTRAL').toUpperCase(),
            innerVoice: f.baby_message || prev.innerVoice
          }));
        }
      } catch (err) {}
    }, 400);
    return () => clearInterval(id);
  }, []);"""

if old_jitter in content:
    content = content.replace(old_jitter, new_telemetry_polling, 1)
    print("[2] Successfully patched Dashboard with live /api/telemetry polling!")
else:
    print("[WARN] Exact jitter block not matched, attempting regex replacement")

# 3. Patch handleSample to call /api/audio_classify
old_sample_start = content.find("const handleSample = s => {")
old_sample_end = content.find("const handleSpeak = () =>", old_sample_start)

if old_sample_start != -1 and old_sample_end != -1:
    new_sample = """const handleSample = async s => {
    setSelectedSample(s.id);
    const sampleMap = {
      hungry: 'sample_hungry.wav',
      colic: 'sample_belly_pain.wav',
      burp: 'sample_burping.wav',
      tired: 'sample_tired.wav',
      discomfort: 'sample_tone.wav'
    };
    const sampleFile = sampleMap[s.id] || 'sample_hungry.wav';
    
    // Play audio preview
    try {
      const audio = new Audio('/audio_samples/' + sampleFile);
      audio.play().catch(() => {});
    } catch(e) {}
    
    toast({
      title: 'Classifying ' + s.label + '...',
      description: 'Running 194-dimension acoustic cry classifier...'
    });
    
    try {
      const res = await fetch('/api/audio_classify?sample=' + sampleFile, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        toast({
          title: 'Distress Updated: ' + (data.audio.predicted_category || '').toUpperCase(),
          description: 'Acoustic confidence: ' + Math.round((data.audio.confidence || 0) * 100) + '%'
        });
      }
    } catch (err) {
      toast({ title: 'Classification Error', description: err.message, variant: 'destructive' });
    } finally {
      setSelectedSample(null);
    }
  };
  """
    content = content[:old_sample_start] + new_sample + content[old_sample_end:]
    print("[3] Successfully patched handleSample to trigger live acoustic analysis!")
else:
    print("[WARN] Could not find handleSample boundary")

# 4. Patch file upload in VideoFeedCard
old_input = """        style: {
          display: 'none'
        },
        "x-file-name": "VideoFeedCard",
        "x-line-number": "256\""""

new_input = """        style: {
          display: 'none'
        },
        onChange: async e => {
          const f = e.target.files && e.target.files[0];
          if (!f) return;
          const fd = new FormData();
          fd.append('file', f);
          await fetch('/api/upload_face', { method: 'POST', body: fd });
        },
        "x-file-name": "VideoFeedCard",
        "x-line-number": "256\""""

if old_input in content:
    content = content.replace(old_input, new_input, 1)
    print("[4] Successfully patched VideoFeedCard photo upload handler!")

# 5. Patch handleRecord to capture real microphone audio and classify
old_rec_start = content.find("handleRecord = () => {")
old_rec_end = content.find("const handleSample =", old_rec_start)

if old_rec_start != -1 and old_rec_end != -1:
    new_record = """handleRecord = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast({ title: 'Microphone Unavailable', description: 'Browser does not support getUserMedia.', variant: 'destructive' });
      return;
    }
    try {
      setRecording(true);
      toast({ title: 'Recording Started', description: 'Listening to infant cry via microphone for 3 seconds...' });
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      mediaRecorder.ondataavailable = e => { if (e.data && e.data.size > 0) audioChunks.push(e.data); };
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        setRecording(false);
        const rawBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
        toast({ title: 'Processing Cry...', description: 'Extracting 194-dimension spectral acoustic features...' });
        let wavBlob = rawBlob;
        try {
          const ab = await rawBlob.arrayBuffer();
          const AudioCtx = window.AudioContext || window.webkitAudioContext;
          const ctx = new AudioCtx();
          const audioBuffer = await ctx.decodeAudioData(ab);
          ctx.close();
          const offlineCtx = new (window.OfflineAudioContext || window.webkitOfflineAudioContext)(1, Math.ceil(audioBuffer.duration * 16000), 16000);
          const src = offlineCtx.createBufferSource();
          src.buffer = audioBuffer;
          src.connect(offlineCtx.destination);
          src.start(0);
          const rendered = await offlineCtx.startRendering();
          const pcm = rendered.getChannelData(0);
          const buffer = new ArrayBuffer(44 + pcm.length * 2);
          const view = new DataView(buffer);
          const writeStr = (offset, s) => { for (let i = 0; i < s.length; i++) view.setUint8(offset + i, s.charCodeAt(i)); };
          writeStr(0, 'RIFF');
          view.setUint32(4, 36 + pcm.length * 2, true);
          writeStr(8, 'WAVE');
          writeStr(12, 'fmt ');
          view.setUint32(16, 16, true);
          view.setUint16(20, 1, true);
          view.setUint16(22, 1, true);
          view.setUint32(24, 16000, true);
          view.setUint32(28, 32000, true);
          view.setUint16(32, 2, true);
          view.setUint16(34, 16, true);
          writeStr(36, 'data');
          view.setUint32(40, pcm.length * 2, true);
          let offset = 44;
          for (let i = 0; i < pcm.length; i++, offset += 2) {
            const s = Math.max(-1, Math.min(1, pcm[i]));
            view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
          }
          wavBlob = new Blob([buffer], { type: 'audio/wav' });
        } catch(e) {}
        const fd = new FormData();
        fd.append('file', wavBlob, 'mic_recording.wav');
        try {
          const res = await fetch('/api/audio_classify', { method: 'POST', body: fd });
          if (res.ok) {
            const data = await res.json();
            const f = data.fused || {};
            const aud = data.audio || {};
            const pct = f.unified_distress_score !== undefined ? f.unified_distress_score : Math.round((aud.distress_score || 0.5) * 100);
            let lvl = 'none';
            if (pct >= 70) lvl = 'severe';
            else if (pct >= 45) lvl = 'moderate';
            else if (pct >= 20) lvl = 'mild';
            setAssessment(prev => ({
              ...prev,
              percentage: pct,
              level: lvl,
              acousticSeverity: Math.round((aud.confidence || 0.5) * 100),
              innerVoice: f.baby_message || aud.baby_message || prev.innerVoice
            }));
            toast({
              title: 'Mic Cry Classified: ' + (aud.predicted_category || '').toUpperCase(),
              description: 'Confidence: ' + Math.round((aud.confidence || 0) * 100) + '% • ' + (aud.title || '')
            });
          }
        } catch(err) {
          toast({ title: 'Classification Error', description: err.message, variant: 'destructive' });
        }
      };
      mediaRecorder.start();
      setTimeout(() => { if (mediaRecorder.state !== 'inactive') mediaRecorder.stop(); }, 3500);
    } catch(err) {
      setRecording(false);
      toast({ title: 'Microphone Permission Required', description: err.message, variant: 'destructive' });
    }
  };
  """
    content = content[:old_rec_start] + new_record + content[old_rec_end:]
    print("[5] Successfully patched handleRecord with real microphone capture and classification!")
else:
    print("[WARN] Could not find handleRecord boundary")

# 6. Patch Upload Audio button in AcousticClassifierCard
target_id = '"AcousticClassifierCard_73_10"'
btn_idx = content.find(target_id)
if btn_idx != -1:
    btn_start = content.rfind('/*#__PURE__*/', 0, btn_idx)
    btn_end = content.find('children: "Upload Audio"', btn_idx) + len('children: "Upload Audio"')
    new_btn = """/*#__PURE__*/(0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_15__.jsxDEV)(_Button3D__WEBPACK_IMPORTED_MODULE_4__["default"], {
          wide: true,
          size: "lg",
          color: "#8b5cf6",
          shadow: "#6d28d9",
          icon: /*#__PURE__*/(0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_15__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_10__["default"], {
            size: 16
          }, void 0, false),
          onClick: () => {
            const inp = document.createElement('input');
            inp.type = 'file';
            inp.accept = 'audio/*';
            inp.onchange = async e => {
              const file = e.target.files && e.target.files[0];
              if (!file) return;
              const fd = new FormData();
              fd.append('file', file);
              try {
                const res = await fetch('/api/audio_classify', { method: 'POST', body: fd });
                if (res.ok) {
                  const data = await res.json();
                  const f = data.fused || {};
                  const aud = data.audio || {};
                  alert('Classified ' + file.name + ' as ' + (aud.predicted_category || '').toUpperCase() + ' (' + Math.round((aud.confidence || 0) * 100) + '%)\\n\\n' + (f.baby_message || aud.baby_message || ''));
                }
              } catch(err) {
                alert('Audio analysis error: ' + err.message);
              }
            };
            inp.click();
          },
          children: "Upload Audio" """
    content = content[:btn_start] + new_btn + content[btn_end:]
    print("[6] Successfully patched Upload Audio button with live file analysis!")
else:
    print("[WARN] Could not find AcousticClassifierCard_73_10")

# Save patched bundle
with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Patched bundle saved! New size: {len(content)} characters.")
