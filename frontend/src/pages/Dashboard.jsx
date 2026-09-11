import React, { useEffect, useState } from 'react';
import { useToast } from '../hooks/use-toast';
import { Toaster } from '../components/ui/toaster';
import Starfield from '../components/Starfield';
import Header from '../components/Header';
import VideoFeedCard from '../components/VideoFeedCard';
import EmotionSpectrumCard from '../components/EmotionSpectrumCard';
import DistressAssessmentCard from '../components/DistressAssessmentCard';
import InnerVoiceCard from '../components/InnerVoiceCard';
import AcousticClassifierCard from '../components/AcousticClassifierCard';
import SoothingProtocolCard from '../components/SoothingProtocolCard';
import DualSensorResultCard from '../components/DualSensorResultCard';
import { emotionClasses, initialAssessment, innerVoiceSamples, archetypeCries } from '../mock';

const clone = (v) => JSON.parse(JSON.stringify(v));

const pickMoodFromClasses = (cls) => {
  const top = [...cls].sort((a, b) => b.value - a.value)[0];
  const map = { Happy: 'happy', Neutral: 'neutral', Sad: 'sad', Angry: 'angry', Surprise: 'surprise', Fear: 'sad', Disgust: 'angry', Contempt: 'neutral' };
  return map[top.key] || 'neutral';
};

const distressFromValues = (visual, acoustic) => {
  const pct = Math.min(100, visual * 0.55 + acoustic * 0.45);
  let level = 'none';
  if (pct >= 70) level = 'severe';
  else if (pct >= 45) level = 'moderate';
  else if (pct >= 20) level = 'mild';
  return { pct, level };
};

const Dashboard = () => {
  const { toast } = useToast();
  const [classes, setClasses] = useState(clone(emotionClasses));
  const [assessment, setAssessment] = useState(initialAssessment);
  const [recording, setRecording] = useState(false);
  const [selectedSample, setSelectedSample] = useState(null);
  const [sensorData, setSensorData] = useState({ visual: null, audio: null, fused: null });

  // Live Telemetry Polling from Python AI Backend
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const res = await fetch('/api/telemetry');
        if (!res.ok) return;
        const data = await res.json();
        setSensorData(data);
        if (data.visual && data.visual.probabilities) {
          setClasses((prev) =>
            prev.map((c) => ({
              ...c,
              value: data.visual.probabilities[c.key] !== undefined ? data.visual.probabilities[c.key] : c.value,
            }))
          );
        }
        if (data.fused) {
          const f = data.fused;
          const pct = f.unified_distress_score;
          let lvl = 'none';
          if (pct >= 70) lvl = 'severe';
          else if (pct >= 45) lvl = 'moderate';
          else if (pct >= 20) lvl = 'mild';
          setAssessment((prev) => ({
            ...prev,
            percentage: pct,
            level: lvl,
            visualStrain: f.visual_distress_score || 0,
            acousticSeverity: f.audio_distress_score || 0,
            primaryAffect: (data.visual && data.visual.dominant_emotion ? data.visual.dominant_emotion : 'NEUTRAL').toUpperCase(),
            innerVoice: f.baby_message || prev.innerVoice,
          }));
        }
      } catch (err) {}
    }, 400);
    return () => clearInterval(id);
  }, []);

  // Recompute assessment when emotion changes
  useEffect(() => {
    const strain = classes
      .filter((c) => ['Sad', 'Angry', 'Fear', 'Disgust', 'Contempt'].includes(c.key))
      .reduce((s, c) => s + c.value, 0);
    const acoustic = assessment.acousticSeverity;
    const { pct, level } = distressFromValues(strain, acoustic);
    const mood = pickMoodFromClasses(classes);
    setAssessment((a) => ({
      ...a,
      percentage: pct,
      level,
      visualStrain: strain,
      primaryAffect: mood.toUpperCase(),
      innerVoice: innerVoiceSamples[level],
    }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [classes]);

  const handleRecord = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast({ title: 'Microphone Unavailable', description: 'Audio capture is not supported by your browser.', variant: 'destructive' });
      return;
    }
    try {
      setRecording(true);
      toast({ title: 'Recording Started', description: 'Listening to infant cry via microphone for 3 seconds...' });
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const chunks = [];
      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        setRecording(false);
        const rawBlob = new Blob(chunks, { type: mediaRecorder.mimeType || 'audio/webm' });
        toast({ title: 'Extracting 194 Spectral Features...', description: 'Analyzing cry acoustics via SVC model...' });
        
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
        } catch(e) {
          console.warn('WAV conversion fallback', e);
        }
        
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
            setAssessment((prev) => ({
              ...prev,
              percentage: pct,
              level: lvl,
              acousticSeverity: Math.round((aud.confidence || 0.5) * 100),
              innerVoice: f.baby_message || aud.baby_message || prev.innerVoice,
            }));
            toast({
              title: `Classified: ${(aud.predicted_category || '').toUpperCase()}`,
              description: `Confidence: ${Math.round((aud.confidence || 0) * 100)}% • ${aud.title || ''}`,
            });
          }
        } catch(err) {
          toast({ title: 'Classification Error', description: err.message, variant: 'destructive' });
        }
      };
      mediaRecorder.start();
      setTimeout(() => {
        if (mediaRecorder.state !== 'inactive') mediaRecorder.stop();
      }, 3500);
    } catch(err) {
      setRecording(false);
      toast({ title: 'Microphone Permission Required', description: err.message, variant: 'destructive' });
    }
  };

  const handleUploadAudio = async (file) => {
    if (!file) return;
    toast({ title: `Classifying ${file.name}...`, description: 'Extracting 194-dimension spectral acoustic features...' });
    const fd = new FormData();
    fd.append('file', file);
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
        setAssessment((prev) => ({
          ...prev,
          percentage: pct,
          level: lvl,
          acousticSeverity: Math.round((aud.confidence || 0.5) * 100),
          innerVoice: f.baby_message || aud.baby_message || prev.innerVoice,
        }));
        toast({
          title: `Audio Classified: ${(aud.predicted_category || '').toUpperCase()}`,
          description: `Confidence: ${Math.round((aud.confidence || 0) * 100)}% • ${aud.title || ''}`,
        });
      }
    } catch(err) {
      toast({ title: 'Upload Error', description: err.message, variant: 'destructive' });
    }
  };

  const handleSample = (s) => {
    setSelectedSample(s.id);
    const severity = { hungry: 42, colic: 78, burp: 30, tired: 25, discomfort: 55 }[s.id] || 40;
    setTimeout(() => {
      setAssessment((a) => {
        const { pct, level } = distressFromValues(a.visualStrain, severity);
        return { ...a, acousticSeverity: severity, percentage: pct, level, innerVoice: innerVoiceSamples[level] };
      });
      setSelectedSample(null);
    }, 1500);
    toast({ title: `Loaded ${s.label}`, description: s.description });
  };

  const handleSpeak = () => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      const utter = new SpeechSynthesisUtterance(assessment.innerVoice.replace(/[\u201c\u201d]/g, ''));
      utter.pitch = 1.4;
      utter.rate = 0.95;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utter);
    }
  };

  const moodForFace = pickMoodFromClasses(classes);

  return (
    <div className="app-shell">
      <Starfield />
      <div className="content-wrap">
        <Header />
        <main className="grid-main">
          <div className="col-left">
            <VideoFeedCard mood={moodForFace} />
            <EmotionSpectrumCard classes={classes} />
          </div>
          <div className="col-right">
            <DualSensorResultCard sensorData={sensorData} assessment={assessment} />
            <DistressAssessmentCard
              percentage={assessment.percentage}
              level={assessment.level}
              visualStrain={assessment.visualStrain}
              acousticSeverity={assessment.acousticSeverity}
              primaryAffect={assessment.primaryAffect}
            />
            <InnerVoiceCard text={assessment.innerVoice} onSpeak={handleSpeak} />
            <AcousticClassifierCard
              onRecord={handleRecord}
              onSample={handleSample}
              onUpload={handleUploadAudio}
              recording={recording}
              selectedSample={selectedSample}
            />
            <SoothingProtocolCard
              items={[
                'Check diaper comfort and skin temperature.',
                'Offer gentle skin-to-skin holding and rhythmic rocking.',
                'Verify feeding schedule and wake window duration.',
              ]}
            />
          </div>
        </main>
        <footer className="foot">
          <span>Multimodal AI: <strong>Ultra-Lightweight Face Detection (Slim 320) + BabyCry AI Classifier</strong></span>
          <span className="mono">Inference: OpenCV DNN AVX2 + Librosa 194-Dim Spectral Analysis</span>
        </footer>
      </div>
      <Toaster />
    </div>
  );
};

export default Dashboard;
