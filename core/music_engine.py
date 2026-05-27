"""AI Reel Agent v5.0 — Music Engine
FFmpeg-generated ambient music pads per topic.
"""
import os
import random
import subprocess

from config.profiles import MUSIC_SYNTH_PARAMS


class MusicEngine:
    """Generates and caches topic-specific ambient background music."""

    def __init__(self, config):
        self.config = config
        self._ffmpeg = config.get_ffmpeg_path()
        self._music_dir = config.get_dir("music")
        self._temp_dir = config.get_dir("temp")
        self._cache_dir = os.path.join(self._temp_dir, "music_cache")
        os.makedirs(self._cache_dir, exist_ok=True)

    def get_music(self, topic: str, duration: float) -> str:
        """Get background music path. Checks user music → cache → synthesize."""
        user_music = self._find_user_music(topic)
        if user_music:
            return user_music

        cache_path = os.path.join(self._cache_dir, f"ambient_{topic}.mp3")
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
            return cache_path

        params = MUSIC_SYNTH_PARAMS.get(topic, MUSIC_SYNTH_PARAMS["_default"])
        pad_duration = max(duration + 5, 35)
        self._synthesize_ambient(params, pad_duration, cache_path)
        return cache_path

    def _find_user_music(self, topic: str):
        """Look for user-provided music files."""
        exts = (".mp3", ".wav", ".m4a", ".ogg")
        topic_dir = os.path.join(self._music_dir, topic)
        if os.path.isdir(topic_dir):
            files = [f for f in os.listdir(topic_dir) if f.lower().endswith(exts)]
            if files:
                return os.path.join(topic_dir, random.choice(files))
        if os.path.isdir(self._music_dir):
            files = [f for f in os.listdir(self._music_dir)
                     if os.path.isfile(os.path.join(self._music_dir, f))
                     and f.lower().endswith(exts)]
            if files:
                return os.path.join(self._music_dir, random.choice(files))
        return None

    def _synthesize_ambient(self, params, duration, output_path):
        """Generate ambient pad using FFmpeg synthesis."""
        f1, f2 = params["freq1"], params["freq2"]
        nc, na = params["noise"], params["noise_amp"]
        sv = params["sine_vol"]
        hp, lp = params["hp"], params["lp"]
        dur = int(duration)
        fd = min(3, dur // 4)

        fc = (
            f"sine=frequency={f1}:duration={dur}[s1];"
            f"sine=frequency={f2}:duration={dur}[s2];"
            f"anoisesrc=duration={dur}:color={nc}:amplitude={na}[n];"
            f"[s1]volume={sv}[sv1];"
            f"[s2]volume={sv * 0.7}[sv2];"
            f"[n]highpass=f={hp}:poles=2,lowpass=f={lp}:poles=2[nf];"
            f"[sv1][sv2][nf]amix=inputs=3:duration=first,"
            f"afade=t=in:d={fd},afade=t=out:st={dur - fd}:d={fd},"
            f"loudnorm=I=-25:TP=-5:LRA=11[out]"
        )
        subprocess.run([
            self._ffmpeg, "-y", "-filter_complex", fc,
            "-map", "[out]", "-ar", "44100", "-b:a", "128k", output_path,
        ], capture_output=True, text=True)

    def clear_cache(self):
        """Remove all cached music files."""
        if os.path.isdir(self._cache_dir):
            for f in os.listdir(self._cache_dir):
                try:
                    os.remove(os.path.join(self._cache_dir, f))
                except OSError:
                    pass
