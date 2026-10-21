---
name: observe-audit
description: "Use when running Boyd's The Observation Audit (observe stage). Boyd's loop starts with Observe, and most people think they've done it because they looked. In his final"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, observe]
    category: productivity
---

# The Observation Audit

**Stage:** observe

Boyd's loop starts with Observe, and most people think they've done it because they looked. In his final diagram, observation feeds on unfolding circumstances, outside information, and your own actions interacting with the environment. Most of what you "observe" is already filtered by what you expect to see.

## Prompt

```
I'm trying to understand a situation clearly: [describe the situation: a market, a competitor, a team problem, a decision I'm facing].

Run Boyd's Observation stage on it:

1. List only raw observations. Facts, numbers, things that actually happened. No interpretation, no adjectives. If a line contains a judgment, flag it and rewrite it as a fact.
2. Now list what I am NOT observing. What information would exist about this situation that I haven't looked at? Who sees this from a different angle than me?
3. Which of my observations are stale? Boyd's loop is continuous. What did I observe months ago that I'm still treating as current?
4. Where am I observing my own actions? What has my behavior so far changed about the situation, and have I accounted for that?
5. Give me the three observations I should go collect this week before I make any decision.
```

## How to run it

- `ooda_prompt(key="observe-audit", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-observe` if a loop is open.
- Record the output with `ooda_record(loop_id, "observe", …)` before moving on.
