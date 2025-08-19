"""
Enneagram personality system data model.
Complete implementation with all psychological aspects.
Migrated to Python 3.11+ with modern features and pathlib support.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, ClassVar
from pathlib import Path

from .enums import (
    EnneagramType, InstinctualVariant, EnneagramTriad, DevelopmentLevel,
    ValidationLimits, DEFAULT_ENNEAGRAM_TYPE, DEFAULT_DEVELOPMENT_LEVEL
)


@dataclass
class EnneagramProfile:
    """
    Complete Enneagram personality profile with all psychological aspects.
    
    Modern implementation using Python 3.11+ dataclass features.
    """
    
    # Class version for migration tracking
    VERSION: ClassVar[str] = "2.0"
    
    # Core type information
    main_type: EnneagramType = DEFAULT_ENNEAGRAM_TYPE
    wing: Optional[EnneagramType] = None
    
    # Instinctual variants (stacking order matters - most dominant first)
    instinctual_stack: List[InstinctualVariant] = field(default_factory=lambda: [
        InstinctualVariant.SELF_PRESERVATION,
        InstinctualVariant.SOCIAL,
        InstinctualVariant.SEXUAL
    ])
    
    # Development and psychological health
    development_level: int = DEFAULT_DEVELOPMENT_LEVEL
    
    # Dynamic aspects (auto-calculated if None)
    integration_point: Optional[EnneagramType] = None
    disintegration_point: Optional[EnneagramType] = None
    
    # Relationships with other types (0.0 to 1.0 affinity scores)
    type_affinities: Dict[EnneagramType, float] = field(default_factory=lambda: {
        t: 0.5 for t in EnneagramType
    })
    
    # Tritype system (optional secondary and tertiary types)
    tritype_secondary: Optional[EnneagramType] = None
    tritype_tertiary: Optional[EnneagramType] = None
    
    # Additional psychological markers
    dominant_instinct_strength: float = 0.7  # How strongly the primary instinct manifests
    self_awareness_level: int = 5  # 1-10 scale of psychological self-awareness
    
    def __post_init__(self) -> None:
        """Initialize computed fields and validate data after creation."""
        self._validate_data()
        self._auto_calculate_missing_fields()
    
    def _validate_data(self) -> None:
        """Validate all Enneagram data for consistency."""
        # Validate development level
        if not ValidationLimits.MIN_DEVELOPMENT_LEVEL <= self.development_level <= ValidationLimits.MAX_DEVELOPMENT_LEVEL:
            raise ValueError(f"Development level must be between {ValidationLimits.MIN_DEVELOPMENT_LEVEL} and {ValidationLimits.MAX_DEVELOPMENT_LEVEL}")
        
        # Validate wing (must be adjacent to main type or None)
        if self.wing is not None:
            adjacent_types = self.get_adjacent_types(self.main_type)
            if self.wing not in adjacent_types:
                raise ValueError(f"Wing {self.wing} is not adjacent to main type {self.main_type}")
        
        # Validate instinctual stack (must contain all three variants exactly once)
        if len(self.instinctual_stack) != 3 or set(self.instinctual_stack) != set(InstinctualVariant):
            raise ValueError("Instinctual stack must contain all three variants exactly once")
        
        # Validate self-awareness level
        if not 1 <= self.self_awareness_level <= 10:
            raise ValueError("Self-awareness level must be between 1 and 10")
        
        # Validate dominant instinct strength
        if not 0.0 <= self.dominant_instinct_strength <= 1.0:
            raise ValueError("Dominant instinct strength must be between 0.0 and 1.0")
    
    def _auto_calculate_missing_fields(self) -> None:
        """Auto-calculate integration and disintegration points if not set."""
        if self.integration_point is None:
            self.integration_point = self.main_type.integration_point
        if self.disintegration_point is None:
            self.disintegration_point = self.main_type.disintegration_point
    
    @staticmethod
    def get_adjacent_types(enneagram_type: EnneagramType) -> List[EnneagramType]:
        """
        Get the two adjacent types for wing possibilities.
        
        Args:
            enneagram_type: The main type
            
        Returns:
            List of two adjacent types
        """
        type_num = int(enneagram_type.value)
        left = EnneagramType(9 if type_num == 1 else type_num - 1)
        right = EnneagramType(1 if type_num == 9 else type_num + 1)
        return [left, right]
    
    @property
    def triad(self) -> EnneagramTriad:
        """Get the triad (center of intelligence) for the main type."""
        return self.main_type.triad
    
    @property
    def primary_instinct(self) -> InstinctualVariant:
        """Get the primary (most dominant) instinctual variant."""
        return self.instinctual_stack[0] if self.instinctual_stack else InstinctualVariant.SELF_PRESERVATION
    
    @property
    def secondary_instinct(self) -> InstinctualVariant:
        """Get the secondary instinctual variant."""
        return self.instinctual_stack[1] if len(self.instinctual_stack) > 1 else InstinctualVariant.SOCIAL
    
    @property
    def blind_spot_instinct(self) -> InstinctualVariant:
        """Get the least developed (blind spot) instinctual variant."""
        return self.instinctual_stack[2] if len(self.instinctual_stack) > 2 else InstinctualVariant.SEXUAL
    
    @property
    def health_category(self) -> str:
        """Get the general health category based on development level."""
        level_enum = DevelopmentLevel(self.development_level)
        return level_enum.health_category
    
    @property
    def is_healthy(self) -> bool:
        """Check if the character is in the healthy range."""
        return self.development_level <= 3
    
    @property
    def is_average(self) -> bool:
        """Check if the character is in the average range."""
        return 4 <= self.development_level <= 6
    
    @property
    def is_unhealthy(self) -> bool:
        """Check if the character is in the unhealthy range."""
        return self.development_level >= 7
    
    def get_integration_point(self) -> EnneagramType:
        """
        Get the integration (growth) point for the main type.
        
        Returns:
            Integration Enneagram type
        """
        return self.main_type.integration_point
    
    def get_disintegration_point(self) -> EnneagramType:
        """
        Get the disintegration (stress) point for the main type.
        
        Returns:
            Disintegration Enneagram type
        """
        return self.main_type.disintegration_point
    
    def get_wing_notation(self) -> str:
        """
        Return the wing notation (e.g., '9w8' or '9w1' or '9').
        
        Returns:
            Wing notation string
        """
        if self.wing:
            return f"{self.main_type.value}w{self.wing.value}"
        return str(self.main_type.value)
    
    def get_tritype_notation(self) -> str:
        """
        Get the tritype notation if secondary and tertiary are set.
        
        Returns:
            Tritype notation (e.g., "9-6-3") or empty string
        """
        if self.tritype_secondary and self.tritype_tertiary:
            return f"{self.main_type.value}-{self.tritype_secondary.value}-{self.tritype_tertiary.value}"
        return ""
    
    def get_instinctual_stacking(self) -> str:
        """
        Get the instinctual stacking notation.
        
        Returns:
            Stacking notation (e.g., "sp/so/sx")
        """
        if len(self.instinctual_stack) >= 3:
            return "/".join(variant.value for variant in self.instinctual_stack)
        return ""
    
    def get_full_notation(self) -> str:
        """
        Get the complete Enneagram notation.
        
        Returns:
            Full notation (e.g., "9w8 sp/so/sx")
        """
        wing_notation = self.get_wing_notation()
        stacking = self.get_instinctual_stacking()
        
        if stacking:
            return f"{wing_notation} {stacking}"
        return wing_notation
    
    def get_compatibility_score(self, other_type: EnneagramType) -> float:
        """
        Get the compatibility/affinity score with another type.
        
        Args:
            other_type: The other Enneagram type
            
        Returns:
            Compatibility score (0.0 to 1.0)
        """
        return self.type_affinities.get(other_type, 0.5)
    
    def set_compatibility_score(self, other_type: EnneagramType, score: float) -> None:
        """
        Set the compatibility/affinity score with another type.
        
        Args:
            other_type: The other Enneagram type
            score: Compatibility score (0.0 to 1.0)
        """
        if not 0.0 <= score <= 1.0:
            raise ValueError("Compatibility score must be between 0.0 and 1.0")
        self.type_affinities[other_type] = score
    
    def get_stress_indicators(self) -> List[str]:
        """
        Get behavioral indicators based on current development level.
        
        Returns:
            List of stress/health indicators
        """
        if self.is_healthy:
            return [
                "Balanced and integrated",
                "Expressing positive qualities",
                "Self-aware and growing"
            ]
        elif self.is_average:
            return [
                "Some compulsive patterns",
                "Moderate self-awareness",
                "Room for growth"
            ]
        else:  # Unhealthy
            return [
                "Strong compulsive patterns",
                "Low self-awareness",
                "Significant stress indicators"
            ]
    
    def move_toward_health(self, steps: int = 1) -> None:
        """
        Move toward healthier development level.
        
        Args:
            steps: Number of levels to improve (default 1)
        """
        new_level = max(ValidationLimits.MIN_DEVELOPMENT_LEVEL, self.development_level - steps)
        self.development_level = new_level
    
    def move_toward_stress(self, steps: int = 1) -> None:
        """
        Move toward more stressed development level.
        
        Args:
            steps: Number of levels to worsen (default 1)
        """
        new_level = min(ValidationLimits.MAX_DEVELOPMENT_LEVEL, self.development_level + steps)
        self.development_level = new_level
    
    def reorder_instinctual_stack(self, new_order: List[InstinctualVariant]) -> None:
        """
        Reorder the instinctual stack.
        
        Args:
            new_order: New order for the instinctual variants
            
        Raises:
            ValueError: If new order is invalid
        """
        if len(new_order) != 3 or set(new_order) != set(InstinctualVariant):
            raise ValueError("New order must contain all three variants exactly once")
        self.instinctual_stack = new_order.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize profile to dictionary for JSON storage.
        
        Returns:
            Dictionary representation using enum values
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
            "tritype_tertiary": self.tritype_tertiary.value if self.tritype_tertiary else None,
            "dominant_instinct_strength": self.dominant_instinct_strength,
            "self_awareness_level": self.self_awareness_level,
            "version": self.VERSION
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EnneagramProfile:
        """
        Create EnneagramProfile from dictionary.
        
        Args:
            data: Dictionary with Enneagram data
            
        Returns:
            EnneagramProfile instance
        """
        # Handle empty or None data
        if not data:
            return cls()
        
        # Parse main type
        main_type = EnneagramType(data.get("main_type", DEFAULT_ENNEAGRAM_TYPE.value))
        
        # Parse wing
        wing = None
        if data.get("wing"):
            try:
                wing = EnneagramType(data["wing"])
            except ValueError:
                wing = None
        
        # Parse instinctual stack
        instinctual_stack = [
            InstinctualVariant.SELF_PRESERVATION,
            InstinctualVariant.SOCIAL,
            InstinctualVariant.SEXUAL
        ]
        if "instinctual_stack" in data and data["instinctual_stack"]:
            try:
                instinctual_stack = [
                    InstinctualVariant(v) for v in data["instinctual_stack"]
                ]
            except (ValueError, TypeError):
                pass  # Use default
        
        # Parse development level
        development_level = data.get("development_level", DEFAULT_DEVELOPMENT_LEVEL)
        if not ValidationLimits.MIN_DEVELOPMENT_LEVEL <= development_level <= ValidationLimits.MAX_DEVELOPMENT_LEVEL:
            development_level = DEFAULT_DEVELOPMENT_LEVEL
        
        # Parse dynamic points
        integration_point = None
        disintegration_point = None
        if data.get("integration_point"):
            try:
                integration_point = EnneagramType(data["integration_point"])
            except ValueError:
                pass
        if data.get("disintegration_point"):
            try:
                disintegration_point = EnneagramType(data["disintegration_point"])
            except ValueError:
                pass
        
        # Parse type affinities
        type_affinities = {t: 0.5 for t in EnneagramType}
        if "type_affinities" in data and data["type_affinities"]:
            try:
                for k, v in data["type_affinities"].items():
                    type_enum = EnneagramType(int(k))
                    score = float(v)
                    if 0.0 <= score <= 1.0:
                        type_affinities[type_enum] = score
            except (ValueError, TypeError):
                pass  # Use defaults
        
        # Parse tritype
        tritype_secondary = None
        tritype_tertiary = None
        if data.get("tritype_secondary"):
            try:
                tritype_secondary = EnneagramType(data["tritype_secondary"])
            except ValueError:
                pass
        if data.get("tritype_tertiary"):
            try:
                tritype_tertiary = EnneagramType(data["tritype_tertiary"])
            except ValueError:
                pass
        
        # Parse additional fields
        dominant_instinct_strength = data.get("dominant_instinct_strength", 0.7)
        if not 0.0 <= dominant_instinct_strength <= 1.0:
            dominant_instinct_strength = 0.7
        
        self_awareness_level = data.get("self_awareness_level", 5)
        if not 1 <= self_awareness_level <= 10:
            self_awareness_level = 5
        
        return cls(
            main_type=main_type,
            wing=wing,
            instinctual_stack=instinctual_stack,
            development_level=development_level,
            integration_point=integration_point,
            disintegration_point=disintegration_point,
            type_affinities=type_affinities,
            tritype_secondary=tritype_secondary,
            tritype_tertiary=tritype_tertiary,
            dominant_instinct_strength=dominant_instinct_strength,
            self_awareness_level=self_awareness_level
        )
    
    @classmethod
    def create_random(cls) -> EnneagramProfile:
        """
        Create a randomized Enneagram profile for testing.
        
        Returns:
            EnneagramProfile with random but valid values
        """
        import random
        
        main_type = random.choice(list(EnneagramType))
        adjacent_types = cls.get_adjacent_types(main_type)
        wing = random.choice([None] + adjacent_types)
        
        # Random but valid instinctual stack
        instincts = list(InstinctualVariant)
        random.shuffle(instincts)
        
        return cls(
            main_type=main_type,
            wing=wing,
            instinctual_stack=instincts,
            development_level=random.randint(1, 9),
            dominant_instinct_strength=random.uniform(0.5, 1.0),
            self_awareness_level=random.randint(1, 10)
        )
    
    @classmethod
    def create_healthy_profile(cls, main_type: EnneagramType, 
                             wing: Optional[EnneagramType] = None) -> EnneagramProfile:
        """
        Create a healthy Enneagram profile.
        
        Args:
            main_type: The main Enneagram type
            wing: Optional wing type
            
        Returns:
            Healthy EnneagramProfile
        """
        return cls(
            main_type=main_type,
            wing=wing,
            development_level=2,  # Healthy level
            self_awareness_level=8,  # High self-awareness
            dominant_instinct_strength=0.8
        )
    
    def __str__(self) -> str:
        """String representation of the profile."""
        return self.get_full_notation()
    
    def __repr__(self) -> str:
        """Developer representation of the profile."""
        return f"EnneagramProfile(main_type={self.main_type}, wing={self.wing}, level={self.development_level})"