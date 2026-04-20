import json
import anthropic
from ir.models import RuleIR

_client = anthropic.Anthropic()

_SYSTEM = """You are a rule optimization assistant. Given a business rule in JSON format, suggest improvements.
Consider: edge cases not covered, overly broad conditions, better action types, priority tuning, naming clarity.

Respond ONLY with valid JSON:
{"suggestions": ["suggestion 1", "suggestion 2", ...]}
Limit to 3-5 actionable suggestions.
"""


def recommend(rule: RuleIR) -> list[str]:
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=_SYSTEM,
        messages=[{"role": "user", "content": rule.model_dump_json(indent=2)}],
    )
    data = json.loads(response.content[0].text.strip())
    return data.get("suggestions", [])
