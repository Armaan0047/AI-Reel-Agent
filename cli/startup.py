"""AI Reel Agent v5.0 — Cinematic Startup Screen"""
import os
import sys
import time
import subprocess
import platform

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from config.defaults import APP_NAME, APP_VERSION, APP_AUTHOR
from cli.animations import TerminalFX
from cli.panels import PanelFactory, PRIMARY, SECONDARY, ACCENT, SUCCESS, WARNING, DIM


# Large ASCII banner
BANNER = r"""
     █████╗ ██╗    ██████╗ ███████╗███████╗██╗
    ██╔══██╗██║    ██╔══██╗██╔════╝██╔════╝██║
    ███████║██║    ██████╔╝█████╗  █████╗  ██║
    ██╔══██║██║    ██╔══██╗██╔══╝  ██╔══╝  ██║
    ██║  ██║██║    ██║  ██║███████╗███████╗███████╗
    ╚═╝  ╚═╝╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
              █████╗  ██████╗ ███████╗███╗   ██╗████████╗
             ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
             ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║
             ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║
             ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║
             ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝
"""


class StartupScreen:
    """Cinematic boot sequence with system checks."""

    def __init__(self, config):
        self.config = config

    def display(self, console: Console):
        """Run the full cinematic startup sequence."""
        # Clear terminal
        os.system("cls" if os.name == "nt" else "clear")

        # Banner with gradient colors
        banner_text = Text(BANNER)
        banner_text.stylize(f"bold {PRIMARY}")
        console.print(banner_text)

        # Version + author panel
        info_text = Text.assemble(
            (f"v{APP_VERSION}", f"bold {ACCENT}"),
            ("  │  ", DIM),
            (f"Developed by {APP_AUTHOR}", f"bold {SECONDARY}"),
            ("  │  ", DIM),
            ("Cinematic Reel Engine", f"{DIM}"),
        )
        console.print(Align.center(info_text))
        console.print()

        # System status checks
        console.print(f"  [bold {PRIMARY}]System Initialization[/]")
        console.print(f"  [{DIM}]{'─' * 50}[/]")
        time.sleep(0.3)

        checks = []

        # Python version
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        checks.append(("Python", "ok", py_ver))

        # FFmpeg
        ffmpeg_info = self.detect_ffmpeg()
        if ffmpeg_info["found"]:
            checks.append(("FFmpeg", "ok", ffmpeg_info["version"]))
        else:
            checks.append(("FFmpeg", "error", "Not found"))

        # GPU
        gpu_info = self.detect_gpu()
        if gpu_info["found"]:
            checks.append(("GPU", "ok", gpu_info["name"]))
        else:
            checks.append(("GPU", "warn", "No NVIDIA GPU detected"))

        # ElevenLabs
        api_key = self.config.get("api.elevenlabs_key", "")
        if api_key:
            checks.append(("ElevenLabs", "ok", "API key configured"))
        else:
            checks.append(("ElevenLabs", "warn", "Not configured (using edge-tts)"))

        # Edge-TTS
        try:
            import edge_tts
            checks.append(("Edge-TTS", "ok", "Ready"))
        except ImportError:
            checks.append(("Edge-TTS", "error", "Not installed"))

        # Assets
        asset_info = self.check_assets()
        checks.append(("Videos", "ok" if asset_info["videos"] > 0 else "error",
                       f"{asset_info['videos']} found"))
        checks.append(("Output Dir", "ok", "Ready"))

        # Animated boot sequence
        TerminalFX.boot_sequence(console, checks)

        console.print(f"  [{DIM}]{'─' * 50}[/]")

        # Final status
        errors = sum(1 for _, s, _ in checks if s == "error")
        if errors == 0:
            console.print(f"\n  [bold {SUCCESS}]◆ System Ready[/]\n")
        else:
            console.print(f"\n  [bold {WARNING}]◆ System Ready ({errors} warning(s))[/]\n")

        time.sleep(0.5)

    def detect_gpu(self) -> dict:
        """Detect NVIDIA GPU via nvidia-smi."""
        try:
            r = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5,
            )
            if r.returncode == 0 and r.stdout.strip():
                parts = r.stdout.strip().split(",")
                name = parts[0].strip()
                vram = f"{int(parts[1].strip())}MB" if len(parts) > 1 else ""
                return {"found": True, "name": f"{name} ({vram})" if vram else name}
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return {"found": False, "name": ""}

    def detect_ffmpeg(self) -> dict:
        """Detect FFmpeg via imageio-ffmpeg or system."""
        ffmpeg_path = self.config.get_ffmpeg_path()
        try:
            r = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                version_line = r.stdout.split("\n")[0]
                # Extract version number
                parts = version_line.split()
                version = parts[2] if len(parts) > 2 else "detected"
                return {"found": True, "version": version}
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return {"found": False, "version": ""}

    def check_assets(self) -> dict:
        """Check available assets."""
        videos_dir = self.config.get_dir("videos")
        video_count = 0
        if os.path.isdir(videos_dir):
            video_count = len([f for f in os.listdir(videos_dir)
                              if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm"))])
        return {"videos": video_count}
