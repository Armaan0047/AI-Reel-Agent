"""AI Reel Agent v5.0 — User Input Collection System"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from cli.panels import PanelFactory, PRIMARY, SECONDARY, ACCENT, SUCCESS, DIM, ERROR
from config.scripts import get_all_topics, get_scripts_by_topic, get_random_script, detect_topic


class PromptSystem:
    """Collects and validates all user inputs before rendering."""

    def __init__(self, console: Console, config):
        self.console = console
        self.config = config

    def collect_reel_config(self, mode: str = "standard") -> dict | None:
        """
        Step-by-step input collection for a single reel.
        Returns config dict or None if cancelled.
        """
        self.console.print(f"\n  [bold {PRIMARY}]═══ REEL CONFIGURATION ═══[/]\n")

        # Step 1: Script selection
        script_data = self._select_script()
        if script_data is None:
            return None

        # Step 2: Mode
        if mode == "standard":
            mode = self._select_mode()

        # Step 3: Quality
        quality = self._select_quality()

        # Build config
        reel_config = {
            "script": script_data["text"],
            "topic": script_data["topic"],
            "mode": mode,
            "quality": quality,
            "script_preview": script_data["text"][:80],
            "voice_engine": self.config.get("voice.default_engine", "edge-tts"),
            "resolution": f"{self.config.get('video.width', 1080)}x{self.config.get('video.height', 1920)}",
        }

        # Step 4: Summary & confirmation
        self.console.print()
        self.console.print(PanelFactory.generation_summary(reel_config))

        if not self._confirm("Proceed with generation?"):
            self.console.print(f"  [bold {ERROR}]Generation cancelled.[/]")
            return None

        return reel_config

    def collect_batch_config(self) -> dict | None:
        """Collect batch generation config."""
        self.console.print(f"\n  [bold {PRIMARY}]═══ BATCH GENERATION ═══[/]\n")

        # Count
        count_str = self.console.input(f"  [{ACCENT}]▸ Number of reels (1-20):[/] ").strip()
        try:
            count = int(count_str)
            if not 1 <= count <= 20:
                self.console.print(PanelFactory.error("Count must be 1-20"))
                return None
        except ValueError:
            self.console.print(PanelFactory.error("Invalid number"))
            return None

        # Topic filter
        topics = get_all_topics()
        self.console.print(f"\n  [{DIM}]Available topics: {', '.join(topics)}[/]")
        topic_input = self.console.input(f"  [{ACCENT}]▸ Topic filter (or 'random'):[/] ").strip().lower()
        force_topic = topic_input if topic_input in topics else None

        # Quality
        quality = self._select_quality()

        batch_config = {
            "count": count,
            "force_topic": force_topic,
            "quality": quality,
            "mode": "standard",
        }

        # Summary
        summary = {
            "topic": force_topic or "random",
            "mode": "BATCH",
            "quality": quality,
            "script_preview": f"{count} reels to generate",
            "voice_engine": self.config.get("voice.default_engine", "edge-tts"),
            "resolution": f"{self.config.get('video.width', 1080)}x{self.config.get('video.height', 1920)}",
        }
        self.console.print(PanelFactory.generation_summary(summary))

        if not self._confirm(f"Generate {count} reels?"):
            return None

        return batch_config

    def _select_script(self) -> dict | None:
        """Script selection submenu."""
        self.console.print(f"  [bold white]Script Source:[/]")
        self.console.print(f"    [{ACCENT}][1][/] Random from library")
        self.console.print(f"    [{ACCENT}][2][/] Pick topic first")
        self.console.print(f"    [{ACCENT}][3][/] Custom script")

        choice = self.console.input(f"\n  [{ACCENT}]▸ Choice:[/] ").strip()

        if choice == "1":
            script = get_random_script()
            self.console.print(PanelFactory.script_preview(script))
            return script

        elif choice == "2":
            topics = get_all_topics()
            for i, t in enumerate(topics, 1):
                count = len(get_scripts_by_topic(t))
                self.console.print(f"    [{ACCENT}][{i}][/] {t} ({count} scripts)")

            idx_str = self.console.input(f"\n  [{ACCENT}]▸ Topic number:[/] ").strip()
            try:
                idx = int(idx_str) - 1
                if 0 <= idx < len(topics):
                    scripts = get_scripts_by_topic(topics[idx])
                    import random
                    script = random.choice(scripts)
                    self.console.print(PanelFactory.script_preview(script))
                    return script
            except (ValueError, IndexError):
                pass
            self.console.print(PanelFactory.error("Invalid selection"))
            return None

        elif choice == "3":
            text = self.console.input(f"  [{ACCENT}]▸ Enter your script:[/] ").strip()
            if not text:
                self.console.print(PanelFactory.error("Empty script"))
                return None
            topic = detect_topic(text)
            script = {"topic": topic, "text": text}
            self.console.print(f"  [{DIM}]Auto-detected topic: {topic}[/]")
            return script

        return None

    def _select_mode(self) -> str:
        """Mode selection."""
        self.console.print(f"\n  [bold white]Render Mode:[/]")
        self.console.print(f"    [{ACCENT}][1][/] Standard")
        self.console.print(f"    [{ACCENT}][2][/] Minecraft")
        self.console.print(f"    [{ACCENT}][3][/] Luxury")
        choice = self.console.input(f"  [{ACCENT}]▸ Mode:[/] ").strip()
        return {"2": "minecraft", "3": "luxury"}.get(choice, "standard")

    def _select_quality(self) -> str:
        """Quality preset selection."""
        self.console.print(f"\n  [bold white]Render Quality:[/]")
        self.console.print(f"    [{ACCENT}][1][/] Fast     [dim](quick, lower quality)[/]")
        self.console.print(f"    [{ACCENT}][2][/] Balanced [dim](recommended)[/]")
        self.console.print(f"    [{ACCENT}][3][/] Quality  [dim](slower, higher quality)[/]")
        choice = self.console.input(f"  [{ACCENT}]▸ Quality:[/] ").strip()
        return {"1": "fast", "3": "quality"}.get(choice, "balanced")

    def _confirm(self, message: str) -> bool:
        """Y/N confirmation."""
        response = self.console.input(
            f"\n  [{SUCCESS}]▸ {message} (Y/n):[/] "
        ).strip().lower()
        return response in ("", "y", "yes")
