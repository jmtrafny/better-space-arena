"""
Validation logic for units and components.

This module provides comprehensive validation of unit configurations including
resource budgets, component dependencies, and balance rules.
"""

from typing import List
from dataclasses import dataclass, field

from ..schemas.unit import UnitConfig, UnitResourceBudget
from ..schemas.component import (
    ComponentConfig,
    PowerGeneratorComponentConfig,
    WeaponComponentConfig,
    EngineComponentConfig,
)
from ..api.components import ComponentRegistry


@dataclass
class ValidationResult:
    """Result of validation check"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """True if valid"""
        return self.valid

    def __str__(self) -> str:
        """String representation"""
        if self.valid:
            result = "✓ Validation passed"
        else:
            result = "✗ Validation failed"

        if self.errors:
            result += "\n  Errors:"
            for e in self.errors:
                result += f"\n    - {e}"

        if self.warnings:
            result += "\n  Warnings:"
            for w in self.warnings:
                result += f"\n    - {w}"

        return result


class ComponentValidator:
    """Validates component definitions"""

    @staticmethod
    def validate_config(config: ComponentConfig) -> ValidationResult:
        """
        Validate component configuration

        Pydantic already did schema validation,
        now check business rules.
        """
        errors = []
        warnings = []

        # Check ID conventions
        if config.id.startswith('test_'):
            warnings.append('Component ID starts with "test_" (dev component?)')

        # Check resource costs are reasonable
        if config.resources.weight < 10:
            warnings.append('Very light component (< 10kg)')

        if config.resources.power_draw > 500:
            warnings.append('High power draw (> 500W)')

        # Check tags
        if not config.tags:
            warnings.append('No tags defined (recommended for filtering)')

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class WeaponValidator:
    """Validates weapon components"""

    @staticmethod
    def validate_balance(weapon: WeaponComponentConfig) -> ValidationResult:
        """Check weapon balance"""
        errors = []
        warnings = []

        # DPS calculation
        dps = weapon.stats.damage * weapon.stats.fire_rate

        # DPS vs power
        power_per_dps = weapon.resources.power_draw / dps if dps > 0 else 0
        if power_per_dps < 0.3:
            errors.append(
                f'Weapon too power-efficient: {power_per_dps:.2f}W/DPS '
                f'(min 0.3W/DPS)'
            )

        # DPS vs weight
        dps_per_kg = dps / weapon.resources.weight
        if dps_per_kg > 3.0:
            errors.append(
                f'Weapon too light for DPS: {dps_per_kg:.1f} DPS/kg (max 3.0)'
            )

        # Range vs DPS
        if weapon.stats.range > 200 and dps > 150:
            warnings.append(
                'Long-range high-DPS weapon may be overpowered'
            )

        # Accuracy vs fire rate
        if weapon.stats.fire_rate > 3.0 and weapon.stats.accuracy > 0.9:
            warnings.append(
                'High fire-rate + high accuracy may be too strong'
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class UnitValidator:
    """Validates unit configurations"""

    def __init__(self, component_registry: ComponentRegistry):
        self.registry = component_registry

    def validate_unit(self, unit_config: UnitConfig) -> ValidationResult:
        """Complete unit validation"""
        errors = []
        warnings = []

        # STEP 1: Validate component references
        component_ids = [cp.component_id for cp in unit_config.components]
        for comp_id in component_ids:
            if not self.registry.has(comp_id):
                errors.append(f'Unknown component: {comp_id}')

        if errors:
            return ValidationResult(valid=False, errors=errors)

        # STEP 2: Load actual components
        components = [
            self.registry.get(cp.component_id)
            for cp in unit_config.components
        ]

        # STEP 3: Check dependencies
        dep_result = self._check_dependencies(components)
        errors.extend(dep_result.errors)
        warnings.extend(dep_result.warnings)

        # STEP 4: Check resource budgets
        budget_result = self._check_resources(components, unit_config.resources)
        errors.extend(budget_result.errors)
        warnings.extend(budget_result.warnings)

        # STEP 5: Check power generation vs consumption
        power_result = self._check_power(components)
        errors.extend(power_result.errors)
        warnings.extend(power_result.warnings)

        # STEP 6: Check unit has required components
        req_result = self._check_required_components(components)
        errors.extend(req_result.errors)
        warnings.extend(req_result.warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_dependencies(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check component dependencies"""
        errors = []
        warnings = []

        # Build set of present component IDs
        present_ids = {c.id for c in components if c is not None}

        for comp in components:
            if comp is None:
                continue

            # Check requires
            if hasattr(comp, 'requires'):
                for required_id in comp.requires:
                    if required_id not in present_ids:
                        errors.append(
                            f'{comp.name} requires {required_id} but it is missing'
                        )

            # Check conflicts
            if hasattr(comp, 'conflicts_with'):
                for conflict_id in comp.conflicts_with:
                    if conflict_id in present_ids:
                        errors.append(
                            f'{comp.name} conflicts with {conflict_id}'
                        )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_resources(
        self,
        components: List[ComponentConfig],
        budget: UnitResourceBudget
    ) -> ValidationResult:
        """Check resource budgets"""
        errors = []
        warnings = []

        # Calculate totals
        total_power = sum(c.power_draw for c in components if c is not None)
        total_weight = sum(c.weight for c in components if c is not None)
        total_slots = sum(c.slots for c in components if c is not None)
        total_cost = sum(c.cost for c in components if c is not None)

        # Check limits
        if total_power > budget.max_power:
            errors.append(
                f'Power budget exceeded: {total_power}/{budget.max_power}W'
            )

        if total_weight > budget.max_weight:
            errors.append(
                f'Weight limit exceeded: {total_weight}/{budget.max_weight}kg'
            )

        if total_slots > budget.max_slots:
            errors.append(
                f'Slot capacity exceeded: {total_slots}/{budget.max_slots}'
            )

        if budget.max_cost and total_cost > budget.max_cost:
            errors.append(
                f'Cost limit exceeded: {total_cost}/{budget.max_cost} credits'
            )

        # Warnings for poor utilization
        power_util = total_power / budget.max_power if budget.max_power > 0 else 0
        if power_util < 0.5:
            warnings.append(
                f'Low power utilization: {power_util:.0%} (< 50%)'
            )

        weight_util = total_weight / budget.max_weight if budget.max_weight > 0 else 0
        if weight_util < 0.5:
            warnings.append(
                f'Low weight utilization: {weight_util:.0%} (< 50%)'
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_power(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check power generation vs consumption"""
        errors = []
        warnings = []

        # Calculate generation
        generation = 0
        for c in components:
            if c is None:
                continue
            if isinstance(c, PowerGeneratorComponentConfig):
                generation += c.stats.max_output

        # Calculate consumption
        consumption = sum(c.power_draw for c in components if c is not None)

        # Check balance
        if consumption > generation:
            errors.append(
                f'Insufficient power: {consumption}W needed, {generation}W available'
            )
        elif generation > consumption * 1.5:
            warnings.append(
                f'Excess power generation: {generation}W vs {consumption}W needed'
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_required_components(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check unit has required component types"""
        errors = []
        warnings = []

        # Count component types
        has_weapon = any(
            isinstance(c, WeaponComponentConfig) for c in components if c is not None
        )
        has_power = any(
            isinstance(c, PowerGeneratorComponentConfig) for c in components if c is not None
        )
        has_engine = any(
            isinstance(c, EngineComponentConfig) for c in components if c is not None
        )

        # Requirements
        if not has_weapon:
            warnings.append('Unit has no weapons')

        if not has_power:
            errors.append('Unit must have at least one power generator')

        if not has_engine:
            warnings.append('Unit has no engines (stationary unit?)')

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
