#!/usr/bin/env python3
"""
NarrativeModel - PyQt model for character narrative events.

This module provides the NarrativeModel class that manages timeline events
for QML consumption with chronological sorting and filtering.
"""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Dict, Any
from PyQt6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
    pyqtSignal,
    pyqtProperty,
    QObject,
    pyqtSlot,
)
from datetime import datetime
import re

from data.character import NarrativeEvent
from data.enums import (
    DEFAULT_EVENT_IMPORTANCE,
    EventChapter,
    EventType,
    ValidationLimits,
)


class NarrativeRoleConstant:
    """Define roles for QML access"""

    IdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    DescriptionRole = Qt.ItemDataRole.UserRole + 3
    DateRole = Qt.ItemDataRole.UserRole + 4
    ImportanceRole = Qt.ItemDataRole.UserRole + 5
    TagsRole = Qt.ItemDataRole.UserRole + 6
    ChapterRole = Qt.ItemDataRole.UserRole + 7
    TypeRole = Qt.ItemDataRole.UserRole + 8
    ColorRole = Qt.ItemDataRole.UserRole + 9
    IconRole = Qt.ItemDataRole.UserRole + 10
    SortOrderRole = Qt.ItemDataRole.UserRole + 11


@dataclass
class NarrativeModel(QAbstractListModel):
    """Model for managing character narrative events in QML."""

    # Signals for QML
    eventAdded: ClassVar[pyqtSignal] = pyqtSignal(str, arguments=["eventId"])
    eventRemoved: ClassVar[pyqtSignal] = pyqtSignal(str, arguments=["eventId"])
    eventUpdated: ClassVar[pyqtSignal] = pyqtSignal(str, arguments=["eventId"])
    countChanged: ClassVar[pyqtSignal] = pyqtSignal()

    _events: List[NarrativeEvent] = field(init=False, default_factory=list)

    def __post_init__(self):
        QAbstractListModel.__init__(self)

    def roleNames(self) -> Dict[int, bytes]:
        """Return role names for QML."""
        return {
            NarrativeRoleConstant.IdRole: b"id",
            NarrativeRoleConstant.TitleRole: b"title",
            NarrativeRoleConstant.DescriptionRole: b"description",
            NarrativeRoleConstant.DateRole: b"date",
            NarrativeRoleConstant.ImportanceRole: b"importance",
            NarrativeRoleConstant.TagsRole: b"tags",
            NarrativeRoleConstant.ChapterRole: b"chapter",
            NarrativeRoleConstant.TypeRole: b"eventType",
            NarrativeRoleConstant.ColorRole: b"color",
            NarrativeRoleConstant.IconRole: b"icon",
            NarrativeRoleConstant.SortOrderRole: b"sortOrder",
        }

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of events."""
        return len(self._events)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for a given index and role."""
        if not self.checkIndex(index):
            return None

        event = self._events[index.row()]

        if role == NarrativeRoleConstant.IdRole:
            return event.id
        elif role == NarrativeRoleConstant.TitleRole:
            return event.title
        elif role == NarrativeRoleConstant.DescriptionRole:
            return event.description
        elif role == NarrativeRoleConstant.DateRole:
            return event.date
        elif role == NarrativeRoleConstant.ImportanceRole:
            return event.importance
        elif role == NarrativeRoleConstant.TagsRole:
            return event.tags
        elif role == NarrativeRoleConstant.ChapterRole:
            return self._get_event_chapter(event)
        elif role == NarrativeRoleConstant.TypeRole:
            return self._get_event_type(event)
        elif role == NarrativeRoleConstant.ColorRole:
            return self._get_event_color(event)
        elif role == NarrativeRoleConstant.IconRole:
            return self._get_event_icon(event)
        elif role == NarrativeRoleConstant.SortOrderRole:
            return self._get_sort_order(event)

        return None

    @pyqtProperty(int, notify=countChanged)
    def count(self) -> int:
        """Get the number of events."""
        return len(self._events)

    @pyqtSlot(str, str, str, int, "QVariantList")
    def addEvent(
        self,
        title: str,
        event_type: EventType = EventType.GENERAL,
        description: str = "",
        date: str = "",
        importance: int = DEFAULT_EVENT_IMPORTANCE,
        tags: List[str] = None,
    ) -> str:
        """
        Add a new narrative event.

        Args:
            title: Event title
            description: Event description
            date: Event date (flexible format)
            importance: Importance scale 1-10
            tags: List of tags

        Returns:
            ID of the created event
        """
        if tags is None:
            tags = []

        event = NarrativeEvent(
            title=title,
            description=description,
            event_type=event_type,
            date=date,
            importance=importance,
            tags=tags,
        )

        # Find insertion point for chronological order
        insert_index = self._find_insertion_index(event)

        self.beginInsertRows(QModelIndex(), insert_index, insert_index)
        self._events.insert(insert_index, event)
        self.endInsertRows()

        self.countChanged.emit()
        self.eventAdded.emit(event.id)

        return event.id

    @pyqtSlot(str, result=bool)
    def removeEvent(self, event_id: str) -> bool:
        """
        Remove an event by ID.

        Args:
            event_id: ID of the event to remove

        Returns:
            True if event was removed, False if not found
        """
        for i, event in enumerate(self._events):
            if event.id == event_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                del self._events[i]
                self.endRemoveRows()
                self.countChanged.emit()
                self.eventRemoved.emit(event_id)
                return True
        return False

    @pyqtSlot(str, str, str, str, int, "QVariantList")
    def updateEvent(
        self,
        event_id: str,
        title: str,
        event_type: EventType,
        description: str,
        date: str,
        importance: int,
        tags: List[str],
    ) -> None:
        """
        Update an existing event.

        Args:
            event_id: ID of the event to update
            title: New title
            description: New description
            date: New date
            importance: New importance
            tags: New tags
        """
        for i, event in enumerate(self._events):
            if event.id == event_id:
                # Update the event
                updated_event = NarrativeEvent(
                    id=event_id,
                    title=title,
                    event_type=event_type,
                    description=description,
                    date=date,
                    importance=importance,
                    tags=tags or [],
                )

                # Remove old event
                self.beginRemoveRows(QModelIndex(), i, i)
                del self._events[i]
                self.endRemoveRows()

                # Insert updated event in correct chronological position
                insert_index = self._find_insertion_index(updated_event)
                self.beginInsertRows(QModelIndex(), insert_index, insert_index)
                self._events.insert(insert_index, updated_event)
                self.endInsertRows()

                self.eventUpdated.emit(event_id)
                break

    @pyqtSlot(str, result="QVariant")
    def getEvent(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get event data by ID.

        Args:
            event_id: ID of the event

        Returns:
            Event data as dictionary or None
        """
        for event in self._events:
            if event.id == event_id:
                return event.to_dict()
        return None

    @pyqtSlot(result="QVariantList")
    def getEventsByImportance(self) -> List[Dict[str, Any]]:
        """
        Get events sorted by importance (highest first).

        Returns:
            List of event dictionaries sorted by importance
        """
        sorted_events = sorted(self._events, key=lambda e: e.importance, reverse=True)
        return [event.to_dict() for event in sorted_events]

    @pyqtSlot(str, result="QVariantList")
    def getEventsByTag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Get events filtered by tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of event dictionaries with the specified tag
        """
        filtered_events = [
            event
            for event in self._events
            if tag.lower() in [t.lower() for t in event.tags]
        ]
        return [event.to_dict() for event in filtered_events]

    @pyqtSlot(result="QVariantList")
    def getAllTags(self) -> List[str]:
        """
        Get all unique tags used in events.

        Returns:
            List of unique tags
        """
        all_tags = set()
        for event in self._events:
            all_tags.update(event.tags)
        return sorted(list(all_tags))

    def set_events(self, events: List[NarrativeEvent]) -> None:
        """
        Set the complete list of events.

        Args:
            events: List of NarrativeEvent objects
        """
        self.beginResetModel()
        self._events = sorted(events, key=self._get_sort_order)
        self.endResetModel()
        self.countChanged.emit()

    def get_events(self) -> List[NarrativeEvent]:
        """
        Get the current list of events.

        Returns:
            List of NarrativeEvent objects
        """
        return self._events.copy()

    def _find_insertion_index(self, event: NarrativeEvent) -> int:
        """
        Find the correct insertion index for chronological ordering.

        Args:
            event: Event to insert

        Returns:
            Index where event should be inserted
        """
        event_order = self._get_sort_order(event)

        for i, existing_event in enumerate(self._events):
            if self._get_sort_order(existing_event) > event_order:
                return i

        return len(self._events)

    def _get_sort_order(self, event: NarrativeEvent) -> float:
        """
        Get sort order for chronological arrangement.
        Events without parseable dates are sorted by importance.

        Args:
            event: Event to get sort order for

        Returns:
            Sort order value (lower = earlier)
        """
        if not event.date:
            # No date: sort by importance at the end
            return 999999 - event.importance

        # Try to parse date in various formats
        try:
            # ISO format: YYYY-MM-DD
            if re.match(r"^\d{4}-\d{2}-\d{2}$", event.date):
                date_obj = datetime.strptime(event.date, "%Y-%m-%d")
                return date_obj.timestamp()

            # Year only: YYYY
            if re.match(r"^\d{4}$", event.date):
                date_obj = datetime.strptime(f"{event.date}-01-01", "%Y-%m-%d")
                return date_obj.timestamp()

            # Month/Year: MM/YYYY
            if re.match(r"^\d{2}/\d{4}$", event.date):
                date_obj = datetime.strptime(f"{event.date}-01", "%m/%Y-%d")
                return date_obj.timestamp()

            # Age format: "Age 15", "15 years old"
            age_match = re.search(r"(\d+)", event.date)
            if age_match:
                age = int(age_match.group(1))
                # Approximate timeline based on age
                return age * 365.25 * 24 * 3600  # Age in seconds

        except (ValueError, TypeError):
            pass

        # Fallback: sort by importance
        return 999999 - event.importance

    def _get_event_chapter(self, event: NarrativeEvent) -> str:
        """Determine chapter/period for the event."""
        if not event.date:
            return EventChapter.UNDATED.value

        try:
            # Try to extract age or year for categorization
            age_match = re.search(r"(\d+)", event.date)
            if age_match:
                age_or_year = int(age_match.group(1))

                if age_or_year < ValidationLimits.MAX_AGE_LIMIT:  # Assume it's age
                    if age_or_year <= ValidationLimits.CHILDHOOD_AGE_LIMIT:
                        return EventChapter.CHILDHOOD.value
                    elif age_or_year <= ValidationLimits.ADOLESCENCE_AGE_LIMIT:
                        return EventChapter.ADOLESCENCE.value
                    elif age_or_year <= ValidationLimits.YOUNG_ADULT_AGE_LIMIT:
                        return EventChapter.YOUNG_ADULT.value
                    elif age_or_year <= ValidationLimits.ADULT_AGE_LIMIT:
                        return EventChapter.ADULT.value
                    else:
                        return EventChapter.MATURE.value
                else:  # Assume it's a year
                    return f"Year {age_or_year}"
        except (ValueError, TypeError):
            pass

        return EventChapter.TIMELINE_DEFAULT.value

    def _get_event_type(self, event: NarrativeEvent) -> str:
        """Determine event type from tags and content."""
        tags = [tag.lower() for tag in event.tags]
        title_lower = event.title.lower()
        desc_lower = event.description.lower()

        # Check for specific event types
        if any(word in tags for word in ["birth", "born"]):
            return EventType.BIRTH.value
        if any(word in tags for word in ["death", "died", "killed"]):
            return EventType.DEATH.value
        if any(word in tags for word in ["meeting", "met", "encounter"]):
            return EventType.MEETING.value
        if any(word in tags for word in ["battle", "fight", "combat"]):
            return EventType.BATTLE.value
        if any(word in tags for word in ["tragedy", "loss", "disaster"]):
            return EventType.TRAGEDY.value
        if any(word in tags for word in ["achievement", "success", "victory"]):
            return EventType.ACHIEVEMENT.value
        if any(word in tags for word in ["training", "learning", "study"]):
            return EventType.TRAINING.value
        if any(word in tags for word in ["romance", "love", "marriage"]):
            return EventType.ROMANCE.value
        if any(word in tags for word in ["adventure", "quest", "journey"]):
            return EventType.ADVENTURE.value

        # Check title and description for keywords
        if any(word in title_lower for word in ["born", "birth"]):
            return EventType.BIRTH.value
        if any(word in title_lower for word in ["met", "meeting", "encounter"]):
            return EventType.MEETING.value
        if any(word in title_lower for word in ["battle", "fight"]):
            return EventType.BATTLE.value
        if any(word in title_lower for word in ["tragedy", "disaster"]):
            return EventType.TRAGEDY.value

        # Default based on importance
        if event.importance >= ValidationLimits.MAJOR_EVENT_TYPE_THRESHOLD:
            return EventType.MAJOR.value
        elif event.importance <= ValidationLimits.MINOR_EVENT_TYPE_THRESHOLD:
            return EventType.MINOR.value
        else:
            return EventType.GENERAL.value

    def _get_event_color(self, event: NarrativeEvent) -> str:
        """Get color for event type visualization."""
        event_type = self._get_event_type(event)

        colors = {
            EventType.BIRTH.value: "#4CAF50",  # Green
            EventType.DEATH.value: "#F44336",  # Red
            EventType.MEETING.value: "#2196F3",  # Blue
            EventType.BATTLE.value: "#FF5722",  # Deep Orange
            EventType.TRAGEDY.value: "#9C27B0",  # Purple
            EventType.ACHIEVEMENT.value: "#FFD700",  # Gold
            EventType.TRAINING.value: "#00BCD4",  # Cyan
            EventType.ROMANCE.value: "#E91E63",  # Pink
            EventType.ADVENTURE.value: "#FF9800",  # Orange
            EventType.MAJOR.value: "#3F51B5",  # Indigo
            EventType.MINOR.value: "#9E9E9E",  # Grey
            EventType.GENERAL.value: "#607D8B",  # Blue Grey
        }

        return colors.get(event_type, "#607D8B")

    def _get_event_icon(self, event: NarrativeEvent) -> str:
        """Get emoji icon for event type."""
        event_type = self._get_event_type(event)

        icons = {
            EventType.BIRTH.value: "👶",
            EventType.DEATH.value: "💀",
            EventType.MEETING.value: "🤝",
            EventType.BATTLE.value: "⚔️",
            EventType.TRAGEDY.value: "💔",
            EventType.ACHIEVEMENT.value: "🏆",
            EventType.TRAINING.value: "📚",
            EventType.ROMANCE.value: "💕",
            EventType.ADVENTURE.value: "🗺️",
            EventType.MAJOR.value: "⭐",
            EventType.MINOR.value: "📝",
            EventType.GENERAL.value: "📅",
        }

        return icons.get(event_type, "📅")
