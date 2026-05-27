"""AI Reel Agent v5.0 — Subtitle Engine
ASS subtitle generation with viral-style animations.
"""
import random
from config.profiles import ANIMATION_PRESETS, HIGHLIGHT_WORDS
from config.defaults import DEFAULT_CONFIG


class SubtitleEngine:
    """Generates ASS subtitle files with animation effects."""

    def __init__(self, config=None):
        if config:
            self.font_size = config.get("caption.font_size", DEFAULT_CONFIG["caption"]["font_size"])
            self.outline_width = config.get("caption.outline_width", DEFAULT_CONFIG["caption"]["outline_width"])
            self.alignment = config.get("caption.alignment", DEFAULT_CONFIG["caption"]["alignment"])
            self.margin_v = config.get("caption.margin_v", DEFAULT_CONFIG["caption"]["margin_v"])
        else:
            self.font_size = DEFAULT_CONFIG["caption"]["font_size"]
            self.outline_width = DEFAULT_CONFIG["caption"]["outline_width"]
            self.alignment = DEFAULT_CONFIG["caption"]["alignment"]
            self.margin_v = DEFAULT_CONFIG["caption"]["margin_v"]

    def pick_animation(self) -> dict:
        """Select and randomize an animation preset."""
        p = random.choice(ANIMATION_PRESETS)
        return {
            "name":       p["name"],
            "fade_in":    random.randint(*p["fade_in"]),
            "fade_out":   random.randint(*p["fade_out"]),
            "scale_up":   random.randint(*p["scale_up"]),
            "scale_time": random.randint(*p["scale_time"]),
        }

    def get_animation_presets(self) -> list:
        """List all animation preset names."""
        return [p["name"] for p in ANIMATION_PRESETS]

    def generate_ass(self, phrases, output_path, is_luxury=False) -> str:
        """Generate ASS subtitle file with viral-style animations."""
        fs = self.font_size
        mv = self.margin_v
        ow = self.outline_width
        al = self.alignment

        anim = self.pick_animation()
        # Luxury reels prefer slower, smoother subtitle animations
        if is_luxury and anim["name"] not in ("luxury_fade", "smooth_breathe"):
            for p in ANIMATION_PRESETS:
                if p["name"] == "luxury_fade":
                    anim = {
                        "name": "luxury_fade",
                        "fade_in":    random.randint(*p["fade_in"]),
                        "fade_out":   random.randint(*p["fade_out"]),
                        "scale_up":   random.randint(*p["scale_up"]),
                        "scale_time": random.randint(*p["scale_time"]),
                    }
                    break

        # Luxury gets gold accent instead of yellow
        hook_color = "&H0001D7FF" if is_luxury else "&H0000FFFF"
        hl_color   = "&H0000CCFF" if is_luxury else "&H0000DDFF"

        ass = f"""[Script Info]
Title: AI Reel Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,{fs},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,{ow},3,{al},40,40,{mv},1
Style: Hook,Arial Black,{fs+14},{hook_color},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,4,0,1,{ow+2},4,{al},40,40,{mv},1
Style: Highlight,Arial Black,{fs+6},{hl_color},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,{ow},3,{al},40,40,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        fi, fo, su, st = anim["fade_in"], anim["fade_out"], anim["scale_up"], anim["scale_time"]

        for i, p in enumerate(phrases):
            s_ts = self._fmt_ass(p["start"])
            e_ts = self._fmt_ass(p["end"])
            style = "Hook" if i < 2 else ("Highlight" if p.get("highlight") else "Default")
            fx = ("{\\fad(" + str(fi) + "," + str(fo) + ")"
                  "\\t(0," + str(st) + ",\\fscx" + str(su) + "\\fscy" + str(su) + ")"
                  "\\t(" + str(st) + "," + str(st*2) + ",\\fscx100\\fscy100)}"
                  + p["text"])
            ass += f"Dialogue: 0,{s_ts},{e_ts},{style},,0,0,0,,{fx}\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ass)
        return output_path

    @staticmethod
    def _fmt_ass(sec):
        """Format seconds to ASS timestamp H:MM:SS.CC"""
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int((sec % 1) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
