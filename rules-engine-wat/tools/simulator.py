from typing import Any
from ir.models import ExecutionResult, RuleIR
from tools.rule_engine import run_rules


def simulate(rule: RuleIR, sample_data: dict[str, Any]) -> ExecutionResult:
    """Test a single rule against sample data without persisting anything."""
    return run_rules([rule], sample_data)
