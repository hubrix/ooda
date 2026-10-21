---
name: mismatch-detector
description: "Use when running Boyd's The Mismatch Detector (orient stage). Boyd argued that conflict is won by generating mismatches: gaps between what the other side expects and what"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, orient]
    category: productivity
---

# The Mismatch Detector

**Stage:** orient

Boyd argued that conflict is won by generating mismatches: gaps between what the other side expects and what actually happens, inside their own decision cycle. The same gaps exist inside your own plans. A mismatch you find first is an advantage. One your competitor or the market finds first is a loss.

## Prompt

```
I'm operating in a competitive environment: [describe the competition, market, or opponent and my current plan].

Using Boyd's mismatch concept:

1. List the predictions my current plan depends on. What do I expect customers, competitors, or the market to do?
2. For each prediction, what has actually happened so far? Mark each one as confirmed, contradicted, or untested.
3. Where is the biggest gap between expectation and reality? That's my internal mismatch. What does it tell me about my orientation?
4. Now flip it. What does my competitor expect ME to do? Where can I act in a way they aren't prepared for, without taking on more risk than I can handle?
5. Give me one move that closes my own mismatch and one move that creates a mismatch for them.
```

## How to run it

- `ooda_prompt(key="mismatch-detector", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-mismatch` if a loop is open.
- Record the output with `ooda_record(loop_id, "orient", …)` before moving on.
