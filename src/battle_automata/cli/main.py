"""Main CLI entry point for Battle Automata Engine."""

import click
from rich.console import Console
from pathlib import Path

from battle_automata import __version__
from battle_automata.api.engine import Engine

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="battle-sim")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-error output")
@click.option("--data-dir", type=click.Path(), help="Data directory path")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, data_dir: str) -> None:
    """
    Battle Automata Engine - Deterministic battle simulation system.

    Create units from modular components, then simulate deterministic battles
    between automata. Supports multiple themes and custom components.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["data_dir"] = data_dir

    # Initialize engine
    if data_dir:
        ctx.obj["engine"] = Engine(data_directory=Path(data_dir))
    else:
        ctx.obj["engine"] = Engine()


@cli.group()
def theme() -> None:
    """Theme management commands."""
    pass


@theme.command("list")
@click.pass_context
def theme_list(ctx: click.Context) -> None:
    """List available themes."""
    engine: Engine = ctx.obj["engine"]
    themes = engine.list_themes()

    if not themes:
        console.print("[yellow]No themes found[/yellow]")
        console.print(f"Create themes in: {engine.theme_loader.themes_dir}")
        return

    console.print("[bold blue]Available Themes:[/bold blue]")
    for theme_name in themes:
        try:
            info = engine.get_theme_info(theme_name)
            console.print(f"  [green]{info.name}[/green] ({theme_name}) - v{info.version}")
            if info.description:
                console.print(f"    {info.description[:80]}...")
        except Exception as e:
            console.print(f"  [yellow]{theme_name}[/yellow] (error loading info: {e})")


@theme.command("info")
@click.argument("theme_name")
@click.pass_context
def theme_info(ctx: click.Context, theme_name: str) -> None:
    """Show detailed theme information."""
    engine: Engine = ctx.obj["engine"]

    try:
        info = engine.get_theme_info(theme_name)

        console.print(f"\n[bold blue]Theme: {info.name}[/bold blue]")
        console.print(f"ID: {info.id}")
        console.print(f"Version: {info.version}")
        if info.author:
            console.print(f"Author: {info.author}")
        if info.license:
            console.print(f"License: {info.license}")
        console.print(f"\n{info.description}\n")

        # Load theme to count components
        num_components = engine.load_theme(theme_name)
        num_units = len(engine.list_units())

        console.print(f"Components: {num_components}")
        console.print(f"Units: {num_units}")

    except FileNotFoundError:
        console.print(f"[red]Error: Theme '{theme_name}' not found[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error loading theme: {e}[/red]")
        ctx.exit(1)


@cli.group()
def component() -> None:
    """Component operations."""
    pass


@component.command("list")
@click.option("--theme", required=True, help="Theme name")
@click.option("--type", "comp_type", help="Filter by component type")
@click.pass_context
def component_list(ctx: click.Context, theme: str, comp_type: str) -> None:
    """List components in a theme."""
    engine: Engine = ctx.obj["engine"]

    try:
        num_loaded = engine.load_theme(theme)
        console.print(f"[blue]Loaded {num_loaded} components from theme '{theme}'[/blue]\n")

        components = engine.list_components(category=comp_type)

        if not components:
            console.print("[yellow]No components found[/yellow]")
            return

        console.print(f"[bold]{'ID':<25} {'Name':<30} {'Category':<15}[/bold]")
        console.print("-" * 70)

        for comp in components:
            comp_id = comp.get("id", "unknown")
            name = comp.get("name", "Unknown")
            category = comp.get("category", "unknown")
            console.print(f"{comp_id:<25} {name:<30} {category:<15}")

    except FileNotFoundError:
        console.print(f"[red]Error: Theme '{theme}' not found[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)


@component.command("show")
@click.argument("component_id")
@click.option("--theme", required=True, help="Theme name")
@click.pass_context
def component_show(ctx: click.Context, component_id: str, theme: str) -> None:
    """Show detailed component information."""
    engine: Engine = ctx.obj["engine"]

    try:
        engine.load_theme(theme)
        comp = engine.get_component(component_id)

        if not comp:
            console.print(f"[red]Component '{component_id}' not found in theme '{theme}'[/red]")
            ctx.exit(1)

        # Display component details
        console.print(f"\n[bold blue]Component: {comp.get('name', 'Unknown')}[/bold blue]")
        console.print(f"ID: {comp.get('id', 'unknown')}")
        console.print(f"Type: {comp.get('type', 'unknown')}")
        console.print(f"Category: {comp.get('category', 'unknown')}")

        if desc := comp.get("description"):
            console.print(f"\n{desc}\n")

        # Display stats
        if stats := comp.get("stats"):
            console.print("[bold]Stats:[/bold]")
            for key, value in stats.items():
                console.print(f"  {key}: {value}")

        # Display resources
        if resources := comp.get("resources"):
            console.print("\n[bold]Resources:[/bold]")
            for key, value in resources.items():
                console.print(f"  {key}: {value}")

        # Display tags
        if tags := comp.get("tags"):
            console.print(f"\n[bold]Tags:[/bold] {', '.join(tags)}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)


@cli.group()
def unit() -> None:
    """Unit operations."""
    pass


@unit.command("list")
@click.option("--theme", required=True, help="Theme name")
@click.pass_context
def unit_list(ctx: click.Context, theme: str) -> None:
    """List units in a theme."""
    engine: Engine = ctx.obj["engine"]

    try:
        engine.load_theme(theme)
        units = engine.list_units()

        if not units:
            console.print("[yellow]No units found[/yellow]")
            return

        console.print(f"[blue]Found {len(units)} units in theme '{theme}'[/blue]\n")
        console.print(f"[bold]{'ID':<20} {'Name':<30} {'Class':<15}[/bold]")
        console.print("-" * 65)

        for unit in units:
            unit_id = unit.get("id", "unknown")
            name = unit.get("name", "Unknown")
            unit_class = unit.get("class_name", "unknown")
            console.print(f"{unit_id:<20} {name:<30} {unit_class:<15}")

    except FileNotFoundError:
        console.print(f"[red]Error: Theme '{theme}' not found[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)


@unit.command("show")
@click.argument("unit_file")
@click.pass_context
def unit_show(ctx: click.Context, unit_file: str) -> None:
    """Show detailed unit information from a file."""
    engine: Engine = ctx.obj["engine"]

    try:
        unit = engine.load_unit_from_file(unit_file)

        console.print(f"\n[bold blue]Unit: {unit.get('name', 'Unknown')}[/bold blue]")
        console.print(f"ID: {unit.get('id', 'unknown')}")
        console.print(f"Theme: {unit.get('theme', 'unknown')}")

        if class_name := unit.get("class_name"):
            console.print(f"Class: {class_name}")

        if desc := unit.get("description"):
            console.print(f"\n{desc}\n")

        # Display layout
        if layout := unit.get("layout"):
            console.print(f"[bold]Layout:[/bold] {layout.get('width')}x{layout.get('height')}")

        # Display components
        if components := unit.get("components"):
            console.print(f"\n[bold]Components ({len(components)}):[/bold]")
            for comp in components:
                comp_id = comp.get("component_id", "unknown")
                pos = comp.get("position", {})
                console.print(f"  - {comp_id} at ({pos.get('x', 0)}, {pos.get('y', 0)})")

        # Display resources
        if resources := unit.get("resources"):
            console.print("\n[bold]Resource Budgets:[/bold]")
            for key, value in resources.items():
                console.print(f"  {key}: {value}")

    except FileNotFoundError:
        console.print(f"[red]Error: Unit file '{unit_file}' not found[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)


@cli.group()
def battle() -> None:
    """Battle simulation commands."""
    pass


@battle.command("simulate")
@click.argument("unit1")
@click.argument("unit2")
@click.option("--seed", type=int, help="Random seed for deterministic results")
@click.option("--output", "-o", type=click.Path(), help="Save results to file")
@click.option("--theme", help="Theme name (if using unit IDs)")
@click.pass_context
def battle_simulate(
    ctx: click.Context,
    unit1: str,
    unit2: str,
    seed: int,
    output: str,
    theme: str,
) -> None:
    """
    Simulate a battle between two units.

    Units can be specified as:
    - File paths: unit1.yaml unit2.yaml
    - Unit IDs: --theme space-ships fighter bomber
    """
    engine: Engine = ctx.obj["engine"]

    try:
        # Load units
        if theme:
            engine.load_theme(theme)
            unit1_data = engine.get_unit(unit1)
            unit2_data = engine.get_unit(unit2)
            if not unit1_data or not unit2_data:
                console.print("[red]Error: One or both units not found in theme[/red]")
                ctx.exit(1)
        else:
            # Try loading as files
            unit1_data = engine.load_unit_from_file(unit1)
            unit2_data = engine.load_unit_from_file(unit2)

        console.print(f"\n[bold blue]Starting Battle Simulation[/bold blue]")
        console.print(f"Unit 1: {unit1_data.get('name', unit1)}")
        console.print(f"Unit 2: {unit2_data.get('name', unit2)}")
        if seed:
            console.print(f"Seed: {seed}\n")

        # Simulate battle (placeholder)
        with console.status("[bold green]Simulating battle..."):
            result = engine.simulate_battle(
                unit1_data.get("id", unit1),
                unit2_data.get("id", unit2),
                seed=seed,
            )

        console.print("\n[bold green]Battle Complete![/bold green]")
        console.print(f"Winner: {result['winner']}")
        console.print(f"\n[yellow]Note: {result['note']}[/yellow]")

        if output:
            import json

            with open(output, "w") as f:
                json.dump(result, f, indent=2)
            console.print(f"\nResults saved to: {output}")

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        ctx.exit(1)


if __name__ == "__main__":
    cli()
