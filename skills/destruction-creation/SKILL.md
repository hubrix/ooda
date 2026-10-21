---
name: destruction-creation
description: "Use when running Boyd's Destruction and Creation (The Snowmobile) (orient stage). In 1976 Boyd wrote an essay arguing that every concept eventually mismatches reality and must be torn apart"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, orient]
    category: productivity
---

# Destruction and Creation (The Snowmobile)

**Stage:** orient

In 1976 Boyd wrote an essay arguing that every concept eventually mismatches reality and must be torn apart and rebuilt from its fragments. His thought experiment: take skis, an outboard motor, bicycle handlebars, and tank treads, break each machine down, and reassemble the parts into a snowmobile. New ideas come from fragments of old ones recombined across domains. Use this when your current approach keeps failing for the same reasons and incremental fixes aren't moving it.

## Prompt

```
I'm stuck with an approach that isn't working: [describe the strategy, product, process, or plan].

Run Boyd's Destruction and Creation on it:

1. DESTRUCTION: Break my current approach into its component parts. List every assumption, mechanism, and piece it's built from.
2. For each part, state the domain it came from and whether it still fits the problem.
3. Pull parts from four unrelated fields: [name four domains, or choose them for me]. What does each field do well that my problem needs?
4. CREATION: Recombine. Build three new approaches from fragments of my old one plus fragments from the other fields. Describe each in one paragraph.
5. Which of the three resolves the mismatch I identified? Give me the first step to test it.
```

## How to run it

- `ooda_prompt(key="destruction-creation", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-destroy` if a loop is open.
- Record the output with `ooda_record(loop_id, "orient", …)` before moving on.
