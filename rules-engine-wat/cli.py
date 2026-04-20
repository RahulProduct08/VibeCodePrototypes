import json
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from tools import rule_store
from tools.simulator import simulate
from tools.trace_engine import render_trace
from workflows.rule_creation import create_rule_from_nl
from workflows.rule_execution import execute

rule_store.init_db()

app = typer.Typer(help="AI-Native Rules Engine CLI")
rules_app = typer.Typer(help="Manage rules")
app.add_typer(rules_app, name="rules")

console = Console()


@rules_app.command("create")
def rules_create(
    text: str = typer.Argument(..., help="Natural language rule description"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Create a rule from natural language."""
    with console.status("Parsing rule with Claude..."):
        rule, validation = create_rule_from_nl(text, skip_confirm=yes)
    console.print(f"[green]Rule created:[/green] {rule.id}")
    console.print(f"  Name: {rule.name}")
    if validation.get("warnings"):
        for w in validation["warnings"]:
            console.print(f"  [yellow]Warning:[/yellow] {w}")


@rules_app.command("list")
def rules_list(all: bool = typer.Option(False, "--all", help="Include disabled rules")):
    """List rules."""
    rules = rule_store.list_rules(enabled_only=not all)
    if not rules:
        console.print("No rules found.")
        return
    table = Table("ID", "Name", "Priority", "Enabled")
    for r in rules:
        table.add_row(r.id or "-", r.name or "-", str(r.priority), str(r.enabled))
    console.print(table)


@rules_app.command("toggle")
def rules_toggle(rule_id: str, enable: bool = typer.Option(True, help="Enable or disable")):
    """Enable or disable a rule."""
    if not rule_store.get_rule(rule_id):
        console.print(f"[red]Rule {rule_id} not found.[/red]")
        raise typer.Exit(1)
    rule_store.toggle_rule(rule_id, enable)
    state = "enabled" if enable else "disabled"
    console.print(f"Rule {rule_id} {state}.")


@rules_app.command("delete")
def rules_delete(rule_id: str, yes: bool = typer.Option(False, "--yes", "-y")):
    """Delete a rule."""
    if not rule_store.get_rule(rule_id):
        console.print(f"[red]Rule {rule_id} not found.[/red]")
        raise typer.Exit(1)
    if not yes:
        typer.confirm(f"Delete rule {rule_id}?", abort=True)
    rule_store.delete_rule(rule_id)
    console.print(f"Rule {rule_id} deleted.")


@rules_app.command("simulate")
def rules_simulate(
    rule_id: str,
    data: str = typer.Option(..., help='JSON data, e.g. \'{"age": 65}\''),
):
    """Simulate a rule against sample data."""
    rule = rule_store.get_rule(rule_id)
    if not rule:
        console.print(f"[red]Rule {rule_id} not found.[/red]")
        raise typer.Exit(1)
    input_data = json.loads(data)
    result = simulate(rule, input_data)
    console.print(render_trace(result))


@app.command("execute")
def run_execute(
    data: str = typer.Option(..., help='JSON input data, e.g. \'{"age": 65}\''),
    explain: bool = typer.Option(False, "--explain", help="Add AI explanation"),
):
    """Run all enabled rules against input data."""
    input_data = json.loads(data)
    with console.status("Evaluating rules..."):
        result = execute(input_data, with_explanation=explain)
    console.print(render_trace(result))
    if explain:
        console.print(f"\n[bold]Explanation:[/bold] {result.decision}")


if __name__ == "__main__":
    app()
