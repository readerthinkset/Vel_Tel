"""VELOCITY TELUGU - language pack, brand and motion design constants."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_DIR = BASE_DIR / "output"
LESSONS_DIR = OUTPUT_DIR / "lessons"
HISTORY_DIR = OUTPUT_DIR / "history"
SCENE_DIR = BASE_DIR / "scene"

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# ---------------------------------------------------------------- brand

BRAND = "VELOCITY TELUGU"
BRAND_LOCKUP_TOP = "VELOCITY"
BRAND_LOCKUP_BOTTOM = "TELUGU"
HANDLE = "@velocitytelugu"
MASCOT_NAME = "Velo"

# ==== LANGUAGE PACK START ====
LANGUAGE = {
    "code": "te",
    "name": "Telugu",
    "native_name": "తెలుగు",
    "history_key": "telugu",
    "english_voice": "en-US-AvaNeural",
    "english_fallback_voice": "en-US-GuyNeural",
    "native_voice": "te-IN-MohanNeural",
    "native_fallback_voice": "te-IN-ShrutiNeural",
    "native_engine": "edge",
    "native_lang_code": "te",
    "english_rate": "-2%",
    "native_rate": "-6%",
    "english_pitch": "+0Hz",
    "native_pitch": "+0Hz",
    "native_label": "తెలుగు",
    "translit_label": "SAY IT LIKE",
    "greeting": "నమస్కారం!",
    "encouragement": "అద్భుతం!",
    "rtl": False,
    "char_tiles": False,
    "script_font": "NotoSansTelugu-Bold.ttf",
}
# ==== LANGUAGE PACK END ====

AI_MODEL = os.getenv("AI_MODEL", "gemini-fast")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

# ---------------------------------------------------------------- timing (seconds)

INTRO_DURATION = 4.0
OUTRO_DURATION = 5.2
EN_CARD_IN = 0.55
GAP_EN_NATIVE = 0.5
NATIVE_CARD_LEAD = 0.35
GAP_BEFORE_REPEAT = 0.8
TAIL_HOLD = 1.4
MAX_REEL_DURATION = 88.0

# ---------------------------------------------------------------- palette

INK = "#3C3C3C"
MUTED = "#8A8A8A"
CREAM = "#FFF8E7"
GREEN = "#58CC02"
GREEN_DARK = "#46A302"
GREEN_DEEP = "#3D8F00"
BLUE = "#1CB0F6"
PURPLE = "#A560E8"
ORANGE = "#FF7A00"
RED = "#FF4B4B"
YELLOW = "#F5A700"
TEAL = "#00A889"
PINK = "#E056A0"

PALETTE = [GREEN, BLUE, PURPLE, ORANGE, RED, YELLOW, TEAL, PINK]

# ---------------------------------------------------------------- categories
# (english, native, icon, accent)

# ==== CATEGORY TABLE START ====
CATEGORY_TABLE = [
    ("Greetings", "పలుకులు", "hand", "#1CB0F6"),
    ("Basic Phrases", "ప్రాథమిక పదబంధాలు", "chat", "#58CC02"),
    ("Common Expressions", "సాధారణ వ్యక్తులు", "chat", "#1CB0F6"),
    ("Travel", "ప్రయాణం", "plane", "#1CB0F6"),
    ("Restaurant", "రెస్టారెంట్", "fork", "#FF7A00"),
    ("Shopping", "షాపింగ్", "bag", "#E056A0"),
    ("Emergency", "అత్యవసరం", "siren", "#FF4B4B"),
    ("Family Terms", "కుటుంబ పదాలు", "heart", "#E056A0"),
    ("Numbers", "సంఖ్యలు", "hash", "#A560E8"),
    ("Time", "సమయం", "clock", "#00A889"),
    ("Motivation", "ప్రేరణ", "rocket", "#A560E8"),
    ("Love", "ప్రేమ", "heart", "#FF4B4B"),
    ("Success", "విజయం", "trophy", "#F5A700"),
    ("Wisdom", "జ్ఞానం", "book", "#A560E8"),
    ("Happiness", "సంతోషం", "smile", "#F5A700"),
    ("Self Improvement", "స్వీయ మెరుగుదల", "leaf", "#58CC02"),
    ("Gratitude", "కృతజ్ఞత", "heart", "#FF7A00"),
    ("Friendship", "స్నేహం", "users", "#00A889"),
    ("Hope", "ఆశ", "sun", "#FF7A00"),
    ("Creativity", "సృజనాత్మకత", "palette", "#E056A0"),
    ("Inner Peace", "అంతర్ శాంతి", "lotus", "#00A889"),
    ("Confidence", "విశ్వాసం", "shield", "#1CB0F6"),
    ("Perseverance", "దృఢత్వం", "mountain", "#FF7A00"),
    ("Inspiration", "స్ఫూర్తి", "sparkles", "#A560E8"),
    ("Positive Life", "సానుకూల జీవితం", "sun", "#58CC02"),
    ("Courage", "ధైర్యం", "shield", "#FF4B4B"),
    ("Kindness", "దయ", "heart", "#E056A0"),
    ("Patience", "ఓపిక", "hourglass", "#00A889"),
    ("Forgiveness", "క్షమాపణ", "hands", "#FF7A00"),
    ("Strength", "బలం", "dumbbell", "#FF4B4B"),
    ("Joy", "ఆనందం", "smile", "#F5A700"),
    ("Balance", "సమతుల్యత", "scale", "#00A889"),
    ("Growth", "వృద్ధి", "sprout", "#58CC02"),
    ("Purpose", "ప్రయోజనం", "target", "#A560E8"),
    ("Mindfulness", "సంపూర్ణ అవగాహన", "lotus", "#00A889"),
]
# ==== CATEGORY TABLE END ====

CATEGORIES = [c[0] for c in CATEGORY_TABLE]
CATEGORIES_NATIVE = {c[0]: c[1] for c in CATEGORY_TABLE}
CATEGORY_META = {c[0]: {"native": c[1], "icon": c[2], "accent": c[3]} for c in CATEGORY_TABLE}
MAX_RECENT_CATEGORIES = 25

# ==== HASHTAGS START ====
HASHTAGS = [
    "#learntelugu",
    "#telugulessons",
    "#teluguforbeginners",
    "#languagelearning",
    "#teluguvocabulary",
    "#velocitytelugu",
    "#dailytelugu",
    "#telugu",
    "#learnlanguages",
    "#speaktelugu",
    "#bilingual",
    "#languagetips",
]
# ==== HASHTAGS END ====
