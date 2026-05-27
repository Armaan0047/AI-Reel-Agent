"""
AI Reel Agent v5.0 — Variation Engine
Applies synonym substitutions, pacing elements, CTAs, and body shuffling
while maintaining perfect grammatical readability and flow.
"""
import re
import random

SYNONYMS = {
    "system": ["matrix", "machine", "distraction program", "social mechanism"],
    "nobody": ["no one", "absolutely no one", "not a single soul"],
    "dangerous": ["lethal", "unstoppable", "highly formidable", "menacing"],
    "wealth": ["absolute freedom", "prosperity", "leverage", "generational power"],
    "grind": ["hustle", "relentless daily execution", "silent build"],
    "scared": ["terrified", "deeply concerned", "panicked"],
    "future": ["next chapter", "tomorrow", "destiny"],
    "sleeping": ["resting", "unaware", "distracted"],
    "empire": ["legacy", "kingdom", "sovereign build"],
    "discipline": ["unwavering focus", "relentless execution", "self-mastery"],
    "comfort zone": ["bubble of safety", "prison of comfort", "slow death of average"],
    "start": ["take the leap", "begin the build", "take immediate action"],
    "rich": ["wealthy", "financially free", "sovereign"],
    "average": ["mediocre", "ordinary", "part of the crowd"],
    "party": ["chase temporary thrills", "waste their energy", "fool around"]
}

CTAS = [
    "Save this video to watch it daily.",
    "Follow for more real talks.",
    "Share this with someone who needs to wake up.",
    "Comment 'READY' if you are with me.",
    "Save this and watch it whenever you lose focus."
]

TRANSITIONS = [
    "Here is the raw truth: ",
    "Listen to me... ",
    "Read that again. ",
    "Let this sink in. "
]

class VariationEngine:
    """Dynamically applies high-impact variations to script text."""

    def __init__(self, synonym_prob: float = 0.3, pacing_prob: float = 0.25, cta_prob: float = 0.7):
        self.synonym_prob = synonym_prob
        self.pacing_prob = pacing_prob
        self.cta_prob = cta_prob

    def apply_variation(self, hook: str, bodies: list, ending: str, seed: int = None) -> str:
        """
        Apply full variation to a script composition.
        Performs sentence shuffling, synonym swapping, pacing adjustments, and appends a CTA.
        Uses a local Random instance for determinism.
        """
        r = random.Random(seed) if seed is not None else random
        
        # 1. Copy body sentences and optionally shuffle them
        varied_bodies = bodies.copy()
        if len(varied_bodies) > 1 and r.random() < 0.6:
            r.shuffle(varied_bodies)

        # 2. Apply synonym substitutions to all phrases
        hook = self._substitute_synonyms(hook, r)
        varied_bodies = [self._substitute_synonyms(b, r) for b in varied_bodies]
        ending = self._substitute_synonyms(ending, r)

        # 3. Apply pacing variations
        # Optionally prepend a dramatic transition to the body
        if varied_bodies and r.random() < self.pacing_prob:
            transition = r.choice(TRANSITIONS)
            varied_bodies[0] = f"{transition}{varied_bodies[0][0].lower()}{varied_bodies[0][1:]}"

        # 4. Assemble the script
        body_text = " ".join(varied_bodies)
        full_text = f"{hook} {body_text} {ending}"

        # 5. Append Call to Action
        if r.random() < self.cta_prob:
            cta = r.choice(CTAS)
            # Ensure proper sentence boundary spacing
            if not full_text.endswith(" "):
                full_text += " "
            full_text += cta

        return full_text

    def _substitute_synonyms(self, text: str, r_inst) -> str:
        """Scan text and replace keywords with high-impact synonyms case-sensitively."""
        for keyword, synonym_list in SYNONYMS.items():
            if keyword in text.lower():
                # Apply replacement with a probability threshold
                if r_inst.random() < self.synonym_prob:
                    synonym = r_inst.choice(synonym_list)
                    text = self._replace_preserve_case(text, keyword, synonym)
        return text

    @staticmethod
    def _replace_preserve_case(text: str, keyword: str, replacement: str) -> str:
        """Replace target word using exact regex boundaries while preserving capitalization."""
        def repl(match):
            matched = match.group(0)
            if matched.isupper():
                return replacement.upper()
            if matched[0].isupper():
                # Handle multi-word replacements case-sensitively on first word
                words = replacement.split()
                words[0] = words[0][0].upper() + words[0][1:]
                return " ".join(words)
            return replacement.lower()

        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        return pattern.sub(repl, text)
