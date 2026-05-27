"""
AI Reel Agent v5.0 — Default Configuration Values
All default values extracted from legacy config.py.
"""

# ─── Application Info ─────────────────────────────────────────────
APP_NAME = "AI Reel Agent"
APP_VERSION = "5.0.0"
APP_AUTHOR = "Master Armaan"

# ─── Default Config Dict ─────────────────────────────────────────
DEFAULT_CONFIG = {
    "api": {
        "elevenlabs_key": "",
        "openai_key": "",
    },
    "video": {
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "max_duration": 30,
        "bitrate": "5M",
        "audio_bitrate": "192k",
    },
    "caption": {
        "font_size": 82,
        "outline_width": 7,
        "alignment": 5,
        "margin_v": 180,
        "words_per_chunk": 3,
        "font_name": "Arial Black",
    },
    "music": {
        "mix_volume": 0.08,
        "fade_duration": 3.0,
    },
    "rendering": {
        "tier1_crf": 18,
        "tier1_preset": "medium",
        "tier2_crf": 20,
        "tier2_preset": "fast",
        "tier3_crf": 22,
        "tier3_preset": "fast",
        "pre_scale_factor": 1.5,
        "zoom_in_probability": 0.7,
    },
    "voice": {
        "default_engine": "edge-tts",
        "audio_sample_rate": 44100,
    },
}

# ─── Directory Names ──────────────────────────────────────────────
DIR_NAMES = {
    "videos": "videos",
    "voices": "voices",
    "outputs": "outputs",
    "reels": "reels",
    "temp": "temp",
    "music": "music",
    "fonts": "fonts",
    "logs": "logs",
}
