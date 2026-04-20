from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.recommender import recommend
from ir.models import ExecutionResult, RuleIR
from tools import rule_store
from tools.simulator import simulate
from tools.trace_engine import render_trace
from workflows.rule_creation import create_rule_from_ir, create_rule_from_nl
from workflows.rule_execution import execute


@asynccontextmanager
async def lifespan(app: FastAPI):
    rule_store.init_db()
    yield


app = FastAPI(title="AI-Native Rules Engine", lifespan=lifespan)


# --- Request/Response models ---

class NLRuleRequest(BaseModel):
    text: str
    priority: int = 0


class ExecuteRequest(BaseModel):
    data: dict[str, Any]
    explain: bool = False


class SimulateRequest(BaseModel):
    data: dict[str, Any]


class ToggleRequest(BaseModel):
    enabled: bool


# --- Rules endpoints ---

@app.post("/rules/from-nl", response_model=RuleIR, status_code=201)
def create_from_nl(req: NLRuleRequest):
    try:
        rule, _ = create_rule_from_nl(req.text, skip_confirm=True)
        if req.priority:
            rule = rule.model_copy(update={"priority": req.priority})
            rule_store.save_rule(rule)
        return rule
    except ValueError as e:
        raise HTTPException(422, detail=str(e))


@app.post("/rules", response_model=RuleIR, status_code=201)
def create_from_ir(rule: RuleIR):
    try:
        saved, _ = create_rule_from_ir(rule)
        return saved
    except ValueError as e:
        raise HTTPException(422, detail=str(e))


@app.get("/rules", response_model=list[RuleIR])
def list_all_rules(enabled_only: bool = False):
    return rule_store.list_rules(enabled_only=enabled_only)


@app.get("/rules/{rule_id}", response_model=RuleIR)
def get_rule(rule_id: str):
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")
    return rule


@app.patch("/rules/{rule_id}/toggle")
def toggle_rule(rule_id: str, req: ToggleRequest):
    if not rule_store.get_rule(rule_id):
        raise HTTPException(404, detail="Rule not found")
    rule_store.toggle_rule(rule_id, req.enabled)
    return {"id": rule_id, "enabled": req.enabled}


@app.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: str):
    if not rule_store.get_rule(rule_id):
        raise HTTPException(404, detail="Rule not found")
    rule_store.delete_rule(rule_id)


@app.post("/rules/{rule_id}/simulate", response_model=ExecutionResult)
def simulate_rule(rule_id: str, req: SimulateRequest):
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")
    return simulate(rule, req.data)


@app.get("/rules/{rule_id}/recommend")
def get_recommendations(rule_id: str):
    rule = rule_store.get_rule(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")
    return {"suggestions": recommend(rule)}


# --- Execution endpoint ---

@app.post("/execute", response_model=ExecutionResult)
def execute_rules(req: ExecuteRequest):
    result = execute(req.data, with_explanation=req.explain)
    return result


# --- Trace endpoint ---

@app.post("/trace")
def render_execution_trace(result: ExecutionResult):
    return {"trace": render_trace(result)}
