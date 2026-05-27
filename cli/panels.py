"""AI Reel Agent v5.0 — Reusable Rich Panel Components"""
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich import box

# ─── Color Palette ────────────────────────────────────────────────
PRIMARY   = "#00D4FF"
SECONDARY = "#FF6EC7"
ACCENT    = "#FFD700"
SUCCESS   = "#00FF88"
WARNING   = "#FFA500"
ERROR     = "#FF3333"
DIM       = "#555555"


class PanelFactory:
    """Factory for creating consistent, styled Rich panels."""

    @staticmethod
    def header(title: str, subtitle: str = "") -> Panel:
        content = Text(title, style=f"bold {PRIMARY}", justify="center")
        if subtitle:
            content.append(f"\n{subtitle}", style=f"{DIM}")
        return Panel(
            Align.center(content),
            border_style=PRIMARY,
            box=box.DOUBLE_EDGE,
            padding=(1, 2),
        )

    @staticmethod
    def success(message: str, details: str = "") -> Panel:
        content = f"[bold {SUCCESS}]✓ {message}[/]"
        if details:
            content += f"\n[{DIM}]{details}[/]"
        return Panel(content, border_style=SUCCESS, box=box.ROUNDED, padding=(0, 2))

    @staticmethod
    def error(message: str, details: str = "") -> Panel:
        content = f"[bold {ERROR}]✗ {message}[/]"
        if details:
            content += f"\n[{DIM}]{details}[/]"
        return Panel(content, border_style=ERROR, box=box.ROUNDED, padding=(0, 2))

    @staticmethod
    def warning(message: str) -> Panel:
        return Panel(
            f"[bold {WARNING}]! {message}[/]",
            border_style=WARNING, box=box.ROUNDED, padding=(0, 2),
        )

    @staticmethod
    def info(message: str) -> Panel:
        return Panel(
            f"[{PRIMARY}]{message}[/]",
            border_style=DIM, box=box.ROUNDED, padding=(0, 2),
        )

    @staticmethod
    def status_grid(items: dict) -> Panel:
        """System status grid."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style=f"{DIM}")
        table.add_column("Value", style=f"bold {PRIMARY}")
        for label, value in items.items():
            table.add_row(label, str(value))
        return Panel(table, border_style=DIM, box=box.ROUNDED, title="[bold]System Info[/]")

    @staticmethod
    def generation_summary(config: dict) -> Panel:
        """Render generation summary panel."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Setting", style=f"bold {DIM}", width=20)
        table.add_column("Value", style=f"bold white")

        field_map = [
            ("Topic", config.get("topic", "random")),
            ("Script", (config.get("script_preview", "Auto-selected")[:60] + "...") if len(config.get("script_preview", "")) > 60 else config.get("script_preview", "Auto-selected")),
            ("Mode", config.get("mode", "standard").upper()),
            ("Voice Engine", config.get("voice_engine", "edge-tts")),
            ("Quality", config.get("quality", "balanced")),
            ("Resolution", config.get("resolution", "1080x1920")),
        ]
        for label, value in field_map:
            table.add_row(label, str(value))

        return Panel(
            table,
            title=f"[bold {ACCENT}]⚡ GENERATION SUMMARY[/]",
            border_style=ACCENT,
            box=box.DOUBLE_EDGE,
            padding=(1, 2),
        )

    @staticmethod
    def script_preview(script: dict) -> Panel:
        """Show a script preview panel."""
        topic = script.get("topic", "unknown")
        text = script.get("text", "")
        return Panel(
            f"[white]{text}[/]",
            title=f"[bold {SECONDARY}]📝 Script [{topic.upper()}][/]",
            border_style=SECONDARY,
            box=box.ROUNDED,
            padding=(1, 2),
        )

    @staticmethod
    def config_table(config: dict, title: str = "Configuration") -> Panel:
        """Display configuration as a table."""
        table = Table(show_header=True, box=box.SIMPLE_HEAVY, header_style=f"bold {PRIMARY}")
        table.add_column("Setting", style=f"{DIM}")
        table.add_column("Value", style="bold white")

        def flatten(d, prefix=""):
            for k, v in d.items():
                key = f"{prefix}{k}" if not prefix else f"{prefix}.{k}"
                if isinstance(v, dict):
                    flatten(v, key)
                else:
                    table.add_row(key, str(v))
        flatten(config)

        return Panel(table, title=f"[bold]{title}[/]", border_style=DIM, box=box.ROUNDED)

    @staticmethod
    def divider(title: str = "") -> None:
        from rich.rule import Rule
        return Rule(title=title, style=DIM)
