"""
Character data model with complete RPG character information.
"""

import uuid
import base64
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from models.enums import (
    StorageKeys, StatType, RelationType,
    EnneagramType, InstinctualVariant
)
from models.enneagram import EnneagramProfile


@dataclass
class CharacterStats:
    """Character ability scores for RPG mechanics."""
    strength: int = 10
    agility: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    
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
    def from_dict(cls, data: Dict[str, int]) -> 'CharacterStats':
        """
        Create CharacterStats from dictionary.
        
        Args:
            data: Dictionary with stat values
            
        Returns:
            CharacterStats instance
        """
        return cls(
            strength=data.get(StatType.STRENGTH.value, 10),
            agility=data.get(StatType.AGILITY.value, 10),
            constitution=data.get(StatType.CONSTITUTION.value, 10),
            intelligence=data.get(StatType.INTELLIGENCE.value, 10),
            wisdom=data.get(StatType.WISDOM.value, 10),
            charisma=data.get(StatType.CHARISMA.value, 10)
        )


@dataclass
class Relationship:
    """Relationship between two characters."""
    target_id: str
    target_name: str
    relationship_type: RelationType
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize relationship to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "target_id": self.target_id,
            "target_name": self.target_name,
            "type": self.relationship_type.value,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        """
        Create Relationship from dictionary.
        
        Args:
            data: Dictionary with relationship data
            
        Returns:
            Relationship instance
        """
        return cls(
            target_id=data["target_id"],
            target_name=data["target_name"],
            relationship_type=RelationType(data["type"]),
            description=data.get("description", "")
        )


@dataclass
class NarrativeEvent:
    """Single event in character's narrative progression."""
    timestamp: datetime
    title: str
    description: str
    chapter: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize event to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "timestamp": self.timestamp.isoformat(),
            "title": self.title,
            "description": self.description,
            "chapter": self.chapter
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NarrativeEvent':
        """
        Create NarrativeEvent from dictionary.
        
        Args:
            data: Dictionary with event data
            
        Returns:
            NarrativeEvent instance
        """
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            title=data["title"],
            description=data["description"],
            chapter=data.get("chapter")
        )


@dataclass
class Character:
    """Complete character profile for medieval RPG."""
    
    # Basic information
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "New Character"
    level: int = 1
    image_data: Optional[str] = None  # Base64 encoded image
    
    # Personality
    enneagram: EnneagramProfile = field(default_factory=EnneagramProfile)
    
    # Game mechanics
    stats: CharacterStats = field(default_factory=CharacterStats)
    
    # Story elements
    biography: str = ""
    relationships: List[Relationship] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    narrative_events: List[NarrativeEvent] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1  # For future compatibility
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize character to dictionary for storage.
        
        Returns:
            Complete dictionary representation
        """
        return {
            StorageKeys.CHARACTER_ID.value: self.id,
            StorageKeys.NAME.value: self.name,
            StorageKeys.LEVEL.value: self.level,
            StorageKeys.IMAGE_DATA.value: self.image_data,
            StorageKeys.ENNEAGRAM.value: self.enneagram.to_dict(),
            StorageKeys.STATS.value: self.stats.to_dict(),
            StorageKeys.BIOGRAPHY.value: self.biography,
            StorageKeys.RELATIONSHIPS.value: [r.to_dict() for r in self.relationships],
            StorageKeys.AFFILIATIONS.value: self.affiliations,
            StorageKeys.NARRATIVE.value: [e.to_dict() for e in self.narrative_events],
            StorageKeys.CREATED_AT.value: self.created_at.isoformat(),
            StorageKeys.UPDATED_AT.value: self.updated_at.isoformat(),
            StorageKeys.VERSION.value: self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """
        Deserialize character from dictionary.
        
        Args:
            data: Dictionary with character data
            
        Returns:
            Character instance
        """
        character = cls()
        
        # Basic information
        character.id = data.get(StorageKeys.CHARACTER_ID.value, character.id)
        character.name = data.get(StorageKeys.NAME.value, character.name)
        character.level = data.get(StorageKeys.LEVEL.value, character.level)
        character.image_data = data.get(StorageKeys.IMAGE_DATA.value)
        
        # Load Enneagram profile
        if StorageKeys.ENNEAGRAM.value in data:
            character.enneagram = EnneagramProfile.from_dict(
                data[StorageKeys.ENNEAGRAM.value]
            )
        
        # Load stats
        if StorageKeys.STATS.value in data:
            character.stats = CharacterStats.from_dict(
                data[StorageKeys.STATS.value]
            )
        
        # Story elements
        character.biography = data.get(StorageKeys.BIOGRAPHY.value, "")
        character.affiliations = data.get(StorageKeys.AFFILIATIONS.value, [])
        
        # Load relationships
        if StorageKeys.RELATIONSHIPS.value in data:
            character.relationships = [
                Relationship.from_dict(r)
                for r in data[StorageKeys.RELATIONSHIPS.value]
            ]
        
        # Load narrative events
        if StorageKeys.NARRATIVE.value in data:
            character.narrative_events = [
                NarrativeEvent.from_dict(e)
                for e in data[StorageKeys.NARRATIVE.value]
            ]
        
        # Metadata
        if StorageKeys.CREATED_AT.value in data:
            character.created_at = datetime.fromisoformat(
                data[StorageKeys.CREATED_AT.value]
            )
        if StorageKeys.UPDATED_AT.value in data:
            character.updated_at = datetime.fromisoformat(
                data[StorageKeys.UPDATED_AT.value]
            )
        character.version = data.get(StorageKeys.VERSION.value, 1)
        
        return character
    
    def add_relationship(self, target: 'Character', 
                        rel_type: RelationType, 
                        description: str = ""):
        """
        Add a relationship to another character.
        
        Args:
            target: Target character
            rel_type: Type of relationship
            description: Optional description
        """
        relationship = Relationship(
            target_id=target.id,
            target_name=target.name,
            relationship_type=rel_type,
            description=description
        )
        self.relationships.append(relationship)
        self.updated_at = datetime.now()
    
    def add_narrative_event(self, title: str, description: str, 
                           chapter: Optional[str] = None):
        """
        Add a narrative event to the character's timeline.
        
        Args:
            title: Event title
            description: Event description
            chapter: Optional chapter name
        """
        event = NarrativeEvent(
            timestamp=datetime.now(),
            title=title,
            description=description,
            chapter=chapter
        )
        self.narrative_events.append(event)
        self.updated_at = datetime.now()
    
    def get_relationship_with(self, character_id: str) -> Optional[Relationship]:
        """
        Get relationship with a specific character.
        
        Args:
            character_id: ID of the other character
            
        Returns:
            Relationship if found, None otherwise
        """
        for rel in self.relationships:
            if rel.target_id == character_id:
                return rel
        return None
    
    def set_image_from_file(self, file_path: Path):
        """
        Set character image from file path.
        
        Args:
            file_path: Path to image file
        """
        if file_path.exists():
            with open(file_path, 'rb') as f:
                self.image_data = base64.b64encode(f.read()).decode('utf-8')
            self.updated_at = datetime.now()
    
    def get_image_pixmap(self):
        """
        Get character image as QPixmap.
        
        Returns:
            QPixmap or None if no image
        """
        if self.image_data:
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(self.image_data))
            return pixmap
        return None