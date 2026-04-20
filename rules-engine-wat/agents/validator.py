import json
import anthropic
from ir.models import RuleIR

_client = anthropic.Anthropic()

_SYSTEM = """You are a rule validation assistant. Given a rule in JSON format, check for:
1. Missing required fields (when, then must be present and non-empty)
2. Invalid operators (only: >, <, >=, <=, ==, !=, in, not_in, contains)
3. Logical errors (e.g., contradictory conditions, empty condition groups)
4. Action validity (set needs field+value, reject/notify can have message, flag needs field)

Respond ONLY with valid JSON:
{"valid": true|false, "errors": ["..."], "warnings": ["..."]}
"""


def validate_ir(rule: RuleIR) -> dict:
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=_SYSTEM,
        messages=[{"role": "user", "content": rule.model_dump_json(indent=2)}],
    )
    return json.loads(response.content[0].text.strip())
