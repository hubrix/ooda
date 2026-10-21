"""schemas.py — what the LLM reads to decide when to call each tool."""

_STAGE_ENUM = ["observe", "orient", "decide", "act"]

OODA_START = {
    "name": "ooda_start",
    "description": (
        "Open a new OODA loop on a situation. Creates a persistent loop record and "
        "returns its id plus the Observe-stage prompt. Use this when the user brings "
        "a decision, competitor, market, or stalled plan and wants Boyd's framework "
        "applied rather than a one-shot answer."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "situation": {
                "type": "string",
                "description": "The situation to run the loop on, in the user's own words.",
            },
            "arena": {
                "type": "string",
                "description": "Optional competitive arena / context (market, team, negotiation).",
            },
        },
        "required": ["situation"],
    },
}

OODA_PROMPT = {
    "name": "ooda_prompt",
    "description": (
        "Return one of the nine John Boyd prompts verbatim, ready to run. Keys: "
        "observe-audit, orient-audit, destruction-creation, mismatch-detector, tempo, "
        "main-effort, interaction-isolation, to-be-or-to-do, full-boyd-loop. A stage "
        "name (observe/orient/decide/act) also resolves to that stage's prompt."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "description": "Prompt key or stage name.",
                "enum": [
                    "observe-audit",
                    "orient-audit",
                    "destruction-creation",
                    "mismatch-detector",
                    "tempo",
                    "main-effort",
                    "interaction-isolation",
                    "to-be-or-to-do",
                    "full-boyd-loop",
                    "observe",
                    "orient",
                    "decide",
                    "act",
                ],
            },
            "situation": {
                "type": "string",
                "description": "Optional situation text to substitute into the prompt's first slot.",
            },
        },
        "required": ["key"],
    },
}

OODA_RECORD = {
    "name": "ooda_record",
    "description": (
        "Append a finding to an open loop at a given stage and advance the loop's "
        "stage pointer. Use after running a stage prompt, to persist what came out "
        "of it so later stages build on it."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "loop_id": {"type": "string", "description": "Loop id from ooda_start."},
            "stage": {"type": "string", "enum": _STAGE_ENUM, "description": "Stage this finding belongs to."},
            "content": {"type": "string", "description": "The finding, condensed to its substance."},
        },
        "required": ["loop_id", "stage", "content"],
    },
}

OODA_STATUS = {
    "name": "ooda_status",
    "description": (
        "Show a loop's situation, current stage, and every recorded entry. Omit "
        "loop_id for the most recent open loop."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "loop_id": {"type": "string", "description": "Loop id. Omit for the active loop."},
        },
        "required": [],
    },
}

OODA_MOVE = {
    "name": "ooda_move",
    "description": (
        "Record THE MOVE — the single decision, the action that resets the loop, and "
        "the observation that tells whether it worked — then close the loop. Use when "
        "the user has converged and is ready to act."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "loop_id": {"type": "string", "description": "Loop id from ooda_start."},
            "decision": {"type": "string", "description": "The single decision to make this week."},
            "action": {"type": "string", "description": "The action that resets the loop."},
            "observation": {"type": "string", "description": "What observation tells us whether it worked."},
        },
        "required": ["loop_id", "decision", "action", "observation"],
    },
}

OODA_LIST = {
    "name": "ooda_list",
    "description": "List recent OODA loops with their situation, stage, and status.",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {"type": "integer", "description": "Max loops to return (default 20)."},
        },
        "required": [],
    },
}
