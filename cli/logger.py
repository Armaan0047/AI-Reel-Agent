"""AI Reel Agent v5.0 — Animated Logger
Dual-output: Rich console + file.
"""
import os
import time
from datetime import datetime
from rich.console import Console


class AnimatedLogger:
    """Production logger with styled console output and file logging."""

    def __init__(self, log_dir: str = "logs", console: Console = None):
        self.console = console or Console()
        self._log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self._log_file = os.path.join(
            log_dir, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        self._entries = []

    def _log(self, level: str, icon: str, msg: str, style: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"  [{style}]{icon}[/] [{style}]{msg}[/]", highlight=False)
        entry = f"[{timestamp}] [{level}] {msg}"
        self._entries.append(entry)
        try:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        except IOError:
            pass

    def info(self, msg: str):
        self._log("INFO", "•", msg, "#00D4FF")

    def success(self, msg: str):
        self._log("OK", "✓", msg, "#00FF88")

    def warning(self, msg: str):
        self._log("WARN", "!", msg, "#FFA500")

    def error(self, msg: str):
        self._log("ERROR", "✗", msg, "#FF3333")

    def debug(self, msg: str):
        self._log("DEBUG", "·", msg, "#555555")

    def stage(self, msg: str):
        self._log("STAGE", "►", msg, "bold #FF6EC7")

    def render(self, msg: str):
        self._log("RENDER", "◆", msg, "bold #00D4FF")

    def get_session_log(self) -> str:
        return self._log_file

    def get_entries(self) -> list:
        return self._entries.copy()
