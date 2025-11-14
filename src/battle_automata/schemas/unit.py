"""
Unit configuration schemas (Pydantic models for validation).

These models are used to load and validate unit definitions from YAML/JSON.
For runtime simulation, use the frozen dataclasses in battle_automata.core.
"""

from typing import List, Dict, Any, Optional, Tuple, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class Position(BaseModel):
    """2D position"""
    x: int = Field(ge=0)
    y: int = Field(ge=0)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    model_config = {"frozen": True}


class ComponentPlacement(BaseModel):
    """Component placement on unit grid"""
    component_id: str = Field(description="ID of component to place")
    position: Position
    facing: float = Field(
        default=0,
        ge=0,
        lt=360,
        description="Facing in degrees (0=forward)"
    )
    slot_name: Optional[str] = Field(
        None,
        description="Logical slot name (e.g., 'weapon_1')"
    )


class UnitLayout(BaseModel):
    """Unit grid layout"""
    width: int = Field(gt=0, le=20, description="Grid width")
    height: int = Field(gt=0, le=20, description="Grid height")

    @model_validator(mode='after')
    def size_reasonable(self) -> 'UnitLayout':
        """Limit total grid size"""
        total = self.width * self.height
        if total > 100:
            raise ValueError(
                f'Grid size {self.width}x{self.height}={total} too large (max 100)'
            )
        return self


class UnitResourceBudget(BaseModel):
    """Resource limits for unit"""
    max_power: int = Field(
        gt=0,
        le=2000,
        description="Maximum power budget in watts"
    )
    max_weight: int = Field(
        gt=0,
        le=10000,
        description="Maximum weight in kg"
    )
    max_slots: int = Field(
        gt=0,
        le=100,
        description="Maximum component slots"
    )
    max_cost: Optional[int] = Field(
        None,
        ge=0,
        description="Optional cost limit in credits"
    )


class AIBehavior(BaseModel):
    """AI behavior configuration"""
    movement_style: Literal[
        "aggressive",
        "defensive",
        "kiting",
        "stationary"
    ] = "aggressive"
    engagement_range: float = Field(
        default=100,
        gt=0,
        description="Preferred combat range"
    )
    retreat_threshold: float = Field(
        default=0.2,
        ge=0,
        le=1,
        description="Retreat when health < this % (0-1)"
    )


class UnitConfig(BaseModel):
    """Complete unit configuration (validated from YAML)"""

    # Identity
    id: str = Field(pattern=r'^[a-z0-9_]+$')
    name: str = Field(min_length=1, max_length=100)
    theme: str = Field(description="Theme this unit belongs to")

    # Description
    description: Optional[str] = Field(None, max_length=1000)
    class_name: Optional[str] = Field(
        None,
        description="Unit class (fighter, bomber, etc.)"
    )

    # Layout
    layout: UnitLayout

    # Components
    components: List[ComponentPlacement]

    # Resources
    resources: UnitResourceBudget

    # AI (optional)
    ai: Optional[AIBehavior] = None

    # Metadata
    tags: List[str] = Field(default_factory=list)
    cost: Optional[int] = Field(None, ge=0)
    build_time: Optional[int] = Field(None, ge=0)

    @field_validator('components')
    @classmethod
    def components_not_empty(cls, v: List[ComponentPlacement]) -> List[ComponentPlacement]:
        """Unit must have components"""
        if not v:
            raise ValueError('Unit must have at least one component')
        return v

    @model_validator(mode='after')
    def validate_component_positions(self) -> 'UnitConfig':
        """Ensure components fit on grid"""
        for comp in self.components:
            pos = comp.position
            if pos.x >= self.layout.width or pos.y >= self.layout.height:
                raise ValueError(
                    f'Component at ({pos.x},{pos.y}) outside grid '
                    f'({self.layout.width}x{self.layout.height})'
                )

        return self
