---
name: interaction-isolation
description: "Use when running Boyd's Interaction and Isolation (decide stage). In a briefing titled 'Strategic Game of ? and ?' Boyd reduced strategy to two words. Interaction: connect"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, decide]
    category: productivity
---

# Interaction and Isolation

**Stage:** decide

In a briefing titled "Strategic Game of ? and ?" Boyd reduced strategy to two words. Interaction: connect yourself to many centers of support, information, and allies. Isolation: cut the adversary off from theirs. He applied it across moral, mental, and physical dimensions. It works for a business, a career, or a negotiation.

## Prompt

```
I want to improve my position against: [describe the competitor, incumbent, or opposing party] in [describe the arena].

Using Boyd's Interaction and Isolation framework:

1. INTERACTION: Who and what am I connected to? Customers, partners, communities, information sources. Where is my network thin?
2. Who could I connect with this month that would make my position harder to attack?
3. ISOLATION: Where does my competitor depend on something they don't control? A platform, a supplier, a narrative, a single customer segment?
4. Which of those dependencies can I legitimately weaken by being the better option, without doing anything that would damage my own credibility?
5. Across moral (trust), mental (clarity), and physical (resources), where is each of us strongest and weakest? Give me the one move that improves my weakest dimension.
```

## How to run it

- `ooda_prompt(key="interaction-isolation", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-isolate` if a loop is open.
- Record the output with `ooda_record(loop_id, "decide", …)` before moving on.
