"""
AI Reel Agent v5.0 — Main Application Controller
Central orchestrator wiring all engines and CLI components together.
"""
import asyncio
import os
import sys
import time

from rich.console import Console
from rich.panel import Panel

from config.manager import ConfigManager
from config.defaults import APP_NAME, APP_VERSION, APP_AUTHOR
from core.script_manager import ScriptManager
from core.voice_engine import VoiceEngine
from core.subtitle_engine import SubtitleEngine
from core.music_engine import MusicEngine
from core.video_renderer import VideoRenderer
from core.queue_manager import RenderQueue
from cli.startup import StartupScreen
from cli.menus import MenuSystem
from cli.panels import PanelFactory, PRIMARY, SECONDARY, ACCENT, SUCCESS, ERROR, DIM
from cli.prompts import PromptSystem
from cli.progress import RenderConsole
from cli.logger import AnimatedLogger
from cli.animations import TerminalFX
from core.utils.paths import get_exe_dir


class AIReelAgent:
    """Main application controller for AI Reel Agent CLI."""

    def __init__(self):
        self.console = Console()
        self.project_root = get_exe_dir()
        self.config = ConfigManager(self.project_root)
        self.logger = AnimatedLogger(
            log_dir=self.config.get_dir("logs"),
            console=self.console,
        )

        # Core engines
        self.scripts = ScriptManager()
        self.subtitles = SubtitleEngine(self.config)
        self.music = MusicEngine(self.config)
        self.renderer = VideoRenderer(
            self.config,
            subtitle_engine=self.subtitles,
            music_engine=self.music,
        )
        self.queue = RenderQueue()

        # CLI components
        self.menus = MenuSystem(self.console)
        self.prompts = PromptSystem(self.console, self.config)
        self.progress = RenderConsole(self.console)

    async def run(self):
        """Main application loop."""
        # Cinematic startup
        startup = StartupScreen(self.config)
        startup.display(self.console)

        # First-run setup
        if self.config.is_first_run():
            self._first_run_setup()

        # Main loop
        while True:
            try:
                choice = self.menus.main_menu()

                if choice == "1":
                    await self.generate_reel()
                elif choice == "2":
                    await self.batch_generate()
                elif choice == "3":
                    await self.generate_reel(mode="minecraft")
                elif choice == "4":
                    await self.generate_reel(mode="luxury")
                elif choice == "5":
                    self.subtitle_settings()
                elif choice == "6":
                    self.voice_settings()
                elif choice == "7":
                    self.render_queue_menu()
                elif choice == "8":
                    self.settings()
                elif choice == "9":
                    self._exit()
                    break
                else:
                    self.console.print(PanelFactory.warning("Invalid option. Enter 1-9."))

            except KeyboardInterrupt:
                self.console.print(f"\n  [{DIM}]Ctrl+C detected[/]")
                self._exit()
                break
            except Exception as e:
                self.console.print(PanelFactory.error("Unexpected Error", str(e)))
                self.logger.error(f"Unhandled exception: {e}")

    # ═══════════════════════════════════════════════════════════════
    #  REEL GENERATION
    # ═══════════════════════════════════════════════════════════════

    async def generate_reel(self, mode: str = "standard"):
        """Generate a single reel with full workflow."""
        # Collect configuration
        reel_config = self.prompts.collect_reel_config(mode=mode)
        if reel_config is None:
            return

        # Execute pipeline
        await self._execute_pipeline(reel_config)

    async def batch_generate(self):
        """Generate multiple reels."""
        batch_config = self.prompts.collect_batch_config()
        if batch_config is None:
            return

        count = batch_config["count"]
        force_topic = batch_config.get("force_topic")
        results = []
        start_time = time.time()

        self.console.print(f"\n  [bold {PRIMARY}]Starting batch generation: {count} reels[/]\n")

        for i in range(count):
            self.console.print(f"\n  [bold {ACCENT}]{'━' * 50}[/]")
            self.console.print(f"  [bold {ACCENT}]  REEL {i + 1} / {count}[/]")
            self.console.print(f"  [bold {ACCENT}]{'━' * 50}[/]\n")

            try:
                # Get script
                if force_topic:
                    from config.scripts import get_scripts_by_topic
                    import random
                    scripts = get_scripts_by_topic(force_topic)
                    script_data = random.choice(scripts) if scripts else self.scripts.get_random()
                else:
                    script_data = self.scripts.get_random()

                reel_config = {
                    "script": script_data["text"],
                    "topic": script_data["topic"],
                    "mode": batch_config.get("mode", "standard"),
                    "quality": batch_config.get("quality", "balanced"),
                    "script_preview": script_data["text"][:80],
                    "voice_engine": "edge-tts",
                    "resolution": f"{self.config.get('video.width', 1080)}x{self.config.get('video.height', 1920)}",
                }

                output = await self._execute_pipeline(reel_config)
                if output and os.path.exists(output):
                    results.append(output)
            except Exception as e:
                self.console.print(PanelFactory.error(f"Reel {i+1} failed", str(e)))
                self.logger.error(f"Batch reel {i+1} failed: {e}")

        # Batch summary
        elapsed = time.time() - start_time
        self.console.print(f"\n  [bold {PRIMARY}]{'═' * 50}[/]")
        self.console.print(f"  [bold {SUCCESS}]  BATCH COMPLETE[/]")
        self.console.print(f"  [bold {PRIMARY}]{'═' * 50}[/]")
        self.console.print(f"  [{DIM}]Generated:[/] [bold]{len(results)}/{count}[/]")
        self.console.print(f"  [{DIM}]Time:[/] [bold]{elapsed:.1f}s[/]")
        for r in results:
            sz = os.path.getsize(r) / (1024 * 1024)
            self.console.print(f"  [{SUCCESS}]→[/] {os.path.basename(r)} ({sz:.1f} MB)")
        self.console.print()

    async def _execute_pipeline(self, reel_config: dict) -> str:
        """Execute the full render pipeline with progress tracking."""
        self.progress.set_metadata(
            topic=reel_config["topic"],
            mode=reel_config.get("mode", "standard"),
            engine=reel_config.get("voice_engine", "edge-tts")
        )
        self.progress.start()
        topic = reel_config["topic"]
        script = reel_config["script"]
        mode = reel_config.get("mode", "standard")

        try:
            # Stage 1: Script
            self.progress.log("Script selected", "ok")
            self.progress.update("script", 1.0, f"Topic: {topic}")

            # Adjust topic for mode
            if mode == "luxury" and topic not in ("luxury", "sigma_luxury"):
                topic = "luxury"
            elif mode == "minecraft" and topic in ("luxury", "sigma_luxury"):
                topic = "motivation"

            # Stage 2: Voice synthesis
            self.progress.log(f"Starting voice synthesis ({reel_config.get('voice_engine', 'edge-tts')})", "info")
            voice_engine = VoiceEngine(
                self.config,
                on_progress=lambda stage, pct, detail: self.progress.update(stage, pct, detail),
            )
            voice_data = await voice_engine.generate(script=script, topic=topic)
            self.progress.log(f"Voice: {voice_data['voice']} | {len(voice_data['subtitle_data'])} phrases", "ok")

            # Stage 3: Video selection
            self.progress.update("subtitle", 0.5, "Selecting background video")
            video_path = self.renderer.get_random_video(topic=topic)
            if not video_path:
                self.progress.error("No background videos found in videos/ directory!")
                return None
            self.progress.log(f"Video: {os.path.basename(video_path)}", "ok")

            # Stage 4-5: Render
            self.progress.log("Starting FFmpeg render pipeline", "info")
            output_name = f"reel_{time.strftime('%Y%m%d_%H%M%S')}"

            # Create renderer with progress callback
            renderer = VideoRenderer(
                self.config,
                subtitle_engine=self.subtitles,
                music_engine=self.music,
                on_progress=lambda stage, pct, detail: self.progress.update(stage, pct, detail),
            )

            reel_path = renderer.render(
                video_path=video_path,
                audio_path=voice_data["audio_path"],
                subtitle_data=voice_data["subtitle_data"],
                output_name=output_name,
                topic=topic,
            )

            # Stage 6: Finalization
            if reel_path and os.path.exists(reel_path):
                self.progress.update("finalize", 1.0, "Complete")
                self.progress.complete(reel_path)
                self.logger.success(f"Reel generated: {os.path.basename(reel_path)}")
                return reel_path
            else:
                self.progress.error("All render tiers failed")
                self.logger.error("Render pipeline failed")
                return None

        except Exception as e:
            self.progress.error(str(e))
            self.logger.error(f"Pipeline error: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════
    #  SETTINGS MENUS
    # ═══════════════════════════════════════════════════════════════

    def subtitle_settings(self):
        """Subtitle settings submenu."""
        while True:
            choice = self.menus.subtitle_settings_menu()
            if choice == "0":
                break
            elif choice == "1":
                val = self.console.input(f"  [{ACCENT}]Font size (current: {self.config.get('caption.font_size')}):[/] ").strip()
                try:
                    self.config.set("caption.font_size", int(val))
                    self.config.save()
                    self.console.print(PanelFactory.success(f"Font size set to {val}"))
                except ValueError:
                    self.console.print(PanelFactory.error("Invalid number"))
            elif choice == "2":
                presets = self.subtitles.get_animation_presets()
                self.console.print(f"  [{DIM}]Available: {', '.join(presets)}[/]")
            elif choice == "3":
                val = self.console.input(f"  [{ACCENT}]Outline width (current: {self.config.get('caption.outline_width')}):[/] ").strip()
                try:
                    self.config.set("caption.outline_width", int(val))
                    self.config.save()
                    self.console.print(PanelFactory.success(f"Outline width set to {val}"))
                except ValueError:
                    self.console.print(PanelFactory.error("Invalid number"))
            elif choice == "4":
                val = self.console.input(f"  [{ACCENT}]Words per chunk (current: {self.config.get('caption.words_per_chunk')}):[/] ").strip()
                try:
                    self.config.set("caption.words_per_chunk", int(val))
                    self.config.save()
                    self.console.print(PanelFactory.success(f"Words per chunk set to {val}"))
                except ValueError:
                    self.console.print(PanelFactory.error("Invalid number"))
            elif choice == "5":
                caption_config = {
                    "font_size": self.config.get("caption.font_size"),
                    "outline_width": self.config.get("caption.outline_width"),
                    "alignment": self.config.get("caption.alignment"),
                    "margin_v": self.config.get("caption.margin_v"),
                    "words_per_chunk": self.config.get("caption.words_per_chunk"),
                    "font_name": self.config.get("caption.font_name"),
                }
                self.console.print(PanelFactory.config_table(caption_config, "Subtitle Settings"))

    def voice_settings(self):
        """Voice settings submenu."""
        while True:
            choice = self.menus.voice_settings_menu()
            if choice == "0":
                break
            elif choice == "1":
                current = self.config.get("voice.default_engine", "edge-tts")
                self.console.print(f"  [{DIM}]Current engine: {current}[/]")
                self.console.print(f"    [{ACCENT}][1][/] edge-tts (free)")
                self.console.print(f"    [{ACCENT}][2][/] ElevenLabs (premium)")
                eng = self.console.input(f"  [{ACCENT}]▸ Engine:[/] ").strip()
                engine = "elevenlabs" if eng == "2" else "edge-tts"
                self.config.set("voice.default_engine", engine)
                self.config.save()
                self.console.print(PanelFactory.success(f"Voice engine set to {engine}"))
            elif choice == "2":
                from config.profiles import VOICE_PROFILES
                from rich.table import Table
                table = Table(title="Voice Profiles", box=None)
                table.add_column("Topic", style=f"{ACCENT}")
                table.add_column("Style", style="white")
                table.add_column("Voices", style=f"{DIM}")
                for topic, profile in VOICE_PROFILES.items():
                    if topic == "_default":
                        continue
                    voices = ", ".join(v.split("-")[-1].replace("Neural", "") for v in profile["voices"])
                    table.add_row(topic, profile["style"], voices)
                self.console.print(table)
            elif choice == "3":
                self.console.print(f"  [{DIM}]Voice preview requires active network connection[/]")
            elif choice == "4":
                key = self.console.input(f"  [{ACCENT}]▸ ElevenLabs API key:[/] ").strip()
                if key:
                    self.config.set("api.elevenlabs_key", key)
                    self.config.save()
                    self.console.print(PanelFactory.success("API key saved"))

    def render_queue_menu(self):
        """Render queue management."""
        status = self.queue.get_status()
        self.console.print(f"\n  [bold {PRIMARY}]Render Queue[/]")
        self.console.print(f"  [{DIM}]Total: {status['total']} | "
                          f"Queued: {status['queued']} | "
                          f"Complete: {status['complete']} | "
                          f"Failed: {status['failed']}[/]\n")

        if status["total"] == 0:
            self.console.print(f"  [{DIM}]Queue is empty. Generate reels to add jobs.[/]")
        else:
            jobs = self.queue.list_jobs()
            from rich.table import Table
            table = Table(box=None)
            table.add_column("ID", style=f"{ACCENT}")
            table.add_column("Topic", style="white")
            table.add_column("Status", style="bold")
            table.add_column("Output", style=f"{DIM}")
            for job in jobs:
                status_color = {"queued": ACCENT, "processing": SECONDARY, "complete": SUCCESS, "failed": ERROR}
                color = status_color.get(job["status"], DIM)
                table.add_row(
                    job["id"],
                    job["config"].get("topic", "?"),
                    f"[{color}]{job['status']}[/]",
                    os.path.basename(job["output"]) if job["output"] else "—",
                )
            self.console.print(table)

    def settings(self):
        """General settings menu."""
        while True:
            choice = self.menus.settings_menu()
            if choice == "0":
                break
            elif choice == "1":
                self.console.print(PanelFactory.config_table(self.config.get_all(), "All Settings"))
            elif choice == "2":
                w = self.console.input(f"  [{ACCENT}]Width (current: {self.config.get('video.width')}):[/] ").strip()
                h = self.console.input(f"  [{ACCENT}]Height (current: {self.config.get('video.height')}):[/] ").strip()
                try:
                    self.config.set("video.width", int(w))
                    self.config.set("video.height", int(h))
                    self.config.save()
                    self.console.print(PanelFactory.success(f"Resolution set to {w}x{h}"))
                except ValueError:
                    self.console.print(PanelFactory.error("Invalid dimensions"))
            elif choice == "3":
                self.console.print(f"    [{ACCENT}][1][/] Fast (CRF 28)")
                self.console.print(f"    [{ACCENT}][2][/] Balanced (CRF 23)")
                self.console.print(f"    [{ACCENT}][3][/] Quality (CRF 18)")
                q = self.console.input(f"  [{ACCENT}]▸ Quality:[/] ").strip()
                presets = {"1": 28, "2": 23, "3": 18}
                if q in presets:
                    self.config.set("rendering.tier1_crf", presets[q])
                    self.config.save()
                    self.console.print(PanelFactory.success(f"Quality updated"))
            elif choice == "4":
                val = self.console.input(f"  [{ACCENT}]Music volume 0.0-1.0 (current: {self.config.get('music.mix_volume')}):[/] ").strip()
                try:
                    vol = float(val)
                    if 0 <= vol <= 1:
                        self.config.set("music.mix_volume", vol)
                        self.config.save()
                        self.console.print(PanelFactory.success(f"Music volume set to {vol}"))
                    else:
                        self.console.print(PanelFactory.error("Volume must be 0.0-1.0"))
                except ValueError:
                    self.console.print(PanelFactory.error("Invalid number"))
            elif choice == "5":
                self.console.print(f"  [{DIM}]ElevenLabs: {'✓ configured' if self.config.get('api.elevenlabs_key') else '✗ not set'}[/]")
                self.console.print(f"  [{DIM}]OpenAI: {'✓ configured' if self.config.get('api.openai_key') else '✗ not set'}[/]")
            elif choice == "6":
                if self.prompts._confirm("Reset ALL settings to defaults?"):
                    self.config.reset()
                    self.console.print(PanelFactory.success("Settings reset to defaults"))

    # ═══════════════════════════════════════════════════════════════
    #  HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _first_run_setup(self):
        """First-run setup wizard."""
        self.console.print(Panel(
            f"[bold {PRIMARY}]Welcome to AI Reel Agent![/]\n\n"
            f"This appears to be your first time running the app.\n"
            f"Let's set up a few things...",
            border_style=ACCENT,
            padding=(1, 2),
        ))

        # ElevenLabs (optional)
        self.console.print(f"\n  [{DIM}]ElevenLabs provides premium AI voices (optional).[/]")
        key = self.console.input(f"  [{ACCENT}]▸ ElevenLabs API key (or press Enter to skip):[/] ").strip()
        if key:
            self.config.set("api.elevenlabs_key", key)

        # Save
        self.config.save()
        self.console.print(PanelFactory.success("Setup complete! Configuration saved."))
        self.console.print()

    def _exit(self):
        """Clean exit with animation."""
        self.console.print()
        TerminalFX.typewriter(self.console, "  Shutting down AI Reel Agent...", style=f"{DIM}", speed=0.02)
        self.console.print(f"  [{DIM}]Session log: {self.logger.get_session_log()}[/]")
        self.console.print(f"\n  [bold {ACCENT}]Built by {APP_AUTHOR}.  Goodbye! ⚡[/]\n")
