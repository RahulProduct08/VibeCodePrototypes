import json
import sqlite3
import uuid
from pathlib import Path
from ir.models import RuleIR


DB_PATH = Path(__file__).parent.parent / "rules.db"


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                priority INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1,
                version INTEGER DEFAULT 1,
                ir_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_rule(rule: RuleIR) -> RuleIR:
    if not rule.id:
        rule = rule.model_copy(update={"id": str(uuid.uuid4())})
    with _conn() as conn:
        existing = conn.execute("SELECT version FROM rules WHERE id=?", (rule.id,)).fetchone()
        version = (existing["version"] + 1) if existing else 1
        conn.execute(
            """INSERT OR REPLACE INTO rules (id, name, description, priority, enabled, version, ir_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (rule.id, rule.name, rule.description, rule.priority,
             int(rule.enabled), version, rule.model_dump_json()),
        )
    return rule


def get_rule(rule_id: str) -> RuleIR | None:
    with _conn() as conn:
        row = conn.execute("SELECT ir_json FROM rules WHERE id=?", (rule_id,)).fetchone()
    return RuleIR.model_validate_json(row["ir_json"]) if row else None


def list_rules(enabled_only: bool = True) -> list[RuleIR]:
    query = "SELECT ir_json FROM rules"
    if enabled_only:
        query += " WHERE enabled=1"
    query += " ORDER BY priority DESC"
    with _conn() as conn:
        rows = conn.execute(query).fetchall()
    return [RuleIR.model_validate_json(r["ir_json"]) for r in rows]


def toggle_rule(rule_id: str, enabled: bool) -> None:
    with _conn() as conn:
        conn.execute("UPDATE rules SET enabled=? WHERE id=?", (int(enabled), rule_id))


def delete_rule(rule_id: str) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM rules WHERE id=?", (rule_id,))
