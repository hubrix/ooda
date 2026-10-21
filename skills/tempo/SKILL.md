---
name: tempo
description: "Use when running Boyd's Tempo and Fast Transients (decide stage). The popular reading of OODA is 'be faster.' Boyd's actual point came from his Energy-Maneuverability work:"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, decide]
    category: productivity
---

# Tempo and Fast Transients

**Stage:** decide

The popular reading of OODA is "be faster." Boyd's actual point came from his Energy-Maneuverability work: what wins is not raw speed but the ability to change state quickly, what he called fast transients. He argued you want to operate at a faster tempo than the adversary so they are always responding to a situation that has already changed.

## Prompt

```
I want to shorten my decision cycle in: [describe the area: product, content, sales, negotiation, a competitive race].

Using Boyd's tempo framework:

1. Map my current loop. How long does it take me to observe a change, update my read, decide, and act? Where does the time actually go?
2. Map the loop of the competitor or environment I'm up against. Where are they slower than me? Where are they faster?
3. Boyd valued fast transients over top speed. Where am I optimizing to move fast in one direction when I should be optimizing to change direction cheaply?
4. What decisions can I make reversible so I can act now and correct later instead of waiting for certainty?
5. Design a loop I can run weekly. What do I observe, what triggers a re-orientation, and what's the smallest action that resets the cycle?
```

## How to run it

- `ooda_prompt(key="tempo", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-tempo` if a loop is open.
- Record the output with `ooda_record(loop_id, "decide", …)` before moving on.
