import React from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import { Camera, Mic, Activity, Sparkles, CheckCircle2, AlertTriangle, Radio } from 'lucide-react';

const DualSensorResultCard = ({ sensorData, assessment }) => {
  const visual = sensorData && sensorData.visual;
  const audio = sensorData && sensorData.audio;
  const fused = sensorData && sensorData.fused;

  const dominantEmotion = (visual && visual.dominant_emotion) || (assessment && assessment.primaryAffect) || 'Neutral';
  const faceConf = visual ? Math.round(visual.confidence || 0) : 0;
  const facesCount = visual ? visual.faces_count : 0;
  const fps = visual ? (visual.fps || 0).toFixed(1) : '30.0';
  const latency = visual ? (visual.latency_ms || 0).toFixed(1) : '13.0';

  const emotionColorMap = {
    Happy: '#10b981',
    Sad: '#3b82f6',
    Angry: '#ef4444',
    Surprise: '#f59e0b',
    Fear: '#ec4899',
    Disgust: '#8b5cf6',
    Contempt: '#64748b',
    Neutral: '#94a3b8',
  };
  const visualColor = emotionColorMap[dominantEmotion] || '#38bdf8';

  const audioCategory = audio ? (audio.predicted_category || '').toUpperCase() : null;
  const audioTitle = audio ? audio.title : 'Awaiting Mic Cry or Audio File Upload';
  const audioConf = audio ? Math.round((audio.confidence || 0) * 100) : null;
  const audioIcon = audio ? (audio.icon || '🎵') : '🎙️';
  const audioColor = audio ? (audio.color || '#a855f7') : '#94a3b8';

  const unifiedScore = fused && fused.unified_distress_score !== undefined
    ? fused.unified_distress_score.toFixed(1)
    : (assessment ? assessment.percentage.toFixed(1) : '0.0');

  const severityBadge = (fused && fused.severity_badge) || (assessment && assessment.level ? assessment.level.toUpperCase() + ' DISTRESS' : 'ASSESSING');
  const severityColor = (fused && fused.severity_color) || '#38bdf8';

  const babyMessage = (fused && fused.baby_message) || (audio && audio.baby_message) || (assessment && assessment.innerVoice) || '';
  const narrative = fused && fused.narrative;
  const soothingTip = audio && audio.soothing_checklist && audio.soothing_checklist[0];

  return (
    <Tilt3D intensity={4} className="glass-card" style={{ padding: '18px 20px', marginBottom: 16 }}>
      {/* Top Banner Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 32,
              height: 32,
              borderRadius: 8,
              background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(168, 85, 247, 0.2))',
              border: '1px solid rgba(56, 189, 248, 0.4)',
            }}
          >
            <Activity size={18} color="#38bdf8" />
          </div>
          <div>
            <div style={{ fontSize: '0.85rem', fontWeight: 800, letterSpacing: '0.12em', color: '#f8fafc' }}>
              DUAL-SENSOR AI DETECTION CONSOLE
            </div>
            <div style={{ fontSize: '0.68rem', color: '#94a3b8', letterSpacing: '0.05em' }}>
              Persistent Camera Vision + Acoustic Cry Classification Feed
            </div>
          </div>
        </div>

        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            padding: '4px 10px',
            borderRadius: 20,
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            fontSize: '0.68rem',
            fontWeight: 700,
            color: '#10b981',
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          <motion.span
            animate={{ scale: [1, 1.3, 1], opacity: [1, 0.6, 1] }}
            transition={{ duration: 1.8, repeat: Infinity }}
            style={{ width: 7, height: 7, borderRadius: '50%', background: '#10b981', display: 'inline-block' }}
          />
          LIVE SYNC
        </div>
      </div>

      {/* Two Sensor Boxes Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: 14,
          marginBottom: 14,
        }}
      >
        {/* Sensor 1: Camera Vision Result */}
        <div
          style={{
            background: 'rgba(15, 23, 42, 0.7)',
            borderRadius: 12,
            border: `1px solid ${visualColor}44`,
            padding: 14,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: `0 4px 20px ${visualColor}15`,
          }}
        >
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  color: '#38bdf8',
                  letterSpacing: '0.08em',
                }}
              >
                <Camera size={14} /> CAMERA VISION FEED
              </span>
              <span
                className="mono"
                style={{
                  fontSize: '0.64rem',
                  padding: '2px 6px',
                  borderRadius: 4,
                  background: facesCount > 0 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                  color: facesCount > 0 ? '#10b981' : '#f59e0b',
                }}
              >
                {facesCount > 0 ? `${facesCount} FACE LOCKED` : 'SEARCHING FACE'}
              </span>
            </div>

            {/* Dominant Affect Display */}
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '8px 0 4px 0' }}>
              <span style={{ fontSize: '1.45rem', fontWeight: 800, color: visualColor, letterSpacing: '-0.01em' }}>
                {dominantEmotion.toUpperCase()}
              </span>
              {faceConf > 0 && (
                <span className="mono" style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                  ({faceConf}%)
                </span>
              )}
            </div>

            <div style={{ fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 }}>
              Facial Affective State: <strong style={{ color: visualColor }}>{dominantEmotion}</strong>
            </div>
          </div>

          <div>
            {/* Visual Telemetry Stats */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: 8,
                padding: '8px 10px',
                background: 'rgba(7, 9, 14, 0.6)',
                borderRadius: 8,
                border: '1px solid rgba(148, 163, 184, 0.08)',
              }}
            >
              <div>
                <div style={{ fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }}>INFERENCE SPEED</div>
                <div className="mono" style={{ fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }}>
                  {fps} FPS ({latency}ms)
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }}>FACIAL STRAIN</div>
                <div className="mono" style={{ fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }}>
                  {assessment ? assessment.visualStrain.toFixed(1) : '0.0'}%
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sensor 2: Acoustic Cry Result */}
        <div
          style={{
            background: 'rgba(15, 23, 42, 0.7)',
            borderRadius: 12,
            border: `1px solid ${audioColor}44`,
            padding: 14,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: `0 4px 20px ${audioColor}15`,
          }}
        >
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  color: '#a855f7',
                  letterSpacing: '0.08em',
                }}
              >
                <Mic size={14} /> ACOUSTIC CRY FEED
              </span>
              <span
                className="mono"
                style={{
                  fontSize: '0.64rem',
                  padding: '2px 6px',
                  borderRadius: 4,
                  background: audio ? 'rgba(168, 85, 247, 0.18)' : 'rgba(148, 163, 184, 0.1)',
                  color: audio ? '#c084fc' : '#94a3b8',
                }}
              >
                {audio ? 'AUDIO CLASSIFIED' : 'STANDBY'}
              </span>
            </div>

            {/* Acoustic Result Display */}
            {audioCategory ? (
              <>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '8px 0 4px 0' }}>
                  <span style={{ fontSize: '1.45rem', fontWeight: 800, color: audioColor, letterSpacing: '-0.01em' }}>
                    {audioIcon} {audioCategory}
                  </span>
                  {audioConf !== null && (
                    <span className="mono" style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                      ({audioConf}%)
                    </span>
                  )}
                </div>

                <div style={{ fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 }}>
                  Diagnosis: <strong style={{ color: audioColor }}>{audioTitle}</strong>
                </div>
              </>
            ) : (
              <div style={{ margin: '14px 0', color: '#94a3b8', fontSize: '0.8rem', lineHeight: 1.4 }}>
                <span style={{ color: '#e2e8f0', fontWeight: 600 }}>No acoustic sample processed yet.</span>
                <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: 4 }}>
                  Use "Record Cry via Mic" or "Upload Audio" below.
                </div>
              </div>
            )}
          </div>

          <div>
            {/* Acoustic Telemetry Stats */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: 8,
                padding: '8px 10px',
                background: 'rgba(7, 9, 14, 0.6)',
                borderRadius: 8,
                border: '1px solid rgba(148, 163, 184, 0.08)',
              }}
            >
              <div>
                <div style={{ fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }}>FEATURE DIMS</div>
                <div className="mono" style={{ fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }}>
                  194-D SVC
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }}>ACOUSTIC SEVERITY</div>
                <div className="mono" style={{ fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }}>
                  {assessment ? assessment.acousticSeverity.toFixed(1) : '0.0'}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Synthesis Panel: Multimodal Combined Verdict */}
      <div
        style={{
          background: 'linear-gradient(90deg, rgba(56, 189, 248, 0.06), rgba(168, 85, 247, 0.06))',
          borderRadius: 10,
          border: '1px solid rgba(148, 163, 184, 0.14)',
          padding: '12px 14px',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              fontSize: '0.72rem',
              fontWeight: 700,
              color: '#cbd5e1',
              letterSpacing: '0.08em',
            }}
          >
            <Sparkles size={14} color="#f59e0b" /> MULTIMODAL COMBINED VERDICT
          </span>
          <span
            className="mono"
            style={{
              fontSize: '0.72rem',
              fontWeight: 700,
              padding: '2px 8px',
              borderRadius: 6,
              background: `${severityColor}22`,
              color: severityColor,
              border: `1px solid ${severityColor}55`,
            }}
          >
            {severityBadge} ({unifiedScore}%)
          </span>
        </div>

        {narrative && (
          <div style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: 6 }}>
            {narrative}
          </div>
        )}

        {babyMessage && (
          <div
            style={{
              fontSize: '0.82rem',
              color: '#e2e8f0',
              fontStyle: 'italic',
              borderLeft: '2px solid #a855f7',
              paddingLeft: 10,
              marginTop: 6,
              lineHeight: 1.45,
            }}
          >
            "{babyMessage}"
          </div>
        )}

        {soothingTip && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              marginTop: 8,
              fontSize: '0.72rem',
              color: '#38bdf8',
            }}
          >
            <CheckCircle2 size={13} />
            <span>Recommended Care: <strong>{soothingTip}</strong></span>
          </div>
        )}
      </div>
    </Tilt3D>
  );
};

export default DualSensorResultCard;
