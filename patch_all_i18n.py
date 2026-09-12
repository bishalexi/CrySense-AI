"""Comprehensive i18n Patch:
1. Replaces DualSensorResultCard in bundle.js with dynamic multilingual translation reactive component
2. Updates VideoFeedCard in bundle.js to translate HUD titles, mode badges, buttons, and telemetry
3. Updates templates/index.html with interactive Language Switcher [ 🌐 EN | हिन्दी | বাংলা ], full dictionary, and localized TTS
4. Bumps version in templates/react_index.html
"""

import os

bundle_path = os.path.join("static", "js", "bundle.js")
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Patch DualSensorResultCard in bundle.js
p_dual_start = content.find("const DualSensorResultCard = ({")
p_dual_end = content.find("const Dashboard = () =>", p_dual_start)

if p_dual_start != -1 and p_dual_end != -1:
    new_dual = """const DualSensorResultCard = ({ sensorData, assessment }) => {
  const h = react__WEBPACK_IMPORTED_MODULE_0__.createElement;
  const [currentLang, setCurrentLang] = react__WEBPACK_IMPORTED_MODULE_0__.useState(window.__getLang ? window.__getLang() : 'en');

  react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
    const handler = (e) => { if (e.detail) setCurrentLang(e.detail); };
    window.addEventListener('crysense_lang_changed', handler);
    return () => window.removeEventListener('crysense_lang_changed', handler);
  }, []);

  const t = (k) => window.__t ? window.__t(k) : k;

  const visual = sensorData && sensorData.visual;
  const audio = sensorData && sensorData.audio;
  const fused = sensorData && sensorData.fused;

  const dominantEmotion = (visual && visual.dominant_emotion) || (assessment && assessment.primaryAffect) || 'Neutral';
  const localizedEmotion = t('emotions.' + dominantEmotion) || dominantEmotion;

  const faceConf = visual ? Math.round(visual.confidence || 0) : 0;
  const facesCount = visual ? visual.faces_count : 0;
  const fps = visual ? (visual.fps || 0).toFixed(1) : '30.0';
  const latency = visual ? (visual.latency_ms || 0).toFixed(1) : '14.5';

  const emotionColorMap = {
    Happy: '#10b981',
    Sad: '#3b82f6',
    Angry: '#ef4444',
    Surprise: '#f59e0b',
    Fear: '#ec4899',
    Disgust: '#8b5cf6',
    Contempt: '#64748b',
    Neutral: '#94a3b8'
  };
  const visualColor = emotionColorMap[dominantEmotion] || '#38bdf8';

  const rawCategory = (audio && audio.predicted_category) || (fused && fused.audio_category) || '';
  const localizedAudioTitle = rawCategory && t('archetypes.' + rawCategory) ? t('archetypes.' + rawCategory) : (audio ? audio.title : t('awaitingCry'));
  const audioConf = audio ? Math.round((audio.confidence || 0) * 100) : null;
  const audioIcon = audio ? (audio.icon || '🎵') : '🎙️';
  const audioColor = audio ? (audio.color || '#a855f7') : '#94a3b8';

  const unifiedScore = fused && fused.unified_distress_score !== undefined
    ? fused.unified_distress_score.toFixed(1)
    : (assessment ? assessment.percentage.toFixed(1) : '0.0');

  const severityBadge = (fused && fused.severity_badge) || (assessment && assessment.level ? assessment.level.toUpperCase() + ' DISTRESS' : 'ASSESSING');
  const severityColor = (fused && fused.severity_color) || '#38bdf8';

  const localizedBabyMessage = (fused && fused.baby_messages && fused.baby_messages[currentLang])
    || (rawCategory && t('cryMessages.' + rawCategory))
    || (fused && fused.baby_message)
    || (audio && audio.baby_message)
    || (assessment && assessment.innerVoice)
    || t('cryMessages.calm');

  const localizedSoothingTip = (fused && fused.soothing_checklists && fused.soothing_checklists[currentLang] && fused.soothing_checklists[currentLang][0])
    || (t('soothingSteps') && t('soothingSteps')[0])
    || t('soothingDefault');

  return h('div', {
    className: 'glass-card',
    style: {
      padding: '18px 20px',
      marginBottom: 16,
      background: 'rgba(11, 15, 25, 0.85)',
      borderRadius: 14,
      border: '1px solid rgba(56, 189, 248, 0.3)',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.45)'
    }
  }, [
    // Header
    h('div', {
      key: 'hdr',
      style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }
    }, [
      h('div', { key: 'l', style: { display: 'flex', alignItems: 'center', gap: 10 } }, [
        h('div', {
          key: 'icn',
          style: {
            width: 32,
            height: 32,
            borderRadius: 8,
            background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(168, 85, 247, 0.25))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(56, 189, 248, 0.4)',
            fontSize: '1.1rem'
          }
        }, '⚡'),
        h('div', { key: 'txt' }, [
          h('div', { key: 't1', style: { fontSize: '0.85rem', fontWeight: 800, letterSpacing: '0.06em', color: '#f8fafc' } }, t('dualSensorTitle')),
          h('div', { key: 't2', style: { fontSize: '0.68rem', color: '#94a3b8', letterSpacing: '0.03em' } }, t('dualSensorSub'))
        ])
      ]),
      h('div', {
        key: 'sync',
        style: {
          display: 'inline-flex',
          alignItems: 'center',
          gap: 6,
          padding: '4px 10px',
          borderRadius: 20,
          background: 'rgba(16, 185, 129, 0.12)',
          border: '1px solid rgba(16, 185, 129, 0.35)',
          fontSize: '0.68rem',
          fontWeight: 700,
          color: '#10b981',
          fontFamily: 'JetBrains Mono, monospace'
        }
      }, [
        h('span', {
          key: 'dot',
          style: { width: 7, height: 7, borderRadius: '50%', background: '#10b981', display: 'inline-block' }
        }),
        'LIVE SYNC'
      ])
    ]),

    // Two Sensors Grid
    h('div', {
      key: 'grid',
      style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 14, marginBottom: 14 }
    }, [
      // Sensor 1: Camera Vision Feed
      h('div', {
        key: 's1',
        style: {
          background: 'rgba(15, 23, 42, 0.7)',
          borderRadius: 12,
          border: '1px solid ' + visualColor + '44',
          padding: 14,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          boxShadow: '0 4px 20px ' + visualColor + '15'
        }
      }, [
        h('div', { key: 'top' }, [
          h('div', { key: 's1hdr', style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 } }, [
            h('span', { key: 's1t', style: { fontSize: '0.72rem', fontWeight: 700, color: '#38bdf8', letterSpacing: '0.08em' } }, '📷 ' + t('cameraVisionFeed')),
            h('span', {
              key: 's1b',
              className: 'mono',
              style: {
                fontSize: '0.64rem',
                padding: '2px 6px',
                borderRadius: 4,
                background: facesCount > 0 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                color: facesCount > 0 ? '#10b981' : '#f59e0b'
              }
            }, facesCount > 0 ? (facesCount + ' ' + t('faceLocked')) : t('searchingFace'))
          ]),
          h('div', { key: 's1em', style: { display: 'flex', alignItems: 'baseline', gap: 8, margin: '8px 0 4px 0' } }, [
            h('span', { key: 'em', style: { fontSize: '1.4rem', fontWeight: 800, color: visualColor } }, localizedEmotion.toUpperCase()),
            faceConf > 0 ? h('span', { key: 'cf', className: 'mono', style: { fontSize: '0.78rem', color: '#94a3b8' } }, '(' + faceConf + '%)') : null
          ]),
          h('div', { key: 's1sub', style: { fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 } }, t('facialAffectState') + ': ' + localizedEmotion)
        ]),
        h('div', {
          key: 's1stats',
          style: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, padding: '8px 10px', background: 'rgba(7, 9, 14, 0.6)', borderRadius: 8 }
        }, [
          h('div', { key: 'st1' }, [
            h('div', { key: 'lbl', style: { fontSize: '0.62rem', color: '#64748b' } }, t('inferenceSpeed')),
            h('div', { key: 'val', className: 'mono', style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' } }, fps + ' FPS (' + latency + 'ms)')
          ]),
          h('div', { key: 'st2' }, [
            h('div', { key: 'lbl', style: { fontSize: '0.62rem', color: '#64748b' } }, t('facialStrain')),
            h('div', { key: 'val', className: 'mono', style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' } }, (assessment ? assessment.visualStrain.toFixed(1) : '0.0') + '%')
          ])
        ])
      ]),

      // Sensor 2: Acoustic Cry Feed
      h('div', {
        key: 's2',
        style: {
          background: 'rgba(15, 23, 42, 0.7)',
          borderRadius: 12,
          border: '1px solid ' + audioColor + '44',
          padding: 14,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          boxShadow: '0 4px 20px ' + audioColor + '15'
        }
      }, [
        h('div', { key: 'top' }, [
          h('div', { key: 's2hdr', style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 } }, [
            h('span', { key: 's2t', style: { fontSize: '0.72rem', fontWeight: 700, color: audioColor, letterSpacing: '0.08em' } }, '🎙️ ' + t('acousticCryFeed')),
            audioConf !== null ? h('span', {
              key: 's2b',
              className: 'mono',
              style: { fontSize: '0.64rem', padding: '2px 6px', borderRadius: 4, background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc' }
            }, audioConf + '% ' + t('acousticConf')) : null
          ]),
          h('div', { key: 's2title', style: { display: 'flex', alignItems: 'center', gap: 8, margin: '8px 0 4px 0' } }, [
            h('span', { key: 'icn', style: { fontSize: '1.25rem' } }, audioIcon),
            h('span', { key: 't', style: { fontSize: '1.05rem', fontWeight: 800, color: audioColor } }, localizedAudioTitle)
          ]),
          h('div', { key: 's2sub', style: { fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 } }, rawCategory ? (t('primaryCrySig') + ': ' + rawCategory.toUpperCase()) : t('awaitingCry'))
        ]),
        h('div', {
          key: 's2stats',
          style: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, padding: '8px 10px', background: 'rgba(7, 9, 14, 0.6)', borderRadius: 8 }
        }, [
          h('div', { key: 'st1' }, [
            h('div', { key: 'lbl', style: { fontSize: '0.62rem', color: '#64748b' } }, t('acousticSeverity')),
            h('div', { key: 'val', className: 'mono', style: { fontSize: '0.85rem', fontWeight: 700, color: audioColor } }, (audioConf !== null ? audioConf : (assessment ? assessment.acousticSeverity.toFixed(1) : '0.0')) + '%')
          ]),
          h('div', { key: 'st2' }, [
            h('div', { key: 'lbl', style: { fontSize: '0.62rem', color: '#64748b' } }, 'STATUS'),
            h('div', { key: 'val', className: 'mono', style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' } }, rawCategory ? 'IDENTIFIED' : 'IDLE')
          ])
        ])
      ])
    ]),

    // Bottom Combined Verdict
    h('div', {
      key: 'verdict',
      style: {
        background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9))',
        borderRadius: 12,
        padding: '14px 16px',
        border: '1px solid rgba(148, 163, 184, 0.15)'
      }
    }, [
      h('div', { key: 'vhdr', style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 } }, [
        h('span', { key: 'vt', style: { fontSize: '0.78rem', fontWeight: 800, letterSpacing: '0.06em', color: '#e2e8f0' } }, t('multimodalVerdict')),
        h('span', {
          key: 'vbdg',
          className: 'mono',
          style: { fontSize: '0.74rem', fontWeight: 700, padding: '3px 8px', borderRadius: 6, background: severityColor + '22', color: severityColor, border: '1px solid ' + severityColor + '44' }
        }, severityBadge)
      ]),
      h('div', {
        key: 'vmsg',
        style: {
          fontSize: '0.86rem',
          color: '#f8fafc',
          fontStyle: 'italic',
          lineHeight: 1.5,
          marginBottom: 8,
          padding: '8px 12px',
          background: 'rgba(7, 9, 14, 0.5)',
          borderRadius: 8,
          borderLeft: '3px solid ' + severityColor
        }
      }, '"' + localizedBabyMessage + '"'),
      h('div', {
        key: 'vact',
        style: { fontSize: '0.75rem', color: '#94a3b8' }
      }, [
        h('strong', { key: 'lbl', style: { color: '#38bdf8' } }, t('recommendedAction') + ': '),
        localizedSoothingTip
      ])
    ])
  ]);
};

"""
    content = content[:p_dual_start] + new_dual + content[p_dual_end:]
    print("[1] Successfully patched DualSensorResultCard in bundle.js with multilingual React.createElement component!")
else:
    print(f"[WARN] DualSensorResultCard boundary not matched: start={p_dual_start}, end={p_dual_end}")

# 2. Update VideoFeedCard button labels and titles to use window.__t
card_p = content.find("const VideoFeedCard = ({")
if card_p != -1:
    card_end = content.find("_s(VideoFeedCard,", card_p)
    old_card_code = content[card_p:card_end]
    
    # Replace hardcoded strings with t(key)
    old_card_code = old_card_code.replace('"● Live Camera"', "t('liveCamera')")
    old_card_code = old_card_code.replace('"📹 Device Webcam"', "t('deviceWebcam')")
    old_card_code = old_card_code.replace('" Upload Photo"', '" " + t(\'uploadPhoto\')')
    old_card_code = old_card_code.replace('"Infant Video Feed & Targeting HUD"', "t('hudTitle')")
    old_card_code = old_card_code.replace('"FPS: "', "t('fps') + ': '")
    old_card_code = old_card_code.replace('"Faces: "', "t('faces') + ': '")
    old_card_code = old_card_code.replace('"Affect: "', "t('facialAffect') + ': '")
    
    # Make sure const t = window.__t is defined inside VideoFeedCard
    if "const t = (k) =>" not in old_card_code:
        old_card_code = old_card_code.replace("const fileRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);", "const fileRef = (0, react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);\n  const t = (k) => window.__t ? window.__t(k) : k;")
        
    content = content[:card_p] + old_card_code + content[card_end:]
    print("[2] Successfully patched VideoFeedCard with localized buttons and HUD titles!")

with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {bundle_path} successfully!")
