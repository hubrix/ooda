# Boyd's The Mismatch Detector (orient stage)

Boyd argued that conflict is won by generating mismatches: gaps between what the other side expects and what

Call `ooda_prompt` with key="mismatch-detector" and situation="$ARGUMENTS" (or the active
loop's situation if no argument). Then run the returned prompt in full.

Record the findings with `ooda_record` at stage "orient" before moving on.
