import json
import anthropic
from ir.models import RuleIR

_client = anthropic.Anthropic()

_SYSTEM = """You are a rule parsing assistant. Convert natural language rule descriptions into a strict JSON object matching this schema:

{
  "name": "string (short rule name)",
  "description": "string (one sentence)",
  "priority": integer (0-100, default 0),
  "when": {
    "all": [ ...conditions... ]   // OR use "any" for OR logic
  },
  "then": [
    {"type": "set|notify|flag|reject", "field": "field_name", "value": any, "message": "string"}
  ]
}

Condition object: {"field": "field_name", "op": ">|<|>=|<=|==|!=|in|not_in|contains", "value": any}

Rules:
- Output ONLY valid JSON. No explanation, no markdown, no code fences.
- Use "all" for AND logic, "any" for OR logic. They can be nested.
- "set" actions require field + value. "reject"/"notify" actions use message. "flag" uses field.
"""


def parse_nl_to_ir(text: str) -> RuleIR:
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    raw = response.content[0].text.strip()
    data = json.loads(raw)
    return RuleIR.model_validate(data)
