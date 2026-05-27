"""AI Reel Agent v5.0 — Voice Engine
Premium voice engine: ElevenLabs → edge-tts fallback.
Topic-aware delivery, FFmpeg mastering, perfect subtitle sync.
"""
import asyncio
import json
import os
import random
import re
import shutil
import subprocess

import edge_tts

from config.profiles import (
    VOICE_PROFILES, HIGHLIGHT_WORDS,
    ELEVENLABS_VOICES, ELEVENLABS_MODEL,
    AUDIO_MASTER_FILTER,
)
from config.scripts import get_random_script, detect_topic
from config.defaults import DEFAULT_CONFIG

# Optional ElevenLabs import
_ELEVEN_AVAILABLE = False
_eleven_client = None


def _init_elevenlabs(api_key):
    """Initialize ElevenLabs client if API key is available."""
    global _ELEVEN_AVAILABLE, _eleven_client
    if api_key:
        try:
            from elevenlabs.client import ElevenLabs
            _eleven_client = ElevenLabs(api_key=api_key)
            _ELEVEN_AVAILABLE = True
        except ImportError:
            pass


class VoiceEngine:
    """Topic-aware voice generation with multi-tier fallback."""

    def __init__(self, config, on_progress=None):
        self.config = config
        self.on_progress = on_progress or (lambda *a: None)
        self._ffmpeg = config.get_ffmpeg_path()
        self._voices_dir = config.get_dir("voices")
        self._temp_dir = config.get_dir("temp")
        self._wpc = config.get("caption.words_per_chunk", DEFAULT_CONFIG["caption"]["words_per_chunk"])

        # Init ElevenLabs if key present
        api_key = config.get("api.elevenlabs_key", "")
        if api_key and not _ELEVEN_AVAILABLE:
            _init_elevenlabs(api_key)

    async def generate(self, script=None, topic=None, output_name=None):
        """
        Generate a high-quality voiceover with topic-aware delivery.
        Returns dict with audio_path, subtitle_data, script, voice, topic, profile.
        """
        if script is None:
            entry = get_random_script()
            script = entry["text"]
            topic = entry.get("topic")
        if topic is None:
            topic = detect_topic(script)
        if output_name is None:
            output_name = f"voice_{random.randint(100000, 999999)}"

        profile = VOICE_PROFILES.get(topic, VOICE_PROFILES["_default"])
        profile_name = profile["style"]
        self.on_progress("voice", 0.1, f"Topic: {topic} → {profile_name}")

        raw_path   = os.path.join(self._temp_dir, f"{output_name}_raw.mp3")
        final_path = os.path.join(self._voices_dir, f"{output_name}.mp3")
        subs_path  = os.path.join(self._temp_dir, f"{output_name}_subs.json")

        voice_used = "unknown"
        all_words  = []
        audio_ok   = False

        # Tier 1: ElevenLabs (if available)
        if _ELEVEN_AVAILABLE:
            try:
                from elevenlabs import save as eleven_save
                eleven_voice = profile.get("eleven_voice", "narrator_male")
                voice_id = ELEVENLABS_VOICES.get(eleven_voice, ELEVENLABS_VOICES["narrator_male"])
                self.on_progress("voice", 0.2, f"ElevenLabs ({eleven_voice})")

                audio_gen = _eleven_client.generate(
                    text=script, voice=voice_id,
                    model=ELEVENLABS_MODEL,
                )
                eleven_save(audio_gen, raw_path)

                if os.path.exists(raw_path) and os.path.getsize(raw_path) > 500:
                    voice_used = f"ElevenLabs:{eleven_voice}"
                    audio_ok = True
            except Exception:
                pass

        # Tier 2: edge-tts two-pass (hook + body)
        if not audio_ok:
            self.on_progress("voice", 0.3, "edge-tts generation")
            voice_used, all_words, audio_ok = await self._edgetts_generate(
                script, profile, output_name, raw_path,
            )

        if not audio_ok:
            raise RuntimeError("All voice generation attempts failed.")

        # Audio mastering
        self.on_progress("voice", 0.7, "Audio mastering")
        self._master_audio(raw_path, final_path)

        # Build subtitle phrases
        self.on_progress("voice", 0.85, "Building subtitle phrases")
        if all_words:
            phrases = self._build_phrases_from_words(all_words, self._wpc)
        else:
            audio_dur = self._get_audio_duration(final_path)
            if audio_dur <= 0:
                audio_dur = self._get_audio_duration(raw_path)
            if audio_dur > 0:
                phrases = self._build_phrases_from_duration(script, audio_dur, self._wpc)
            else:
                phrases = self._build_phrases_fallback(script, self._wpc)

        with open(subs_path, "w", encoding="utf-8") as f:
            json.dump(phrases, f, indent=2, ensure_ascii=False)

        self.on_progress("voice", 1.0, f"Done — {len(phrases)} subtitle chunks")

        return {
            "audio_path": final_path,
            "subtitle_data": phrases,
            "script": script,
            "voice": voice_used,
            "topic": topic,
            "profile": profile_name,
        }

    # ── Edge-TTS Engine ────────────────────────────────────────────

    async def _edgetts_generate(self, script, profile, output_name, raw_path):
        available_voices = list(profile["voices"])
        random.shuffle(available_voices)
        hook_text, body_text = self._split_hook_body(script)

        hook_path = os.path.join(self._temp_dir, f"{output_name}_hook.mp3")
        body_path = os.path.join(self._temp_dir, f"{output_name}_body.mp3")

        voice_used = available_voices[0]
        all_words  = []

        # Two-pass attempt
        for attempt, voice in enumerate(available_voices):
            self.on_progress("voice", 0.4, f"edge-tts → {voice.split('-')[-1].replace('Neural', '')}")
            try:
                hw, hb = await self._generate_segment(
                    hook_text, voice,
                    rate=profile["hook_rate"], pitch=profile["hook_pitch"],
                    output_path=hook_path,
                )
                if hb < 500:
                    continue

                bw, bb = [], 0
                if body_text.strip():
                    bw, bb = await self._generate_segment(
                        body_text, voice,
                        rate=profile["rate"], pitch=profile["pitch"],
                        output_path=body_path,
                    )

                if bb > 100 and os.path.exists(body_path):
                    self._concat_audio(hook_path, body_path, raw_path)
                    hook_dur = self._get_audio_duration(hook_path)
                    for w in bw:
                        w["start"] += hook_dur
                        w["end"]   += hook_dur
                    all_words = hw + bw
                else:
                    shutil.copy2(hook_path, raw_path)
                    all_words = hw

                voice_used = voice
                self.on_progress("voice", 0.6, "Two-pass OK")
                return voice_used, all_words, True

            except Exception:
                pass

        # Single-pass fallback
        self.on_progress("voice", 0.5, "Single-pass fallback")
        clean = script.replace("...", ".").replace("..", ".")
        fallback = list(available_voices)
        if "en-US-ChristopherNeural" not in fallback:
            fallback.insert(0, "en-US-ChristopherNeural")

        for fv in fallback:
            try:
                sw, sb = await self._generate_segment(
                    clean, fv, rate="+8%", pitch="+0Hz",
                    output_path=raw_path,
                )
                if sb > 500:
                    return fv, sw, True
            except Exception:
                pass

        return voice_used, [], False

    # ── Internal Helpers ──────────────────────────────────────────

    @staticmethod
    def _split_hook_body(script):
        parts = re.split(r'(?<=[.!?])\s+', script.strip())
        if not parts:
            return script, ""
        hook = parts[0]
        if len(hook.split()) < 8 and len(parts) > 1:
            hook = parts[0] + " " + parts[1]
            body = " ".join(parts[2:])
        else:
            body = " ".join(parts[1:])
        return hook.strip(), body.strip()

    @staticmethod
    async def _generate_segment(text, voice, rate, pitch, output_path):
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
        word_data = []
        audio_bytes = 0
        with open(output_path, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                    audio_bytes += len(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    offset = chunk["offset"] / 10_000_000
                    dur    = chunk["duration"] / 10_000_000
                    word_data.append({"text": chunk["text"], "start": offset, "end": offset + dur})
        return word_data, audio_bytes

    def _concat_audio(self, a, b, out):
        lst = out + ".txt"
        with open(lst, "w") as f:
            f.write(f"file '{a}'\nfile '{b}'\n")
        subprocess.run([self._ffmpeg, "-y", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", out], capture_output=True)
        try:
            os.remove(lst)
        except OSError:
            pass

    def _get_audio_duration(self, path):
        if not os.path.exists(path):
            return 0
        r = subprocess.run([self._ffmpeg, "-i", path, "-f", "null", "-"],
                           capture_output=True, text=True)
        for line in r.stderr.split("\n"):
            if "Duration:" in line:
                p = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = p.split(":")
                return float(h)*3600 + float(m)*60 + float(s)
        return 0

    def _master_audio(self, inp, out):
        r = subprocess.run([
            self._ffmpeg, "-y", "-i", inp,
            "-af", AUDIO_MASTER_FILTER,
            "-ar", "44100", "-b:a", "192k", out,
        ], capture_output=True, text=True)

        if r.returncode != 0:
            r2 = subprocess.run([
                self._ffmpeg, "-y", "-i", inp,
                "-af", "loudnorm=I=-14:TP=-1:LRA=11",
                "-ar", "44100", "-b:a", "192k", out,
            ], capture_output=True, text=True)
            if r2.returncode != 0:
                shutil.copy2(inp, out)

    # ── Subtitle Phrase Builders ──────────────────────────────────

    @staticmethod
    def _build_phrases_from_words(word_data, default_wpc=3):
        phrases = []
        i = 0
        while i < len(word_data):
            if word_data[i]["start"] < 3.0:
                wpc = random.choice([1, 2])
            else:
                wpc = default_wpc
            chunk = word_data[i:i+wpc]
            i += wpc
            text = " ".join(w["text"] for w in chunk).upper()
            has_hl = any(w["text"].strip(".,!?;:'\"").upper() in HIGHLIGHT_WORDS for w in chunk)
            phrases.append({
                "text": text,
                "start": round(chunk[0]["start"], 3),
                "end":   round(chunk[-1]["end"], 3),
                "highlight": has_hl,
            })
        return phrases

    @staticmethod
    def _build_phrases_from_duration(script, duration, default_wpc=3):
        clean = script.replace("...", " ").replace("..", " ")
        words = clean.split()
        if not words:
            return []
        tpw = (duration * 0.95) / len(words)
        gap = 0.03
        phrases = []
        t = 0.1
        i = 0
        while i < len(words):
            if t < 3.0:
                wpc = random.choice([1, 2])
            else:
                wpc = default_wpc
            chunk = words[i:i+wpc]
            i += wpc
            text = " ".join(chunk).upper()
            dur  = len(chunk) * tpw
            has_hl = any(w.strip(".,!?;:'\"").upper() in HIGHLIGHT_WORDS for w in chunk)
            phrases.append({"text": text, "start": round(t, 3),
                            "end": round(t + dur, 3), "highlight": has_hl})
            t += dur + gap
        return phrases

    @staticmethod
    def _build_phrases_fallback(script, default_wpc=3):
        words = script.split()
        tpw = 0.35
        phrases = []
        i = 0
        t = 0
        while i < len(words):
            if t < 3.0:
                wpc = random.choice([1, 2])
            else:
                wpc = default_wpc
            chunk = words[i:i+wpc]
            i += wpc
            text = " ".join(chunk).upper()
            has_hl = any(w.strip(".,!?;:'\"").upper() in HIGHLIGHT_WORDS for w in chunk)
            phrases.append({"text": text, "start": round(t, 3),
                            "end": round(t + (len(chunk)*tpw), 3), "highlight": has_hl})
            t += len(chunk) * tpw
        return phrases

    def is_elevenlabs_available(self) -> bool:
        return _ELEVEN_AVAILABLE
