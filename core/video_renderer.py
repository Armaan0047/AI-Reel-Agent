"""AI Reel Agent v5.0 — Video Renderer
Multi-style cinematic engine with topic-aware visuals & background music.
3-tier render fallback with validation.
"""
import os
import random
import re
import subprocess
import time

from config.profiles import (
    RENDER_STYLE_MINECRAFT, RENDER_STYLE_LUXURY,
    MUSIC_MIX_VOLUME,
)
from config.scripts import LUXURY_TOPICS
from config.defaults import DEFAULT_CONFIG


class VideoRenderer:
    """3-tier cinematic video rendering engine."""

    def __init__(self, config, subtitle_engine=None, music_engine=None, on_progress=None):
        self.config = config
        self.subtitle_engine = subtitle_engine
        self.music_engine = music_engine
        self.on_progress = on_progress or (lambda *a: None)
        self._ffmpeg = config.get_ffmpeg_path()
        self._videos_dir = config.get_dir("videos")
        self._outputs_dir = config.get_dir("outputs")
        self._reels_dir = config.get_dir("reels")
        self._temp_dir = config.get_dir("temp")

        # Video settings from config
        self._width = config.get("video.width", DEFAULT_CONFIG["video"]["width"])
        self._height = config.get("video.height", DEFAULT_CONFIG["video"]["height"])
        self._fps = config.get("video.fps", DEFAULT_CONFIG["video"]["fps"])
        self._max_dur = config.get("video.max_duration", DEFAULT_CONFIG["video"]["max_duration"])
        self._v_bitrate = config.get("video.bitrate", DEFAULT_CONFIG["video"]["bitrate"])
        self._a_bitrate = config.get("video.audio_bitrate", DEFAULT_CONFIG["video"]["audio_bitrate"])

    def get_random_video(self, topic=None) -> str:
        """Select background video based on topic."""
        is_luxury = topic in LUXURY_TOPICS
        if is_luxury:
            luxury_path = os.path.join(self._videos_dir, "Luxury.mp4")
            if os.path.isfile(luxury_path) and os.path.getsize(luxury_path) > 10_000:
                return luxury_path

        valid = []
        for f in os.listdir(self._videos_dir):
            fp = os.path.join(self._videos_dir, f)
            if (os.path.isfile(fp)
                and f.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm"))
                and not f.lower().endswith(".crswap")
                and os.path.getsize(fp) > 10_000):
                valid.append(fp)
        return random.choice(valid) if valid else None

    @staticmethod
    def is_luxury_topic(topic: str) -> bool:
        return topic in LUXURY_TOPICS

    def render(self, video_path, audio_path, subtitle_data, output_name, topic="motivation"):
        """Render a complete viral reel with 3-tier fallback."""
        luxury = self.is_luxury_topic(topic)
        style = RENDER_STYLE_LUXURY if luxury else RENDER_STYLE_MINECRAFT
        landscape = self._is_landscape(video_path)

        audio_dur = self._get_duration(audio_path)
        if audio_dur <= 0:
            audio_dur = 15
        reel_dur = min(audio_dur + 0.5, self._max_dur)

        video_dur = self._get_duration(video_path)
        max_offset = max(0, video_dur - reel_dur - 5)
        offset = random.uniform(0, max_offset) if max_offset > 0 else 0

        zoom       = round(random.uniform(*style["zoom"]), 4)
        contrast   = round(random.uniform(*style["contrast"]), 2)
        saturation = round(random.uniform(*style["saturation"]), 2)
        brightness = round(random.uniform(*style["brightness"]), 3)
        vignette   = round(random.uniform(*style["vignette"]), 1)
        sharpen    = round(random.uniform(*style["sharpen"]), 2)

        # Use outputs dir (reels/ kept for compat)
        reel_path = os.path.join(self._outputs_dir, f"{output_name}.mp4")
        ass_path  = os.path.join(self._temp_dir, f"{output_name}.ass")

        # Generate subtitles
        self.on_progress("render", 0.1, "Generating subtitles")
        if self.subtitle_engine:
            self.subtitle_engine.generate_ass(subtitle_data, ass_path, is_luxury=luxury)
        
        # Get music
        self.on_progress("render", 0.2, "Preparing music")
        music_path = None
        if self.music_engine:
            music_path = self.music_engine.get_music(topic, reel_dur)

        self.on_progress("render", 0.3, "Starting FFmpeg render")

        # Try rendering tiers with validation
        ok = self._render_tier1(video_path, audio_path, music_path, ass_path,
                               reel_path, reel_dur, offset, zoom,
                               contrast, saturation, brightness, vignette, sharpen,
                               luxury, landscape)

        if ok and not self._validate_render(reel_path):
            ok = False

        if not ok:
            self.on_progress("render", 0.5, "Tier 1 failed → Tier 2")
            ok = self._render_tier2(video_path, audio_path, music_path, ass_path,
                                   reel_path, reel_dur, offset, luxury, landscape)

        if ok and not self._validate_render(reel_path):
            ok = False

        if not ok:
            self.on_progress("render", 0.7, "Tier 2 failed → Tier 3")
            ok = self._render_tier3(video_path, audio_path, reel_path, reel_dur,
                                   offset, landscape)

        if ok:
            size_mb = os.path.getsize(reel_path) / (1024 * 1024)
            self.on_progress("render", 1.0, f"Done — {size_mb:.1f} MB")

        return reel_path if ok else None

    # ── Scaling ────────────────────────────────────────────────────

    def _build_scale_filter(self, w, h, landscape):
        if landscape:
            return f"scale=-2:{h}:flags=lanczos,crop={w}:{h}"
        else:
            return f"scale={w}:-2:flags=lanczos,crop={w}:{h}"

    # ── Render Tiers (ALL FFmpeg filter chains preserved EXACTLY) ─

    def _render_tier1(self, video, audio, music, ass, out, dur, offset,
                     zoom, contrast, sat, bright, vignette, sharpen,
                     luxury, landscape):
        w, h = self._width, self._height
        fps = self._fps
        total_frames = int(dur * fps)
        zoom_per_frame = zoom / total_frames

        zoom_dir = "in" if random.random() < self.config.get("rendering.zoom_in_probability", 0.7) else "out"
        if zoom_dir == "in":
            zexpr = f"1+(on*{zoom_per_frame})"
        else:
            zexpr = f"(1+{zoom})-(on*{zoom_per_frame})"

        pan_x = random.uniform(-1.0, 1.0)
        pan_y = random.uniform(-1.0, 1.0)

        scale_factor = self.config.get("rendering.pre_scale_factor", 1.5)
        sw, sh = int(w * scale_factor), int(h * scale_factor)

        if landscape:
            pre_scale = f"scale=-2:{sh}:flags=lanczos,crop={sw}:{sh}"
        else:
            pre_scale = f"scale={sw}:-2:flags=lanczos,crop={sw}:{sh}"

        xexpr = f"min(max(iw/2-(iw/zoom/2)+(on*{pan_x}),0),iw-iw/zoom)"
        yexpr = f"min(max(ih/2-(ih/zoom/2)+(on*{pan_y}),0),ih-ih/zoom)"

        vf = (
            f"{pre_scale},"
            f"zoompan=z='{zexpr}':x='{xexpr}':y='{yexpr}'"
            f":d=1:s={w}x{h}:fps={fps},"
            f"fps={fps},"
            f"eq=contrast={contrast}:saturation={sat}:brightness={bright},"
            f"unsharp=5:5:{sharpen}:5:5:0,"
            f"vignette=PI/{vignette},"
            f"ass='{self._esc(ass)}'"
        )

        mv = MUSIC_MIX_VOLUME
        af = (
            f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo[voice];"
            f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,"
            f"volume={mv},"
            f"afade=t=in:d=1.5,"
            f"afade=t=out:st={max(0, dur - 2.5)}:d=2.5[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]"
        )

        fc = f"[0:v]{vf}[vout];{af}"

        cmd = [
            self._ffmpeg, "-y",
            "-stream_loop", "-1", "-ss", str(offset), "-i", video,
            "-i", audio,
            "-stream_loop", "-1", "-i", music,
            "-filter_complex", fc,
            "-map", "[vout]", "-map", "[aout]",
            "-t", str(dur),
            "-c:v", "libx264", "-preset", self.config.get("rendering.tier1_preset", "medium"),
            "-crf", str(self.config.get("rendering.tier1_crf", 18)),
            "-b:v", self._v_bitrate, "-maxrate", self._v_bitrate, "-bufsize", "10M",
            "-c:a", "aac", "-b:a", self._a_bitrate,
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            out,
        ]

        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 10_000:
            return True
        if r.stderr:
            err_lines = [l for l in r.stderr.split("\n") if "Error" in l or "error" in l or "Invalid" in l]
            for el in err_lines[:5]:
                self.on_progress("render", 0.3, f"FFmpeg: {el.strip()}")
        return False

    def _render_tier2(self, video, audio, music, ass, out, dur, offset, luxury, landscape):
        w, h = self._width, self._height
        scale = self._build_scale_filter(w, h, landscape)
        vf = f"{scale},fps={self._fps},ass='{self._esc(ass)}'"

        mv = MUSIC_MIX_VOLUME
        af = (
            f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo[voice];"
            f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,"
            f"volume={mv},afade=t=in:d=1,afade=t=out:st={max(0, dur-2)}:d=2[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first[aout]"
        )

        fc = f"[0:v]{vf}[vout];{af}"

        cmd = [
            self._ffmpeg, "-y",
            "-stream_loop", "-1", "-ss", str(offset), "-i", video,
            "-i", audio,
            "-stream_loop", "-1", "-i", music,
            "-filter_complex", fc,
            "-map", "[vout]", "-map", "[aout]",
            "-t", str(dur),
            "-c:v", "libx264", "-preset", self.config.get("rendering.tier2_preset", "fast"),
            "-crf", str(self.config.get("rendering.tier2_crf", 20)),
            "-c:a", "aac", "-b:a", self._a_bitrate,
            "-pix_fmt", "yuv420p", out,
        ]

        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 10_000:
            return True
        if r.stderr:
            err_lines = [l for l in r.stderr.split("\n") if "Error" in l or "error" in l or "Invalid" in l]
            for el in err_lines[:5]:
                self.on_progress("render", 0.5, f"FFmpeg: {el.strip()}")
        return False

    def _render_tier3(self, video, audio, out, dur, offset, landscape):
        w, h = self._width, self._height
        scale = self._build_scale_filter(w, h, landscape)
        vf = f"{scale},fps={self._fps}"
        fc = f"[0:v]{vf}[vout]"

        cmd = [
            self._ffmpeg, "-y",
            "-stream_loop", "-1", "-ss", str(offset), "-i", video,
            "-i", audio,
            "-filter_complex", fc,
            "-map", "[vout]", "-map", "1:a",
            "-t", str(dur),
            "-c:v", "libx264", "-preset", self.config.get("rendering.tier3_preset", "fast"),
            "-crf", str(self.config.get("rendering.tier3_crf", 22)),
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", out,
        ]

        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 10_000:
            return True
        if r.stderr:
            err_lines = [l for l in r.stderr.split("\n") if "Error" in l or "error" in l or "Invalid" in l]
            for el in err_lines[:5]:
                self.on_progress("render", 0.7, f"FFmpeg: {el.strip()}")
        return False

    # ── Validation ────────────────────────────────────────────────

    def _validate_render(self, path):
        if not os.path.exists(path):
            return False
        file_size = os.path.getsize(path)
        if file_size < 50_000:
            return False

        probe_path = path + ".probe.raw"
        cmd = [
            self._ffmpeg, "-y",
            "-ss", "2", "-i", path,
            "-frames:v", "1",
            "-vf", "scale=16:16",
            "-f", "rawvideo", "-pix_fmt", "gray",
            probe_path,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)

        if r.returncode != 0 or not os.path.exists(probe_path):
            return file_size > 200_000

        probe_size = os.path.getsize(probe_path)
        if probe_size == 0:
            self._cleanup(probe_path)
            return False

        with open(probe_path, "rb") as f:
            data = f.read()
        self._cleanup(probe_path)

        avg_brightness = sum(data) / len(data) if data else 0
        return avg_brightness >= 5

    # ── Helpers ────────────────────────────────────────────────────

    def _get_video_dimensions(self, path):
        cmd = [self._ffmpeg, "-i", path]
        r = subprocess.run(cmd, capture_output=True, text=True)
        m = re.search(r'(\d{2,5})x(\d{2,5})', r.stderr)
        if m:
            return int(m.group(1)), int(m.group(2))
        return 0, 0

    def _is_landscape(self, path):
        w, h = self._get_video_dimensions(path)
        return w > h

    def _get_duration(self, path):
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

    @staticmethod
    def _esc(path):
        try:
            if os.path.isabs(path):
                rel = os.path.relpath(path)
                if not os.path.isabs(rel):
                    path = rel
        except Exception:
            pass
        return path.replace("\\", "/").replace(":", "\\:")

    @staticmethod
    def _cleanup(path):
        try:
            os.remove(path)
        except OSError:
            pass
