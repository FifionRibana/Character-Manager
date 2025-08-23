from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from .enums import (
    DEFAULT_RELATIONSHIP_STRENGTH,
    StorageKeys,
    RelationType,
    ValidationLimits,
)


@dataclass
class Relationship:
    """Relationship between two characters."""

    target_id: str
    target_name: str
    relationship_type: RelationType = field(default=RelationType.NEUTRAL)
    description: str = field(default="")
    strength: int = field(default=DEFAULT_RELATIONSHIP_STRENGTH)  # 1-10 scale

    def __post_init__(self) -> None:
        """Validate relationship data."""
        if (
            not ValidationLimits.MIN_CHARACTER_NAME_LENGTH
            <= len(self.target_name)
            <= ValidationLimits.MAX_CHARACTER_NAME_LENGTH
        ):
            raise ValueError("Target name length is invalid")

        if (
            not ValidationLimits.MIN_RELATIONSHIP_STRENGTH
            <= self.strength
            <= ValidationLimits.MAX_RELATIONSHIP_STRENGTH
        ):
            raise ValueError("Relationship strength must be between 1 and 10")

        if len(self.description) > ValidationLimits.MAX_RELATIONSHIP_DESCRIPTION_LENGTH:
            raise ValueError("Relationship description too long")

    @property
    def is_positive(self) -> bool:
        """Check if this is generally a positive relationship."""
        positive_types = {
            RelationType.FAMILY,
            RelationType.FRIEND,
            RelationType.MENTOR,
            RelationType.APPRENTICE,
            RelationType.ALLY,
            RelationType.LOVER,
        }
        return self.relationship_type in positive_types

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize relationship to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            StorageKeys.CHARACTER_ID.value: self.target_id,
            StorageKeys.NAME.value: self.target_name,
            StorageKeys.RELATIONSHIP_TYPE.value: self.relationship_type.value,
            StorageKeys.DESCRIPTION.value: self.description,
            StorageKeys.STRENGTH.value: self.strength,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Relationship:
        """
        Create Relationship from dictionary.

        Args:
            data: Dictionary with relationship data

        Returns:
            Relationship instance
        """
        return cls(
            target_id=data.get(StorageKeys.CHARACTER_ID.value, ""),
            target_name=data.get(StorageKeys.NAME.value, ""),
            relationship_type=RelationType(
                data.get(
                    StorageKeys.RELATIONSHIP_TYPE.value, RelationType.NEUTRAL.value
                )
            ),
            description=data.get(StorageKeys.DESCRIPTION.value, ""),
            strength=data.get(
                StorageKeys.RELATIONSHIP_STRENGTH.value, DEFAULT_RELATIONSHIP_STRENGTH
            ),
        )
