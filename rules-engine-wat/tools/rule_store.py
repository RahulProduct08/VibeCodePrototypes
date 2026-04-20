import os
import uuid
from sqlalchemy import create_engine, text
from ir.models import RuleIR

_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rules.db")
# Railway/Render provide postgres:// but SQLAlchemy requires postgresql://
if _DATABASE_URL.startswith("postgres://"):
    _DATABASE_URL = _DATABASE_URL.replace("postgres://", "postgresql://", 1)

_connect_args = {"check_same_thread": False} if _DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(_DATABASE_URL, connect_args=_connect_args)

_CREATE_TABLE = """
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
"""


def init_db() -> None:
    with engine.connect() as conn:
        conn.execute(text(_CREATE_TABLE))
        conn.commit()


def save_rule(rule: RuleIR) -> RuleIR:
    if not rule.id:
        rule = rule.model_copy(update={"id": str(uuid.uuid4())})
    with engine.connect() as conn:
        row = conn.execute(text("SELECT version FROM rules WHERE id=:id"), {"id": rule.id}).fetchone()
        version = (row[0] + 1) if row else 1
        conn.execute(
            text("""
                INSERT INTO rules (id, name, description, priority, enabled, version, ir_json)
                VALUES (:id, :name, :desc, :priority, :enabled, :version, :ir_json)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name, description=excluded.description,
                    priority=excluded.priority, enabled=excluded.enabled,
                    version=excluded.version, ir_json=excluded.ir_json
            """),
            {
                "id": rule.id, "name": rule.name, "desc": rule.description,
                "priority": rule.priority, "enabled": int(rule.enabled),
                "version": version, "ir_json": rule.model_dump_json(),
            },
        )
        conn.commit()
    return rule


def get_rule(rule_id: str) -> RuleIR | None:
    with engine.connect() as conn:
        row = conn.execute(text("SELECT ir_json FROM rules WHERE id=:id"), {"id": rule_id}).fetchone()
    return RuleIR.model_validate_json(row[0]) if row else None


def list_rules(enabled_only: bool = True) -> list[RuleIR]:
    query = "SELECT ir_json FROM rules"
    if enabled_only:
        query += " WHERE enabled=1"
    query += " ORDER BY priority DESC"
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()
    return [RuleIR.model_validate_json(r[0]) for r in rows]


def toggle_rule(rule_id: str, enabled: bool) -> None:
    with engine.connect() as conn:
        conn.execute(text("UPDATE rules SET enabled=:e WHERE id=:id"), {"e": int(enabled), "id": rule_id})
        conn.commit()


def delete_rule(rule_id: str) -> None:
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM rules WHERE id=:id"), {"id": rule_id})
        conn.commit()
