"""
store.py — loop state on disk.

Loops and their stage entries live in a SQLite DB under the plugin data dir
(plugin_db), which survives `hermes plugins update` / `remove` and follows the
active profile. Never write state into the plugin install tree.
"""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone

from plugins.plugin_storage import plugin_db

PLUGIN_ID = "ooda"
STAGES = ["observe", "orient", "decide", "act"]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS loops (
    id          TEXT PRIMARY KEY,
    situation   TEXT NOT NULL,
    arena       TEXT NOT NULL DEFAULT '',
    stage       TEXT NOT NULL DEFAULT 'observe',
    status      TEXT NOT NULL DEFAULT 'open',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    loop_id     TEXT NOT NULL,
    stage       TEXT NOT NULL,
    content     TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_entries_loop ON entries(loop_id);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _conn():
    conn = plugin_db(PLUGIN_ID)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def create(situation: str, arena: str = "") -> dict:
    loop_id = uuid.uuid4().hex[:10]
    now = _now()
    conn = _conn()
    conn.execute(
        "INSERT INTO loops (id, situation, arena, stage, status, created_at, updated_at)"
        " VALUES (?, ?, ?, 'observe', 'open', ?, ?)",
        (loop_id, situation, arena, now, now),
    )
    conn.commit()
    return get(loop_id)


def get(loop_id: str) -> dict | None:
    conn = _conn()
    row = conn.execute("SELECT * FROM loops WHERE id = ?", (loop_id,)).fetchone()
    if row is None:
        return None
    loop = dict(row)
    loop["entries"] = [
        dict(r)
        for r in conn.execute(
            "SELECT stage, content, created_at FROM entries WHERE loop_id = ? ORDER BY id",
            (loop_id,),
        )
    ]
    return loop


def active() -> dict | None:
    conn = _conn()
    row = conn.execute(
        "SELECT id FROM loops WHERE status = 'open' ORDER BY updated_at DESC LIMIT 1"
    ).fetchone()
    return get(row["id"]) if row else None


def list_loops(limit: int = 20) -> list[dict]:
    conn = _conn()
    rows = conn.execute(
        "SELECT id, situation, arena, stage, status, created_at, updated_at"
        " FROM loops ORDER BY updated_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def record(loop_id: str, stage: str, content: str) -> dict | None:
    """Append an entry and advance the loop's stage pointer."""
    if stage not in STAGES:
        stage = "observe"
    conn = _conn()
    if conn.execute("SELECT 1 FROM loops WHERE id = ?", (loop_id,)).fetchone() is None:
        return None
    now = _now()
    conn.execute(
        "INSERT INTO entries (loop_id, stage, content, created_at) VALUES (?, ?, ?, ?)",
        (loop_id, stage, content, now),
    )
    idx = STAGES.index(stage)
    next_stage = STAGES[min(idx + 1, len(STAGES) - 1)]
    conn.execute(
        "UPDATE loops SET stage = ?, updated_at = ? WHERE id = ?",
        (next_stage, now, loop_id),
    )
    conn.commit()
    return get(loop_id)


def close(loop_id: str) -> dict | None:
    conn = _conn()
    if conn.execute("SELECT 1 FROM loops WHERE id = ?", (loop_id,)).fetchone() is None:
        return None
    conn.execute(
        "UPDATE loops SET status = 'closed', updated_at = ? WHERE id = ?",
        (_now(), loop_id),
    )
    conn.commit()
    return get(loop_id)


def reopen(loop_id: str) -> dict | None:
    conn = _conn()
    if conn.execute("SELECT 1 FROM loops WHERE id = ?", (loop_id,)).fetchone() is None:
        return None
    conn.execute(
        "UPDATE loops SET status = 'open', updated_at = ? WHERE id = ?",
        (_now(), loop_id),
    )
    conn.commit()
    return get(loop_id)
