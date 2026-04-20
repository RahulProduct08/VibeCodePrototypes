import anthropic
from ir.models import ExecutionResult
from tools.trace_engine import render_trace

_client = anthropic.Anthropic()

_SYSTEM = """You are a decision explainer. Given a rule execution trace, produce a clear, concise explanation
for a non-technical audience. Describe what happened, which rules fired, what decision was reached and why.
Write 2-4 sentences. Plain English only."""


def explain(result: ExecutionResult) -> str:
    trace_text = render_trace(result)
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=_SYSTEM,
        messages=[{"role": "user", "content": trace_text}],
    )
    return response.content[0].text.strip()
