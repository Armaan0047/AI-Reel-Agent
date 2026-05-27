"""
AI Reel Agent v5.0 — Live Render Console
Real-time progress tracking with stunning Cinematic Rich Live layout.
"""
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich import box

from cli.panels import PRIMARY, SECONDARY, ACCENT, SUCCESS, ERROR, DIM

STAGES = [
    ("script",   "📝 Script Dynamic Composition"),
    ("voice",    "🎙️ Premium Voice Synthesis"),
    ("subtitle", "📝 Subtitle Track Creation"),
    ("music",    "🎵 Ambient Music Synthesis"),
    ("render",   "🎬 FFmpeg Video Rendering"),
    ("finalize", "✨ Finalization & Validation"),
]


class RenderConsole:
    """Live rendering progress display using Rich Live Dashboard Panel."""

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self._current_stage = 0
        self._stage_progress = 0.0
        self._log_entries = []
        self._start_time = None
        self._live = None
        self._overall_progress = 0.0
        
        # Meta info
        self._topic = "unknown"
        self._mode = "standard"
        self._engine = "edge-tts"

    def set_metadata(self, topic: str, mode: str, engine: str):
        """Set generation metadata for display inside the Live Panel."""
        self._topic = topic
        self._mode = mode
        self._engine = engine

    def start(self):
        """Initialize and fire up the Live rendering dashboard."""
        self._start_time = time.time()
        self._current_stage = 0
        self._stage_progress = 0.0
        self._log_entries = []
        self._overall_progress = 0.0
        
        self.console.print()
        # Instantiate and start the Rich Live view
        self._live = Live(
            self._generate_panel(),
            console=self.console,
            refresh_per_second=8,
            transient=True  # Clear the panel from terminal on completion
        )
        self._live.start()

    def update(self, stage: str, progress: float, detail: str = ""):
        """Update current stage, progress, and refresh the dashboard."""
        # Find stage index
        for i, (key, _) in enumerate(STAGES):
            if key == stage:
                self._current_stage = i
                break

        self._stage_progress = progress
        self._overall_progress = (self._current_stage + progress) / len(STAGES)

        # Log details if any
        if detail:
            timestamp = time.strftime("%H:%M:%S")
            stage_name = STAGES[self._current_stage][1]
            self._log_entries.append(f"[{DIM}][{timestamp}][/] [{SUCCESS}]✓[/] {stage_name}: {detail}")

        # Trigger redraw
        if self._live:
            self._live.update(self._generate_panel())

    def log(self, msg: str, level: str = "info"):
        """Append log message and refresh the dashboard."""
        timestamp = time.strftime("%H:%M:%S")
        icons = {"info": "•", "ok": "✓", "warn": "!", "error": "✗"}
        colors = {"info": PRIMARY, "ok": SUCCESS, "warn": "#FFA500", "error": ERROR}
        icon = icons.get(level, "•")
        color = colors.get(level, PRIMARY)
        
        log_str = f"[{DIM}][{timestamp}][/] [{color}]{icon}[/] {msg}"
        self._log_entries.append(log_str)
        
        if self._live:
            self._live.update(self._generate_panel())

    def _generate_panel(self) -> Panel:
        """Generate the fully customized cinematic layout panel."""
        stage_name = STAGES[self._current_stage][1] if self._current_stage < len(STAGES) else "Processing"
        
        pct = int(self._overall_progress * 100)
        bar_width = 32
        filled = int(bar_width * self._overall_progress)
        bar = f"[{SUCCESS}]{'█' * filled}[/][{DIM}]{'░' * (bar_width - filled)}[/]"
        
        # Dynamic spinner frame
        spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        frame = spinners[int(time.time() * 8) % len(spinners)]
        
        elapsed = time.time() - self._start_time if self._start_time else 0
        
        # Build panel body
        body = []
        body.append(f"  [{PRIMARY}]{frame}[/]  [{PRIMARY}]{stage_name}[/]")
        body.append(f"  {bar} [bold white]{pct}%[/]  [{DIM}]{elapsed:.1f}s elapsed[/]")
        body.append(f"[{DIM}]{'─' * 62}[/]")
        
        # Last 5 logs inside the panel
        logs_to_show = self._log_entries[-5:]
        while len(logs_to_show) < 5:
            logs_to_show.insert(0, f"[{DIM}]  · waiting...[/]")
            
        for l in logs_to_show:
            body.append(f"  {l}")
            
        body.append(f"[{DIM}]{'─' * 62}[/]")
        body.append(f"  [bold {ACCENT}]Topic:[/] {self._topic.upper()}  "
                    f"│  [bold {SECONDARY}]Mode:[/] {self._mode.upper()}  "
                    f"│  [bold {PRIMARY}]Engine:[/] {self._engine}")
        
        panel = Panel(
            "\n".join(body),
            title=f"[bold {PRIMARY}]🎬 AI REEL GENERATION PIPELINE[/]",
            border_style=PRIMARY,
            box=box.ROUNDED,
            padding=(1, 2),
            width=68
        )
        return panel

    def complete(self, output_path: str):
        """Cleanly stop the Live display and render the final success panel."""
        if self._live:
            try:
                self._live.stop()
            except Exception:
                pass
        
        elapsed = time.time() - self._start_time if self._start_time else 0
        self.console.print()

        import os
        size_mb = 0
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style=f"bold {PRIMARY}", width=18)
        table.add_column("Value", style="white")
        table.add_row("✨ Output File", os.path.basename(output_path))
        table.add_row("📊 File Size", f"[bold {SUCCESS}]{size_mb:.2f} MB[/]")
        table.add_row("⚡ Render Time", f"[bold {SECONDARY}]{elapsed:.1f}s[/]")
        table.add_row("📂 Storage Path", f"[{ACCENT}]{output_path}[/]")

        panel = Panel(
            table,
            title=f"[bold {SUCCESS}] 🎉 REEL CREATED SUCCESSFULLY 🎉 [/]",
            subtitle=f"[bold {PRIMARY}] AI Reel Agent v5.5 [/]",
            border_style=SUCCESS,
            box=box.DOUBLE_EDGE,
            padding=(1, 3),
            width=68
        )
        self.console.print(panel)

    def error(self, msg: str):
        """Cleanly stop the Live display and render the error panel."""
        if self._live:
            try:
                self._live.stop()
            except Exception:
                pass
        
        self.console.print()
        from cli.panels import PanelFactory
        self.console.print(PanelFactory.error("Render Failed", msg))
