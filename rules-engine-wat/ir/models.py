from __future__ import annotations
from enum import Enum
from typing import Any
from pydantic import BaseModel


class Operator(str, Enum):
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    EQ = "=="
    NEQ = "!="
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"


class Condition(BaseModel):
    field: str
    op: Operator
    value: Any


class ConditionGroup(BaseModel):
    all: list[Condition | ConditionGroup] | None = None
    any: list[Condition | ConditionGroup] | None = None


class ActionType(str, Enum):
    SET = "set"
    NOTIFY = "notify"
    FLAG = "flag"
    REJECT = "reject"


class Action(BaseModel):
    type: ActionType
    field: str | None = None
    value: Any = None
    message: str | None = None


class RuleIR(BaseModel):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    priority: int = 0
    enabled: bool = True
    when: ConditionGroup
    then: list[Action]


class TraceStep(BaseModel):
    rule_id: str
    rule_name: str | None
    condition_matched: bool
    actions_executed: list[str]
    detail: str


class ExecutionResult(BaseModel):
    input_data: dict[str, Any]
    matched_rules: list[str]
    final_state: dict[str, Any]
    trace: list[TraceStep]
    decision: str | None = None
