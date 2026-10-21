# Boyd's The Observation Audit (observe stage)

Boyd's loop starts with Observe, and most people think they've done it because they looked. In his final

Call `ooda_prompt` with key="observe-audit" and situation="$ARGUMENTS" (or the active
loop's situation if no argument). Then run the returned prompt in full.

Record the findings with `ooda_record` at stage "observe" before moving on.
