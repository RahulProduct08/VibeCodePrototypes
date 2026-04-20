from typing import Any
from agents.explainer import explain
from ir.models import ExecutionResult
from tools.rule_engine import run_rules
from tools.rule_store import list_rules


def execute(input_data: dict[str, Any], with_explanation: bool = False) -> ExecutionResult:
    """Fetch enabled rules, evaluate by priority, optionally explain."""
    rules = list_rules(enabled_only=True)
    result = run_rules(rules, input_data)

    if with_explanation:
        result = result.model_copy(update={"decision": explain(result)})

    return result
