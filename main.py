#!/usr/bin/env python3
"""
AI REEL AGENT v5.0 — Cinematic Terminal Application
Premium AI-powered viral reel generation engine.

Developed by Master Armaan

Usage:
    python main.py                 # Interactive CLI
    python main.py --count 5       # Batch generate (legacy compat)
    python main.py --topic luxury  # Force topic (legacy compat)
    python main.py --help          # Show help
"""
import sys
import os
import io

# ─── Force UTF-8 encoding ────────────────────────────────────────
if sys.stdout and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "buffer"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Ensure project root is in path ──────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import asyncio


def main():
    """Entry point for AI Reel Agent."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    # Legacy CLI compatibility: --count N, --topic TOPIC
    if "--count" in args or "--topic" in args or "--voice-only" in args:
        _legacy_mode(args)
        return

    # Modern interactive CLI
    from cli.app import AIReelAgent
    app = AIReelAgent()
    asyncio.run(app.run())


def _legacy_mode(args):
    """Legacy CLI argument support for backward compatibility."""
    from cli.app import AIReelAgent
    app = AIReelAgent()

    count = 1
    force_topic = None

    if "--count" in args:
        idx = args.index("--count")
        if idx + 1 < len(args):
            try:
                count = int(args[idx + 1])
            except ValueError:
                print("Error: --count must be a number")
                return

    if "--topic" in args:
        idx = args.index("--topic")
        if idx + 1 < len(args):
            force_topic = args[idx + 1]

    # Run in batch mode with legacy args
    async def _run():
        from cli.startup import StartupScreen
        startup = StartupScreen(app.config)
        startup.display(app.console)

        batch_config = {
            "count": count,
            "force_topic": force_topic,
            "quality": "balanced",
            "mode": "standard",
        }

        import time
        results = []
        start_time = time.time()

        for i in range(count):
            try:
                script_data = app.scripts.get_random()
                if force_topic:
                    from config.scripts import get_scripts_by_topic
                    import random
                    scripts = get_scripts_by_topic(force_topic)
                    if scripts:
                        script_data = random.choice(scripts)

                reel_config = {
                    "script": script_data["text"],
                    "topic": script_data["topic"],
                    "mode": "standard",
                    "quality": "balanced",
                    "script_preview": script_data["text"][:80],
                    "voice_engine": "edge-tts",
                    "resolution": "1080x1920",
                }

                output = await app._execute_pipeline(reel_config)
                if output:
                    results.append(output)
            except Exception as e:
                app.console.print(f"  [red]Error: {e}[/]")

        elapsed = time.time() - start_time
        app.console.print(f"\n  Generated {len(results)}/{count} reels in {elapsed:.1f}s")

    asyncio.run(_run())


if __name__ == "__main__":
    main()
