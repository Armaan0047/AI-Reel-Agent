"""
AI Reel Agent v5.0 — Viral Script Library
31 viral scripts tagged with topics, plus topic detection system.
Extracted from legacy config.py — all scripts preserved exactly.
"""
import random


# ══════════════════════════════════════════════════════════════════
#  TOPIC SYSTEM — Dual-style routing
# ══════════════════════════════════════════════════════════════════

LUXURY_TOPICS = {"luxury", "sigma_luxury"}

MINECRAFT_TOPICS = {
    "ai_tech", "cybersecurity", "motivation", "dark_psych",
    "money", "society", "sigma", "student", "pov", "harsh_truth",
}

TOPIC_KEYWORDS = {
    "ai_tech":       ["AI", "robot", "automat", "code", "program", "technology", "machine", "algorithm"],
    "cybersecurity": ["hack", "dark web", "password", "data", "privacy", "tracking", "leaked"],
    "motivation":    ["grind", "discipline", "hustle", "empire", "comfort zone", "sacrifice", "dream"],
    "dark_psych":    ["manipulat", "psychology", "dopamine", "exploit", "programmed", "obedience"],
    "money":         ["money", "rich", "rat race", "nine to five", "financial", "debt"],
    "society":       ["generation", "cooked", "attention span", "social media", "distract"],
    "sigma":         ["sigma", "silence", "results", "dangerous", "alone", "chase"],
    "student":       ["classmate", "study", "school", "student", "boss", "boring"],
    "pov":           ["POV", "pov", "realize", "stopped caring", "deleted the apps"],
    "harsh_truth":   ["harsh", "truth", "owe", "degree", "talent", "loneliness"],
    "luxury":        ["luxury", "lambo", "yacht", "penthouse", "billionaire", "private jet",
                      "ferrari", "rolex", "lifestyle", "mansion", "supercar", "wealth",
                      "expensive", "first class", "champagne"],
    "sigma_luxury":  ["sigma billionaire", "luxury sigma", "rich mindset", "wealthy discipline"],
}


def detect_topic(text: str) -> str:
    """Auto-detect topic from script text by keyword scoring."""
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[topic] = score
    return max(scores, key=scores.get) if scores else "motivation"


def get_random_script() -> dict:
    """Return a random script from the library."""
    return random.choice(VIRAL_SCRIPTS)


def get_scripts_by_topic(topic: str) -> list:
    """Return all scripts matching a given topic."""
    return [s for s in VIRAL_SCRIPTS if s["topic"] == topic]


def get_all_topics() -> list:
    """Return sorted list of all unique topics in the script library."""
    return sorted(set(s["topic"] for s in VIRAL_SCRIPTS))


# ══════════════════════════════════════════════════════════════════
#  VIRAL SCRIPT LIBRARY — 31 scripts tagged with topics
# ══════════════════════════════════════════════════════════════════

VIRAL_SCRIPTS = [
    # ─── AI Revolution ───────────────────────────────────────────
    {"topic": "ai_tech", "text":
     "Nobody tells you this. AI is replacing jobs faster than you think. "
     "What took humans years... now takes seconds. "
     "And the scariest part? We are just getting started. "
     "Adapt or become irrelevant. There is no middle ground."},
    {"topic": "ai_tech", "text":
     "The system was designed to keep you busy. "
     "While you scroll... AI is learning everything. "
     "It writes code. Creates art. Builds companies. "
     "And it never sleeps. Wake up... before it's too late."},
    {"topic": "ai_tech", "text":
     "AI just did in five seconds... what took a team two weeks. "
     "Programmers are scared. Designers are worried. Writers are panicking. "
     "But here is the truth nobody wants to hear. "
     "The ones who learn AI... will control everything."},
    {"topic": "ai_tech", "text":
     "You are being replaced... right now. "
     "AI is studying your job. Your patterns. Your skills. "
     "In three years, half of today's jobs won't exist. "
     "This isn't fear. This is a fact. Choose wisely."},
    {"topic": "ai_tech", "text":
     "Stop scrolling. This AI cheat code is literally unfair. "
     "People are using this secret tool to do 50 hours of work in 5 minutes. "
     "And the best part? It's completely free. "
     "If you don't use this, you are actually throwing money away."},
    {"topic": "ai_tech", "text":
     "Everyone is sleeping on this AI hack. "
     "While they complain about the job market, smart people are automating everything. "
     "I literally built a business in 30 minutes using one prompt. "
     "Wake up before you get left completely behind."},

    # ─── Cybersecurity ───────────────────────────────────────────
    {"topic": "cybersecurity", "text":
     "Hackers can break into your phone... in under sixty seconds. "
     "Your password? Already leaked on the dark web. "
     "Every app you use is tracking everything you do. "
     "You are not the user. You are the product."},
    {"topic": "cybersecurity", "text":
     "The internet knows more about you... than your best friend does. "
     "Every search. Every click. Every pause on a video. "
     "Algorithms are building a digital version of you. "
     "And they are using it... to predict your next move."},

    # ─── Motivation ──────────────────────────────────────────────
    {"topic": "motivation", "text":
     "Everyone wants the lifestyle... but nobody wants the grind. "
     "They see the results but ignore the sacrifice. "
     "While you were sleeping, someone was building their empire. "
     "Discipline is choosing between what you want now... and what you want most."},
    {"topic": "motivation", "text":
     "Nobody is coming to save you. Read that again. "
     "Your parents can not guide you through a world they never experienced. "
     "School did not prepare you for this. "
     "The only person who can change your life... is staring at your screen right now."},
    {"topic": "motivation", "text":
     "Your comfort zone is the most dangerous place you can be. "
     "Every day you stay comfortable... someone hungry is catching up. "
     "Pain is temporary. Regret is forever. "
     "Choose the pain of discipline... over the pain of regret."},
    {"topic": "motivation", "text":
     "Bro, listen to me. 99% of people will watch this and do nothing. "
     "They will keep scrolling. Keep complaining. Keep making excuses. "
     "Be the 1% that actually takes action today. "
     "Your future self is literally begging you to start."},

    # ─── Dark Psychology ─────────────────────────────────────────
    {"topic": "dark_psych", "text":
     "You are being manipulated... every single day. "
     "Social media is designed to keep you addicted. "
     "Every notification is a dopamine hit... calculated by algorithms. "
     "They do not want you focused. They want you distracted."},
    {"topic": "dark_psych", "text":
     "They programmed you to be average. "
     "School taught you to follow rules... not break them. "
     "Society rewards obedience, not intelligence. "
     "The moment you realize this... everything changes."},

    # ─── Sigma Mindset ───────────────────────────────────────────
    {"topic": "sigma", "text":
     "Discipline is not motivation. Motivation disappears. "
     "Discipline is doing what needs to be done... when you feel nothing. "
     "The world belongs to those who show up every single day. "
     "No excuses. No breaks. No mercy."},
    {"topic": "sigma", "text":
     "Stop telling people your plans. "
     "Show them your results instead. "
     "The silent ones are always the most dangerous. "
     "Build in the dark. Shine in the light."},

    # ─── Money / Rat Race ────────────────────────────────────────
    {"topic": "money", "text":
     "Smart people are leaving the rat race. "
     "They realized working nine to five... makes someone else rich. "
     "Your time is being traded for pennies. "
     "The system was designed to keep you just comfortable enough... to never leave."},
    {"topic": "money", "text":
     "You were born into a system that profits from your confusion. "
     "They want you in debt. They want you consuming. "
     "Financial freedom starts with one simple truth. "
     "If you do not build your own dream... someone will hire you to build theirs."},
    {"topic": "money", "text":
     "The biggest lie you've been sold is that saving money makes you rich. "
     "Inflation is literally eating your bank account alive. "
     "Rich people don't save money. They buy assets that print money. "
     "Stop playing the game by their rules, because you are designed to lose."},

    # ─── Society ─────────────────────────────────────────────────
    {"topic": "society", "text":
     "This generation is cooked. And I mean that seriously. "
     "Attention spans shorter than goldfish. "
     "Everyone wants success but nobody can focus for ten minutes. "
     "You are competing against people... who deleted social media."},
    {"topic": "society", "text":
     "You are being distracted on purpose. "
     "While you watch reels... someone your age is learning skills. "
     "While you argue online... someone is building a business. "
     "Time is the only thing... you can never get back."},

    # ─── Student / Self-Improvement ──────────────────────────────
    {"topic": "student", "text":
     "While your classmates party... you study. "
     "While they sleep... you grind. "
     "They will call you boring now. "
     "They will call you boss... in five years."},
    {"topic": "student", "text":
     "The best investment you will ever make... is in yourself. "
     "Not stocks. Not crypto. Not real estate. "
     "A sharp mind and relentless discipline will outperform everything. "
     "Invest in skills that can not be taken away."},

    # ─── POV Style ───────────────────────────────────────────────
    {"topic": "pov", "text":
     "POV: You stopped caring what people think. "
     "You deleted the apps that wasted your time. "
     "You started waking up at five AM. "
     "And slowly... everything in your life started changing."},
    {"topic": "pov", "text":
     "POV: You realize your parents sacrificed everything for you. "
     "They worked jobs they hated... so you could dream. "
     "And you are sitting here... wasting the opportunity. "
     "This is your sign to make it count."},

    # ─── Harsh Truth ─────────────────────────────────────────────
    {"topic": "harsh_truth", "text":
     "Harsh truth. Most people will never achieve their dreams. "
     "Not because they can not. But because they will not. "
     "Talent is common. Discipline is rare. "
     "The gap between dreaming and doing... is called action."},
    {"topic": "harsh_truth", "text":
     "Loneliness is not being alone. "
     "Loneliness is being surrounded by people who do not understand you. "
     "The path to greatness is walked alone. "
     "Embrace the silence. That is where growth lives."},

    # ═══ LUXURY / BILLIONAIRE ════════════════════════════════════
    {"topic": "luxury", "text":
     "While they argue about prices... you compare private jets. "
     "While they save for shoes... you invest in assets. "
     "Luxury is not a dream. It is a decision. "
     "And that decision starts... right now."},
    {"topic": "luxury", "text":
     "Most people will never sit in a first class seat. "
     "Most people will never drive a car worth six figures. "
     "Not because they can not afford it... "
     "but because they were never taught to think that big."},
    {"topic": "luxury", "text":
     "The billionaire mindset is simple. "
     "Buy assets. Build systems. Protect your time. "
     "While everyone is chasing trends... "
     "the wealthy are building generational empires in silence."},
    {"topic": "luxury", "text":
     "Look at this. This isn't luck. This is obsession. "
     "You don't get this lifestyle by working 9 to 5 and hoping for a raise. "
     "You get this by taking insane risks and outworking everybody else. "
     "The choice is literally yours."},
    {"topic": "luxury", "text":
     "Your environment determines your net worth. "
     "Surround yourself with people who talk about investments... not gossip. "
     "Luxury is not about showing off. "
     "Luxury is about freedom. And freedom... is the ultimate currency."},
    {"topic": "luxury", "text":
     "They laughed when you said you would be rich. "
     "They stopped laughing when you pulled up in a Lamborghini. "
     "Success is the best revenge. "
     "Let your lifestyle do the talking."},
    {"topic": "sigma_luxury", "text":
     "A sigma does not flex. A sigma lets results speak. "
     "The penthouse. The watch. The portfolio. "
     "All built in silence while everyone was busy being loud. "
     "Discipline plus patience... equals wealth."},
    {"topic": "sigma_luxury", "text":
     "They ask how you afford it. You do not answer. "
     "Sigma rule. Never reveal your income. "
     "Let them wonder while you build your empire. "
     "The quiet ones always win."},
    {"topic": "luxury", "text":
     "Five AM. Empty roads. You and your goals. "
     "While the world sleeps... you compound your wealth. "
     "Every hour before sunrise is an investment. "
     "The rich understand what the poor never will... time is money."},
]
