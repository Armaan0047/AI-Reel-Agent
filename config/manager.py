"""
AI Reel Agent v5.0 — Configuration Manager
Handles loading, saving, validating, and accessing configuration.
Supports first-run setup wizard with Rich prompts.
"""
import json
import os
import copy

from config.defaults import DEFAULT_CONFIG, DIR_NAMES, APP_VERSION
from core.utils.paths import get_exe_dir, resource_path


class ConfigManager:
    """Central configuration manager for AI Reel Agent."""

    def __init__(self, project_root: str):
        self.project_root = get_exe_dir()
        self._config_dir = os.path.join(self.project_root, "config")
        self._settings_path = os.path.join(self._config_dir, "settings.json")
        self._config = {}
        self._ffmpeg_path = None

        # Ensure all project directories exist
        self._ensure_directories()

        # Load configuration
        self.load()

    # ─── Directory Management ─────────────────────────────────────

    def _ensure_directories(self):
        """Create all required project directories."""
        for name, dir_name in DIR_NAMES.items():
            if name == "fonts":
                # Fonts are read-only bundled inside EXE, skip creation on disk
                continue
            path = os.path.join(self.project_root, dir_name)
            os.makedirs(path, exist_ok=True)

    def get_dir(self, name: str) -> str:
        """Get absolute path to a project directory."""
        dir_name = DIR_NAMES.get(name, name)
        if name == "fonts":
            return resource_path(dir_name)
        return os.path.join(self.project_root, dir_name)

    # ─── Load / Save ──────────────────────────────────────────────

    def load(self) -> dict:
        """Load settings.json and merge with defaults."""
        self._config = copy.deepcopy(DEFAULT_CONFIG)

        if os.path.exists(self._settings_path):
            try:
                with open(self._settings_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                self._deep_merge(self._config, user_config)
            except (json.JSONDecodeError, IOError):
                pass  # Use defaults on error

        # Override with environment variables
        env_eleven = os.environ.get("ELEVENLABS_API_KEY", "")
        if env_eleven:
            self._config["api"]["elevenlabs_key"] = env_eleven

        env_openai = os.environ.get("OPENAI_API_KEY", "")
        if env_openai:
            self._config["api"]["openai_key"] = env_openai

        return self._config

    def save(self):
        """Save current config to settings.json."""
        os.makedirs(self._config_dir, exist_ok=True)

        # Don't persist API keys that came from env vars
        save_config = copy.deepcopy(self._config)
        if os.environ.get("ELEVENLABS_API_KEY"):
            save_config["api"]["elevenlabs_key"] = ""
        if os.environ.get("OPENAI_API_KEY"):
            save_config["api"]["openai_key"] = ""

        with open(self._settings_path, "w", encoding="utf-8") as f:
            json.dump(save_config, f, indent=2, ensure_ascii=False)

    # ─── Access ───────────────────────────────────────────────────

    def get(self, key: str, default=None):
        """Get a config value using dot-notation: 'video.width'."""
        parts = key.split(".")
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def set(self, key: str, value):
        """Set a config value using dot-notation."""
        parts = key.split(".")
        current = self._config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def get_all(self) -> dict:
        """Return the full configuration dict."""
        return copy.deepcopy(self._config)

    # ─── Validation ───────────────────────────────────────────────

    def validate(self) -> list:
        """Validate configuration. Returns list of issues (empty = OK)."""
        issues = []

        # Check video dimensions
        w = self.get("video.width", 0)
        h = self.get("video.height", 0)
        if w <= 0 or h <= 0:
            issues.append("Video dimensions must be positive")

        # Check FPS
        fps = self.get("video.fps", 0)
        if fps not in (24, 25, 30, 60):
            issues.append(f"Unusual FPS value: {fps}")

        # Check music volume
        vol = self.get("music.mix_volume", 0)
        if not 0 <= vol <= 1:
            issues.append(f"Music volume must be 0.0-1.0, got {vol}")

        # Check directories
        videos_dir = self.get_dir("videos")
        if not os.path.isdir(videos_dir):
            issues.append(f"Videos directory not found: {videos_dir}")
        else:
            vids = [f for f in os.listdir(videos_dir)
                    if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm"))]
            if not vids:
                issues.append("No background videos found in videos/")

        return issues

    def is_first_run(self) -> bool:
        """Check if this is the first time running the app."""
        return not os.path.exists(self._settings_path)

    # ─── FFmpeg ───────────────────────────────────────────────────

    def get_ffmpeg_path(self) -> str:
        """Get FFmpeg path from imageio-ffmpeg."""
        if self._ffmpeg_path is None:
            try:
                from imageio_ffmpeg import get_ffmpeg_exe
                self._ffmpeg_path = get_ffmpeg_exe()
            except ImportError:
                self._ffmpeg_path = "ffmpeg"  # Fall back to system PATH
        return self._ffmpeg_path

    # ─── Reset ────────────────────────────────────────────────────

    def reset(self):
        """Reset configuration to defaults."""
        self._config = copy.deepcopy(DEFAULT_CONFIG)
        self.save()

    # ─── Helpers ──────────────────────────────────────────────────

    @staticmethod
    def _deep_merge(base: dict, override: dict):
        """Deep merge override into base (modifies base in-place)."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                ConfigManager._deep_merge(base[key], value)
            else:
                base[key] = value
