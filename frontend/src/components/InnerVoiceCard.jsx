import React from 'react';
import { motion } from 'framer-motion';
import Tilt3D from './Tilt3D';
import Button3D from './Button3D';
import { MessageCircle, Volume2 } from 'lucide-react';

const InnerVoiceCard = ({ text, onSpeak }) => {
  return (
    <Tilt3D intensity={4} className="glass-card" style={{ padding: '18px 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            fontSize: '0.78rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            color: '#a5b4fc',
          }}
        >
          <MessageCircle size={16} /> BABY’S INNER VOICE TRANSLATION
        </div>
        <Button3D onClick={onSpeak} color="#818cf8" shadow="#4f46e5" size="sm" icon={<Volume2 size={14} />}>
          Listen
        </Button3D>
      </div>
      <motion.div
        key={text}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        style={{
          fontSize: '0.95rem',
          color: '#e2e8f0',
          fontStyle: 'italic',
          lineHeight: 1.55,
          borderLeft: '3px solid #818cf8',
          paddingLeft: 12,
        }}
      >
        {text}
      </motion.div>
    </Tilt3D>
  );
};

export default InnerVoiceCard;
