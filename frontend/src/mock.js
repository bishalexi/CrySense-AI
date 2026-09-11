export const emotionClasses = [
  { key: 'Happy', label: 'Happy', emoji: '😊', color: '#10b981', value: 4.2 },
  { key: 'Neutral', label: 'Neutral', emoji: '😐', color: '#94a3b8', value: 58.3 },
  { key: 'Surprise', label: 'Surprise', emoji: '😲', color: '#f59e0b', value: 6.1 },
  { key: 'Sad', label: 'Sad', emoji: '😢', color: '#38bdf8', value: 12.5 },
  { key: 'Angry', label: 'Angry', emoji: '😡', color: '#f43f5e', value: 8.7 },
  { key: 'Disgust', label: 'Disgust', emoji: '🤢', color: '#14b8a6', value: 2.1 },
  { key: 'Fear', label: 'Fear', emoji: '😨', color: '#a855f7', value: 5.3 },
  { key: 'Contempt', label: 'Contempt', emoji: '😏', color: '#ec4899', value: 2.8 },
];

export const distressLevels = {
  none: { label: 'Calm & Content', color: '#10b981', badge: 'NO DISTRESS' },
  mild: { label: 'Mild Discomfort / Fussy', color: '#f59e0b', badge: 'MILD DISTRESS' },
  moderate: { label: 'Moderate Distress', color: '#f97316', badge: 'MODERATE DISTRESS' },
  severe: { label: 'Severe Distress', color: '#ef4444', badge: 'SEVERE DISTRESS' },
};

export const initialAssessment = {
  percentage: 37.5,
  level: 'mild',
  visualStrain: 37.5,
  acousticSeverity: 0.0,
  primaryAffect: 'NEUTRAL',
  innerVoice: '“I am feeling calm, peaceful, and comfortable right now with you, Mommy and Daddy!”',
};

export const archetypeCries = [
  { id: 'hungry', label: 'demo_hungry.wav', icon: 'Music2', tone: '#38bdf8', description: 'Rhythmic hunger cry' },
  { id: 'colic', label: 'Belly Pain (Colic)', icon: 'Bandage', tone: '#f43f5e', description: 'High-pitch colic pattern' },
  { id: 'burp', label: 'Burping Needed', icon: 'Wind', tone: '#a855f7', description: 'Grunt with pauses' },
  { id: 'hunger', label: 'Hunger Cry', icon: 'Milk', tone: '#f59e0b', description: 'Sustained low-pitch cry' },
  { id: 'tired', label: 'Tired Cry', icon: 'Moon', tone: '#38bdf8', description: 'Whiny descending pattern' },
  { id: 'discomfort', label: 'Discomfort Cry', icon: 'AlertCircle', tone: '#ec4899', description: 'Irregular sharp cry' },
];

export const soothingProtocols = [
  'Check diaper comfort and skin temperature.',
  'Offer gentle skin-to-skin holding and rhythmic rocking.',
  'Verify feeding schedule and wake window duration.',
  'Reduce environmental stimulation and dim ambient lighting.',
  'Introduce soft white noise and a slow lullaby cadence.',
];

export const innerVoiceSamples = {
  none: '“I am feeling calm, peaceful, and comfortable right now with you, Mommy and Daddy!”',
  mild: '“I feel a little uneasy — maybe check my diaper or give me a gentle cuddle please.”',
  moderate: '“Something is bothering me and I need your help soon, please hold me close.”',
  severe: '“I really need you right now — please pick me up and comfort me immediately!”',
};

export const acousticClasses = [
  { key: 'belly_pain', label: 'Belly Pain', color: '#f43f5e', value: 0 },
  { key: 'burping', label: 'Burping', color: '#a855f7', value: 0 },
  { key: 'discomfort', label: 'Discomfort', color: '#ec4899', value: 0 },
  { key: 'hungry', label: 'Hungry', color: '#f59e0b', value: 0 },
  { key: 'tired', label: 'Tired', color: '#38bdf8', value: 0 },
];
