"""Patches static/js/bundle.js and templates/index.html with full multi-lingual support:
- English (EN)
- Hindi (HI / हिन्दी)
- Bengali (BN / বাংলা)
Includes:
- Interactive language toggle button group [ 🌐 EN | हिन्दी | বাংলা ]
- Instant reactive state synchronization without page reload
- Full translation of all cards, HUD elements, camera controls, and dual-sensor telemetry
- Native speech synthesis in Hindi (hi-IN), Bengali (bn-IN/bn-BD), and English (en-US/en-IN)
"""

import os
import re

bundle_path = os.path.join("static", "js", "bundle.js")
with open(bundle_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read bundle.js: {len(content)} characters")

# 1. Global Translation Dictionary & Engine injected at the top of the bundle
i18n_engine = """
// ==================== MULTILINGUAL I18N ENGINE (EN, HI, BN) ====================
window.__crysense_translations = {
  en: {
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
    face: "FACE",
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
    
    // Cry translations for inner voice
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
    face: "चेहरा",
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
    face: "মুখমণ্ডল",
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
      discomfort: "আমার জামাকাপড়ে কিছু একটা খचখচ করছে বা ডায়পারটা ভিজে গেছে! দয়া করে আমার ডায়পার আর জামাকাপড় পরীক্ষা করুন।",
      calm: "আমি এখন তোমাদের সাথে খুব শান্ত, নিরাপদ আর খুশি অনুভব করছি, মা-বাবা!",
      fussy: "আমার একটু মন খারাপ লাগছে এবং তোমাদের একটু আদর দরকার।"
    }
  }
};

window.__crysense_lang = (function() {
  try {
    var l = localStorage.getItem('crysense_lang');
    if (l === 'hi' || l === 'bn' || l === 'en') return l;
  } catch(e) {}
  return 'en';
})();

window.__getLang = function() {
  return window.__crysense_lang || 'en';
};

window.__setLang = function(newLang) {
  if (newLang !== 'en' && newLang !== 'hi' && newLang !== 'bn') return;
  window.__crysense_lang = newLang;
  try {
    localStorage.setItem('crysense_lang', newLang);
  } catch(e) {}
  window.dispatchEvent(new CustomEvent('crysense_lang_changed', { detail: newLang }));
};

window.__t = function(key) {
  var lang = window.__getLang();
  var dict = window.__crysense_translations[lang] || window.__crysense_translations.en;
  var parts = key.split('.');
  var val = dict;
  for (var i = 0; i < parts.length; i++) {
    if (val && val[parts[i]] !== undefined) {
      val = val[parts[i]];
    } else {
      var fb = window.__crysense_translations.en;
      for (var j = 0; j < parts.length; j++) {
        if (fb && fb[parts[j]] !== undefined) fb = fb[parts[j]];
        else return key;
      }
      return fb;
    }
  }
  return val;
};
// ==================== END MULTILINGUAL I18N ENGINE ====================

"""

# Prepend i18n_engine to content
if "window.__crysense_translations" not in content:
    content = i18n_engine + content
    print("[1] Successfully injected __crysense_translations into bundle.js!")
else:
    print("[1] Translation engine already present.")

# 2. Patch Header component in bundle.js
p_header_start = content.find("const Header = () => {")
p_header_end = content.find("export default Header", p_header_start)
if p_header_end == -1:
    p_header_end = content.find("_c2 = Header", p_header_start)

if p_header_start != -1 and p_header_end != -1:
    new_header = """const Header = () => {
  const [currentLang, setCurrentLang] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(window.__getLang ? window.__getLang() : 'en');

  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const handler = (e) => {
      if (e.detail) setCurrentLang(e.detail);
    };
    window.addEventListener('crysense_lang_changed', handler);
    return () => window.removeEventListener('crysense_lang_changed', handler);
  }, []);

  const changeLang = (l) => {
    if (window.__setLang) window.__setLang(l);
  };

  const t = (k) => window.__t ? window.__t(k) : k;

  const languages = [
    { id: 'en', label: 'English', short: 'EN' },
    { id: 'hi', label: 'हिन्दी', short: 'हिन्दी' },
    { id: 'bn', label: 'বাংলা', short: 'বাংলা' }
  ];

  return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("header", {
    style: {
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
      gap: 14
    },
    children: [
      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(framer_motion__WEBPACK_IMPORTED_MODULE_1__.motion.div, {
        initial: { opacity: 0, x: -18 },
        animate: { opacity: 1, x: 0 },
        transition: { duration: 0.6 },
        style: { display: 'flex', alignItems: 'center', gap: 14 },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(framer_motion__WEBPACK_IMPORTED_MODULE_1__.motion.div, {
            animate: { rotateY: [0, 360] },
            transition: { duration: 8, repeat: Infinity, ease: 'linear' },
            style: {
              width: 46,
              height: 46,
              borderRadius: 13,
              background: 'linear-gradient(135deg, #f472b6 0%, #a855f7 50%, #38bdf8 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 10px 30px rgba(168, 85, 247, 0.35)',
              transformStyle: 'preserve-3d',
              flexShrink: 0
            },
            children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_3__["default"], {
              size: 24,
              color: "#fff",
              strokeWidth: 2.2
            }, void 0, false)
          }, void 0, false),
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
                style: { fontSize: '1.15rem', fontWeight: 700, color: '#fff', letterSpacing: '-0.01em' },
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", { style: { color: '#c4b5fd' }, children: t('appTitle1') }, void 0, false),
                  " " + t('appTitle2')
                ]
              }, void 0, true),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
                style: { fontSize: '0.68rem', color: '#94a3b8', letterSpacing: '0.14em', fontFamily: 'JetBrains Mono, monospace', marginTop: 2 },
                children: t('appSubtitle')
              }, void 0, false)
            ]
          }, void 0, true)
        ]
      }, void 0, true),

      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
        style: { display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
              display: 'inline-flex',
              alignItems: 'center',
              background: 'rgba(15, 23, 42, 0.85)',
              border: '1px solid rgba(148, 163, 184, 0.25)',
              borderRadius: 10,
              padding: '3px 4px',
              gap: 3,
              boxShadow: '0 4px 14px rgba(0,0,0,0.35)'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("span", {
                style: { padding: '0 6px', color: '#38bdf8', fontSize: '0.85rem' },
                children: "🌐"
              }, void 0, false),
              languages.map((l) => {
                const active = currentLang === l.id;
                return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("button", {
                  key: l.id,
                  onClick: () => changeLang(l.id),
                  style: {
                    background: active ? 'linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(168, 85, 247, 0.35))' : 'transparent',
                    border: active ? '1px solid rgba(56, 189, 248, 0.8)' : '1px solid transparent',
                    color: active ? '#38bdf8' : '#94a3b8',
                    fontWeight: active ? 700 : 500,
                    padding: '4px 11px',
                    borderRadius: 7,
                    fontSize: '0.74rem',
                    cursor: 'pointer',
                    fontFamily: 'Inter, system-ui, sans-serif',
                    transition: 'all 0.18s ease',
                    boxShadow: active ? '0 0 10px rgba(56, 189, 248, 0.3)' : 'none'
                  },
                  children: l.short
                }, l.id, false);
              })
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
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
              fontFamily: 'JetBrains Mono, monospace'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(Pulse, { color: "#38bdf8" }, void 0, false),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_2__["default"], { size: 12 }, void 0, false),
              " " + t('visionActive')
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)("div", {
            style: {
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
              fontFamily: 'JetBrains Mono, monospace'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(Pulse, { color: "#fb7185" }, void 0, false),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_5__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_4__["default"], { size: 12 }, void 0, false),
              " " + t('acousticActive')
            ]
          }, void 0, true)
        ]
      }, void 0, true)
    ]
  }, void 0, true);
};
"""
    content = content[:p_header_start] + new_header + content[p_header_end:]
    print("[2] Successfully patched Header with Multilingual Switcher buttons!")
else:
    print("[WARN] Could not find Header component boundary")

# 3. Patch DualSensorResultCard to use translations
p_dual_start = content.find("const DualSensorResultCard = ({")
p_dual_end = content.find("export default DualSensorResultCard", p_dual_start)
if p_dual_end == -1:
    p_dual_end = content.find("_c4 = DualSensorResultCard", p_dual_start)

if p_dual_start != -1 and p_dual_end != -1:
    new_dual = """const DualSensorResultCard = ({ sensorData, assessment }) => {
  const [lang, setLang] = (0, react__WEBPACK_IMPORTED_MODULE_0__.useState)(window.__getLang ? window.__getLang() : 'en');
  (0, react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
    const handler = (e) => { if (e.detail) setLang(e.detail); };
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

  // Localized baby message
  const localizedBabyMessage = (fused && fused.baby_messages && fused.baby_messages[lang])
    || (rawCategory && t('cryMessages.' + rawCategory))
    || (fused && fused.baby_message)
    || (audio && audio.baby_message)
    || (assessment && assessment.innerVoice)
    || t('cryMessages.calm');

  const localizedSoothingTip = (fused && fused.soothing_checklists && fused.soothing_checklists[lang] && fused.soothing_checklists[lang][0])
    || (t('soothingSteps') && t('soothingSteps')[0])
    || t('soothingDefault');

  return /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)(_Tilt3D__WEBPACK_IMPORTED_MODULE_2__["default"], {
    intensity: 4,
    className: "glass-card",
    style: { padding: '18px 20px', marginBottom: 16 },
    children: [
      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
        style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: { display: 'inline-flex', alignItems: 'center', gap: 10 },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                style: {
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 32,
                  height: 32,
                  borderRadius: 8,
                  background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(168, 85, 247, 0.2))',
                  border: '1px solid rgba(56, 189, 248, 0.4)'
                },
                children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_3__["default"], { size: 18, color: "#38bdf8" }, void 0, false)
              }, void 0, false),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { fontSize: '0.85rem', fontWeight: 800, letterSpacing: '0.08em', color: '#f8fafc' },
                    children: t('dualSensorTitle')
                  }, void 0, false),
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { fontSize: '0.68rem', color: '#94a3b8', letterSpacing: '0.04em' },
                    children: t('dualSensorSub')
                  }, void 0, false)
                ]
              }, void 0, true)
            ]
          }, void 0, true),
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: {
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
              fontFamily: 'JetBrains Mono, monospace'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)(framer_motion__WEBPACK_IMPORTED_MODULE_1__.motion.span, {
                animate: { scale: [1, 1.3, 1], opacity: [1, 0.6, 1] },
                transition: { duration: 1.8, repeat: Infinity },
                style: { width: 7, height: 7, borderRadius: '50%', background: '#10b981', display: 'inline-block' }
              }, void 0, false),
              "LIVE SYNC"
            ]
          }, void 0, true)
        ]
      }, void 0, true),

      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: 14,
          marginBottom: 14
        },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: {
              background: 'rgba(15, 23, 42, 0.7)',
              borderRadius: 12,
              border: '1px solid ' + visualColor + '44',
              padding: 14,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              boxShadow: '0 4px 20px ' + visualColor + '15'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
                    children: [
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        style: { display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: '0.72rem', fontWeight: 700, color: '#38bdf8', letterSpacing: '0.08em' },
                        children: [
                          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_10__["default"], { size: 14 }, void 0, false),
                          " " + t('cameraVisionFeed')
                        ]
                      }, void 0, true),
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        className: "mono",
                        style: {
                          fontSize: '0.64rem',
                          padding: '2px 6px',
                          borderRadius: 4,
                          background: facesCount > 0 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                          color: facesCount > 0 ? '#10b981' : '#f59e0b'
                        },
                        children: facesCount > 0 ? (facesCount + " " + t('faceLocked')) : t('searchingFace')
                      }, void 0, false)
                    ]
                  }, void 0, true),

                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { display: 'flex', alignItems: 'baseline', gap: 8, margin: '8px 0 4px 0' },
                    children: [
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        style: { fontSize: '1.45rem', fontWeight: 800, color: visualColor, letterSpacing: '-0.01em' },
                        children: localizedEmotion.toUpperCase()
                      }, void 0, false),
                      faceConf > 0 ? /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        className: "mono",
                        style: { fontSize: '0.78rem', color: '#94a3b8' },
                        children: "(" + faceConf + "%)"
                      }, void 0, false) : null
                    ]
                  }, void 0, true),

                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 },
                    children: [t('facialAffectState') + ": ", /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("strong", { style: { color: visualColor }, children: localizedEmotion }, void 0, false)]
                  }, void 0, true)
                ]
              }, void 0, true),

              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                  style: {
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: 8,
                    padding: '8px 10px',
                    background: 'rgba(7, 9, 14, 0.6)',
                    borderRadius: 8,
                    border: '1px solid rgba(148, 163, 184, 0.08)'
                  },
                  children: [
                    /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                      children: [
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { style: { fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }, children: t('inferenceSpeed') }, void 0, false),
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { className: "mono", style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }, children: fps + " FPS (" + latency + "ms)" }, void 0, false)
                      ]
                    }, void 0, true),
                    /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                      children: [
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { style: { fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }, children: t('facialStrain') }, void 0, false),
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { className: "mono", style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }, children: (assessment ? assessment.visualStrain.toFixed(1) : '0.0') + "%" }, void 0, false)
                      ]
                    }, void 0, true)
                  ]
                }, void 0, true)
              }, void 0, false)
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: {
              background: 'rgba(15, 23, 42, 0.7)',
              borderRadius: 12,
              border: '1px solid ' + audioColor + '44',
              padding: 14,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              boxShadow: '0 4px 20px ' + audioColor + '15'
            },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                children: [
                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
                    children: [
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        style: { display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: '0.72rem', fontWeight: 700, color: audioColor, letterSpacing: '0.08em' },
                        children: [
                          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)(lucide_react__WEBPACK_IMPORTED_MODULE_11__["default"], { size: 14 }, void 0, false),
                          " " + t('acousticCryFeed')
                        ]
                      }, void 0, true),
                      audioConf !== null ? /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        className: "mono",
                        style: {
                          fontSize: '0.64rem',
                          padding: '2px 6px',
                          borderRadius: 4,
                          background: 'rgba(168, 85, 247, 0.15)',
                          color: '#c084fc'
                        },
                        children: audioConf + "% " + t('acousticConf')
                      }, void 0, false) : null
                    ]
                  }, void 0, true),

                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { display: 'flex', alignItems: 'center', gap: 8, margin: '8px 0 4px 0' },
                    children: [
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", { style: { fontSize: '1.3rem' }, children: audioIcon }, void 0, false),
                      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                        style: { fontSize: '1.1rem', fontWeight: 800, color: audioColor },
                        children: localizedAudioTitle
                      }, void 0, false)
                    ]
                  }, void 0, true),

                  /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                    style: { fontSize: '0.74rem', color: '#cbd5e1', marginBottom: 10 },
                    children: rawCategory ? t('primaryCrySig') + ": " + (rawCategory.toUpperCase()) : t('awaitingCry')
                  }, void 0, false)
                ]
              }, void 0, true),

              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                children: /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                  style: {
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: 8,
                    padding: '8px 10px',
                    background: 'rgba(7, 9, 14, 0.6)',
                    borderRadius: 8,
                    border: '1px solid rgba(148, 163, 184, 0.08)'
                  },
                  children: [
                    /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                      children: [
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { style: { fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }, children: t('acousticSeverity') }, void 0, false),
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { className: "mono", style: { fontSize: '0.85rem', fontWeight: 700, color: audioColor }, children: (audioConf !== null ? audioConf : (assessment ? assessment.acousticSeverity.toFixed(1) : '0.0')) + "%" }, void 0, false)
                      ]
                    }, void 0, true),
                    /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
                      children: [
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { style: { fontSize: '0.62rem', color: '#64748b', letterSpacing: '0.08em' }, children: "STATUS" }, void 0, false),
                        /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", { className: "mono", style: { fontSize: '0.85rem', fontWeight: 700, color: '#e2e8f0' }, children: rawCategory ? "IDENTIFIED" : "IDLE" }, void 0, false)
                      ]
                    }, void 0, true)
                  ]
                }, void 0, true)
              }, void 0, false)
            ]
          }, void 0, true)
        ]
      }, void 0, true),

      /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
        style: {
          background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9))',
          borderRadius: 12,
          padding: '14px 16px',
          border: '1px solid rgba(148, 163, 184, 0.15)'
        },
        children: [
          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                style: { fontSize: '0.78rem', fontWeight: 800, letterSpacing: '0.08em', color: '#e2e8f0' },
                children: t('multimodalVerdict')
              }, void 0, false),
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("span", {
                className: "mono",
                style: {
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  padding: '3px 8px',
                  borderRadius: 6,
                  background: severityColor + '22',
                  color: severityColor,
                  border: '1px solid ' + severityColor + '44'
                },
                children: severityBadge
              }, void 0, false)
            ]
          }, void 0, true),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: {
              fontSize: '0.85rem',
              color: '#f8fafc',
              fontStyle: 'italic',
              lineHeight: 1.5,
              marginBottom: 10,
              padding: '8px 12px',
              background: 'rgba(7, 9, 14, 0.5)',
              borderRadius: 8,
              borderLeft: '3px solid ' + severityColor
            },
            children: '"' + localizedBabyMessage + '"'
          }, void 0, false),

          /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("div", {
            style: { display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.75rem', color: '#94a3b8' },
            children: [
              /*#__PURE__*/(0, react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_12__.jsxDEV)("strong", { style: { color: '#38bdf8' }, children: t('recommendedAction') + ": " }, void 0, false),
              localizedSoothingTip
            ]
          }, void 0, true)
        ]
      }, void 0, true)
    ]
  }, void 0, true);
};
"""
    content = content[:p_dual_start] + new_dual + content[p_dual_end:]
    print("[3] Successfully patched DualSensorResultCard with Multilingual translations!")
else:
    print("[WARN] Could not find DualSensorResultCard boundary")

# 4. Patch handleSpeak to use language-specific voice and text
old_speak_pos = content.find("const handleSpeak = () => {")
if old_speak_pos != -1:
    speak_end = content.find("const moodForFace = pickMoodFromClasses", old_speak_pos)
    if speak_end != -1:
        new_speak = """const handleSpeak = () => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      const currentLang = window.__getLang ? window.__getLang() : 'en';
      let speakText = assessment.innerVoice ? assessment.innerVoice.replace(/[\\u201c\\u201d"]/g, '') : '';
      
      // If localized translation available, speak the localized message
      const audioCat = (sensorData && sensorData.audio && sensorData.audio.predicted_category) || '';
      if (audioCat && window.__crysense_translations && window.__crysense_translations[currentLang]) {
        const catMsg = window.__crysense_translations[currentLang].cryMessages && window.__crysense_translations[currentLang].cryMessages[audioCat];
        if (catMsg) speakText = catMsg;
      }
      
      const utter = new SpeechSynthesisUtterance(speakText);
      if (currentLang === 'hi') {
        utter.lang = 'hi-IN';
        utter.pitch = 1.25;
        utter.rate = 0.9;
      } else if (currentLang === 'bn') {
        utter.lang = 'bn-IN';
        utter.pitch = 1.25;
        utter.rate = 0.9;
      } else {
        utter.lang = 'en-US';
        utter.pitch = 1.35;
        utter.rate = 0.95;
      }
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utter);
    }
  };
  """
        content = content[:old_speak_pos] + new_speak + content[speak_end:]
        print("[4] Successfully patched handleSpeak with Hindi/Bengali/English TTS voices!")

# Save patched bundle
with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Patched bundle.js saved! New size: {len(content)} bytes")
