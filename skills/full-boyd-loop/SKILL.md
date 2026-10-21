---
name: full-boyd-loop
description: "Use when running Boyd's The Full Boyd Loop (act stage). The master prompt. It runs a situation through the whole system, with orientation at the center where Boyd"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, act]
    category: productivity
---

# The Full Boyd Loop

**Stage:** act

The master prompt. It runs a situation through the whole system, with orientation at the center where Boyd put it.

## Prompt

```
I'm facing a critical situation: [describe your biggest current challenge: a launch, a competitor, a career move, a strategy that's stalling].

Run a full John Boyd analysis:

OBSERVE: What are the raw facts, and what am I not looking at?

ORIENT: What assumptions, history, and culture are shaping my read? Which ones are mismatched with reality?

DESTRUCTION AND CREATION: Break my current approach into parts. Recombine them with ideas from other fields into something new.

MISMATCH: Where does my plan expect something the world isn't doing? Where does my opponent expect something I don't have to do?

TEMPO: Where is my loop slow, and which decisions can become cheap to reverse?

MAIN EFFORT: What is the one effort that makes everything else easier, and what gets cut to protect it?

INTERACTION AND ISOLATION: Who should I connect with, and where is the other side dependent and exposed?

TO BE OR TO DO: Am I choosing this because it's right or because it's safe?

THE MOVE: Based on all of the above, what is the single decision I should make this week, what action resets my loop, and what observation tells me whether it worked?
```

## How to run it

- `ooda_prompt(key="full-boyd-loop", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-full` if a loop is open.
- Record the output with `ooda_record(loop_id, "act", …)` before moving on.
