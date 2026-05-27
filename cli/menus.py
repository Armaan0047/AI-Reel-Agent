"""AI Reel Agent v5.0 — Interactive Menu System"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

from cli.panels import PRIMARY, SECONDARY, ACCENT, SUCCESS, DIM, ERROR


class MenuSystem:
    """Rich-based interactive menu system."""

    def __init__(self, console: Console):
        self.console = console

    def main_menu(self) -> str:
        """Display main menu and return selected option."""
        menu_items = [
            ("1", "🎬", "Generate Reel", "Create a single viral reel"),
            ("2", "📦", "Batch Generate", "Generate multiple reels at once"),
            ("3", "🎮", "Minecraft Mode", "Minecraft gameplay background"),
            ("4", "💎", "Luxury Mode", "Cinematic luxury visuals"),
            ("5", "📝", "Subtitle Settings", "Font, animation, style"),
            ("6", "🎙️", "Voice Settings", "Engine, profiles, preview"),
            ("7", "📋", "Render Queue", "Manage pending renders"),
            ("8", "⚙️", "Settings", "Configuration & API keys"),
            ("9", "🚪", "Exit", "Close AI Reel Agent"),
        ]

        table = Table(
            show_header=False, box=None, padding=(0, 2),
            expand=True,
        )
        table.add_column("Key", style=f"bold {ACCENT}", width=4, justify="right")
        table.add_column("Icon", width=3)
        table.add_column("Option", style=f"bold white")
        table.add_column("Description", style=f"{DIM}")

        for key, icon, name, desc in menu_items:
            table.add_row(f"[{key}]", icon, name, desc)

        panel = Panel(
            table,
            title=f"[bold {PRIMARY}]⚡ COMMAND CENTER[/]",
            border_style=PRIMARY,
            box=box.DOUBLE_EDGE,
            padding=(1, 2),
        )
        self.console.print(panel)

        choice = self.console.input(f"  [{ACCENT}]▸ Select option:[/] ").strip()
        return choice

    def subtitle_settings_menu(self) -> str:
        """Subtitle settings submenu."""
        items = [
            ("1", "Font Size"),
            ("2", "Animation Style"),
            ("3", "Outline Width"),
            ("4", "Words Per Chunk"),
            ("5", "View Current Settings"),
            ("0", "Back to Main Menu"),
        ]
        return self._submenu("Subtitle Settings", items)

    def voice_settings_menu(self) -> str:
        """Voice settings submenu."""
        items = [
            ("1", "Voice Engine (edge-tts / ElevenLabs)"),
            ("2", "View Voice Profiles"),
            ("3", "Test Voice Preview"),
            ("4", "ElevenLabs API Key"),
            ("0", "Back to Main Menu"),
        ]
        return self._submenu("Voice Settings", items)

    def settings_menu(self) -> str:
        """General settings submenu."""
        items = [
            ("1", "View All Settings"),
            ("2", "Video Resolution"),
            ("3", "Render Quality"),
            ("4", "Music Volume"),
            ("5", "API Keys"),
            ("6", "Reset to Defaults"),
            ("0", "Back to Main Menu"),
        ]
        return self._submenu("Settings", items)

    def _submenu(self, title: str, items: list) -> str:
        """Generic submenu renderer."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style=f"bold {ACCENT}", width=4, justify="right")
        table.add_column("Option", style="bold white")

        for key, name in items:
            table.add_row(f"[{key}]", name)

        panel = Panel(
            table,
            title=f"[bold {SECONDARY}]{title}[/]",
            border_style=SECONDARY,
            box=box.ROUNDED,
            padding=(1, 2),
        )
        self.console.print(panel)

        choice = self.console.input(f"  [{ACCENT}]▸ Select option:[/] ").strip()
        return choice
