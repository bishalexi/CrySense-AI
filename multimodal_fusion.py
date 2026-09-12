"""Multimodal Infant Distress Fusion Engine.
Combines visual facial expression/strain signals from Ultra-Light Face Detection
with acoustic vocalization analysis from BabyCry AI into a unified clinical distress profile.
"""

from typing import Dict, Any, Optional


class MultimodalDistressFusion:
    DISTRESS_WEIGHTS = {
        "belly_pain": 0.95,
        "hungry": 0.85,
        "burping": 0.75,
        "discomfort": 0.65,
        "tired": 0.55
    }

    def __init__(self, visual_weight: float = 0.45, audio_weight: float = 0.55):
        self.visual_weight = visual_weight
        self.audio_weight = audio_weight

    def calculate_visual_distress(self, emotion_result: Optional[Dict[str, Any]]) -> float:
        """Derives a normalized distress score [0.0, 1.0] from facial expression probabilities."""
        if not emotion_result or "probabilities" not in emotion_result:
            return 0.2  # Baseline assumption if face is unobserved

        probs = emotion_result["probabilities"]
        
        # Distress contributors
        p_angry = probs.get("Angry", 0.0)      # Facial grimace / crying scowl
        p_sad = probs.get("Sad", 0.0)          # Downward quivering lips / whimpering
        p_fear = probs.get("Fear", 0.0)        # Wide-eyed startled distress
        p_disgust = probs.get("Disgust", 0.0)  # Nasal wrinkling / aversion
        
        # Comfort contributors
        p_happy = probs.get("Happy", 0.0)
        p_neutral = probs.get("Neutral", 0.0)
        
        raw_distress = (
            p_angry * 1.0 +
            p_sad * 0.85 +
            p_fear * 0.80 +
            p_disgust * 0.70 -
            p_happy * 1.0 -
            p_neutral * 0.60
        )
        
        # Map roughly from [-1.0, 1.0] to [0.0, 1.0]
        normalized = (raw_distress + 0.6) / 1.6
        return float(max(0.0, min(1.0, normalized)))

    def calculate_audio_distress(self, cry_result: Optional[Dict[str, Any]]) -> float:
        """Derives a normalized acoustic distress score [0.0, 1.0] from cry classification."""
        if not cry_result:
            return 0.0
            
        category = cry_result.get("predicted_category", "discomfort")
        conf = cry_result.get("confidence", 0.5)
        severity_mult = self.DISTRESS_WEIGHTS.get(category, 0.7)
        
        audio_distress = conf * severity_mult
        return float(max(0.0, min(1.0, audio_distress)))

    def fuse(
        self,
        visual_data: Optional[Dict[str, Any]],
        audio_data: Optional[Dict[str, Any]],
        baby_name: str = "Baby"
    ) -> Dict[str, Any]:
        """Fuses visual and acoustic modalities into a unified distress assessment."""
        v_score = self.calculate_visual_distress(visual_data) if visual_data else None
        a_score = self.calculate_audio_distress(audio_data) if audio_data else None

        # Cross-modal fusion weighting
        if v_score is not None and a_score is not None:
            unified_index = self.visual_weight * v_score + self.audio_weight * a_score
            modality_used = "Bimodal (Face + Acoustic Cry)"
        elif a_score is not None:
            unified_index = a_score
            modality_used = "Acoustic Cry Only"
        elif v_score is not None:
            unified_index = v_score
            modality_used = "Facial Strain Only"
        else:
            unified_index = 0.0
            modality_used = "Awaiting Telemetry"

        unified_pct = round(unified_index * 100.0, 1)

        # Classify Severity Level
        if unified_pct < 25.0:
            severity_label = "Calm & Content"
            severity_color = "#10b981"  # Emerald
            severity_badge = "LOW DISTRESS"
        elif unified_pct < 50.0:
            severity_label = "Mild Discomfort / Fussy"
            severity_color = "#3b82f6"  # Sky Blue
            severity_badge = "MILD DISTRESS"
        elif unified_pct < 75.0:
            severity_label = "Moderate Distress"
            severity_color = "#f59e0b"  # Amber
            severity_badge = "MODERATE DISTRESS"
        else:
            severity_label = "Acute Distress / Colic Spike"
            severity_color = "#ef4444"  # Vivid Red
            severity_badge = "ACUTE DISTRESS"

        # Formulate synthesized clinical cross-modal narrative
        cry_cat = audio_data.get("predicted_category", "neutral") if audio_data else None
        face_emo = visual_data.get("dominant_emotion", "Neutral") if visual_data else None

        if cry_cat and face_emo:
            narrative = (
                f"Acoustic classification identified '{cry_cat.upper()}' ({int((audio_data.get('confidence', 0)*100))}%) "
                f"correlating with facial affective tension '{face_emo.upper()}'."
            )
        elif cry_cat:
            narrative = f"Acoustic classification isolated primary cry signature: '{cry_cat.upper()}'."
        elif face_emo:
            narrative = f"Visual facial detector observing primary affect: '{face_emo.upper()}'."
        else:
            narrative = "Monitoring infant video and audio telemetry in real time."

        # Multilingual Baby perspective translation
        multilingual_msgs = {
            "hungry": {
                "en": "My little tummy is rumbling and feeling so empty! I am super hungry and need some warm milk please.",
                "hi": "मेरा नन्हा पेट खाली है और भूख से गुड़गुड़ा रहा है! मुझे बहुत भूख लगी है, कृपया मुझे थोड़ा गर्म दूध पिलाइए।",
                "bn": "আমার ছোট্ট পেটটা খালি হয়ে গেছে আর খিদে পেয়েছে! আমার খুব খিদে পেয়েছে, দয়া করে আমাকে একটু উষ্ণ দুধ খাওয়ান।"
            },
            "belly_pain": {
                "en": "My little tummy really cramps and hurts inside! I have stubborn gas bubbles. Please bicycle my legs gently and rub my tummy.",
                "hi": "मेरे पेट में मरोड़ और ऐंठन हो रही है! गैस फंसी है। कृपया मेरे पैर साइकिल की तरह चलाएं और पेट की हल्की मालिश करें।",
                "bn": "আমার পেটে মোচড় দিয়ে ব্যথা করছে আর অস্বস্তি হচ্ছে! পেটে হালকা মালিশ আর একটু উষ্ণ সেঁক দিলে খুব আরাম পাব।"
            },
            "burping": {
                "en": "There is a sneaky air bubble trapped in my chest after drinking milk! Please hold me upright over your shoulder and gently pat my back.",
                "hi": "दूध पीने के बाद छाती में एक हवा का बुलबुला फंस गया है! कृपया मुझे कंधे पर सीधा लेकर पीठ थपथपाएं।",
                "bn": "দুধ খাওয়ার পর বুকে একটা বাতাসের বুদ্বুদ আটকে আছে! দয়া করে আমাকে কাঁধের ওপর সোজা করে ধরে পিঠে হালকা চাপড় দিন।"
            },
            "tired": {
                "en": "My eyes are heavy and everything around me is too bright and loud! Please wrap me snugly, dim the lights, and rock me to sleep.",
                "hi": "आसपास बहुत उजाला और शोर है, मेरी पलकें भारी हो रही हैं! कृपया मुझे किसी शांत और मंद कमरे में झुलाकर सुलाएं।",
                "bn": "চারপাশে খুব আওয়াজ আর আলো, আমার চোখ দুটো ভারী হয়ে আসছে! দয়া করে একটি শান্ত আবছা আলোর ঘরে নিয়ে আমাকে একটু দোল দিন যাতে আমি ঘুমাতে পারি।"
            },
            "discomfort": {
                "en": "Something is tickling, pinching, or bothering my sensitive skin! Please check if my diaper is wet or if my clothes are tight.",
                "hi": "मेरे कपड़ों में कुछ चुभ रहा है या मेरा डायपर गीला हो सकता है! कृपया मेरे कपड़े और डायपर जांचें।",
                "bn": "আমার জামাকাপড়ে কিছু একটা খচখচ করছে বা ডায়পারটা ভিজে গেছে! দয়া করে আমার ডায়পার আর জামাকাপড় পরীক্ষা করুন।"
            },
            "calm": {
                "en": "I am feeling calm, peaceful, and comfortable right now with you, Mommy and Daddy!",
                "hi": "मैं इस समय आपके साथ बहुत शांत, सुरक्षित और खुश महसूस कर रहा हूँ, मम्मी-पापा!",
                "bn": "আমি এখন তোমাদের সাথে খুব শান্ত, নিরাপদ আর খুশি অনুভব করছি, মা-বাবা!"
            },
            "fussy": {
                "en": "I am feeling a little fussy right now and need some gentle comfort.",
                "hi": "मुझे थोड़ी परेशानी हो रही है और मुझे आपके प्यार और दुलार की जरूरत है।",
                "bn": "আমার একটু মন খারাপ লাগছে এবং তোমাদের একটু আদর দরকার।"
            }
        }

        multilingual_soothing = {
            "en": [
                "Check diaper comfort and skin temperature.",
                "Offer gentle skin-to-skin holding and rhythmic rocking.",
                "Verify feeding schedule and wake window duration.",
                "Swaddle snugly in a quiet, softly lit nursery environment."
            ],
            "hi": [
                "डायपर का सूखापन और शरीर का तापमान जांचें।",
                "शिशु को सीने से लगाकर रखें और हल्के हाथों से झुलाएं।",
                "दूध पिलाने का समय और जागने का अंतराल जांचें।",
                "शांत और मंद रोशनी वाले कमरे में शिशु को हल्के कपड़े में लपेटें।"
            ],
            "bn": [
                "ডায়পারের আরাম ও শরীরের তাপমাত্রা পরীক্ষা করুন।",
                "কোলে নিয়ে শান্তভাবে ছন্দময়ভাবে দোল দিন।",
                "খাওয়ানোর সময় এবং জেগে থাকার সময়সীমা পরীক্ষা করুন।",
                "একটি শান্ত ও আবছা আলোর ঘরে আরামদায়কভাবে জড়িয়ে রাখুন।"
            ]
        }

        if cry_cat and cry_cat in multilingual_msgs:
            baby_msgs = multilingual_msgs[cry_cat]
        elif face_emo in ["Happy", "Neutral"]:
            baby_msgs = multilingual_msgs["calm"]
        else:
            baby_msgs = multilingual_msgs["fussy"]

        baby_msg = baby_msgs["en"]
        soothing_steps = audio_data.get("soothing_checklist", []) if audio_data else multilingual_soothing["en"]

        return {
            "unified_distress_score": unified_pct,
            "severity_label": severity_label,
            "severity_badge": severity_badge,
            "severity_color": severity_color,
            "modality_used": modality_used,
            "visual_distress_score": round(v_score * 100.0, 1) if v_score is not None else None,
            "audio_distress_score": round(a_score * 100.0, 1) if a_score is not None else None,
            "narrative": narrative,
            "baby_message": baby_msg,
            "baby_messages": baby_msgs,
            "soothing_checklist": soothing_steps,
            "soothing_checklists": multilingual_soothing,
            "audio_category": cry_cat,
            "visual_emotion": face_emo
        }
