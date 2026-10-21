"""
prompts.py — the nine John Boyd prompts, verbatim.

Single source of truth: the bundled skills are generated from this module by
scripts/build_skills.py, and the ooda_prompt tool reads it directly. Edit here,
then re-run the build script.

Source: @heynavtoor's thread on John Boyd / OODA
(https://x.com/heynavtoor/status/2112546579328733660).
"""

import re

STAGES = ["observe", "orient", "decide", "act"]

# key -> {title, stage, why, prompt}
PROMPTS = {
    "observe-audit": {
        "title": "The Observation Audit",
        "stage": "observe",
        "why": (
            "Boyd's loop starts with Observe, and most people think they've done it "
            "because they looked. In his final diagram, observation feeds on unfolding "
            "circumstances, outside information, and your own actions interacting with "
            "the environment. Most of what you \"observe\" is already filtered by what "
            "you expect to see."
        ),
        "prompt": """I'm trying to understand a situation clearly: [describe the situation: a market, a competitor, a team problem, a decision I'm facing].

Run Boyd's Observation stage on it:

1. List only raw observations. Facts, numbers, things that actually happened. No interpretation, no adjectives. If a line contains a judgment, flag it and rewrite it as a fact.
2. Now list what I am NOT observing. What information would exist about this situation that I haven't looked at? Who sees this from a different angle than me?
3. Which of my observations are stale? Boyd's loop is continuous. What did I observe months ago that I'm still treating as current?
4. Where am I observing my own actions? What has my behavior so far changed about the situation, and have I accounted for that?
5. Give me the three observations I should go collect this week before I make any decision.""",
    },
    "orient-audit": {
        "title": "The Orientation Audit",
        "stage": "orient",
        "why": (
            "This is the one almost everyone skips. In Boyd's diagram every arrow runs "
            "through Orient. He described orientation as the product of genetic heritage, "
            "cultural tradition, previous experience, and new information, constantly "
            "destroyed and rebuilt. You don't lose because you decided slowly. You lose "
            "because you're oriented to a world that stopped existing."
        ),
        "prompt": """I want to audit the lens I'm using to read my situation: [describe your situation and what you currently believe about it].

Using Boyd's Orientation framework:

1. Map my orientation. What past experiences, industry culture, and assumptions are shaping how I read this? List them explicitly.
2. For each one, ask: when was this formed, and is the world it was formed in still here?
3. Where is there a mismatch between my orientation and the raw facts? Boyd argued that mismatches between your mental model and reality are where defeat begins. Name mine.
4. Which single assumption, if it turned out to be wrong, would change every decision downstream?
5. Rewrite my orientation in three sentences as if I had arrived in this situation today with no history. What do I see that the old orientation hid?""",
    },
    "destruction-creation": {
        "title": "Destruction and Creation (The Snowmobile)",
        "stage": "orient",
        "why": (
            "In 1976 Boyd wrote an essay arguing that every concept eventually mismatches "
            "reality and must be torn apart and rebuilt from its fragments. His thought "
            "experiment: take skis, an outboard motor, bicycle handlebars, and tank treads, "
            "break each machine down, and reassemble the parts into a snowmobile. New ideas "
            "come from fragments of old ones recombined across domains. Use this when your "
            "current approach keeps failing for the same reasons and incremental fixes "
            "aren't moving it."
        ),
        "prompt": """I'm stuck with an approach that isn't working: [describe the strategy, product, process, or plan].

Run Boyd's Destruction and Creation on it:

1. DESTRUCTION: Break my current approach into its component parts. List every assumption, mechanism, and piece it's built from.
2. For each part, state the domain it came from and whether it still fits the problem.
3. Pull parts from four unrelated fields: [name four domains, or choose them for me]. What does each field do well that my problem needs?
4. CREATION: Recombine. Build three new approaches from fragments of my old one plus fragments from the other fields. Describe each in one paragraph.
5. Which of the three resolves the mismatch I identified? Give me the first step to test it.""",
    },
    "mismatch-detector": {
        "title": "The Mismatch Detector",
        "stage": "orient",
        "why": (
            "Boyd argued that conflict is won by generating mismatches: gaps between what "
            "the other side expects and what actually happens, inside their own decision "
            "cycle. The same gaps exist inside your own plans. A mismatch you find first is "
            "an advantage. One your competitor or the market finds first is a loss."
        ),
        "prompt": """I'm operating in a competitive environment: [describe the competition, market, or opponent and my current plan].

Using Boyd's mismatch concept:

1. List the predictions my current plan depends on. What do I expect customers, competitors, or the market to do?
2. For each prediction, what has actually happened so far? Mark each one as confirmed, contradicted, or untested.
3. Where is the biggest gap between expectation and reality? That's my internal mismatch. What does it tell me about my orientation?
4. Now flip it. What does my competitor expect ME to do? Where can I act in a way they aren't prepared for, without taking on more risk than I can handle?
5. Give me one move that closes my own mismatch and one move that creates a mismatch for them.""",
    },
    "tempo": {
        "title": "Tempo and Fast Transients",
        "stage": "decide",
        "why": (
            "The popular reading of OODA is \"be faster.\" Boyd's actual point came from his "
            "Energy-Maneuverability work: what wins is not raw speed but the ability to "
            "change state quickly, what he called fast transients. He argued you want to "
            "operate at a faster tempo than the adversary so they are always responding to "
            "a situation that has already changed."
        ),
        "prompt": """I want to shorten my decision cycle in: [describe the area: product, content, sales, negotiation, a competitive race].

Using Boyd's tempo framework:

1. Map my current loop. How long does it take me to observe a change, update my read, decide, and act? Where does the time actually go?
2. Map the loop of the competitor or environment I'm up against. Where are they slower than me? Where are they faster?
3. Boyd valued fast transients over top speed. Where am I optimizing to move fast in one direction when I should be optimizing to change direction cheaply?
4. What decisions can I make reversible so I can act now and correct later instead of waiting for certainty?
5. Design a loop I can run weekly. What do I observe, what triggers a re-orientation, and what's the smallest action that resets the cycle?""",
    },
    "main-effort": {
        "title": "The Main Effort",
        "stage": "decide",
        "why": (
            "Boyd's rule for focus: pick the one effort that makes everything else easier "
            "or unnecessary, and make everything else support it. He took the idea from "
            "German doctrine, where it's called Schwerpunkt, and paired it with mission "
            "orders: leaders communicate intent, not step-by-step instructions, so people "
            "can act on their own when the situation shifts."
        ),
        "prompt": """I have multiple priorities competing for attention: [list them].

Using Boyd's Main Effort framework:

1. If only one of these can succeed this quarter, which one makes the others easier or unnecessary? That's the main effort. Defend the choice.
2. For every other priority, state in one sentence how it supports the main effort. If it doesn't, flag it for cutting or pausing.
3. Write my intent in two sentences: what we are trying to achieve and why. Something my team could use to make a decision at 11pm without asking me.
4. Where am I currently giving instructions when I should be giving intent? Where am I giving intent when the person actually needs instructions?
5. List what I will stop doing this week to protect the main effort.""",
    },
    "interaction-isolation": {
        "title": "Interaction and Isolation",
        "stage": "decide",
        "why": (
            "In a briefing titled \"Strategic Game of ? and ?\" Boyd reduced strategy to two "
            "words. Interaction: connect yourself to many centers of support, information, "
            "and allies. Isolation: cut the adversary off from theirs. He applied it across "
            "moral, mental, and physical dimensions. It works for a business, a career, or "
            "a negotiation."
        ),
        "prompt": """I want to improve my position against: [describe the competitor, incumbent, or opposing party] in [describe the arena].

Using Boyd's Interaction and Isolation framework:

1. INTERACTION: Who and what am I connected to? Customers, partners, communities, information sources. Where is my network thin?
2. Who could I connect with this month that would make my position harder to attack?
3. ISOLATION: Where does my competitor depend on something they don't control? A platform, a supplier, a narrative, a single customer segment?
4. Which of those dependencies can I legitimately weaken by being the better option, without doing anything that would damage my own credibility?
5. Across moral (trust), mental (clarity), and physical (resources), where is each of us strongest and weakest? Give me the one move that improves my weakest dimension.""",
    },
    "to-be-or-to-do": {
        "title": "To Be or To Do",
        "stage": "decide",
        "why": (
            "Coram records a speech Boyd gave to each of his protégés. The gist: one day "
            "you'll reach a fork. One path leads to being somebody, with the promotions and "
            "the good assignments, at the cost of compromise. The other leads to doing "
            "something that matters, often without recognition. Boyd made his choice and "
            "paid for it for 20 years."
        ),
        "prompt": """I'm facing a career or life decision: [describe it].

Using Boyd's To Be or To Do framework:

1. Describe the 'to be' version of this choice. What status, title, or approval does it give me? What compromises does it require?
2. Describe the 'to do' version. What would I actually build or change? What recognition would I give up?
3. Which compromises have I already made that I've been calling 'strategy'? List them honestly.
4. In ten years, which choice do I tell the story about? Which one do I avoid mentioning?
5. I don't want the comfortable answer. Give me the case for 'to do,' then tell me what it would cost me this year.""",
    },
    "full-boyd-loop": {
        "title": "The Full Boyd Loop",
        "stage": "act",
        "why": (
            "The master prompt. It runs a situation through the whole system, with "
            "orientation at the center where Boyd put it."
        ),
        "prompt": """I'm facing a critical situation: [describe your biggest current challenge: a launch, a competitor, a career move, a strategy that's stalling].

Run a full John Boyd analysis:

OBSERVE: What are the raw facts, and what am I not looking at?

ORIENT: What assumptions, history, and culture are shaping my read? Which ones are mismatched with reality?

DESTRUCTION AND CREATION: Break my current approach into parts. Recombine them with ideas from other fields into something new.

MISMATCH: Where does my plan expect something the world isn't doing? Where does my opponent expect something I don't have to do?

TEMPO: Where is my loop slow, and which decisions can become cheap to reverse?

MAIN EFFORT: What is the one effort that makes everything else easier, and what gets cut to protect it?

INTERACTION AND ISOLATION: Who should I connect with, and where is the other side dependent and exposed?

TO BE OR TO DO: Am I choosing this because it's right or because it's safe?

THE MOVE: Based on all of the above, what is the single decision I should make this week, what action resets my loop, and what observation tells me whether it worked?""",
    },
}

# Order the prompts are presented in.
ORDER = [
    "observe-audit",
    "orient-audit",
    "destruction-creation",
    "mismatch-detector",
    "tempo",
    "main-effort",
    "interaction-isolation",
    "to-be-or-to-do",
    "full-boyd-loop",
]


def get(key: str) -> dict | None:
    """Return a prompt record by key (accepts a stage name too)."""
    if key in PROMPTS:
        return PROMPTS[key]
    for k, v in PROMPTS.items():
        if v["stage"] == key:
            return v
    return None


def render(key: str, situation: str = "") -> str:
    """Return the prompt text, with the situation substituted into the first slot."""
    rec = get(key)
    if rec is None:
        return ""
    text = rec["prompt"]
    if situation:
        text = re.sub(r"\[[^\]]*\]", f"[{situation}]", text, count=1)
    return text
