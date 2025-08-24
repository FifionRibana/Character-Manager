#!/usr/bin/env python3
"""
CharacterModel - Extended for Phase 4 with Relationships and Narrative.

This module provides the main CharacterModel class that exposes character data
and sub-models to QML with complete relationship and narrative functionality.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, ClassVar
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QTimer

from data.character import Character
from data.enums import (
    DEFAULT_CHARACTER_AGE,
    DEFAULT_DEVELOPMENT_LEVEL,
    DEFAULT_ENNEAGRAM_TYPE,
    DEFAULT_STAT_VALUE,
    InstinctualVariant,
    StorageKeys,
    UIConstants,
    ValidationLimits,
)
from models.relationship_model import RelationshipModel
from models.narrative_model import NarrativeModel


@dataclass
class CharacterModel(QObject):
    """Model that exposes Character data to QML with relationships and narrative."""

    # Basic character signals
    characterChanged: ClassVar[pyqtSignal] = pyqtSignal()
    idChanged: ClassVar[pyqtSignal] = pyqtSignal()
    nameChanged: ClassVar[pyqtSignal] = pyqtSignal()
    levelChanged: ClassVar[pyqtSignal] = pyqtSignal()
    ageChanged: ClassVar[pyqtSignal] = pyqtSignal()
    occupationChanged: ClassVar[pyqtSignal] = pyqtSignal()
    locationChanged: ClassVar[pyqtSignal] = pyqtSignal()
    imageDataChanged: ClassVar[pyqtSignal] = pyqtSignal()
    hasImageChanged: ClassVar[pyqtSignal] = pyqtSignal()
    biographyChanged: ClassVar[pyqtSignal] = pyqtSignal()
    affiliationsChanged: ClassVar[pyqtSignal] = pyqtSignal()
    relationshipsChanged: ClassVar[pyqtSignal] = pyqtSignal()
    narrativeEventsChanged: ClassVar[pyqtSignal] = pyqtSignal()
    relationshipCountChanged: ClassVar[pyqtSignal] = pyqtSignal()
    eventCountChanged: ClassVar[pyqtSignal] = pyqtSignal()

    # Stats signals
    statsChanged: ClassVar[pyqtSignal] = pyqtSignal()
    strengthChanged: ClassVar[pyqtSignal] = pyqtSignal()
    agilityChanged: ClassVar[pyqtSignal] = pyqtSignal()
    constitutionChanged: ClassVar[pyqtSignal] = pyqtSignal()
    intelligenceChanged: ClassVar[pyqtSignal] = pyqtSignal()
    wisdomChanged: ClassVar[pyqtSignal] = pyqtSignal()
    charismaChanged: ClassVar[pyqtSignal] = pyqtSignal()

    # Enneagram signals
    enneagramChanged: ClassVar[pyqtSignal] = pyqtSignal()
    enneagramTypeChanged: ClassVar[pyqtSignal] = pyqtSignal()
    wingChanged: ClassVar[pyqtSignal] = pyqtSignal()
    developmentLevelChanged: ClassVar[pyqtSignal] = pyqtSignal()
    instinctChanged: ClassVar[pyqtSignal] = pyqtSignal()

    _character: Character = field(default_factory=lambda: Character())
    _relationship_model: RelationshipModel = field(init=False, default_factory=lambda: RelationshipModel())
    _narrative_model: NarrativeModel = field(init=False, default_factory=lambda: NarrativeModel())

    _auto_save_timer: QTimer = field(init=False, default_factory=lambda: QTimer())
    _auto_save_interval: int = field(init=False, default=UIConstants.AUTOSAVE_INTERVAL)

    def __post_init__(self):
        QObject.__init__(self)

        # Ensure the character has an ID
        if not hasattr(self._character, "id") or not self._character.id:
            import uuid

            self._character.id = str(uuid.uuid4())

        # Ensure the character has a level
        if not hasattr(self._character, "level"):
            self._character.level = ValidationLimits.MIN_CHARACTER_LEVEL

        # Ensure the character has a level
        if not hasattr(self._character, "age"):
            self._character.level = DEFAULT_CHARACTER_AGE

        # Auto-save timer
        self._auto_save_timer.setSingleShot(True)
        self._auto_save_timer.timeout.connect(self._on_auto_save)

        # Connect sub-model signals
        self._setup_sub_model_connections()

        # Initialize sub-models with current data
        self._sync_sub_models()

    def __post_init__(self):
        QObject.__init__(self)

    def _setup_sub_model_connections(self) -> None:
        """Connect sub-model signals to update the main character."""
        # Relationship model connections
        self._relationship_model.relationshipAdded.connect(self._on_relationship_added)
        self._relationship_model.relationshipRemoved.connect(
            self._on_relationship_removed
        )
        self._relationship_model.relationshipUpdated.connect(
            self._on_relationship_updated
        )
        self._relationship_model.countChanged.connect(self.relationshipCountChanged)

        # Narrative model connections
        self._narrative_model.eventAdded.connect(self._on_event_added)
        self._narrative_model.eventRemoved.connect(self._on_event_removed)
        self._narrative_model.eventUpdated.connect(self._on_event_updated)
        self._narrative_model.countChanged.connect(self.eventCountChanged)

    def _sync_sub_models(self) -> None:
        """Synchronize sub-models with current character data."""
        if self._character:
            self._relationship_model.set_relationships(self._character.relationships)
            self._narrative_model.set_events(self._character.narrative_events)

    # === Basic Character Properties ===

    @pyqtProperty(str, notify=idChanged)
    def id(self) -> str:
        """Get character ID."""
        if self._character:
            if not hasattr(self._character, "id") or not self._character.id:
                import uuid

                self._character.id = str(uuid.uuid4())
            return self._character.id
        return ""

    @pyqtProperty(int, notify=levelChanged)
    def level(self) -> int:
        """Get character level."""
        if self._character:
            if not hasattr(self._character, "level"):
                self._character.level = 1
            return self._character.level
        return 1

    @level.setter
    def level(self, value: int) -> None:
        """Set character level."""
        if self._character and value != self._character.level:
            self._character.level = value
            self._character.touch()
            self.levelChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=nameChanged)
    def name(self) -> str:
        """Get character name."""
        return self._character.name if self._character else ""

    @name.setter
    def name(self, value: str) -> None:
        """Set character name."""
        if self._character and self._character.name != value:
            self._character.name = value
            self._character.touch()
            self.nameChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=ageChanged)
    def age(self) -> int:
        """Get character age."""
        if self._character:
            if not hasattr(self._character, "age"):
                self._character.age = DEFAULT_CHARACTER_AGE
            return self._character.age
        return 20

    @age.setter
    def age(self, value: int) -> None:
        """Set character age."""
        if self._character and self._character.age != value:
            self._character.age = value
            self._character.touch()
            self.ageChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=occupationChanged)
    def occupation(self) -> str:
        """Get character occupation."""
        if self._character:
            if not hasattr(self._character, "occupation"):
                self._character.occupation = ""
            return self._character.occupation
        return ""

    @occupation.setter
    def occupation(self, value: str) -> None:
        """Set character occupation."""
        if self._character and self._character.occupation != value:
            self._character.occupation = value
            self._character.touch()
            self.occupationChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=locationChanged)
    def location(self) -> str:
        """Get character location."""
        if self._character:
            if not hasattr(self._character, "location"):
                self._character.location = ""
            return self._character.location
        return ""

    @location.setter
    def location(self, value: str) -> None:
        """Set character location."""
        if self._character and self._character.location != value:
            self._character.location = value
            self._character.touch()
            self.locationChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=biographyChanged)
    def biography(self) -> str:
        """Get character biography."""
        return self._character.biography if self._character else ""

    @biography.setter
    def biography(self, value: str) -> None:
        """Set character biography."""
        if self._character and self._character.biography != value:
            self._character.biography = value
            self._character.touch()
            self.biographyChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=imageDataChanged)
    def imageData(self) -> str:
        """Get character image data."""
        return self._character.image_data if self._character else ""

    @imageData.setter
    def imageData(self, value: str) -> None:
        """Set character image data."""
        if self._character and self._character.image_data != value:
            self._character.image_data = value
            self._character.touch()
            self.imageDataChanged.emit()
            self.hasImageChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(bool, notify=hasImageChanged)
    def hasImage(self) -> bool:
        """Has the character an image"""
        return self._character.has_image

    @pyqtProperty("QVariantList", notify=affiliationsChanged)
    def affiliations(self) -> List[str]:
        """Get character affiliations."""
        return self._character.affiliations if self._character else []

    # === Stats Properties ===

    @pyqtProperty(int, notify=strengthChanged)
    def strength(self) -> int:
        """Get strength stat."""
        return self._character.stats.strength if self._character else DEFAULT_STAT_VALUE

    @strength.setter
    def strength(self, value: int) -> None:
        """Set strength stat."""
        if self._character and self._character.stats.strength != value:
            self._character.stats.strength = value
            self._character.touch()
            self.strengthChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=agilityChanged)
    def agility(self) -> int:
        """Get agility stat."""
        return self._character.stats.agility if self._character else DEFAULT_STAT_VALUE

    @agility.setter
    def agility(self, value: int) -> None:
        """Set agility stat."""
        if self._character and self._character.stats.agility != value:
            self._character.stats.agility = value
            self._character.touch()
            self.agilityChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=constitutionChanged)
    def constitution(self) -> int:
        """Get constitution stat."""
        return (
            self._character.stats.constitution
            if self._character
            else DEFAULT_STAT_VALUE
        )

    @constitution.setter
    def constitution(self, value: int) -> None:
        """Set constitution stat."""
        if self._character and self._character.stats.constitution != value:
            self._character.stats.constitution = value
            self._character.touch()
            self.constitutionChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=intelligenceChanged)
    def intelligence(self) -> int:
        """Get intelligence stat."""
        return (
            self._character.stats.intelligence
            if self._character
            else DEFAULT_STAT_VALUE
        )

    @intelligence.setter
    def intelligence(self, value: int) -> None:
        """Set intelligence stat."""
        if self._character and self._character.stats.intelligence != value:
            self._character.stats.intelligence = value
            self._character.touch()
            self.intelligenceChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=wisdomChanged)
    def wisdom(self) -> int:
        """Get wisdom stat."""
        return self._character.stats.wisdom if self._character else DEFAULT_STAT_VALUE

    @wisdom.setter
    def wisdom(self, value: int) -> None:
        """Set wisdom stat."""
        if self._character and self._character.stats.wisdom != value:
            self._character.stats.wisdom = value
            self._character.touch()
            self.wisdomChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(int, notify=charismaChanged)
    def charisma(self) -> int:
        """Get charisma stat."""
        return self._character.stats.charisma if self._character else DEFAULT_STAT_VALUE

    @charisma.setter
    def charisma(self, value: int) -> None:
        """Set charisma stat."""
        if self._character and self._character.stats.charisma != value:
            self._character.stats.charisma = value
            self._character.touch()
            self.charismaChanged.emit()
            self.statsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    # === Calculated Stats Properties ===

    @pyqtProperty(int, notify=statsChanged)
    def totalPoints(self) -> int:
        """Get total stat points."""
        return (
            self._character.stats.total_points
            if self._character
            else 6 * DEFAULT_STAT_VALUE
        )

    @pyqtProperty(float, notify=statsChanged)
    def averageStats(self) -> float:
        """Get average stat value."""
        return self._character.stats.average if self._character else 10.0

    @pyqtProperty(int, notify=statsChanged)
    def pointBuyCost(self) -> int:
        """Get point buy cost."""
        return self._character.stats.point_buy_cost if self._character else 0

    # === Enneagram Properties ===

    @pyqtProperty(int, notify=enneagramTypeChanged)
    def enneagramType(self) -> int:
        """Get Enneagram type."""
        return (
            self._character.enneagram.main_type.value
            if self._character
            else DEFAULT_ENNEAGRAM_TYPE.value
        )

    @enneagramType.setter
    def enneagramType(self, value: int) -> None:
        """Set Enneagram type."""
        if self._character and self._character.enneagram.main_type.value != value:
            from data.enums import EnneagramType

            try:
                self._character.enneagram.main_type = EnneagramType(value)
                self._character.touch()
                self.enneagramTypeChanged.emit()
                self.enneagramChanged.emit()
                self.characterChanged.emit()
                self._schedule_auto_save()
            except ValueError:
                pass  # Invalid value

    @pyqtProperty(int, notify=wingChanged)
    def wing(self) -> int:
        """Get Enneagram wing."""
        return self._character.enneagram.wing if self._character else 0

    @wing.setter
    def wing(self, value: int) -> None:
        """Set Enneagram wing."""
        if self._character and self._character.enneagram.wing != value:
            self._character.enneagram.wing = value
            self._character.touch()
            self.wingChanged.emit()
            self.enneagramChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    @pyqtProperty(str, notify=instinctChanged)
    def instinct(self) -> str:
        """Get Instinctual Variant."""
        return (
            self._character.enneagram.instinctual_variant.value
            if self._character
            else InstinctualVariant.SELF_PRESERVATION
        )

    @instinct.setter
    def instinct(self, value: str) -> None:
        """Set Instinctual Variant."""
        if self._character and self._character.enneagram.instinctual_variant.value != value:
            from data.enums import InstinctualVariant

            try:
                self._character.enneagram.instinctual_variant = InstinctualVariant(value)
                self._character.touch()
                self.instinctChanged.emit()
                self.enneagramChanged.emit()
                self.characterChanged.emit()
                self._schedule_auto_save()
            except ValueError:
                pass  # Invalid value

    @pyqtProperty(int, notify=developmentLevelChanged)
    def developmentLevel(self) -> int:
        """Get Enneagram development level."""
        return self._character.enneagram.development_level if self._character else DEFAULT_DEVELOPMENT_LEVEL

    @developmentLevel.setter
    def developmentLevel(self, value: int) -> None:
        """Set Enneagram development level."""
        if self._character and self._character.enneagram.development_level != value:
            self._character.enneagram.development_level = value
            self._character.touch()
            self.developmentLevelChanged.emit()
            self.enneagramChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()
        

    # === Phase 4: Sub-Models Properties ===

    @pyqtProperty(QObject, constant=True)
    def relationshipModel(self) -> RelationshipModel:
        """Get the relationship model."""
        return self._relationship_model

    @pyqtProperty(QObject, constant=True)
    def narrativeModel(self) -> NarrativeModel:
        """Get the narrative model."""
        return self._narrative_model

    @pyqtProperty(int, notify=relationshipCountChanged)
    def relationshipCount(self) -> int:
        """Get the number of relationships."""
        return len(self._character.relationships) if self._character else 0

    @pyqtProperty(int, notify=eventCountChanged)
    def eventCount(self) -> int:
        """Get the number of narrative events."""
        return len(self._character.narrative_events) if self._character else 0

    # === Character Management Methods ===

    def set_character(self, character: Character) -> None:
        """
        Set a new character and update all properties.

        Args:
            character: New Character instance
        """
        self._character = character
        self._sync_sub_models()

        # Emit all change signals
        self.characterChanged.emit()
        self.nameChanged.emit()
        self.ageChanged.emit()
        self.occupationChanged.emit()
        self.locationChanged.emit()
        self.biographyChanged.emit()
        self.imageDataChanged.emit()
        self.hasImageChanged.emit()
        self.affiliationsChanged.emit()
        self.statsChanged.emit()
        self.strengthChanged.emit()
        self.agilityChanged.emit()
        self.constitutionChanged.emit()
        self.intelligenceChanged.emit()
        self.wisdomChanged.emit()
        self.charismaChanged.emit()
        self.enneagramChanged.emit()
        self.enneagramTypeChanged.emit()
        self.wingChanged.emit()
        self.instinctChanged.emit()
        self.relationshipsChanged.emit()
        self.narrativeEventsChanged.emit()
        self.relationshipCountChanged.emit()
        self.eventCountChanged.emit()

    def get_character(self) -> Character:
        """
        Get the current character instance.

        Returns:
            Current Character instance
        """
        return self._character

    # === Affiliation Management ===

    @pyqtSlot(str)
    def addAffiliation(self, affiliation: str) -> None:
        """Add a new affiliation."""
        if self._character and affiliation.strip():
            affiliation = affiliation.strip()
            if affiliation not in self._character.affiliations:
                self._character.affiliations.append(affiliation)
                self._character.touch()
                self.affiliationsChanged.emit()
                self.characterChanged.emit()
                self._schedule_auto_save()

    @pyqtSlot(str)
    def removeAffiliation(self, affiliation: str) -> None:
        """Remove an affiliation."""
        if self._character and affiliation in self._character.affiliations:
            self._character.affiliations.remove(affiliation)
            self._character.touch()
            self.affiliationsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    # === Stats Management ===
    @pyqtSlot()
    def rollStats(self) -> None:
        """Roll stats using 4d6 drop lowest."""
        if self._character:
            self._character.stats.roll_4d6_drop_lowest()
            self._character.touch()
            self._emit_all_stats_signals()
            self._schedule_auto_save()

    @pyqtSlot()
    def resetStats(self) -> None:
        """Reset all stats to 10."""
        if self._character:
            self._character.stats.reset_to_default()
            self._character.touch()
            self._emit_all_stats_signals()
            self._schedule_auto_save()

    def _emit_all_stats_signals(self) -> None:
        """Emit all stats-related signals."""
        self.statsChanged.emit()
        self.strengthChanged.emit()
        self.agilityChanged.emit()
        self.constitutionChanged.emit()
        self.intelligenceChanged.emit()
        self.wisdomChanged.emit()
        self.charismaChanged.emit()
        self.characterChanged.emit()

    # === Phase 4: Relationship Management Callbacks ===

    def _on_relationship_added(self, target_id: str) -> None:
        """Handle relationship addition."""
        if self._character:
            # Get the relationship from the model
            relationships = self._relationship_model.get_relationships()
            self._character.relationships = relationships
            self._character.touch()
            self.relationshipsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    def _on_relationship_removed(self, target_id: str) -> None:
        """Handle relationship removal."""
        if self._character:
            relationships = self._relationship_model.get_relationships()
            self._character.relationships = relationships
            self._character.touch()
            self.relationshipsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    def _on_relationship_updated(self, target_id: str) -> None:
        """Handle relationship update."""
        if self._character:
            relationships = self._relationship_model.get_relationships()
            self._character.relationships = relationships
            self._character.touch()
            self.relationshipsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    # === Phase 4: Narrative Management Callbacks ===

    def _on_event_added(self, event_id: str) -> None:
        """Handle narrative event addition."""
        if self._character:
            events = self._narrative_model.get_events()
            self._character.narrative_events = events
            self._character.touch()
            self.narrativeEventsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    def _on_event_removed(self, event_id: str) -> None:
        """Handle narrative event removal."""
        if self._character:
            events = self._narrative_model.get_events()
            self._character.narrative_events = events
            self._character.touch()
            self.narrativeEventsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    def _on_event_updated(self, event_id: str) -> None:
        """Handle narrative event update."""
        if self._character:
            events = self._narrative_model.get_events()
            self._character.narrative_events = events
            self._character.touch()
            self.narrativeEventsChanged.emit()
            self.characterChanged.emit()
            self._schedule_auto_save()

    # === Auto-save functionality ===

    def _schedule_auto_save(self) -> None:
        """Schedule an auto-save operation."""
        self._auto_save_timer.start(self._auto_save_interval)

    def _on_auto_save(self) -> None:
        """Handle auto-save timer timeout."""
        # Signal that the character needs saving
        # This will be connected to the storage controller
        pass

    # === Utility Methods ===

    @pyqtSlot(result="QVariantMap")
    def getCharacterSummary(self) -> Dict[str, Any]:
        """
        Get a summary of the character for overview displays.

        Returns:
            Dictionary with character summary data
        """
        if not self._character:
            return {}

        return {
            StorageKeys.NAME.value: self._character.name,
            StorageKeys.AGE.value: self._character.age,
            StorageKeys.OCCUPATION.value: self._character.occupation,
            StorageKeys.LOCATION.value: self._character.location,
            StorageKeys.RELATIONSHIP_COUNT.value: len(self._character.relationships),
            StorageKeys.EVENT_COUNT.value: len(self._character.narrative_events),
            StorageKeys.TOTAL_STAT_POINTS.value: self._character.stats.total_points,
            StorageKeys.ENNEAGRAM_TYPE.value: self._character.enneagram.main_type.value,
            StorageKeys.HAS_IMAGE.value: bool(self._character.image_data),
            StorageKeys.LAST_MODIFIED.value: self._character.last_modified,
        }

    @pyqtSlot(result="QVariantList")
    def getRelationshipSummary(self) -> List[Dict[str, Any]]:
        """
        Get a summary of relationships for quick display.

        Returns:
            List of relationship summary dictionaries
        """
        if not self._character:
            return []

        summaries = []
        for rel in self._character.relationships:
            summaries.append(
                {
                    StorageKeys.NAME.value: rel.target_name,
                    StorageKeys.RELATIONSHIP_TYPE.value: rel.relationship_type.value,
                    StorageKeys.RELATIONSHIP_STRENGTH.value: rel.strength,
                    StorageKeys.POSITIVE_RELATIONSHIP.value: rel.is_positive,
                }
            )

        return summaries

    @pyqtSlot(result="QVariantList")
    def getTimelineHighlights(self) -> List[Dict[str, Any]]:
        """
        Get timeline highlights (major events) for quick display.

        Returns:
            List of major event dictionaries
        """
        if not self._character:
            return []

        highlights = []
        major_events = [
            e for e in self._character.narrative_events if e.importance >= 7
        ]

        for event in sorted(major_events, key=lambda e: e.importance, reverse=True)[:5]:
            highlights.append(
                {
                    StorageKeys.EVENT_TITLE.value: event.title,
                    StorageKeys.EVENT_DATE.value: event.date,
                    StorageKeys.EVENT_IMPORTANCE.value: event.importance,
                    StorageKeys.EVENT_DESCRIPTION.value: (
                        event.description[:100] + "..."
                        if len(event.description) > 100
                        else event.description
                    ),
                }
            )

        return highlights
