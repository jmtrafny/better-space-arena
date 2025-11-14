"""Integration tests for CLI commands."""

import pytest
from click.testing import CliRunner
from pathlib import Path

from battle_automata.cli.main import cli


@pytest.fixture
def runner():
    """Create Click test runner."""
    return CliRunner()


@pytest.fixture
def data_dir(tmp_path):
    """Create temporary data directory with test theme."""
    themes_dir = tmp_path / "themes" / "test-theme"
    themes_dir.mkdir(parents=True)

    # Create theme.yaml
    theme_yaml = themes_dir / "theme.yaml"
    theme_yaml.write_text(
        """
id: test-theme
name: "Test Theme"
version: "1.0.0"
description: "Test theme for integration tests"
"""
    )

    # Create components directory
    (themes_dir / "components").mkdir()

    # Create units directory
    (themes_dir / "units").mkdir()

    return tmp_path


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Battle Automata Engine" in result.output


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "battle-sim" in result.output


def test_theme_list_empty(runner, data_dir):
    """Test listing themes when none exist."""
    empty_dir = data_dir / "empty"
    empty_dir.mkdir()

    result = runner.invoke(cli, ["--data-dir", str(empty_dir), "theme", "list"])
    assert result.exit_code == 0
    assert "No themes found" in result.output


def test_theme_list(runner, data_dir):
    """Test listing themes."""
    result = runner.invoke(cli, ["--data-dir", str(data_dir), "theme", "list"])
    assert result.exit_code == 0
    assert "test-theme" in result.output or "Test Theme" in result.output


def test_theme_info(runner, data_dir):
    """Test showing theme info."""
    result = runner.invoke(cli, ["--data-dir", str(data_dir), "theme", "info", "test-theme"])
    assert result.exit_code == 0
    assert "Test Theme" in result.output
    assert "1.0.0" in result.output


def test_component_list_no_theme(runner):
    """Test listing components without theme fails."""
    result = runner.invoke(cli, ["component", "list"])
    assert result.exit_code != 0


def test_component_list_empty(runner, data_dir):
    """Test listing components in empty theme."""
    result = runner.invoke(cli, ["--data-dir", str(data_dir), "component", "list", "--theme", "test-theme"])
    assert result.exit_code == 0
    assert "0 components" in result.output or "No components" in result.output


def test_unit_list_empty(runner, data_dir):
    """Test listing units in empty theme."""
    result = runner.invoke(cli, ["--data-dir", str(data_dir), "unit", "list", "--theme", "test-theme"])
    assert result.exit_code == 0
    assert "No units found" in result.output or "0 units" in result.output
