"""
AI Reel Agent v5.0 — Profiles & Presets
Voice profiles, animation presets, render styles, music synthesis parameters.
Extracted from legacy config.py — all values preserved exactly.
"""

# ══════════════════════════════════════════════════════════════════
#  SUBTITLE ANIMATION PRESETS
# ══════════════════════════════════════════════════════════════════

ANIMATION_PRESETS = [
    {"name": "hard_snap",      "fade_in": (15, 40),  "fade_out": (15, 35),  "scale_up": (118, 135), "scale_time": (35, 65)},
    {"name": "pop_punch",      "fade_in": (50, 90),  "fade_out": (35, 70),  "scale_up": (108, 120), "scale_time": (55, 90)},
    {"name": "slam",           "fade_in": (10, 25),  "fade_out": (10, 20),  "scale_up": (125, 145), "scale_time": (25, 50)},
    {"name": "smooth_breathe", "fade_in": (80, 130), "fade_out": (60, 100), "scale_up": (104, 112), "scale_time": (90, 140)},
    {"name": "luxury_fade",    "fade_in": (120, 180),"fade_out": (100, 150),"scale_up": (102, 108), "scale_time": (120, 200)},
    {"name": "bouncy_pop",     "fade_in": (15, 30),  "fade_out": (15, 30),  "scale_up": (125, 140), "scale_time": (30, 45)},
    {"name": "kinetic_whip",   "fade_in": (10, 20),  "fade_out": (10, 20),  "scale_up": (115, 125), "scale_time": (20, 30)},
]

# ══════════════════════════════════════════════════════════════════
#  HIGHLIGHT WORDS — Trigger highlight styling in subtitles
# ══════════════════════════════════════════════════════════════════

HIGHLIGHT_WORDS = {
    "AI", "NEVER", "ALWAYS", "EVERYTHING", "NOBODY", "EVERYONE",
    "REPLACE", "DESTROY", "CREATE", "BUILD", "FUTURE", "SECRET",
    "CRAZY", "INSANE", "SCARY", "MIND", "CHANGE", "CONTROL",
    "STOP", "WAIT", "LISTEN", "WATCH", "NOW", "TODAY",
    "IMPOSSIBLE", "INCREDIBLE", "POWERFUL", "BEHIND", "TRAPPED",
    "MONEY", "RICH", "BROKE", "SLAVE", "FREE", "SYSTEM",
    "DESIGNED", "PURPOSE", "DISTRACTED", "MANIPULATED",
    "COOKED", "DOOMED", "WINNING", "LOSING", "WAKE",
    "MATRIX", "ESCAPE", "RAT", "RACE", "GRIND", "HUSTLE",
    "DISCIPLINE", "WEAK", "STRONG", "AVERAGE", "ELITE",
    "GENERATION", "BRAIN", "ADDICTED", "PROGRAMMED",
    "BILLIONS", "MILLIONS", "REPLACED", "AUTOMATED",
    "DANGEROUS", "SILENT", "INVISIBLE", "HIDDEN",
    "LUXURY", "WEALTH", "EMPIRE", "PRIVATE", "BILLIONAIRE",
    "LAMBO", "YACHT", "PENTHOUSE", "FERRARI", "ROLEX",
    "JET", "MILLION", "DOLLAR", "SUCCESS", "LEGACY",
    "FR", "NGL", "LITERALLY", "WTF", "BRO", "FACTS",
    "OBSESSED", "HACK", "CHEAT", "CODE", "UNFAIR", "ADVANTAGE",
}

# ══════════════════════════════════════════════════════════════════
#  VOICE PROFILES — Topic-aware voice + pacing
# ══════════════════════════════════════════════════════════════════

VOICE_PROFILES = {
    "ai_tech":       {"voices": ["en-US-GuyNeural", "en-US-ChristopherNeural"],
                      "rate": "+8%",  "pitch": "+2Hz",  "hook_rate": "+2%",  "hook_pitch": "+4Hz",
                      "style": "futuristic_intense", "eleven_voice": "narrator_deep"},
    "cybersecurity": {"voices": ["en-US-GuyNeural", "en-US-ChristopherNeural"],
                      "rate": "+5%",  "pitch": "-2Hz",  "hook_rate": "+0%",  "hook_pitch": "-3Hz",
                      "style": "mysterious_smart",   "eleven_voice": "narrator_deep"},
    "motivation":    {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+10%", "pitch": "+3Hz",  "hook_rate": "+5%",  "hook_pitch": "+5Hz",
                      "style": "inspiring_confident", "eleven_voice": "narrator_male"},
    "dark_psych":    {"voices": ["en-US-GuyNeural", "en-US-ChristopherNeural"],
                      "rate": "+3%",  "pitch": "-3Hz",  "hook_rate": "+0%",  "hook_pitch": "-4Hz",
                      "style": "creepy_calm",        "eleven_voice": "narrator_deep"},
    "money":         {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+8%",  "pitch": "+1Hz",  "hook_rate": "+3%",  "hook_pitch": "+3Hz",
                      "style": "deep_emotional",     "eleven_voice": "narrator_male"},
    "society":       {"voices": ["en-US-GuyNeural", "en-US-AndrewNeural"],
                      "rate": "+12%", "pitch": "+2Hz",  "hook_rate": "+8%",  "hook_pitch": "+4Hz",
                      "style": "conversational_fast", "eleven_voice": "narrator_male"},
    "sigma":         {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+5%",  "pitch": "-1Hz",  "hook_rate": "+0%",  "hook_pitch": "-2Hz",
                      "style": "commanding_cold",    "eleven_voice": "narrator_deep"},
    "student":       {"voices": ["en-US-GuyNeural", "en-US-AndrewNeural"],
                      "rate": "+10%", "pitch": "+3Hz",  "hook_rate": "+5%",  "hook_pitch": "+5Hz",
                      "style": "inspiring_confident", "eleven_voice": "narrator_male"},
    "pov":           {"voices": ["en-US-GuyNeural", "en-US-AndrewNeural"],
                      "rate": "+8%",  "pitch": "+1Hz",  "hook_rate": "+3%",  "hook_pitch": "+2Hz",
                      "style": "storytelling_natural","eleven_voice": "narrator_male"},
    "harsh_truth":   {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+6%",  "pitch": "+0Hz",  "hook_rate": "+2%",  "hook_pitch": "+2Hz",
                      "style": "documentary_narrator","eleven_voice": "narrator_deep"},
    "luxury":        {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+3%",  "pitch": "-2Hz",  "hook_rate": "+0%",  "hook_pitch": "-1Hz",
                      "style": "calm_billionaire",   "eleven_voice": "narrator_calm"},
    "sigma_luxury":  {"voices": ["en-US-ChristopherNeural", "en-US-GuyNeural"],
                      "rate": "+5%",  "pitch": "-1Hz",  "hook_rate": "+2%",  "hook_pitch": "-1Hz",
                      "style": "commanding_luxury",  "eleven_voice": "narrator_deep"},
    "_default":      {"voices": ["en-US-GuyNeural", "en-US-ChristopherNeural"],
                      "rate": "+8%",  "pitch": "+1Hz",  "hook_rate": "+3%",  "hook_pitch": "+3Hz",
                      "style": "documentary_narrator","eleven_voice": "narrator_male"},
}

# ══════════════════════════════════════════════════════════════════
#  ELEVENLABS VOICE IDS
# ══════════════════════════════════════════════════════════════════

ELEVENLABS_VOICES = {
    "narrator_male":   "pNInz6obpgDQGcFmaJgB",   # Adam
    "narrator_deep":   "VR6AewLTigWG4xSOukaG",   # Arnold
    "narrator_calm":   "EXAVITQu4vr4xnSDxMaL",   # Bella
}

ELEVENLABS_MODEL = "eleven_multilingual_v2"

# ══════════════════════════════════════════════════════════════════
#  RENDERING PROFILES — Visual style per topic category
# ══════════════════════════════════════════════════════════════════

RENDER_STYLE_MINECRAFT = {
    "contrast":   (1.02, 1.08),
    "saturation": (1.05, 1.18),
    "brightness": (0.0, 0.03),
    "vignette":   (5.0, 8.0),
    "sharpen":    (0.15, 0.35),
    "zoom":       (0.008, 0.018),
}

RENDER_STYLE_LUXURY = {
    "contrast":   (1.06, 1.14),
    "saturation": (0.88, 1.05),
    "brightness": (-0.01, 0.02),
    "vignette":   (3.5, 6.0),
    "sharpen":    (0.2, 0.5),
    "zoom":       (0.005, 0.02),
}

# ══════════════════════════════════════════════════════════════════
#  AMBIENT MUSIC SYNTHESIS — FFmpeg-generated per topic
# ══════════════════════════════════════════════════════════════════

MUSIC_SYNTH_PARAMS = {
    "motivation": {
        "freq1": 261.63, "freq2": 329.63,
        "noise": "pink", "noise_amp": 0.008,
        "hp": 150, "lp": 2000, "sine_vol": 0.012,
        "label": "cinematic_rise",
    },
    "luxury": {
        "freq1": 130.81, "freq2": 196.00,
        "noise": "brown", "noise_amp": 0.005,
        "hp": 60, "lp": 800, "sine_vol": 0.015,
        "label": "luxury_ambient",
    },
    "ai_tech": {
        "freq1": 87.31, "freq2": 123.47,
        "noise": "brown", "noise_amp": 0.010,
        "hp": 40, "lp": 600, "sine_vol": 0.010,
        "label": "cyber_dark",
    },
    "cybersecurity": {
        "freq1": 92.50, "freq2": 130.81,
        "noise": "brown", "noise_amp": 0.012,
        "hp": 50, "lp": 500, "sine_vol": 0.008,
        "label": "cyber_dark",
    },
    "dark_psych": {
        "freq1": 110.00, "freq2": 146.83,
        "noise": "brown", "noise_amp": 0.010,
        "hp": 40, "lp": 700, "sine_vol": 0.010,
        "label": "dark_ambient",
    },
    "money": {
        "freq1": 220.00, "freq2": 261.63,
        "noise": "pink", "noise_amp": 0.006,
        "hp": 100, "lp": 1500, "sine_vol": 0.010,
        "label": "emotional_piano",
    },
    "sigma": {
        "freq1": 65.41, "freq2": 98.00,
        "noise": "brown", "noise_amp": 0.015,
        "hp": 30, "lp": 400, "sine_vol": 0.018,
        "label": "sigma_bass",
    },
    "sigma_luxury": {
        "freq1": 82.41, "freq2": 123.47,
        "noise": "brown", "noise_amp": 0.012,
        "hp": 40, "lp": 500, "sine_vol": 0.015,
        "label": "dark_luxury",
    },
    "_default": {
        "freq1": 196.00, "freq2": 261.63,
        "noise": "pink", "noise_amp": 0.006,
        "hp": 80, "lp": 1200, "sine_vol": 0.010,
        "label": "ambient_pad",
    },
}

MUSIC_MIX_VOLUME = 0.08

# ══════════════════════════════════════════════════════════════════
#  AUDIO MASTERING — FFmpeg filter chain for studio quality
# ══════════════════════════════════════════════════════════════════

AUDIO_MASTER_FILTER = (
    "highpass=f=80,"
    "acompressor=threshold=-18dB:ratio=4:attack=5:release=100:makeup=2dB,"
    "equalizer=f=200:t=q:w=1.0:g=-2,"
    "equalizer=f=3000:t=q:w=1.5:g=4,"
    "equalizer=f=8000:t=q:w=1.5:g=3,"
    "loudnorm=I=-14:TP=-1:LRA=11"
)
