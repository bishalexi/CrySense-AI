import React from 'react';
import { motion } from 'framer-motion';
import { Baby, Activity, Radio, Globe } from 'lucide-react';
import { useTranslation } from '../i18n';

const Pulse = ({ color }) => (
  <motion.span
    animate={{ scale: [1, 1.4, 1], opacity: [0.9, 0.4, 0.9] }}
    transition={{ duration: 1.6, repeat: Infinity }}
    style={{
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: color,
      display: 'inline-block',
      boxShadow: `0 0 12px ${color}`,
    }}
  />
);

const Header = () => {
  const { lang, changeLanguage, t } = useTranslation();

  const languages = [
    { id: 'en', label: 'English', short: 'EN' },
    { id: 'hi', label: 'हिन्दी', short: 'हिन्दी' },
    { id: 'bn', label: 'বাংলা', short: 'বাংলা' },
  ];

  return (
    <header
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 32px',
        position: 'relative',
        zIndex: 10,
        borderBottom: '1px solid rgba(148, 163, 184, 0.12)',
        background: 'rgba(10, 14, 24, 0.65)',
        backdropFilter: 'blur(14px)',
        flexWrap: 'wrap',
        gap: 14,
      }}
    >
      {/* App Logo & Title */}
      <motion.div
        initial={{ opacity: 0, x: -18 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        style={{ display: 'flex', alignItems: 'center', gap: 14 }}
      >
        <motion.div
          animate={{ rotateY: [0, 360] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'linear' }}
          style={{
            width: 46,
            height: 46,
            borderRadius: 13,
            background:
              'linear-gradient(135deg, #f472b6 0%, #a855f7 50%, #38bdf8 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow:
              '0 10px 30px rgba(168, 85, 247, 0.35), inset 0 1px 0 rgba(255,255,255,0.35)',
            transformStyle: 'preserve-3d',
            flexShrink: 0,
          }}
        >
          <Baby size={24} color="#fff" strokeWidth={2.2} />
        </motion.div>
        <div>
          <div
            style={{
              fontSize: '1.15rem',
              fontWeight: 700,
              color: '#fff',
              letterSpacing: '-0.01em',
            }}
          >
            <span style={{ color: '#c4b5fd' }}>{t('appTitle1')}</span> {t('appTitle2')}
          </div>
          <div
            style={{
              fontSize: '0.68rem',
              color: '#94a3b8',
              letterSpacing: '0.14em',
              fontFamily: 'JetBrains Mono, monospace',
              marginTop: 2,
            }}
          >
            {t('appSubtitle')}
          </div>
        </div>
      </motion.div>

      {/* Right Controls: Language Switcher & Status Indicators */}
      <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
        {/* Language Switcher Buttons */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            background: 'rgba(15, 23, 42, 0.85)',
            border: '1px solid rgba(148, 163, 184, 0.25)',
            borderRadius: 10,
            padding: '3px 4px',
            gap: 3,
            boxShadow: '0 4px 14px rgba(0,0,0,0.35)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', padding: '0 6px', color: '#38bdf8' }}>
            <Globe size={13} />
          </div>
          {languages.map((l) => {
            const active = lang === l.id;
            return (
              <button
                key={l.id}
                onClick={() => changeLanguage(l.id)}
                style={{
                  background: active
                    ? 'linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(168, 85, 247, 0.35))'
                    : 'transparent',
                  border: active
                    ? '1px solid rgba(56, 189, 248, 0.8)'
                    : '1px solid transparent',
                  color: active ? '#38bdf8' : '#94a3b8',
                  fontWeight: active ? 700 : 500,
                  padding: '4px 11px',
                  borderRadius: 7,
                  fontSize: '0.74rem',
                  cursor: 'pointer',
                  fontFamily: 'Inter, system-ui, sans-serif',
                  transition: 'all 0.18s ease',
                  boxShadow: active ? '0 0 10px rgba(56, 189, 248, 0.3)' : 'none',
                }}
              >
                {l.short}
              </button>
            );
          })}
        </div>

        {/* Vision Active Badge */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 7,
            padding: '7px 12px',
            borderRadius: 9,
            background: 'rgba(56, 189, 248, 0.10)',
            border: '1px solid rgba(56, 189, 248, 0.30)',
            color: '#38bdf8',
            fontSize: '0.7rem',
            fontWeight: 700,
            letterSpacing: '0.12em',
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          <Pulse color="#38bdf8" />
          <Activity size={12} /> {t('visionActive')}
        </div>

        {/* Acoustic Active Badge */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 7,
            padding: '7px 12px',
            borderRadius: 9,
            background: 'rgba(244, 63, 94, 0.10)',
            border: '1px solid rgba(244, 63, 94, 0.30)',
            color: '#fb7185',
            fontSize: '0.7rem',
            fontWeight: 700,
            letterSpacing: '0.12em',
            fontFamily: 'JetBrains Mono, monospace',
          }}
        >
          <Pulse color="#fb7185" />
          <Radio size={12} /> {t('acousticActive')}
        </div>
      </div>
    </header>
  );
};

export default Header;
