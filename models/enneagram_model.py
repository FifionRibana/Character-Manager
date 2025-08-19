"""
Enneagram model for PyQt6/QML integration.
Provides reactive properties for Enneagram personality data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty
from PyQt6.QtQml import QQmlEngine, qmlRegisterType

from data.enums import EnneagramType, InstinctualVariant, DevelopmentLevel
from data.enneagram import EnneagramProfile


class EnneagramModel(QObject):
    """
    PyQt model for Enneagram data with QML property bindings.
    
    Provides reactive properties for:
    - Core type selection
    - Wing configuration  
    - Instinctual variant
    - Development level
    - Type affinities
    """
    
    # Property change signals
    mainTypeChanged = pyqtSignal()
    wingChanged = pyqtSignal()
    instinctualVariantChanged = pyqtSignal()
    developmentLevelChanged = pyqtSignal()
    integrationPointChanged = pyqtSignal()
    disintegrationPointChanged = pyqtSignal()
    wingNotationChanged = pyqtSignal()
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._profile = EnneagramProfile()
        
    def set_profile(self, profile: EnneagramProfile) -> None:
        """
        Set the Enneagram profile and emit change signals.
        
        Args:
            profile: EnneagramProfile instance
        """
        if profile != self._profile:
            old_profile = self._profile
            self._profile = profile
            
            # Emit signals only for changed properties
            if old_profile.main_type != profile.main_type:
                self.mainTypeChanged.emit()
                self.integrationPointChanged.emit()
                self.disintegrationPointChanged.emit()
                self.wingNotationChanged.emit()
                
            if old_profile.wing != profile.wing:
                self.wingChanged.emit()
                self.wingNotationChanged.emit()
                
            if old_profile.instinctual_stack != profile.instinctual_stack:
                self.instinctualVariantChanged.emit()
                
            if old_profile.development_level != profile.development_level:
                self.developmentLevelChanged.emit()
    
    def get_profile(self) -> EnneagramProfile:
        """
        Get the current Enneagram profile.
        
        Returns:
            Current EnneagramProfile instance
        """
        return self._profile
    
    # Core type properties
    @pyqtProperty(int, notify=mainTypeChanged)
    def mainType(self) -> int:
        """Current main Enneagram type (1-9)."""
        return int(self._profile.main_type.value)
    
    @mainType.setter
    def mainType(self, value: int) -> None:
        """Set main Enneagram type."""
        if 1 <= value <= 9:
            new_type = EnneagramType(value)
            if self._profile.main_type != new_type:
                self._profile.main_type = new_type
                # Auto-update integration/disintegration points
                self._profile.integration_point = self._profile.get_integration_point()
                self._profile.disintegration_point = self._profile.get_disintegration_point()
                
                self.mainTypeChanged.emit()
                self.integrationPointChanged.emit()
                self.disintegrationPointChanged.emit()
                self.wingNotationChanged.emit()
    
    @pyqtProperty(int, notify=wingChanged)
    def wing(self) -> int:
        """Current wing type (0 for no wing, 1-9 for wing type)."""
        return int(self._profile.wing.value) if self._profile.wing else 0
    
    @wing.setter
    def wing(self, value: int) -> None:
        """Set wing type."""
        new_wing = EnneagramType(value) if value > 0 else None
        if self._profile.wing != new_wing:
            self._profile.wing = new_wing
            self.wingChanged.emit()
            self.wingNotationChanged.emit()
    
    @pyqtProperty(str, notify=instinctualVariantChanged)
    def instinctualVariant(self) -> str:
        """Primary instinctual variant (sp, so, sx)."""
        return self._profile.instinctual_stack[0].value if self._profile.instinctual_stack else "sp"
    
    @instinctualVariant.setter
    def instinctualVariant(self, value: str) -> None:
        """Set primary instinctual variant."""
        try:
            new_variant = InstinctualVariant(value)
            if not self._profile.instinctual_stack or self._profile.instinctual_stack[0] != new_variant:
                # Move selected variant to first position
                self._profile.instinctual_stack = [new_variant] + [
                    v for v in self._profile.instinctual_stack if v != new_variant
                ]
                # Ensure we have all three variants
                for variant in InstinctualVariant:
                    if variant not in self._profile.instinctual_stack:
                        self._profile.instinctual_stack.append(variant)
                
                self.instinctualVariantChanged.emit()
        except ValueError:
            pass  # Invalid variant value
    
    @pyqtProperty(int, notify=developmentLevelChanged)
    def developmentLevel(self) -> int:
        """Current development level (1-9)."""
        return self._profile.development_level
    
    @developmentLevel.setter
    def developmentLevel(self, value: int) -> None:
        """Set development level."""
        if 1 <= value <= 9 and self._profile.development_level != value:
            self._profile.development_level = value
            self.developmentLevelChanged.emit()
    
    # Computed properties
    @pyqtProperty(int, notify=integrationPointChanged)
    def integrationPoint(self) -> int:
        """Integration (growth) point for current type."""
        return int(self._profile.get_integration_point().value)
    
    @pyqtProperty(int, notify=disintegrationPointChanged)
    def disintegrationPoint(self) -> int:
        """Disintegration (stress) point for current type."""
        return int(self._profile.get_disintegration_point().value)
    
    @pyqtProperty(str, notify=wingNotationChanged)
    def wingNotation(self) -> str:
        """Wing notation (e.g., '9w8' or '9w1')."""
        return self._profile.get_wing_notation()
    
    # Helper methods for QML
    @pyqtProperty(list, constant=True)
    def availableTypes(self) -> List[Dict[str, Any]]:
        """List of all Enneagram types for QML models."""
        return [
            {"value": t.value, "name": f"Type {t.value}", "title": self._get_type_title(t)}
            for t in EnneagramType
        ]
    
    @pyqtProperty(list, constant=True)
    def availableInstincts(self) -> List[Dict[str, Any]]:
        """List of instinctual variants for QML models."""
        return [
            {"value": v.value, "name": self._get_instinct_name(v)}
            for v in InstinctualVariant
        ]
    
    def _get_type_title(self, enneagram_type: EnneagramType) -> str:
        """Get the title/name for an Enneagram type."""
        titles = {
            EnneagramType.TYPE_1: "The Reformer",
            EnneagramType.TYPE_2: "The Helper", 
            EnneagramType.TYPE_3: "The Achiever",
            EnneagramType.TYPE_4: "The Individualist",
            EnneagramType.TYPE_5: "The Investigator",
            EnneagramType.TYPE_6: "The Loyalist",
            EnneagramType.TYPE_7: "The Enthusiast",
            EnneagramType.TYPE_8: "The Challenger",
            EnneagramType.TYPE_9: "The Peacemaker"
        }
        return titles.get(enneagram_type, "Unknown")
    
    def _get_instinct_name(self, variant: InstinctualVariant) -> str:
        """Get the display name for an instinctual variant."""
        names = {
            InstinctualVariant.SELF_PRESERVATION: "Self-Preservation (SP)",
            InstinctualVariant.SOCIAL: "Social (SO)",
            InstinctualVariant.SEXUAL: "Sexual/One-to-One (SX)"
        }
        return names.get(variant, "Unknown")
    
    # QML callable methods
    @pyqtProperty(list)
    def getWingOptions(self) -> List[Dict[str, Any]]:
        """Get available wing options for current type."""
        current_type = int(self._profile.main_type.value)
        left_wing = 9 if current_type == 1 else current_type - 1
        right_wing = 1 if current_type == 9 else current_type + 1
        
        return [
            {"value": 0, "text": "No Wing"},
            {"value": left_wing, "text": f"Wing {left_wing}"},
            {"value": right_wing, "text": f"Wing {right_wing}"}
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize model to dictionary.
        
        Returns:
            Dictionary representation
        """
        return self._profile.to_dict()
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load model from dictionary.
        
        Args:
            data: Dictionary with Enneagram data
        """
        old_profile = self._profile
        self._profile = EnneagramProfile.from_dict(data)
        
        # Emit all change signals since we replaced the entire profile
        if old_profile.main_type != self._profile.main_type:
            self.mainTypeChanged.emit()
            self.integrationPointChanged.emit()
            self.disintegrationPointChanged.emit()
            
        if old_profile.wing != self._profile.wing:
            self.wingChanged.emit()
            
        if old_profile.instinctual_stack != self._profile.instinctual_stack:
            self.instinctualVariantChanged.emit()
            
        if old_profile.development_level != self._profile.development_level:
            self.developmentLevelChanged.emit()
            
        self.wingNotationChanged.emit()


def register_enneagram_model() -> None:
    """Register EnneagramModel for QML usage."""
    qmlRegisterType(EnneagramModel, 'EnneagramModels', 1, 0, 'EnneagramModel')


# Module-level registration
def register_types() -> None:
    """Register all Enneagram-related types."""
    register_enneagram_model()