---
name: main-effort
description: "Use when running Boyd's The Main Effort (decide stage). Boyd's rule for focus: pick the one effort that makes everything else easier or unnecessary, and make"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, decide]
    category: productivity
---

# The Main Effort

**Stage:** decide

Boyd's rule for focus: pick the one effort that makes everything else easier or unnecessary, and make everything else support it. He took the idea from German doctrine, where it's called Schwerpunkt, and paired it with mission orders: leaders communicate intent, not step-by-step instructions, so people can act on their own when the situation shifts.

## Prompt

```
I have multiple priorities competing for attention: [list them].

Using Boyd's Main Effort framework:

1. If only one of these can succeed this quarter, which one makes the others easier or unnecessary? That's the main effort. Defend the choice.
2. For every other priority, state in one sentence how it supports the main effort. If it doesn't, flag it for cutting or pausing.
3. Write my intent in two sentences: what we are trying to achieve and why. Something my team could use to make a decision at 11pm without asking me.
4. Where am I currently giving instructions when I should be giving intent? Where am I giving intent when the person actually needs instructions?
5. List what I will stop doing this week to protect the main effort.
```

## How to run it

- `ooda_prompt(key="main-effort", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-effort` if a loop is open.
- Record the output with `ooda_record(loop_id, "decide", …)` before moving on.
