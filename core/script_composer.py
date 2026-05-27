"""
AI Reel Agent v5.0 — Script Composer
Modular phrase assembly engine with duplicate prevention and deterministic seed support.
Integrates itertools-based combinatorial template expansion and VariationEngine.
"""
import os
import json
import random
import re
import itertools

from core.variation_engine import VariationEngine
from core.utils.paths import resource_path

DEFAULT_POOLS = {
    "motivation": {
        "hooks": ["Nobody is coming to save you. Read that again."],
        "body": ["While you were sleeping, someone was building their empire."],
        "endings": ["Be the one percent that actually takes action today."]
    }
}

class ScriptComposer:
    """Composes dynamic scripts by expanding modular phrase templates."""

    def __init__(self, project_root: str):
        self.project_root = os.path.abspath(project_root)
        self.scripts_dir = resource_path("scripts")
        self.topics = ["motivation", "sigma", "luxury", "dark_psych", "ai_tech", "cybersecurity", "student", "money"]
        self.pools = {}
        self.variation_engine = VariationEngine()
        self.load_pools()

    def load_pools(self):
        """Load phrase pools from templates.json files, expanding them combinatorially."""
        for topic in self.topics:
            topic_dir = os.path.join(self.scripts_dir, topic)
            self.pools[topic] = {
                "hooks": [],
                "body": [],
                "endings": []
            }

            templates_path = os.path.join(topic_dir, "templates.json")
            if os.path.exists(templates_path):
                try:
                    with open(templates_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                    for pool_name in ["hooks", "body", "endings"]:
                        if pool_name in data:
                            pool_data = data[pool_name]
                            templates = pool_data.get("templates", [])
                            replacements = pool_data.get("replacements", {})
                            
                            expanded_list = []
                            for template in templates:
                                expanded_list.extend(self._expand_template(template, replacements))
                            
                            if expanded_list:
                                self.pools[topic][pool_name] = expanded_list
                except Exception:
                    pass

            # Fallback to default/starter JSON lists if template load failed or is empty
            for pool_name in ["hooks", "body", "endings"]:
                if not self.pools[topic][pool_name]:
                    # Fallback to loading from legacy hooks.json/body.json/endings.json
                    file_path = os.path.join(topic_dir, f"{pool_name}.json")
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                list_data = json.load(f)
                                if isinstance(list_data, list) and len(list_data) > 0:
                                    self.pools[topic][pool_name] = list_data
                        except Exception:
                            pass

                # Ultimate hardcoded fallback
                if not self.pools[topic][pool_name]:
                    self.pools[topic][pool_name] = DEFAULT_POOLS.get(
                        topic, DEFAULT_POOLS["motivation"]
                    )[pool_name].copy()

    def compose(self, topic: str, num_body: int = 1, variation: bool = True, seed: int = None) -> dict:
        """
        Assemble a unique, natural-sounding script.
        Combines 1 hook + body phrases + 1 ending, then optionally applies variation.
        Uses a local Random instance to preserve isolated determinism.
        """
        if topic not in self.pools:
            topic = "motivation"

        pool = self.pools[topic]
        r = random.Random(seed) if seed is not None else random

        hook = r.choice(pool["hooks"])
        
        # Prevent duplicates of the same body sentence in a single script
        bodies = pool["body"]
        num_body = min(len(bodies), num_body)
        body_phrases = r.sample(bodies, num_body)
        
        ending = r.choice(pool["endings"])

        if variation:
            text = self.variation_engine.apply_variation(hook, body_phrases, ending, seed=seed)
        else:
            text = f"{hook} {' '.join(body_phrases)} {ending}"

        return {
            "topic": topic,
            "text": text
        }

    def get_random_topic(self, seed: int = None) -> str:
        """Pick a topic using weighted topic selection (default equal weights)."""
        r = random.Random(seed) if seed is not None else random
        return r.choice(self.topics)

    def _expand_template(self, template_str: str, replacements: dict) -> list:
        """Parse placeholder tags and generate cartesian product combinations."""
        placeholders = re.findall(r'\{([^{}]+)\}', template_str)
        if not placeholders:
            return [template_str]

        # Map placeholders to their replacement lists
        lists = []
        for p in placeholders:
            if p in replacements:
                lists.append(replacements[p])
            else:
                lists.append([""]) # Empty fallback for unknown keys

        # Generate combinations
        expanded = []
        for combo in itertools.product(*lists):
            formatted = template_str
            for p, val in zip(placeholders, combo):
                formatted = formatted.replace("{" + p + "}", val)
            expanded.append(formatted)
        return expanded
