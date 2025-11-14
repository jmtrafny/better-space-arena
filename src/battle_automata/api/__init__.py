"""Public API for Battle Automata Engine."""

from .battle import Battle, BattleConfig, BattleResult, BattleStep

# Try to import Engine if available (added by other agents)
try:
    from battle_automata.api.engine import Engine
    __all__ = [
        'Battle',
        'BattleConfig',
        'BattleResult',
        'BattleStep',
        'Engine',
    ]
except ImportError:
    __all__ = [
        'Battle',
        'BattleConfig',
        'BattleResult',
        'BattleStep',
    ]
