"""
Enneagram personality system data model.
Complete implementation with all psychological aspects.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from models.enums import (
    EnneagramType, InstinctualVariant, EnneagramTriad, DevelopmentLevel
)


@dataclass
class EnneagramProfile:
    """Complete Enneagram personality profile with all aspects."""
    
    # Core type
    main_type: EnneagramType = EnneagramType.TYPE_9
    wing: Optional[EnneagramType] = None
    
    # Instinctual variants (stacking order matters)
    instinctual_stack: List[InstinctualVariant] = field(default_factory=lambda: [
        InstinctualVariant.SELF_PRESERVATION,
        InstinctualVariant.SOCIAL,
        InstinctualVariant.SEXUAL
    ])
    
    # Development and health
    development_level: int = 5  # 1-9, with 1 being healthiest
    
    # Dynamic aspects
    integration_point: Optional[EnneagramType] = None
    disintegration_point: Optional[EnneagramType] = None
    
    # Relationships with other types (0.0 to 1.0)
    type_affinities: Dict[EnneagramType, float] = field(default_factory=lambda: {
        t: 0.5 for t in EnneagramType
    })
    
    # Additional psychological markers
    tritype_secondary: Optional[EnneagramType] = None
    tritype_tertiary: Optional[EnneagramType] = None
    
    def __post_init__(self):
        """Initialize integration and disintegration points based on type."""
        if not self.integration_point:
            self.integration_point = self.get_integration_point()
        if not self.disintegration_point:
            self.disintegration_point = self.get_disintegration_point()
    
    def get_integration_point(self) -> EnneagramType:
        """
        Get the integration (growth) point for the main type.
        
        Returns:
            Integration Enneagram type
        """
        integrations = {
            EnneagramType.TYPE_1: EnneagramType.TYPE_7,
            EnneagramType.TYPE_2: EnneagramType.TYPE_4,
            EnneagramType.TYPE_3: EnneagramType.TYPE_6,
            EnneagramType.TYPE_4: EnneagramType.TYPE_1,
            EnneagramType.TYPE_5: EnneagramType.TYPE_8,
            EnneagramType.TYPE_6: EnneagramType.TYPE_9,
            EnneagramType.TYPE_7: EnneagramType.TYPE_5,
            EnneagramType.TYPE_8: EnneagramType.TYPE_2,
            EnneagramType.TYPE_9: EnneagramType.TYPE_3
        }
        return integrations.get(self.main_type, self.main_type)
    
    def get_disintegration_point(self) -> EnneagramType:
        """
        Get the disintegration (stress) point for the main type.
        
        Returns:
            Disintegration Enneagram type
        """
        disintegrations = {
            EnneagramType.TYPE_1: EnneagramType.TYPE_4,
            EnneagramType.TYPE_2: EnneagramType.TYPE_8,
            EnneagramType.TYPE_3: EnneagramType.TYPE_9,
            EnneagramType.TYPE_4: EnneagramType.TYPE_2,
            EnneagramType.TYPE_5: EnneagramType.TYPE_7,
            EnneagramType.TYPE_6: EnneagramType.TYPE_3,
            EnneagramType.TYPE_7: EnneagramType.TYPE_1,
            EnneagramType.TYPE_8: EnneagramType.TYPE_5,
            EnneagramType.TYPE_9: EnneagramType.TYPE_6
        }
        return disintegrations.get(self.main_type, self.main_type)
    
    def get_triad(self) -> EnneagramTriad:
        """
        Get the triad (center of intelligence) for the main type.
        
        Returns:
            Enneagram triad
        """
        if self.main_type in [EnneagramType.TYPE_8, EnneagramType.TYPE_9, EnneagramType.TYPE_1]:
            return EnneagramTriad.BODY
        elif self.main_type in [EnneagramType.TYPE_2, EnneagramType.TYPE_3, EnneagramType.TYPE_4]:
            return EnneagramTriad.HEART
        else:  # Types 5, 6, 7
            return EnneagramTriad.HEAD
    
    def get_wing_notation(self) -> str:
        """
        Return the wing notation (e.g., '9w8' or '9w1').
        
        Returns:
            Wing notation string
        """
        if self.wing:
            return f"{self.main_type.value}w{self.wing.value}"
        return str(self.main_type.value)
    
    def get_tritype_designation(self) -> str:
        """
        Return special designations based on wing.
        For Type 9: alpha (9w8) or mu (9w1)
        
        Returns:
            Tritype designation or empty string
        """
        designations = {
            # Type 9 designations
            (EnneagramType.TYPE_9, EnneagramType.TYPE_8): "alpha",
            (EnneagramType.TYPE_9, EnneagramType.TYPE_1): "mu",
            # Type 3 designations  
            (EnneagramType.TYPE_3, EnneagramType.TYPE_2): "beta",
            (EnneagramType.TYPE_3, EnneagramType.TYPE_4): "gamma",
            # Add more as needed for other types
        }
        
        if self.wing:
            return designations.get((self.main_type, self.wing), "")
        return ""
    
    def get_instinctual_variant_description(self) -> str:
        """
        Get description of the dominant instinctual variant.
        
        Returns:
            Description of primary instinct
        """
        if not self.instinctual_stack:
            return ""
        
        primary = self.instinctual_stack[0]
        
        descriptions = {
            InstinctualVariant.SELF_PRESERVATION: "Focus on safety, comfort, and material security",
            InstinctualVariant.SOCIAL: "Focus on social standing, groups, and community",
            InstinctualVariant.SEXUAL: "Focus on intensity, chemistry, and one-on-one connections"
        }
        
        return descriptions.get(primary, "")
    
    def get_health_description(self) -> str:
        """
        Get description of current development level.
        
        Returns:
            Health level description
        """
        if self.development_level <= 3:
            return "Healthy: Self-actualizing and integrated"
        elif self.development_level <= 6:
            return "Average: Functional with typical ego patterns"
        else:
            return "Unhealthy: Destructive and pathological patterns"
    
    def get_tritype(self) -> List[EnneagramType]:
        """
        Get the complete tritype (one from each triad).
        
        Returns:
            List of three types forming the tritype
        """
        tritype = [self.main_type]
        
        if self.tritype_secondary:
            tritype.append(self.tritype_secondary)
        if self.tritype_tertiary:
            tritype.append(self.tritype_tertiary)
        
        return tritype
    
    def validate_wing(self) -> bool:
        """
        Check if the current wing is valid for the main type.
        
        Returns:
            True if wing is valid or None
        """
        if not self.wing:
            return True
        
        # Wings must be adjacent types
        valid_wings = self.get_valid_wings()
        return self.wing in valid_wings
    
    def get_valid_wings(self) -> List[EnneagramType]:
        """
        Get valid wing options for the main type.
        
        Returns:
            List of valid wing types
        """
        if self.main_type == EnneagramType.TYPE_9:
            return [EnneagramType.TYPE_8, EnneagramType.TYPE_1]
        elif self.main_type == EnneagramType.TYPE_1:
            return [EnneagramType.TYPE_9, EnneagramType.TYPE_2]
        else:
            # For types 2-8, wings are +1 and -1
            return [
                EnneagramType(self.main_type.value - 1),
                EnneagramType(self.main_type.value + 1)
            ]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize Enneagram profile to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "main_type": self.main_type.value,
            "wing": self.wing.value if self.wing else None,
            "instinctual_stack": [v.value for v in self.instinctual_stack],
            "development_level": self.development_level,
            "integration_point": self.integration_point.value if self.integration_point else None,
            "disintegration_point": self.disintegration_point.value if self.disintegration_point else None,
            "type_affinities": {
                str(k.value): v for k, v in self.type_affinities.items()
            },
            "tritype_secondary": self.tritype_secondary.value if self.tritype_secondary else None,
            "tritype_tertiary": self.tritype_tertiary.value if self.tritype_tertiary else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnneagramProfile':
        """
        Create EnneagramProfile from dictionary.
        
        Args:
            data: Dictionary with Enneagram data
            
        Returns:
            EnneagramProfile instance
        """
        profile = cls()
        
        # Core type
        profile.main_type = EnneagramType(data.get("main_type", 9))
        profile.wing = EnneagramType(data["wing"]) if data.get("wing") else None
        
        # Instinctual stack
        if "instinctual_stack" in data:
            profile.instinctual_stack = [
                InstinctualVariant(v) for v in data["instinctual_stack"]
            ]
        
        # Development level
        profile.development_level = data.get("development_level", 5)
        
        # Dynamic points
        if data.get("integration_point"):
            profile.integration_point = EnneagramType(data["integration_point"])
        if data.get("disintegration_point"):
            profile.disintegration_point = EnneagramType(data["disintegration_point"])
        
        # Type affinities
        if "type_affinities" in data:
            profile.type_affinities = {
                EnneagramType(int(k)): v 
                for k, v in data["type_affinities"].items()
            }
        
        # Tritype
        if data.get("tritype_secondary"):
            profile.tritype_secondary = EnneagramType(data["tritype_secondary"])
        if data.get("tritype_tertiary"):
            profile.tritype_tertiary = EnneagramType(data["tritype_tertiary"])
        
        return profile