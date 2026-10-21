---
name: to-be-or-to-do
description: "Use when running Boyd's To Be or To Do (decide stage). Coram records a speech Boyd gave to each of his protégés. The gist: one day you'll reach a fork. One path"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, decide]
    category: productivity
---

# To Be or To Do

**Stage:** decide

Coram records a speech Boyd gave to each of his protégés. The gist: one day you'll reach a fork. One path leads to being somebody, with the promotions and the good assignments, at the cost of compromise. The other leads to doing something that matters, often without recognition. Boyd made his choice and paid for it for 20 years.

## Prompt

```
I'm facing a career or life decision: [describe it].

Using Boyd's To Be or To Do framework:

1. Describe the 'to be' version of this choice. What status, title, or approval does it give me? What compromises does it require?
2. Describe the 'to do' version. What would I actually build or change? What recognition would I give up?
3. Which compromises have I already made that I've been calling 'strategy'? List them honestly.
4. In ten years, which choice do I tell the story about? Which one do I avoid mentioning?
5. I don't want the comfortable answer. Give me the case for 'to do,' then tell me what it would cost me this year.
```

## How to run it

- `ooda_prompt(key="to-be-or-to-do", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-tobetodo` if a loop is open.
- Record the output with `ooda_record(loop_id, "decide", …)` before moving on.
