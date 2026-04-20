from ir.models import ExecutionResult


def render_trace(result: ExecutionResult) -> str:
    lines = [
        "=== Execution Trace ===",
        f"Input: {result.input_data}",
        f"Decision: {result.decision}",
        f"Matched rules: {result.matched_rules or 'none'}",
        "",
        "--- Steps ---",
    ]
    for i, step in enumerate(result.trace, 1):
        status = "MATCH" if step.condition_matched else "skip"
        lines.append(f"{i}. [{status}] {step.detail}")
        for action in step.actions_executed:
            lines.append(f"     -> {action}")
    lines += ["", f"Final state: {result.final_state}"]
    return "\n".join(lines)
