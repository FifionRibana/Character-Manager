from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .enums import StatType, ValidationLimits, DEFAULT_STAT_VALUE


@dataclass
class CharacterStats:
    """
    Character ability scores for RPG mechanics.

    Uses dataclass with type hints and validation.
    """

    strength: int = DEFAULT_STAT_VALUE
    agility: int = DEFAULT_STAT_VALUE
    constitution: int = DEFAULT_STAT_VALUE
    intelligence: int = DEFAULT_STAT_VALUE
    wisdom: int = DEFAULT_STAT_VALUE
    charisma: int = DEFAULT_STAT_VALUE

    def __post_init__(self) -> None:
        """Validate stat values after initialization."""
        self._validate_stats()

    def _validate_stats(self) -> None:
        """Validate that all stats are within acceptable ranges."""
        for stat_name in [
            "strength",
            "agility",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]:
            value = getattr(self, stat_name)
            if (
                not ValidationLimits.MIN_STAT_VALUE
                <= value
                <= ValidationLimits.MAX_STAT_VALUE
            ):
                raise ValueError(
                    f"{stat_name} must be between {ValidationLimits.MIN_STAT_VALUE} and {ValidationLimits.MAX_STAT_VALUE}"
                )

    @property
    def total_points(self) -> int:
        """Calculate total stat points allocated."""
        return (
            self.strength
            + self.agility
            + self.constitution
            + self.intelligence
            + self.wisdom
            + self.charisma
        )

    @property
    def average_stat(self) -> float:
        """Calculate average stat value."""
        return self.total_points / 6

    def get_modifier(self, stat_type: StatType) -> int:
        """
        Calculate D&D 5e style modifier for a stat.

        Args:
            stat_type: The stat to calculate modifier for

        Returns:
            Modifier value (-5 to +7 for stats 1-25)
        """
        stat_value = getattr(self, stat_type.value)
        return (stat_value - 10) // 2

    def to_dict(self) -> Dict[str, int]:
        """
        Convert stats to dictionary with enum keys.

        Returns:
            Dictionary with stat types as keys
        """
        return {
            StatType.STRENGTH.value: self.strength,
            StatType.AGILITY.value: self.agility,
            StatType.CONSTITUTION.value: self.constitution,
            StatType.INTELLIGENCE.value: self.intelligence,
            StatType.WISDOM.value: self.wisdom,
            StatType.CHARISMA.value: self.charisma,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> CharacterStats:
        """
        Create CharacterStats from dictionary.

        Args:
            data: Dictionary with stat values

        Returns:
            CharacterStats instance
        """
        return cls(
            strength=data.get(StatType.STRENGTH.value, DEFAULT_STAT_VALUE),
            agility=data.get(StatType.AGILITY.value, DEFAULT_STAT_VALUE),
            constitution=data.get(StatType.CONSTITUTION.value, DEFAULT_STAT_VALUE),
            intelligence=data.get(StatType.INTELLIGENCE.value, DEFAULT_STAT_VALUE),
            wisdom=data.get(StatType.WISDOM.value, DEFAULT_STAT_VALUE),
            charisma=data.get(StatType.CHARISMA.value, DEFAULT_STAT_VALUE),
        )

    @classmethod
    def create_point_buy(cls, **stat_values: int) -> CharacterStats:
        """
        Create stats using point buy system.

        Args:
            **stat_values: Keyword arguments for stat values

        Returns:
            CharacterStats instance
        """
        defaults = {stat.value: 8 for stat in StatType}
        defaults.update(stat_values)
        return cls.from_dict(defaults)
