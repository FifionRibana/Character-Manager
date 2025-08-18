"""
Character model for QML interface.
Exposes character data to QML views using Qt's property system.
Enhanced with full character data support.
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, QUrl
from PyQt6.QtGui import QPixmap
from typing import Optional, List
from data.character import Character
from data.enums import StatType, EnneagramType


class CharacterModel(QObject):
    """
    Enhanced character model that exposes character data to QML.
    Handles property binding and change notifications for all character aspects.
    """
    
    # Signals for property changes
    nameChanged = pyqtSignal()
    levelChanged = pyqtSignal()
    imageChanged = pyqtSignal()
    statsChanged = pyqtSignal()
    enneagramChanged = pyqtSignal()
    biographyChanged = pyqtSignal()
    affiliationsChanged = pyqtSignal()
    relationshipsChanged = pyqtSignal()
    narrativeChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._character: Optional[Character] = None
    
    def load_character(self, character: Character):
        """Load a character and emit change signals."""
        if self._character == character:
            return
            
        self._character = character
        
        # Emit all change signals
        self.nameChanged.emit()
        self.levelChanged.emit()
        self.imageChanged.emit()
        self.statsChanged.emit()
        self.enneagramChanged.emit()
        self.biographyChanged.emit()
        self.affiliationsChanged.emit()
        self.relationshipsChanged.emit()
        self.narrativeChanged.emit()
    
    def clear(self):
        """Clear the current character."""
        if self._character is None:
            return
            
        self._character = None
        
        # Emit all change signals
        self.nameChanged.emit()
        self.levelChanged.emit()
        self.imageChanged.emit()
        self.statsChanged.emit()
        self.enneagramChanged.emit()
        self.biographyChanged.emit()
        self.affiliationsChanged.emit()
        self.relationshipsChanged.emit()
        self.narrativeChanged.emit()
    
    # Basic Character Properties
    @pyqtProperty(str, notify=nameChanged)
    def name(self) -> str:
        return self._character.name if self._character else ""
    
    @name.setter
    def name(self, value: str):
        if self._character and self._character.name != value:
            self._character.name = value
            self.nameChanged.emit()
    
    @pyqtProperty(int, notify=levelChanged)
    def level(self) -> int:
        return self._character.level if self._character else 1
    
    @level.setter
    def level(self, value: int):
        if self._character and self._character.level != value:
            self._character.level = value
            self.levelChanged.emit()
    
    # Image property
    @pyqtProperty(QUrl, notify=imageChanged)
    def imageUrl(self) -> QUrl:
        if not self._character or not self._character.image_data:
            return QUrl()
        
        # Convert base64 to data URL for QML
        return QUrl(f"data:image/png;base64,{self._character.image_data}")
    
    # Stats properties
    @pyqtProperty(int, notify=statsChanged)
    def strength(self) -> int:
        return self._character.stats.strength if self._character else 10
    
    @strength.setter
    def strength(self, value: int):
        if self._character and self._character.stats.strength != value:
            self._character.stats.strength = value
            self.statsChanged.emit()
    
    @pyqtProperty(int, notify=statsChanged)
    def agility(self) -> int:
        return self._character.stats.agility if self._character else 10
    
    @agility.setter
    def agility(self, value: int):
        if self._character and self._character.stats.agility != value:
            self._character.stats.agility = value
            self.statsChanged.emit()
    
    @pyqtProperty(int, notify=statsChanged)
    def constitution(self) -> int:
        return self._character.stats.constitution if self._character else 10
    
    @constitution.setter
    def constitution(self, value: int):
        if self._character and self._character.stats.constitution != value:
            self._character.stats.constitution = value
            self.statsChanged.emit()
    
    @pyqtProperty(int, notify=statsChanged)
    def intelligence(self) -> int:
        return self._character.stats.intelligence if self._character else 10
    
    @intelligence.setter
    def intelligence(self, value: int):
        if self._character and self._character.stats.intelligence != value:
            self._character.stats.intelligence = value
            self.statsChanged.emit()
    
    @pyqtProperty(int, notify=statsChanged)
    def wisdom(self) -> int:
        return self._character.stats.wisdom if self._character else 10
    
    @wisdom.setter
    def wisdom(self, value: int):
        if self._character and self._character.stats.wisdom != value:
            self._character.stats.wisdom = value
            self.statsChanged.emit()
    
    @pyqtProperty(int, notify=statsChanged)
    def charisma(self) -> int:
        return self._character.stats.charisma if self._character else 10
    
    @charisma.setter
    def charisma(self, value: int):
        if self._character and self._character.stats.charisma != value:
            self._character.stats.charisma = value
            self.statsChanged.emit()
    
    # Enneagram properties
    @pyqtProperty(int, notify=enneagramChanged)
    def enneagramType(self) -> int:
        return self._character.enneagram.main_type.value if self._character else 9
    
    @enneagramType.setter
    def enneagramType(self, value: int):
        if self._character and self._character.enneagram.main_type.value != value:
            self._character.enneagram.main_type = EnneagramType(value)
            self.enneagramChanged.emit()
    
    @pyqtProperty(str, notify=enneagramChanged)
    def enneagramWing(self) -> str:
        if not self._character:
            return ""
        return self._character.enneagram.get_wing_notation()
    
    @pyqtProperty(int, notify=enneagramChanged)
    def developmentLevel(self) -> int:
        return self._character.enneagram.development_level if self._character else 5
    
    @developmentLevel.setter
    def developmentLevel(self, value: int):
        if self._character and self._character.enneagram.development_level != value:
            self._character.enneagram.development_level = value
            self.enneagramChanged.emit()
    
    # Biography property
    @pyqtProperty(str, notify=biographyChanged)
    def biography(self) -> str:
        return self._character.biography if self._character else ""
    
    @biography.setter
    def biography(self, value: str):
        if self._character and self._character.biography != value:
            self._character.biography = value
            self.biographyChanged.emit()
    
    # Affiliations (as string list for QML)
    @pyqtProperty('QStringList', notify=affiliationsChanged)
    def affiliations(self) -> List[str]:
        return self._character.affiliations if self._character else []
    
    # Relationships count
    @pyqtProperty(int, notify=relationshipsChanged)
    def relationshipsCount(self) -> int:
        return len(self._character.relationships) if self._character else 0
    
    # Narrative events count
    @pyqtProperty(int, notify=narrativeChanged)
    def narrativeEventsCount(self) -> int:
        return len(self._character.narrative_events) if self._character else 0
    
    # Helper methods for QML
    @pyqtProperty(bool, notify=nameChanged)
    def hasCharacter(self) -> bool:
        """Check if a character is loaded."""
        return self._character is not None
    
    @pyqtProperty(str, notify=nameChanged)
    def characterId(self) -> str:
        """Get character ID."""
        return self._character.id if self._character else ""
    
    # Character creation/modification dates
    @pyqtProperty(str, notify=nameChanged)
    def createdAt(self) -> str:
        """Get creation date as string."""
        if not self._character:
            return ""
        return self._character.created_at.strftime("%Y-%m-%d %H:%M")
    
    @pyqtProperty(str, notify=nameChanged)
    def updatedAt(self) -> str:
        """Get last update date as string."""
        if not self._character:
            return ""
        return self._character.updated_at.strftime("%Y-%m-%d %H:%M")
    
    @pyqtProperty(int, notify=nameChanged)
    def version(self) -> int:
        """Get character version."""
        return self._character.version if self._character else 1
    
    # Stats helper methods
    def getStatModifier(self, stat_value: int) -> int:
        """Calculate D&D style modifier for a stat."""
        return (stat_value - 10) // 2
    
    @pyqtProperty(int, notify=statsChanged)
    def totalStatPoints(self) -> int:
        """Get total stat points."""
        if not self._character:
            return 60
        
        return (self._character.stats.strength + self._character.stats.agility + 
                self._character.stats.constitution + self._character.stats.intelligence + 
                self._character.stats.wisdom + self._character.stats.charisma)
    
    # Enneagram helper methods
    @pyqtProperty(str, notify=enneagramChanged)
    def enneagramTypeName(self) -> str:
        """Get the name of the current Enneagram type."""
        if not self._character:
            return "The Peacemaker"
        
        type_names = {
            1: "The Reformer", 2: "The Helper", 3: "The Achiever",
            4: "The Individualist", 5: "The Investigator", 6: "The Loyalist",
            7: "The Enthusiast", 8: "The Challenger", 9: "The Peacemaker"
        }
        return type_names.get(self._character.enneagram.main_type.value, "Unknown")
    
    @pyqtProperty(str, notify=enneagramChanged)
    def enneagramTypeDescription(self) -> str:
        """Get the description of the current Enneagram type."""
        if not self._character:
            return "Receptive, reassuring, complacent, and resigned."
        
        type_descriptions = {
            1: "Principled, purposeful, self-controlled, and perfectionistic.",
            2: "Generous, demonstrative, people-pleasing, and possessive.",
            3: "Adaptable, excelling, driven, and image-conscious.",
            4: "Expressive, dramatic, self-absorbed, and temperamental.",
            5: "Perceptive, innovative, secretive, and isolated.",
            6: "Engaging, responsible, anxious, and suspicious.",
            7: "Spontaneous, versatile, acquisitive, and scattered.",
            8: "Self-confident, decisive, willful, and confrontational.",
            9: "Receptive, reassuring, complacent, and resigned."
        }
        return type_descriptions.get(self._character.enneagram.main_type.value, "Unknown type.")
    
    # Methods callable from QML
    @pyqtSlot(str)
    def addAffiliation(self, name: str):
        """Add an affiliation to the character."""
        if self._character and name.strip():
            self._character.affiliations.append(name.strip())
            self.affiliationsChanged.emit()
    
    @pyqtSlot(int)
    def removeAffiliation(self, index: int):
        """Remove an affiliation by index."""
        if self._character and 0 <= index < len(self._character.affiliations):
            del self._character.affiliations[index]
            self.affiliationsChanged.emit()
    
    @pyqtSlot(str, result=str)
    def setImageFromPath(self, path: str) -> str:
        """Set character image from file path."""
        if not self._character:
            return "No character loaded"
        
        try:
            # Remove file:// prefix if present
            if path.startswith("file://"):
                path = path[7:]
            
            from pathlib import Path
            file_path = Path(path)
            
            if file_path.exists():
                import base64
                with open(file_path, 'rb') as f:
                    self._character.image_data = base64.b64encode(f.read()).decode('utf-8')
                self.imageChanged.emit()
                return "Image loaded successfully"
            else:
                return "File not found"
        except Exception as e:
            return f"Error loading image: {str(e)}"