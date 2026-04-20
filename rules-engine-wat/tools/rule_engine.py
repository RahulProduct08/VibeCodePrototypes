from __future__ import annotations
from typing import Any
from ir.models import (
    Action, ActionType, Condition, ConditionGroup, ExecutionResult, RuleIR, TraceStep,
)


def _eval_condition(cond: Condition, data: dict[str, Any]) -> bool:
    val = data.get(cond.field)
    op = cond.op.value
    if op == ">":
        return val > cond.value
    if op == "<":
        return val < cond.value
    if op == ">=":
        return val >= cond.value
    if op == "<=":
        return val <= cond.value
    if op == "==":
        return val == cond.value
    if op == "!=":
        return val != cond.value
    if op == "in":
        return val in cond.value
    if op == "not_in":
        return val not in cond.value
    if op == "contains":
        return cond.value in val
    return False


def _eval_group(group: ConditionGroup, data: dict[str, Any]) -> bool:
    if group.all is not None:
        return all(_eval_item(item, data) for item in group.all)
    if group.any is not None:
        return any(_eval_item(item, data) for item in group.any)
    return True


def _eval_item(item: Condition | ConditionGroup, data: dict[str, Any]) -> bool:
    if isinstance(item, Condition):
        return _eval_condition(item, data)
    return _eval_group(item, data)


def _apply_action(action: Action, state: dict[str, Any]) -> str:
    if action.type == ActionType.SET and action.field is not None:
        state[action.field] = action.value
        return f"set {action.field}={action.value!r}"
    if action.type == ActionType.FLAG and action.field is not None:
        state.setdefault("flags", []).append(action.field)
        return f"flag {action.field}"
    if action.type == ActionType.NOTIFY:
        return f"notify: {action.message}"
    if action.type == ActionType.REJECT:
        state["rejected"] = True
        if action.message:
            state["rejection_reason"] = action.message
        return f"reject: {action.message or 'no reason'}"
    return f"unknown action {action.type}"


def execute_rule(rule: RuleIR, data: dict[str, Any], state: dict[str, Any]) -> TraceStep:
    matched = _eval_group(rule.when, data)
    actions_executed: list[str] = []
    if matched:
        for action in rule.then:
            actions_executed.append(_apply_action(action, state))
    return TraceStep(
        rule_id=rule.id or "",
        rule_name=rule.name,
        condition_matched=matched,
        actions_executed=actions_executed,
        detail=f"Rule '{rule.name or rule.id}' {'matched' if matched else 'did not match'}",
    )


def run_rules(rules: list[RuleIR], input_data: dict[str, Any]) -> ExecutionResult:
    state: dict[str, Any] = {}
    trace: list[TraceStep] = []
    matched_rules: list[str] = []

    for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
        step = execute_rule(rule, input_data, state)
        trace.append(step)
        if step.condition_matched:
            matched_rules.append(rule.id or "")

    decision = None
    if state.get("rejected"):
        decision = "rejected"
    elif "risk" in state:
        decision = f"risk={state['risk']}"
    elif matched_rules:
        decision = "matched"
    else:
        decision = "no_match"

    return ExecutionResult(
        input_data=input_data,
        matched_rules=matched_rules,
        final_state=state,
        trace=trace,
        decision=decision,
    )
