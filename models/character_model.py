"""
Extended Character model for PyQt6/QML integration.
Provides reactive properties for all character data including Enneagram.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict, List
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty
from PyQt6.QtQml import QQmlEngine, qmlRegisterType

from data.character import Character
from data.enneagram import EnneagramProfile
from data.enums import EnneagramType, StatType, DEFAULT_CHARACTER_LEVEL


class CharacterModel(QObject):
    """
    Extended PyQt model for Character data with comprehensive QML property bindings.
    
    Provides reactive properties for:
    - Core character info (name, level, image)
    - Complete Enneagram profile
    - All character stats
    - Biographical information
    - Timestamps and metadata
    """
    
    # Core property change signals
    nameChanged = pyqtSignal()
    levelChanged = pyqtSignal()
    imageDataChanged = pyqtSignal()
    
    # Enneagram property signals
    enneagramTypeChanged = pyqtSignal()
    enneagramWingChanged = pyqtSignal()
    instinctualVariantChanged = pyqtSignal()
    developmentLevelChanged = pyqtSignal()
    enneagramNotationChanged = pyqtSignal()
    
    # Stats property signals
    strengthChanged = pyqtSignal()
    agilityChanged = pyqtSignal()
    constitutionChanged = pyqtSignal()
    intelligenceChanged = pyqtSignal()
    wisdomChanged = pyqtSignal()
    charismaChanged = pyqtSignal()
    totalStatsChanged = pyqtSignal()
    
    # Biographical signals
    biographyChanged = pyqtSignal()
    affiliationsChanged = pyqtSignal()
    
    # Metadata signals
    createdAtChanged = pyqtSignal()
    updatedAtChanged = pyqtSignal()
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._character: Optional[Character] = None
        
    def set_character(self, character: Optional[Character]) -> None:
        """
        Set the character and emit all necessary change signals.
        
        Args:
            character: Character instance or None
        """
        if self._character == character:
            return
            
        self._character = character
        
        # Emit all change signals to update QML bindings
        self.nameChanged.emit()
        self.levelChanged.emit()
        self.imageDataChanged.emit()
        
        # Enneagram signals
        self.enneagramTypeChanged.emit()
        self.enneagramWingChanged.emit()
        self.instinctualVariantChanged.emit()
        self.developmentLevelChanged.emit()
        self.enneagramNotationChanged.emit()
        
        # Stats signals
        self.strengthChanged.emit()
        self.agilityChanged.emit()
        self.constitutionChanged.emit()
        self.intelligenceChanged.emit()
        self.wisdomChanged.emit()
        self.charismaChanged.emit()
        self.totalStatsChanged.emit()
        
        # Biography signals
        self.biographyChanged.emit()
        self.affiliationsChanged.emit()
        
        # Metadata signals
        self.createdAtChanged.emit()
        self.updatedAtChanged.emit()
    
    def get_character(self) -> Optional[Character]:
        """
        Get the current character.
        
        Returns:
            Current Character instance or None
        """
        return self._character
    
    # Core character properties
    @pyqtProperty(str, notify=nameChanged)
    def name(self) -> str:
        """Character name."""
        return self._character.name if self._character else ""
    
    @name.setter
    def name(self, value: str) -> None:
        """Set character name."""
        if self._character and self._character.name != value:
            self._character.name = value
            self._character.touch()
            self.nameChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=levelChanged)
    def level(self) -> int:
        """Character level."""
        return self._character.level if self._character else DEFAULT_CHARACTER_LEVEL
    
    @level.setter
    def level(self, value: int) -> None:
        """Set character level."""
        if self._character and self._character.level != value:
            self._character.level = value
            self._character.touch()
            self.levelChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(str, notify=imageDataChanged)
    def imageData(self) -> str:
        """Character image data (base64)."""
        return self._character.image_data if self._character else ""
    
    @imageData.setter
    def imageData(self, value: str) -> None:
        """Set character image data."""
        if self._character and self._character.image_data != value:
            self._character.image_data = value
            self._character.touch()
            self.imageDataChanged.emit()
            self.updatedAtChanged.emit()
    
    # Enneagram properties
    @pyqtProperty(int, notify=enneagramTypeChanged)
    def enneagramType(self) -> int:
        """Main Enneagram type (1-9)."""
        return int(self._character.enneagram.main_type.value) if self._character else 9
    
    @enneagramType.setter
    def enneagramType(self, value: int) -> None:
        """Set main Enneagram type."""
        if self._character and 1 <= value <= 9:
            new_type = EnneagramType(value)
            if self._character.enneagram.main_type != new_type:
                self._character.enneagram.main_type = new_type
                # Auto-update integration/disintegration points
                self._character.enneagram.integration_point = new_type.integration_point
                self._character.enneagram.disintegration_point = new_type.disintegration_point
                self._character.touch()
                
                self.enneagramTypeChanged.emit()
                self.enneagramNotationChanged.emit()
                self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=enneagramWingChanged)
    def enneagramWing(self) -> int:
        """Enneagram wing (0 for no wing, 1-9 for wing type)."""
        return int(self._character.enneagram.wing.value) if self._character and self._character.enneagram.wing else 0
    
    @enneagramWing.setter
    def enneagramWing(self, value: int) -> None:
        """Set Enneagram wing."""
        if self._character:
            new_wing = EnneagramType(value) if value > 0 else None
            if self._character.enneagram.wing != new_wing:
                self._character.enneagram.wing = new_wing
                self._character.touch()
                
                self.enneagramWingChanged.emit()
                self.enneagramNotationChanged.emit()
                self.updatedAtChanged.emit()
    
    @pyqtProperty(str, notify=instinctualVariantChanged)
    def instinctualVariant(self) -> str:
        """Primary instinctual variant (sp, so, sx)."""
        if self._character and self._character.enneagram.instinctual_stack:
            return self._character.enneagram.instinctual_stack[0].value
        return "sp"
    
    @instinctualVariant.setter
    def instinctualVariant(self, value: str) -> None:
        """Set primary instinctual variant."""
        if self._character:
            try:
                from data.enums import InstinctualVariant
                new_variant = InstinctualVariant(value)
                current_stack = self._character.enneagram.instinctual_stack
                
                if not current_stack or current_stack[0] != new_variant:
                    # Reorder stack to put new variant first
                    new_stack = [new_variant]
                    for variant in current_stack:
                        if variant != new_variant:
                            new_stack.append(variant)
                    
                    # Ensure we have all three variants
                    for variant in InstinctualVariant:
                        if variant not in new_stack:
                            new_stack.append(variant)
                    
                    self._character.enneagram.instinctual_stack = new_stack[:3]
                    self._character.touch()
                    
                    self.instinctualVariantChanged.emit()
                    self.updatedAtChanged.emit()
            except ValueError:
                pass  # Invalid variant
    
    @pyqtProperty(int, notify=developmentLevelChanged)
    def developmentLevel(self) -> int:
        """Enneagram development level (1-9)."""
        return self._character.enneagram.development_level if self._character else 5
    
    @developmentLevel.setter
    def developmentLevel(self, value: int) -> None:
        """Set development level."""
        if self._character and 1 <= value <= 9:
            if self._character.enneagram.development_level != value:
                self._character.enneagram.development_level = value
                self._character.touch()
                
                self.developmentLevelChanged.emit()
                self.updatedAtChanged.emit()
    
    @pyqtProperty(str, notify=enneagramNotationChanged)
    def enneagramNotation(self) -> str:
        """Full Enneagram notation (e.g., '9w8')."""
        return self._character.enneagram.get_wing_notation() if self._character else "9"
    
    # Character stats properties
    @pyqtProperty(int, notify=strengthChanged)
    def strength(self) -> int:
        """Strength stat."""
        return self._character.stats.strength if self._character else 10
    
    @strength.setter
    def strength(self, value: int) -> None:
        """Set strength stat."""
        if self._character and self._character.stats.strength != value:
            self._character.stats.strength = value
            self._character.touch()
            self.strengthChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=agilityChanged)
    def agility(self) -> int:
        """Agility stat."""
        return self._character.stats.agility if self._character else 10
    
    @agility.setter
    def agility(self, value: int) -> None:
        """Set agility stat."""
        if self._character and self._character.stats.agility != value:
            self._character.stats.agility = value
            self._character.touch()
            self.agilityChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=constitutionChanged)
    def constitution(self) -> int:
        """Constitution stat."""
        return self._character.stats.constitution if self._character else 10
    
    @constitution.setter
    def constitution(self, value: int) -> None:
        """Set constitution stat."""
        if self._character and self._character.stats.constitution != value:
            self._character.stats.constitution = value
            self._character.touch()
            self.constitutionChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=intelligenceChanged)
    def intelligence(self) -> int:
        """Intelligence stat."""
        return self._character.stats.intelligence if self._character else 10
    
    @intelligence.setter
    def intelligence(self, value: int) -> None:
        """Set intelligence stat."""
        if self._character and self._character.stats.intelligence != value:
            self._character.stats.intelligence = value
            self._character.touch()
            self.intelligenceChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=wisdomChanged)
    def wisdom(self) -> int:
        """Wisdom stat."""
        return self._character.stats.wisdom if self._character else 10
    
    @wisdom.setter
    def wisdom(self, value: int) -> None:
        """Set wisdom stat."""
        if self._character and self._character.stats.wisdom != value:
            self._character.stats.wisdom = value
            self._character.touch()
            self.wisdomChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=charismaChanged)
    def charisma(self) -> int:
        """Charisma stat."""
        return self._character.stats.charisma if self._character else 10
    
    @charisma.setter
    def charisma(self, value: int) -> None:
        """Set charisma stat."""
        if self._character and self._character.stats.charisma != value:
            self._character.stats.charisma = value
            self._character.touch()
            self.charismaChanged.emit()
            self.totalStatsChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(int, notify=totalStatsChanged)
    def totalStats(self) -> int:
        """Total of all stat points."""
        return self._character.stats.total_points if self._character else 60
    
    # Biographical properties
    @pyqtProperty(str, notify=biographyChanged)
    def biography(self) -> str:
        """Character biography."""
        return self._character.biography if self._character else ""
    
    @biography.setter
    def biography(self, value: str) -> None:
        """Set character biography."""
        if self._character and self._character.biography != value:
            self._character.biography = value
            self._character.touch()
            self.biographyChanged.emit()
            self.updatedAtChanged.emit()
    
    @pyqtProperty(list, notify=affiliationsChanged)
    def affiliations(self) -> List[str]:
        """Character affiliations."""
        return self._character.affiliations if self._character else []
    
    @affiliations.setter
    def affiliations(self, value: List[str]) -> None:
        """Set character affiliations."""
        if self._character and self._character.affiliations != value:
            self._character.affiliations = value.copy()
            self._character.touch()
            self.affiliationsChanged.emit()
            self.updatedAtChanged.emit()
    
    # Metadata properties
    @pyqtProperty(str, notify=createdAtChanged)
    def createdAt(self) -> str:
        """Creation timestamp as ISO string."""
        return self._character.created_at.isoformat() if self._character else ""
    
    @pyqtProperty(str, notify=updatedAtChanged)
    def updatedAt(self) -> str:
        """Last update timestamp as ISO string."""
        return self._character.updated_at.isoformat() if self._character else ""
    
    # Computed properties for QML
    @pyqtProperty(bool, constant=True)
    def hasCharacter(self) -> bool:
        """Check if a character is currently loaded."""
        return self._character is not None
    
    @pyqtProperty(bool, notify=imageDataChanged)
    def hasImage(self) -> bool:
        """Check if character has an image."""
        return bool(self._character and self._character.image_data)
    
    @pyqtProperty(int, notify=totalStatsChanged)
    def averageStat(self) -> int:
        """Average stat value (rounded)."""
        if self._character:
            return round(self._character.stats.average_stat)
        return 10
    
    @pyqtProperty(str, notify=enneagramTypeChanged)
    def enneagramTitle(self) -> str:
        """Get the title for the current Enneagram type."""
        if self._character:
            return self._character.enneagram.main_type.title
        return "The Peacemaker"
    
    @pyqtProperty(str, notify=developmentLevelChanged)
    def healthCategory(self) -> str:
        """Get health category (Healthy/Average/Unhealthy)."""
        if self._character:
            return self._character.enneagram.health_category
        return "Average"
    
    # Utility methods for QML
    @pyqtProperty(int)
    def getStatModifier(self) -> int:
        """Get D&D 5e modifier for a stat."""
        # This would need to be called with a specific stat in QML
        # For now, returning strength modifier as example
        if self._character:
            return self._character.stats.get_modifier(StatType.STRENGTH)
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize character to dictionary.
        
        Returns:
            Dictionary representation or empty dict if no character
        """
        return self._character.to_dict() if self._character else {}
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load character from dictionary.
        
        Args:
            data: Dictionary with character data
        """
        character = Character.from_dict(data)
        self.set_character(character)


def register_character_model() -> None:
    """Register CharacterModel for QML usage."""
    qmlRegisterType(CharacterModel, 'CharacterModels', 1, 0, 'CharacterModel')


# Module-level function for easy registration
def register_types() -> None:
    """Register all character-related types."""
    register_character_model()