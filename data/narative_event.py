from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any

from .enums import EventType, StorageKeys, DEFAULT_EVENT_IMPORTANCE, ValidationLimits


@dataclass
class NarrativeEvent:
    """A significant event in the character's story."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = field(default="")
    event_type: EventType = field(default=EventType.GENERAL)
    description: str = field(default="")
    date: str = field(default="")  # Flexible date format for fantasy settings
    importance: int = field(default=DEFAULT_EVENT_IMPORTANCE)  # 1-10 scale
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate event data."""
        if (
            not ValidationLimits.MIN_EVENT_IMPORTANCE
            <= self.importance
            <= ValidationLimits.MAX_EVENT_IMPORTANCE
        ):
            raise ValueError("Event importance must be between 1 and 10")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            StorageKeys.CHARACTER_ID.value: self.id,
            StorageKeys.EVENT_TITLE.value: self.title,
            StorageKeys.EVENT_TYPE.value: self.event_type.value,
            StorageKeys.EVENT_DESCRIPTION.value: self.description,
            StorageKeys.EVENT_DATE.value: self.date,
            StorageKeys.EVENT_IMPORTANCE.value: self.importance,
            StorageKeys.TAGS.value: self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NarrativeEvent:
        """Create NarrativeEvent from dictionary."""
        return cls(
            id=data.get(StorageKeys.CHARACTER_ID.value, str(uuid.uuid4())),
            title=data.get(StorageKeys.EVENT_TITLE.value, ""),
            type=data.get(StorageKeys.EVENT_TYPE.value, EventType.GENERAL),
            description=data.get(StorageKeys.EVENT_DESCRIPTION.value, ""),
            date=data.get(StorageKeys.EVENT_DATE.value, ""),
            importance=data.get(
                StorageKeys.EVENT_IMPORTANCE.value, DEFAULT_EVENT_IMPORTANCE
            ),
            tags=data.get(StorageKeys.TAGS.value, []),
        )
