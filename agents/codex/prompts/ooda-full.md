# Boyd's The Full Boyd Loop (act stage)

The master prompt. It runs a situation through the whole system, with orientation at the center where Boyd

Call `ooda_prompt` with key="full-boyd-loop" and situation="$ARGUMENTS" (or the active
loop's situation if no argument). Then run the returned prompt in full.

Record the findings with `ooda_record` at stage "act" before moving on.
