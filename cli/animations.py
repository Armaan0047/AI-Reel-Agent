"""AI Reel Agent v5.0 — Terminal Animations & Effects"""
import time
import random
from rich.console import Console
from rich.text import Text
from rich.style import Style


class TerminalFX:
    """Cinematic terminal visual effects."""

    @staticmethod
    def typewriter(console: Console, text: str, style: str = "", speed: float = 0.02):
        """Print text character by character."""
        for char in text:
            console.print(char, end="", style=style)
            time.sleep(speed)
        console.print()

    @staticmethod
    def loading_dots(console: Console, message: str, duration: float = 2.0, style: str = "bold cyan"):
        """Animated loading dots."""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            frame = frames[i % len(frames)]
            console.print(f"\r  {frame} {message}", end="", style=style)
            time.sleep(0.08)
            i += 1
        console.print()

    @staticmethod
    def glitch_text(console: Console, text: str, iterations: int = 3):
        """Glitch effect on text."""
        glitch_chars = "█▓▒░╬╫╪┼┤├"
        for _ in range(iterations):
            glitched = ""
            for char in text:
                if random.random() < 0.3:
                    glitched += random.choice(glitch_chars)
                else:
                    glitched += char
            console.print(f"\r  {glitched}", end="", style="bold red")
            time.sleep(0.1)
        console.print(f"\r  {text}", style="bold #00D4FF")

    @staticmethod
    def fade_in_text(console: Console, text: str):
        """Gradual brightness fade-in."""
        shades = ["#333333", "#555555", "#777777", "#999999", "#BBBBBB", "#DDDDDD", "#FFFFFF"]
        for shade in shades:
            console.print(f"\r  {text}", end="", style=f"bold {shade}")
            time.sleep(0.06)
        console.print()

    @staticmethod
    def scan_line(console: Console, lines: list, style: str = "bold #00D4FF"):
        """Reveal text line by line."""
        for line in lines:
            console.print(f"  {line}", style=style)
            time.sleep(0.05)

    @staticmethod
    def boot_sequence(console: Console, items: list):
        """Animated boot sequence with checkmarks."""
        for label, status, detail in items:
            if status == "ok":
                icon = "[bold #00FF88]✓[/]"
            elif status == "warn":
                icon = "[bold #FFA500]![/]"
            else:
                icon = "[bold #FF3333]✗[/]"
            console.print(f"  {icon} {label}", end="")
            if detail:
                console.print(f" [dim]— {detail}[/]")
            else:
                console.print()
            time.sleep(0.15)
