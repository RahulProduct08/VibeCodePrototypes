# AI-Native Rules Engine

WAT architecture: **Workflow-driven, Agent-assisted, Tool-executed** decision system.

## Architecture

```
User Input (NL)
    ↓
[Agent] NL Parser (Claude) → RuleIR (JSON)
    ↓
[Agent] Validator (Claude) → errors / warnings
    ↓
[Tool]  Rule Store (SQLite) → versioned rules
    ↓
[Workflow] Rule Execution
    ↓
[Tool]  Rule Engine (deterministic) → ExecutionResult + Trace
    ↓
[Agent] Explainer (Claude) → human-readable explanation
```

## Project Structure

```
ir/models.py          — Pydantic IR: RuleIR, Condition, Action, ExecutionResult
agents/nl_parser.py   — NL → IR via Claude
agents/validator.py   — IR validation via Claude
agents/recommender.py — improvement suggestions via Claude
agents/explainer.py   — trace → plain English via Claude
tools/rule_engine.py  — deterministic rule evaluator
tools/rule_store.py   — SQLite CRUD for rules
tools/simulator.py    — test a rule without saving
tools/trace_engine.py — render trace as text
workflows/rule_creation.py  — NL → validate → save pipeline
workflows/rule_execution.py — fetch → evaluate → explain pipeline
main.py               — FastAPI REST API
cli.py                — Typer CLI
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Run

**API server:**
```bash
uvicorn main:app --reload
# Docs: http://localhost:8000/docs
```

**CLI:**
```bash
python cli.py rules create "if age > 60 then set risk to high"
python cli.py rules list
python cli.py execute --data '{"age": 65}'
python cli.py rules simulate <rule-id> --data '{"age": 65}'
```

## IR Example

```json
{
  "name": "Senior risk flag",
  "priority": 10,
  "when": { "all": [{"field": "age", "op": ">", "value": 60}] },
  "then": [{"type": "set", "field": "risk", "value": "high"}]
}
```

## Design Principles

- **Deterministic execution** — rule evaluation is pure logic, no AI
- **AI at input layer only** — Claude handles NL parsing, validation, explanation
- **Full observability** — every evaluation produces a trace
- **Composability** — `all`/`any` nesting, multi-rule pipelines
- **Isolation** — agents, tools, and workflows are independent modules

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/rules/from-nl` | Create rule from natural language |
| POST | `/rules` | Create rule from IR JSON |
| GET | `/rules` | List rules |
| GET | `/rules/{id}` | Get rule |
| PATCH | `/rules/{id}/toggle` | Enable/disable |
| DELETE | `/rules/{id}` | Delete |
| POST | `/rules/{id}/simulate` | Test rule against sample data |
| GET | `/rules/{id}/recommend` | Get AI suggestions |
| POST | `/execute` | Run all rules against input |
| POST | `/trace` | Render an ExecutionResult as text |
