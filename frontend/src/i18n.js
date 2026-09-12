import { useState, useEffect } from 'react';

export const TRANSLATIONS = {
  en: {
    // Header
    appTitle1: "Multimodal",
    appTitle2: "Infant Distress Monitor",
    appSubtitle: "FACE EMOTION AI (SLIM 320) + BABYCRY AI ACOUSTICS",
    visionActive: "VISION ACTIVE",
    acousticActive: "ACOUSTIC ACTIVE",
    
    // Video Card & HUD
    hudTitle: "Infant Video Feed & Targeting HUD",
    hudSub: "Slim 320 SSD (320x240) + FERPlus",
    liveCamera: "● Live Camera",
    deviceWebcam: "📹 Device Webcam",
    uploadPhoto: "📁 Upload Photo",
    targetLocked: "TARGET LOCKED",
    searchingTarget: "SEARCHING TARGET • NEURAL SCAN ACTIVE",
    liveHwWebcam: "◈ LIVE HARDWARE WEBCAM",
    browserWebcamActive: "◈ BROWSER WEBCAM ACTIVE",
    photoArchetype: "◈ PHOTO ARCHETYPE",
    fps: "FPS",
    latency: "LATENCY",
    faces: "Faces",
    facialAffect: "Affect",
    
    // Dual-Sensor Console
    dualSensorTitle: "DUAL-SENSOR AI DETECTION CONSOLE",
    dualSensorSub: "Persistent Camera Vision + Acoustic Cry Classification Feed",
    cameraVisionFeed: "CAMERA VISION FEED",
    faceLocked: "FACE LOCKED",
    searchingFace: "SEARCHING FACE",
    facialAffectState: "Facial Affective State",
    inferenceSpeed: "INFERENCE SPEED",
    facialStrain: "FACIAL STRAIN",
    acousticCryFeed: "ACOUSTIC CRY FEED",
    awaitingCry: "Awaiting Mic Cry or Audio File Upload",
    primaryCrySig: "PRIMARY CRY SIGNATURE",
    acousticSeverity: "ACOUSTIC SEVERITY",
    acousticConf: "Confidence",
    multimodalVerdict: "MULTIMODAL COMBINED VERDICT",
    unifiedDistressScore: "UNIFIED DISTRESS SCORE",
    recommendedAction: "RECOMMENDED SOOTHING ACTION",
    soothingDefault: "Check diaper comfort, offer gentle rhythmic rocking, and hold baby close.",
    
    // Emotions
    emotions: {
      Neutral: "Neutral",
      Happy: "Happy",
      Sad: "Sad",
      Surprise: "Surprise",
      Fear: "Fear",
      Disgust: "Disgust",
      Angry: "Angry",
      Contempt: "Contempt"
    },
    spectrumTitle: "Facial Emotion Spectrum (Visual Tension)",
    ferplusSub: "FERPLUS (8 CLASSES)",
    
    // Distress Assessment
    distressTitle: "Multimodal Distress Gauge",
    distressLevels: {
      severe: "SEVERE DISTRESS",
      moderate: "MODERATE DISTRESS",
      mild: "MILD DISTRESS",
      none: "CALM / NOMINAL",
      nominal: "CALM / NOMINAL"
    },
    visualStrainLabel: "Visual Strain",
    acousticStrainLabel: "Acoustic Strain",
    primaryAffectLabel: "Primary Affect",
    
    // Inner Voice
    innerVoiceTitle: "Infant Inner Voice (AI Translation)",
    innerVoiceSub: "CROSS-MODAL REASONING",
    speakBtn: "Speak Message",
    speakingBtn: "Speaking...",
    
    // Acoustic Classifier
    acousticTitle: "Acoustic Cry Classifier",
    acousticSub: "194-DIMENSION SVC SPECTRAL MODEL",
    recordMicBtn: "Record Cry via Mic (3s)",
    recordingMicBtn: "Listening... (3s)",
    uploadAudioBtn: "Upload Audio",
    archetypeHeading: "Standard Pediatric Cry Archetypes",
    archetypes: {
      hungry: "Hunger Cry (Milk)",
      belly_pain: "Colic & Belly Pain",
      colic: "Colic & Belly Pain",
      burp: "Burping Needed",
      burping: "Burping Needed",
      tired: "Tiredness & Sleepy",
      discomfort: "Diaper / Discomfort"
    },
    
    // Soothing Protocol
    soothingTitle: "Pediatric Soothing Checklist",
    soothingSub: "CLINICAL PROTOCOL",
    soothingSteps: [
      "Check diaper comfort and skin temperature.",
      "Offer gentle skin-to-skin holding and rhythmic rocking.",
      "Verify feeding schedule and wake window duration.",
      "Swaddle snugly in a quiet, softly lit nursery environment."
    ],
    
    // Inner Voice Messages
    cryMessages: {
      hungry: "My little tummy is rumbling and feeling so empty! I am super hungry and need some warm milk please.",
      belly_pain: "My little tummy really cramps and hurts inside! I have stubborn gas bubbles. Please bicycle my legs gently and rub my tummy.",
      colic: "My little tummy really cramps and hurts inside! I have stubborn gas bubbles. Please bicycle my legs gently and rub my tummy.",
      burping: "There is a sneaky air bubble trapped in my chest after drinking milk! Please hold me upright over your shoulder and gently pat my back.",
      burp: "There is a sneaky air bubble trapped in my chest after drinking milk! Please hold me upright over your shoulder and gently pat my back.",
      tired: "My eyes are heavy and everything around me is too bright and loud! Please wrap me snugly, dim the lights, and rock me to sleep.",
      discomfort: "Something is tickling, pinching, or bothering my sensitive skin! Please check if my diaper is wet or if my clothes are tight.",
      calm: "I am feeling calm, peaceful, and comfortable right now with you, Mommy and Daddy!",
      fussy: "I am feeling a little fussy right now and need some gentle comfort."
    }
  },

  hi: {
    // Header
    appTitle1: "मल्टीमॉडल",
    appTitle2: "शिशु संकट मॉनिटर",
    appSubtitle: "चेहरे के भाव एआई (स्लिम 320) + शिशु रुदन ध्वनिकी",
    visionActive: "दृष्टि सक्रिय",
    acousticActive: "ध्वनि सक्रिय",
    
    // Video Card & HUD
    hudTitle: "शिशु वीडियो फ़ीड और लक्ष्यीकरण एचयूडी",
    hudSub: "स्लिम 320 एसएसडी + एफईआरप्लस",
    liveCamera: "● लाइव कैमरा",
    deviceWebcam: "📹 डिवाइस वेबकैम",
    uploadPhoto: "📁 फोटो अपलोड करें",
    targetLocked: "लक्ष्य लॉक",
    searchingTarget: "लक्ष्य की खोज जारी • न्यूरल स्कैन सक्रिय",
    liveHwWebcam: "◈ लाइव हार्डवेयर वेबकैम",
    browserWebcamActive: "◈ ब्राउज़र वेबकैम सक्रिय",
    photoArchetype: "◈ फोटो नमूना",
    fps: "एफपीएस",
    latency: "विलंबता",
    faces: "चेहरे",
    facialAffect: "मनोभाव",
    
    // Dual-Sensor Console
    dualSensorTitle: "दोहरे सेंसर एआई डिटेक्शन कंसोल",
    dualSensorSub: "निरंतर कैमरा विज़न + रुदन ध्वनि वर्गीकरण फ़ीड",
    cameraVisionFeed: "कैमरा विज़न फ़ीड",
    faceLocked: "चेहरा लॉक",
    searchingFace: "चेहरा खोज रहे हैं",
    facialAffectState: "चेहरे की भावनात्मक स्थिति",
    inferenceSpeed: "अनुमान गति",
    facialStrain: "चेहरे का तनाव",
    acousticCryFeed: "शिशु रुदन ध्वनि फ़ीड",
    awaitingCry: "माइक रिकॉर्डिंग या ऑडियो फ़ाइल की प्रतीक्षा है",
    primaryCrySig: "प्राथमिक रुदन संकेत",
    acousticSeverity: "ध्वनि गंभीरता",
    acousticConf: "विश्वसनीयता",
    multimodalVerdict: "मल्टीमॉडल संयुक्त निष्कर्ष",
    unifiedDistressScore: "एकीकृत संकट स्तर",
    recommendedAction: "सुझाया गया शांत करने का उपाय",
    soothingDefault: "डायपर का सूखापन जांचें, शिशु को सीने से लगाकर रखें और हल्के हाथों से झुलाएं।",
    
    // Emotions
    emotions: {
      Neutral: "शांत / सामान्य",
      Happy: "प्रसन्न",
      Sad: "उदास",
      Surprise: "आश्चर्य",
      Fear: "भय",
      Disgust: "अप्रिय",
      Angry: "क्रोधित",
      Contempt: "खिन्न"
    },
    spectrumTitle: "चेहरे के भाव स्पेक्ट्रम (दृश्य तनाव)",
    ferplusSub: "एफईआरप्लस (8 श्रेणियां)",
    
    // Distress Assessment
    distressTitle: "मल्टीमॉडल संकट मूल्यांकन",
    distressLevels: {
      severe: "अत्यधिक संकट",
      moderate: "मध्यम संकट",
      mild: "हल्का संकट",
      none: "शांत / सामान्य",
      nominal: "शांत / सामान्य"
    },
    visualStrainLabel: "दृश्य तनाव",
    acousticStrainLabel: "ध्वनि तनाव",
    primaryAffectLabel: "प्राथमिक मनोभाव",
    
    // Inner Voice
    innerVoiceTitle: "शिशु के मन की बात (एआई अनुवाद)",
    innerVoiceSub: "क्रॉस-मॉडल विश्लेषण",
    speakBtn: "आवाज़ में सुनें",
    speakingBtn: "बोल रहा है...",
    
    // Acoustic Classifier
    acousticTitle: "रुदन ध्वनि क्लासिफायर",
    acousticSub: "194-आयामी स्पेक्ट्रल मॉडल",
    recordMicBtn: "माइक से रोना रिकॉर्ड करें (3s)",
    recordingMicBtn: "सुन रहे हैं... (3s)",
    uploadAudioBtn: "ऑडियो अपलोड करें",
    archetypeHeading: "मानक शिशु रुदन नमूने",
    archetypes: {
      hungry: "भूख (दूध चाहिए)",
      belly_pain: "पेट में गैस / मरोड़",
      colic: "पेट में गैस / मरोड़",
      burp: "डकार की जरूरत",
      burping: "डकार की जरूरत",
      tired: "नींद / थकान",
      discomfort: "डायपर / असुविधा"
    },
    
    // Soothing Protocol
    soothingTitle: "शिशु देखभाल और शांत करने के चरण",
    soothingSub: "क्लिनिकल प्रोटोकॉल",
    soothingSteps: [
      "डायपर का सूखापन और शरीर का तापमान जांचें।",
      "शिशु को सीने से लगाकर रखें और हल्के हाथों से झुलाएं।",
      "दूध पिलाने का समय और जागने का अंतराल जांचें।",
      "शांत और मंद रोशनी वाले कमरे में शिशु को हल्के कपड़े में लपेटें।"
    ],
    
    // Inner Voice Messages
    cryMessages: {
      hungry: "मेरा नन्हा पेट खाली है और भूख से गुड़गुड़ा रहा है! मुझे बहुत भूख लगी है, कृपया मुझे थोड़ा गर्म दूध पिलाइए।",
      belly_pain: "मेरे पेट में मरोड़ और ऐंठन हो रही है! गैस फंसी है। कृपया मेरे पैर साइकिल की तरह चलाएं और पेट की हल्की मालिश करें।",
      colic: "मेरे पेट में मरोड़ और ऐंठन हो रही है! गैस फंसी है। कृपया मेरे पैर साइकिल की तरह चलाएं और पेट की हल्की मालिश करें।",
      burping: "दूध पीने के बाद छाती में एक हवा का बुलबुला फंस गया है! कृपया मुझे कंधे पर सीधा लेकर पीठ थपथपाएं।",
      burp: "दूध पीने के बाद छाती में एक हवा का बुलबुला फंस गया है! कृपया मुझे कंधे पर सीधा लेकर पीठ थपथपाएं।",
      tired: "आसपास बहुत उजाला और शोर है, मेरी पलकें भारी हो रही हैं! कृपया मुझे किसी शांत और मंद कमरे में झुलाकर सुलाएं।",
      discomfort: "मेरे कपड़ों में कुछ चुभ रहा है या मेरा डायपर गीला हो सकता है! कृपया मेरे कपड़े और डायपर जांचें।",
      calm: "मैं इस समय आपके साथ बहुत शांत, सुरक्षित और खुश महसूस कर रहा हूँ, मम्मी-पापा!",
      fussy: "मुझे थोड़ी परेशानी हो रही है और मुझे आपके प्यार और दुलार की जरूरत है।"
    }
  },

  bn: {
    // Header
    appTitle1: "মাল্টিমোডাল",
    appTitle2: "শিশু কষ্ট মনিটর",
    appSubtitle: "মুখের অভিব্যক্তি এআই (স্লিম ৩২০) + শিশুর কান্নার ধ্বনিবিজ্ঞান",
    visionActive: "দৃষ্টি সক্রিয়",
    acousticActive: "শব্দ সক্রিয়",
    
    // Video Card & HUD
    hudTitle: "শিশু ভিডিও ফিড এবং টার্গেটিং এইচইউডি",
    hudSub: "স্লিম ৩২০ এসএসডি + এফইআরপ্লাস",
    liveCamera: "● লাইভ ক্যামেরা",
    deviceWebcam: "📹 ডিভাইস ওয়েবক্যাম",
    uploadPhoto: "📁 ছবি আপলোড করুন",
    targetLocked: "টার্গেট লক",
    searchingTarget: "টার্গেট খোঁজা হচ্ছে • নিউরাল স্ক্যান সক্রিয়",
    liveHwWebcam: "◈ লাইভ হার্ডওয়্যার ওয়েবক্যাম",
    browserWebcamActive: "◈ ব্রাউজার ওয়েবক্যাম সক্রিয়",
    photoArchetype: "◈ ছবির নমুনা",
    fps: "এফপিএস",
    latency: "বিলম্ব",
    faces: "মুখ",
    facialAffect: "অনুভূতি",
    
    // Dual-Sensor Console
    dualSensorTitle: "দ্বৈত-সেন্সর এআই সনাক্তকরণ কনসোল",
    dualSensorSub: "ধারাবাহিক ক্যামেরা ভিশন + কান্না শব্দ শ্রেণিবিভাগ ফিড",
    cameraVisionFeed: "ক্যামেরা ভিশন ফিড",
    faceLocked: "মুখমণ্ডল লক",
    searchingFace: "মুখমণ্ডল খোঁজা হচ্ছে",
    facialAffectState: "মুখের মানসিক অবস্থা",
    inferenceSpeed: "অনুমান গতি",
    facialStrain: "মুখের চাপ",
    acousticCryFeed: "শিশুর কান্না শব্দ ফিড",
    awaitingCry: "মাইক রেকর্ডিং বা অডিও ফাইলের অপেক্ষায়",
    primaryCrySig: "প্রধান কান্নার ধরন",
    acousticSeverity: "শব্দের তীব্রতা",
    acousticConf: "নির্ভরযোগ্যতা",
    multimodalVerdict: "মাল্টিমোডাল সম্মিলিত সিদ্ধান্ত",
    unifiedDistressScore: "সম্মিলিত কষ্টের মাত্রা",
    recommendedAction: "প্রস্তাবিত শান্ত করার পদক্ষেপ",
    soothingDefault: "ডায়পারের আরাম পরীক্ষা করুন, শান্তভাবে ছন্দময়ভাবে দোল দিন এবং শিশুকে বুকে জড়িয়ে রাখুন।",
    
    // Emotions
    emotions: {
      Neutral: "স্বাভাবিক",
      Happy: "খুশি",
      Sad: "বিষণ্ণ",
      Surprise: "বিস্মিত",
      Fear: "ভয়",
      Disgust: "বিরক্ত",
      Angry: "রাগান্বিত",
      Contempt: "উদাসীন"
    },
    spectrumTitle: "মুখের অভিব্যক্তি স্পেকট্রাম (ভিজ্যুয়াল চাপ)",
    ferplusSub: "এফইআরপ্লাস (৮টি শ্রেণি)",
    
    // Distress Assessment
    distressTitle: "মাল্টিমোডাল কষ্ট মূল্যায়ন",
    distressLevels: {
      severe: "তীব্র কষ্ট",
      moderate: "মাঝারি কষ্ট",
      mild: "সামান্য কষ্ট",
      none: "শান্ত / স্বাভাবিক",
      nominal: "শান্ত / স্বাভাবিক"
    },
    visualStrainLabel: "ভিজ্যুয়াল চাপ",
    acousticStrainLabel: "শব্দ চাপ",
    primaryAffectLabel: "প্রধান অনুভূতি",
    
    // Inner Voice
    innerVoiceTitle: "শিশুর মনের কথা (এআই অনুবাদ)",
    innerVoiceSub: "ক্রস-মোডাল বিশ্লেষণ",
    speakBtn: "শুনুন",
    speakingBtn: "বলা হচ্ছে...",
    
    // Acoustic Classifier
    acousticTitle: "কান্নার শব্দ ক্লাসিফায়ার",
    acousticSub: "১৯৪-মাত্রিক স্পেকট্রাল মডেল",
    recordMicBtn: "মাইকে কান্না রেকর্ড করুন (৩ সে.)",
    recordingMicBtn: "শুনছি... (৩ সে.)",
    uploadAudioBtn: "অডিও আপলোড করুন",
    archetypeHeading: "স্ট্যান্ডার্ড শিশুর কান্নার নমুনা",
    archetypes: {
      hungry: "ক্ষুধার্ত (দুধের প্রয়োজন)",
      belly_pain: "পেটে গ্যাস / ব্যথা",
      colic: "পেটে গ্যাস / ব্যথা",
      burp: "ঢেকুর তোলা প্রয়োজন",
      burping: "ঢেকুর তোলা প্রয়োজন",
      tired: "ক্লান্তি / ঘুম",
      discomfort: "ডায়পার / অস্বস্তি"
    },
    
    // Soothing Protocol
    soothingTitle: "শিশুকে শান্ত করার পদক্ষেপ",
    soothingSub: "ক্লিনিকাল নির্দেশিকা",
    soothingSteps: [
      "ডায়পারের আরাম ও শরীরের তাপমাত্রা পরীক্ষা করুন।",
      "কোলে নিয়ে শান্তভাবে ছন্দময়ভাবে দোল দিন।",
      "খাওয়ানোর সময় এবং জেগে থাকার সময়সীমা পরীক্ষা করুন।",
      "একটি শান্ত ও আবছা আলোর ঘরে আরামদায়কভাবে জড়িয়ে রাখুন।"
    ],
    
    // Inner Voice Messages
    cryMessages: {
      hungry: "আমার ছোট্ট পেটটা খালি হয়ে গেছে আর খিদে পেয়েছে! আমার খুব খিদে পেয়েছে, দয়া করে আমাকে একটু উষ্ণ দুধ খাওয়ান।",
      belly_pain: "আমার পেটে মোচড় দিয়ে ব্যথা করছে আর অস্বস্তি হচ্ছে! পেটে হালকা মালিশ আর একটু উষ্ণ সেঁক দিলে খুব আরাম পাব।",
      colic: "আমার পেটে মোচড় দিয়ে ব্যথা করছে আর অস্বস্তি হচ্ছে! পেটে হালকা মালিশ আর একটু উষ্ণ সেঁক দিলে খুব আরাম পাব।",
      burping: "দুধ খাওয়ার পর বুকে একটা বাতাসের বুদ্বুদ আটকে আছে! দয়া করে আমাকে কাঁধের ওপর সোজা করে ধরে পিঠে হালকা চাপড় দিন।",
      burp: "দুধ খাওয়ার পর বুকে একটা বাতাসের বুদ্বুদ আটকে আছে! দয়া করে আমাকে কাঁধের ওপর সোজা করে ধরে পিঠে হালকা চাপড় দিন।",
      tired: "চারপাশে খুব আওয়াজ আর আলো, আমার চোখ দুটো ভারী হয়ে আসছে! দয়া করে একটি শান্ত আবছা আলোর ঘরে নিয়ে আমাকে একটু দোল দিন যাতে আমি ঘুমাতে পারি।",
      discomfort: "আমার জামাকাপড়ে কিছু একটা খচখচ করছে বা ডায়পারটা ভিজে গেছে! দয়া করে আমার ডায়পার আর জামাকাপড় পরীক্ষা করুন।",
      calm: "আমি এখন তোমাদের সাথে খুব শান্ত, নিরাপদ আর খুশি অনুভব করছি, মা-বাবা!",
      fussy: "আমার একটু মন খারাপ লাগছে এবং তোমাদের একটু আদর দরকার।"
    }
  }
};

export const getInitialLanguage = () => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('crysense_lang');
    if (saved && ['en', 'hi', 'bn'].includes(saved)) {
      return saved;
    }
  }
  return 'en';
};

export const setStoredLanguage = (lang) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('crysense_lang', lang);
    window.dispatchEvent(new CustomEvent('crysense_lang_changed', { detail: lang }));
  }
};

export const useTranslation = () => {
  const [lang, setLangState] = useState(getInitialLanguage);

  useEffect(() => {
    const handler = (e) => {
      if (e.detail && ['en', 'hi', 'bn'].includes(e.detail)) {
        setLangState(e.detail);
      }
    };
    window.addEventListener('crysense_lang_changed', handler);
    return () => window.removeEventListener('crysense_lang_changed', handler);
  }, []);

  const changeLanguage = (newLang) => {
    if (['en', 'hi', 'bn'].includes(newLang)) {
      setLangState(newLang);
      setStoredLanguage(newLang);
    }
  };

  const t = (key) => {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
    const parts = key.split('.');
    let val = dict;
    for (const p of parts) {
      if (val && val[p] !== undefined) {
        val = val[p];
      } else {
        // Fallback to English
        let fallback = TRANSLATIONS.en;
        for (const fp of parts) {
          if (fallback && fallback[fp] !== undefined) {
            fallback = fallback[fp];
          } else {
            return key;
          }
        }
        return fallback;
      }
    }
    return val;
  };

  return { lang, changeLanguage, t, translations: TRANSLATIONS[lang] || TRANSLATIONS.en };
};

export default useTranslation;
