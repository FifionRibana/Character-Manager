"""
Character data model with complete RPG character information.
Migrated to Python 3.11+ with modern features and pathlib support.
"""

from __future__ import annotations

import uuid
import base64
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, ClassVar
from pathlib import Path

from .enums import (
    StorageKeys, StatType, RelationType, EnneagramType, 
    InstinctualVariant, DevelopmentLevel, ValidationLimits,
    DEFAULT_STAT_VALUE, DEFAULT_DEVELOPMENT_LEVEL, 
    DEFAULT_CHARACTER_LEVEL, DEFAULT_ENNEAGRAM_TYPE
)
from .enneagram import EnneagramProfile


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
        for stat_name in ["strength", "agility", "constitution", "intelligence", "wisdom", "charisma"]:
            value = getattr(self, stat_name)
            if not ValidationLimits.MIN_STAT_VALUE <= value <= ValidationLimits.MAX_STAT_VALUE:
                raise ValueError(f"{stat_name} must be between {ValidationLimits.MIN_STAT_VALUE} and {ValidationLimits.MAX_STAT_VALUE}")
    
    @property
    def total_points(self) -> int:
        """Calculate total stat points allocated."""
        return self.strength + self.agility + self.constitution + self.intelligence + self.wisdom + self.charisma
    
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
            StatType.CHARISMA.value: self.charisma
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
            charisma=data.get(StatType.CHARISMA.value, DEFAULT_STAT_VALUE)
        )
    
    @classmethod
    def create_standard_array(cls) -> CharacterStats:
        """Create stats using D&D 5e standard array."""
        return cls(
            strength=15, agility=14, constitution=13,
            intelligence=12, wisdom=10, charisma=8
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


@dataclass
class Relationship:
    """Relationship between two characters."""
    target_id: str
    target_name: str
    relationship_type: RelationType
    description: str = ""
    strength: int = 5  # 1-10 scale
    
    def __post_init__(self) -> None:
        """Validate relationship data."""
        if not ValidationLimits.MIN_CHARACTER_NAME_LENGTH <= len(self.target_name) <= ValidationLimits.MAX_CHARACTER_NAME_LENGTH:
            raise ValueError("Target name length is invalid")
        
        if not 1 <= self.strength <= 10:
            raise ValueError("Relationship strength must be between 1 and 10")
        
        if len(self.description) > ValidationLimits.MAX_RELATIONSHIP_DESCRIPTION_LENGTH:
            raise ValueError("Relationship description too long")
    
    @property
    def is_positive(self) -> bool:
        """Check if this is generally a positive relationship."""
        positive_types = {
            RelationType.FAMILY, RelationType.FRIEND, RelationType.MENTOR,
            RelationType.APPRENTICE, RelationType.ALLY, RelationType.LOVER
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
            "type": self.relationship_type.value,
            "description": self.description,
            "strength": self.strength
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
            relationship_type=RelationType(data.get("type", RelationType.NEUTRAL.value)),
            description=data.get("description", ""),
            strength=data.get("strength", 5)
        )


@dataclass
class NarrativeEvent:
    """A significant event in the character's story."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    date: str = ""  # Flexible date format for fantasy settings
    importance: int = 5  # 1-10 scale
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validate event data."""
        if not 1 <= self.importance <= 10:
            raise ValueError("Event importance must be between 1 and 10")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            StorageKeys.CHARACTER_ID.value: self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "importance": self.importance,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NarrativeEvent:
        """Create NarrativeEvent from dictionary."""
        return cls(
            id=data.get(StorageKeys.CHARACTER_ID.value, str(uuid.uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            date=data.get("date", ""),
            importance=data.get("importance", 5),
            tags=data.get("tags", [])
        )


@dataclass
class Character:
    """
    Complete character data model for RPG characters.
    
    Modern implementation using Python 3.11+ features.
    """
    
    # Class variable for version tracking
    VERSION: ClassVar[str] = "2.0"
    
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unnamed Character"
    level: int = DEFAULT_CHARACTER_LEVEL
    age: int = 20
    occupation: str = "Adventurer"
    location: str = "Kingdom"
    
    # Visual representation
    image_data: str = ""  # Base64 encoded image
    
    # Personality and psychology
    enneagram: EnneagramProfile = field(default_factory=EnneagramProfile)
    
    # Game mechanics
    stats: CharacterStats = field(default_factory=CharacterStats)
    
    # Biographical information
    biography: str = ""
    affiliations: List[str] = field(default_factory=list)
    
    # Social connections
    relationships: List[Relationship] = field(default_factory=list)
    
    # Story and narrative
    narrative_events: List[NarrativeEvent] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    def __post_init__(self) -> None:
        """Validate character data after initialization."""
        self._validate_core_data()
        self.touch()  # Update timestamp
    
    def _validate_core_data(self) -> None:
        """Validate core character data."""
        # Validate name
        if not isinstance(self.name, str):
            raise ValueError("Character name must be a string")
        
        name_length = len(self.name.strip())
        if not ValidationLimits.MIN_CHARACTER_NAME_LENGTH <= name_length <= ValidationLimits.MAX_CHARACTER_NAME_LENGTH:
            raise ValueError(f"Character name must be {ValidationLimits.MIN_CHARACTER_NAME_LENGTH}-{ValidationLimits.MAX_CHARACTER_NAME_LENGTH} characters")
        
        # Validate level - CORRECTION DU PROBLÈME PRINCIPAL
        if not isinstance(self.level, int):
            raise ValueError("Character level must be an integer")
        
        if not ValidationLimits.MIN_CHARACTER_LEVEL <= self.level <= ValidationLimits.MAX_CHARACTER_LEVEL:
            raise ValueError(f"Character level must be {ValidationLimits.MIN_CHARACTER_LEVEL}-{ValidationLimits.MAX_CHARACTER_LEVEL}")
        
        # Validate biography length
        if isinstance(self.biography, str) and len(self.biography) > ValidationLimits.MAX_BIOGRAPHY_LENGTH:
            raise ValueError(f"Biography must be less than {ValidationLimits.MAX_BIOGRAPHY_LENGTH} characters")

    
    def touch(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.now()
    
    @property
    def age_days(self) -> int:
        """Calculate how many days old this character is."""
        return (datetime.now() - self.created_at).days
    
    @property
    def enneagram_display(self) -> str:
        """Get formatted Enneagram type display."""
        return self.enneagram.get_wing_notation()
    
    @property
    def total_stat_points(self) -> int:
        """Get total stat points allocated."""
        return self.stats.total_points
    
    @property
    def relationship_count(self) -> int:
        """Get the number of relationships."""
        return len(self.relationships)
    
    @property
    def has_image(self) -> bool:
        """Check if character has an image."""
        return bool(self.image_data)
    
    def add_relationship(self, target_id: str, target_name: str, 
                        relationship_type: RelationType, description: str = "") -> None:
        """
        Add a new relationship.
        
        Args:
            target_id: ID of the target character
            target_name: Name of the target character
            relationship_type: Type of relationship
            description: Optional description
        """
        # Check if relationship already exists
        for rel in self.relationships:
            if rel.target_id == target_id:
                # Update existing relationship
                rel.relationship_type = relationship_type
                rel.description = description
                self.touch()
                return
        
        # Add new relationship
        new_relationship = Relationship(
            target_id=target_id,
            target_name=target_name,
            relationship_type=relationship_type,
            description=description
        )
        self.relationships.append(new_relationship)
        self.touch()
    
    def remove_relationship(self, target_id: str) -> bool:
        """
        Remove a relationship by target ID.
        
        Args:
            target_id: ID of the target character
            
        Returns:
            True if relationship was removed, False if not found
        """
        for i, rel in enumerate(self.relationships):
            if rel.target_id == target_id:
                del self.relationships[i]
                self.touch()
                return True
        return False
    
    def add_narrative_event(self, title: str, description: str = "", 
                          date: str = "", importance: int = 5, tags: List[str] | None = None) -> str:
        """
        Add a new narrative event.
        
        Args:
            title: Event title
            description: Event description
            date: Event date (flexible format)
            importance: Importance scale 1-10
            tags: Optional tags
            
        Returns:
            ID of the created event
        """
        if tags is None:
            tags = []
        
        event = NarrativeEvent(
            title=title,
            description=description,
            date=date,
            importance=importance,
            tags=tags
        )
        self.narrative_events.append(event)
        self.touch()
        return event.id
    
    def remove_narrative_event(self, event_id: str) -> bool:
        """
        Remove a narrative event by ID.
        
        Args:
            event_id: ID of the event to remove
            
        Returns:
            True if event was removed, False if not found
        """
        for i, event in enumerate(self.narrative_events):
            if event.id == event_id:
                del self.narrative_events[i]
                self.touch()
                return True
        return False
    
    def set_image_from_path(self, image_path: Path) -> None:
        """
        Load and set character image from file path.
        
        Args:
            image_path: Path to image file
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If file is not a valid image
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            with image_path.open("rb") as image_file:
                image_bytes = image_file.read()
                self.image_data = base64.b64encode(image_bytes).decode("utf-8")
                self.touch()
        except Exception as e:
            raise ValueError(f"Failed to load image: {e}") from e
    
    def save_image_to_path(self, output_path: Path) -> None:
        """
        Save character image to file path.
        
        Args:
            output_path: Path where to save the image
            
        Raises:
            ValueError: If no image data available
        """
        if not self.image_data:
            raise ValueError("No image data available")
        
        try:
            image_bytes = base64.b64decode(self.image_data)
            with output_path.open("wb") as output_file:
                output_file.write(image_bytes)
        except Exception as e:
            raise ValueError(f"Failed to save image: {e}") from e
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize character to dictionary for JSON storage.
        
        Returns:
            Dictionary representation using enum keys
        """
        return {
            StorageKeys.CHARACTER_ID.value: self.id,
            StorageKeys.NAME.value: self.name,
            StorageKeys.LEVEL.value: self.level,
            StorageKeys.IMAGE_DATA.value: self.image_data,
            StorageKeys.ENNEAGRAM.value: self.enneagram.to_dict(),
            StorageKeys.STATS.value: self.stats.to_dict(),
            StorageKeys.BIOGRAPHY.value: self.biography,
            StorageKeys.AFFILIATIONS.value: self.affiliations,
            StorageKeys.RELATIONSHIPS.value: [rel.to_dict() for rel in self.relationships],
            StorageKeys.NARRATIVE.value: [event.to_dict() for event in self.narrative_events],
            StorageKeys.CREATED_AT.value: self.created_at.isoformat(),
            StorageKeys.UPDATED_AT.value: self.updated_at.isoformat(),
            StorageKeys.VERSION.value: self.VERSION,
            "tags": self.tags,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Character:
        """
        Create Character from dictionary.
        
        Args:
            data: Dictionary with character data
            
        Returns:
            Character instance
        """
        # Parse datetime fields
        created_at = datetime.fromisoformat(data.get(StorageKeys.CREATED_AT.value, datetime.now().isoformat()))
        updated_at = datetime.fromisoformat(data.get(StorageKeys.UPDATED_AT.value, datetime.now().isoformat()))
        
        # Parse complex objects
        enneagram_data = data.get(StorageKeys.ENNEAGRAM.value, {})
        enneagram = EnneagramProfile.from_dict(enneagram_data) if enneagram_data else EnneagramProfile()
        
        stats_data = data.get(StorageKeys.STATS.value, {})
        stats = CharacterStats.from_dict(stats_data) if stats_data else CharacterStats()
        
        relationships = [
            Relationship.from_dict(rel_data) 
            for rel_data in data.get(StorageKeys.RELATIONSHIPS.value, [])
        ]
        
        narrative_events = [
            NarrativeEvent.from_dict(event_data)
            for event_data in data.get(StorageKeys.NARRATIVE.value, [])
        ]
        
        return cls(
            id=data.get(StorageKeys.CHARACTER_ID.value, str(uuid.uuid4())),
            name=data.get(StorageKeys.NAME.value, "Unnamed Character"),
            level=data.get(StorageKeys.LEVEL.value, DEFAULT_CHARACTER_LEVEL),
            image_data=data.get(StorageKeys.IMAGE_DATA.value, ""),
            enneagram=enneagram,
            stats=stats,
            biography=data.get(StorageKeys.BIOGRAPHY.value, ""),
            affiliations=data.get(StorageKeys.AFFILIATIONS.value, []),
            relationships=relationships,
            narrative_events=narrative_events,
            created_at=created_at,
            updated_at=updated_at,
            tags=data.get("tags", []),
            notes=data.get("notes", "")
        )
    
    @classmethod
    def create_default(cls, name: str = "New Character") -> Character:
        """
        Create a character with sensible defaults.
        
        Args:
            name: Character name
            
        Returns:
            Character with default values
        """
        return cls(
            name=name,
            stats=CharacterStats(),
            enneagram=EnneagramProfile()
        )
    
    def clone(self, new_name: str | None = None) -> Character:
        """
        Create a copy of this character with a new ID.
        
        Args:
            new_name: Optional new name for the clone
            
        Returns:
            Cloned character
        """
        character_dict = self.to_dict()
        character_dict[StorageKeys.CHARACTER_ID.value] = str(uuid.uuid4())
        
        if new_name:
            character_dict[StorageKeys.NAME.value] = new_name
        else:
            character_dict[StorageKeys.NAME.value] = f"{self.name} (Copy)"
        
        # Reset timestamps
        now = datetime.now()
        character_dict[StorageKeys.CREATED_AT.value] = now.isoformat()
        character_dict[StorageKeys.UPDATED_AT.value] = now.isoformat()
        
        return cls.from_dict(character_dict)