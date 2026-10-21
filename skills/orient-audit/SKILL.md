---
name: orient-audit
description: "Use when running Boyd's The Orientation Audit (orient stage). This is the one almost everyone skips. In Boyd's diagram every arrow runs through Orient. He described"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, orient]
    category: productivity
---

# The Orientation Audit

**Stage:** orient

This is the one almost everyone skips. In Boyd's diagram every arrow runs through Orient. He described orientation as the product of genetic heritage, cultural tradition, previous experience, and new information, constantly destroyed and rebuilt. You don't lose because you decided slowly. You lose because you're oriented to a world that stopped existing.

## Prompt

```
I want to audit the lens I'm using to read my situation: [describe your situation and what you currently believe about it].

Using Boyd's Orientation framework:

1. Map my orientation. What past experiences, industry culture, and assumptions are shaping how I read this? List them explicitly.
2. For each one, ask: when was this formed, and is the world it was formed in still here?
3. Where is there a mismatch between my orientation and the raw facts? Boyd argued that mismatches between your mental model and reality are where defeat begins. Name mine.
4. Which single assumption, if it turned out to be wrong, would change every decision downstream?
5. Rewrite my orientation in three sentences as if I had arrived in this situation today with no history. What do I see that the old orientation hid?
```

## How to run it

- `ooda_prompt(key="orient-audit", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-orient` if a loop is open.
- Record the output with `ooda_record(loop_id, "orient", …)` before moving on.
