from agents.nl_parser import parse_nl_to_ir
from agents.validator import validate_ir
from ir.models import RuleIR
from tools.rule_store import save_rule


def create_rule_from_nl(text: str, skip_confirm: bool = False) -> tuple[RuleIR, dict]:
    """Parse NL → IR → validate → save. Returns (saved_rule, validation_result)."""
    rule = parse_nl_to_ir(text)
    validation = validate_ir(rule)

    if not validation.get("valid", False):
        raise ValueError(f"Rule validation failed: {validation.get('errors', [])}")

    if not skip_confirm:
        print("\n--- Rule Preview ---")
        print(rule.model_dump_json(indent=2))
        print(f"\nValidation: {validation}")
        confirm = input("\nSave this rule? [y/N]: ").strip().lower()
        if confirm != "y":
            raise RuntimeError("Rule creation cancelled by user.")

    saved = save_rule(rule)
    return saved, validation


def create_rule_from_ir(rule: RuleIR) -> tuple[RuleIR, dict]:
    """Validate and save a pre-built IR rule."""
    validation = validate_ir(rule)
    if not validation.get("valid", False):
        raise ValueError(f"Rule validation failed: {validation.get('errors', [])}")
    saved = save_rule(rule)
    return saved, validation
