"""AI Reel Agent v5.0 — Script Manager"""
import os
from config.scripts import detect_topic, LUXURY_TOPICS, MINECRAFT_TOPICS
from core.script_composer import ScriptComposer
from core.utils.paths import get_exe_dir


class ScriptManager:
    """Manages modular phrase composition and topic detection, wrapping ScriptComposer."""

    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = get_exe_dir()
        self.composer = ScriptComposer(project_root)

    def get_random(self) -> dict:
        """Compose and return a random script."""
        topic = self.composer.get_random_topic()
        return self.composer.compose(topic)

    def get_by_topic(self, topic: str, count: int = 5) -> list:
        """Generate a list of unique composed scripts for a topic."""
        scripts = []
        seen = set()
        # Prevent duplicates
        for _ in range(count * 4):
            s = self.composer.compose(topic)
            if s["text"] not in seen:
                seen.add(s["text"])
                scripts.append(s)
                if len(scripts) >= count:
                    break
        return scripts

    def get_topics(self) -> list:
        """Return all available topics."""
        return self.composer.topics.copy()

    def detect_topic(self, text: str) -> str:
        """Auto-detect topic from script text by keyword scoring."""
        return detect_topic(text)

    def use_custom(self, text: str, topic: str = None) -> dict:
        """Wrap user text as a script dictionary."""
        if topic is None:
            topic = self.detect_topic(text)
        return {"topic": topic, "text": text}

    def list_scripts(self) -> list:
        """Return a dynamic list of composed scripts (2 examples per topic)."""
        scripts = []
        for topic in self.composer.topics:
            scripts.extend(self.get_by_topic(topic, count=2))
        return scripts

    def is_luxury(self, topic: str) -> bool:
        """Check if topic uses luxury style."""
        return topic in LUXURY_TOPICS

    def is_minecraft(self, topic: str) -> bool:
        """Check if topic uses minecraft style."""
        return topic in MINECRAFT_TOPICS

    def get_topic_counts(self) -> dict:
        """Return the virtual count of scripts per topic."""
        return {t: 5 for t in self.composer.topics}
