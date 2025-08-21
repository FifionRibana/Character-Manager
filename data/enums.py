#!/usr/bin/env python3
"""
Enums and constants for the Medieval Character Manager application.
Following Python 3.11 best practices with StrEnum and IntEnum.
"""

from enum import Enum, StrEnum, IntEnum, IntFlag, auto
from pathlib import Path
from typing import Final

from PyQt6.QtCore import pyqtEnum, QObject


class Archetype(StrEnum):
    """Character archetypes"""

    HERO = "hero"
    MAGE = "mage"
    ROGUE = "rogue"
    WARRIOR = "warrior"
    SAGE = "sage"
    VILLAIN = "villain"
    NEUTRAL = "neutral"


class Affinity(StrEnum):
    """Character moral affinities"""

    LAWFUL = "lawful"
    NEUTRAL = "neutral"
    CHAOTIC = "chaotic"
    GOOD = "good"
    EVIL = "evil"


class Gender(StrEnum):
    """Character gender"""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNSPECIFIED = "unspecified"


class CharacterStatus(StrEnum):
    """Character status"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DECEASED = "deceased"
    MISSING = "missing"
    RETIRED = "retired"


class Wing(IntEnum):
    """Enneagram wing types"""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Instinct(StrEnum):
    """Instinctual variants (same as InstinctualVariant)"""

    SELF_PRESERVATION = "sp"
    SOCIAL = "so"
    SEXUAL = "sx"


class TriadCenter(StrEnum):
    """Enneagram triad centers (same as EnneagramTriad)"""

    BODY = "body"
    HEART = "heart"
    HEAD = "head"


class StatCategory(StrEnum):
    """Stat categories for grouping"""

    PHYSICAL = "physical"
    MENTAL = "mental"
    SOCIAL = "social"
    COMBAT = "combat"
    MAGIC = "magic"


class Language(StrEnum):
    """Supported application languages."""

    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"

    @property
    def display_name(self) -> str:
        """Get the display name for this language."""
        names = {
            self.ENGLISH: "English",
            self.FRENCH: "Français",
            self.SPANISH: "Español",
            self.GERMAN: "Deutsch",
        }
        return names[self]


class EnneagramType(IntEnum):
    """Enneagram personality types (1-9)."""

    TYPE_1 = 1  # The Perfectionist
    TYPE_2 = 2  # The Helper
    TYPE_3 = 3  # The Achiever
    TYPE_4 = 4  # The Individualist
    TYPE_5 = 5  # The Investigator
    TYPE_6 = 6  # The Loyalist
    TYPE_7 = 7  # The Enthusiast
    TYPE_8 = 8  # The Challenger
    TYPE_9 = 9  # The Peacemaker

    @property
    def title(self) -> str:
        """Get the descriptive title for this type."""
        titles = {
            self.TYPE_1: "The Reformer",
            self.TYPE_2: "The Helper",
            self.TYPE_3: "The Achiever",
            self.TYPE_4: "The Individualist",
            self.TYPE_5: "The Investigator",
            self.TYPE_6: "The Loyalist",
            self.TYPE_7: "The Enthusiast",
            self.TYPE_8: "The Challenger",
            self.TYPE_9: "The Peacemaker",
        }
        return titles[self]

    @property
    def integration_point(self) -> "EnneagramType":
        """Get the integration (growth) point for this type."""
        integrations = {
            self.TYPE_1: self.TYPE_7,
            self.TYPE_2: self.TYPE_4,
            self.TYPE_3: self.TYPE_6,
            self.TYPE_4: self.TYPE_1,
            self.TYPE_5: self.TYPE_8,
            self.TYPE_6: self.TYPE_9,
            self.TYPE_7: self.TYPE_5,
            self.TYPE_8: self.TYPE_2,
            self.TYPE_9: self.TYPE_3,
        }
        return integrations[self]

    @property
    def disintegration_point(self) -> "EnneagramType":
        """Get the disintegration (stress) point for this type."""
        disintegrations = {
            self.TYPE_1: self.TYPE_4,
            self.TYPE_2: self.TYPE_8,
            self.TYPE_3: self.TYPE_9,
            self.TYPE_4: self.TYPE_2,
            self.TYPE_5: self.TYPE_7,
            self.TYPE_6: self.TYPE_3,
            self.TYPE_7: self.TYPE_1,
            self.TYPE_8: self.TYPE_5,
            self.TYPE_9: self.TYPE_6,
        }
        return disintegrations[self]

    @property
    def triad(self) -> "EnneagramTriad":
        """Get the triad (center of intelligence) for this type."""
        if self in (self.TYPE_8, self.TYPE_9, self.TYPE_1):
            return EnneagramTriad.BODY
        elif self in (self.TYPE_2, self.TYPE_3, self.TYPE_4):
            return EnneagramTriad.HEART
        else:  # Types 5, 6, 7
            return EnneagramTriad.HEAD


class InstinctualVariant(StrEnum):
    """Instinctual subtypes for Enneagram."""

    SELF_PRESERVATION = "sp"
    SOCIAL = "so"
    SEXUAL = "sx"

    @property
    def full_name(self) -> str:
        """Get the full descriptive name."""
        names = {
            self.SELF_PRESERVATION: "Self-Preservation",
            self.SOCIAL: "Social",
            self.SEXUAL: "Sexual/One-to-One",
        }
        return names[self]

    @property
    def description(self) -> str:
        """Get a brief description of this variant."""
        descriptions = {
            self.SELF_PRESERVATION: "Focus on physical safety, health, and material security",
            self.SOCIAL: "Focus on social dynamics, group belonging, and community",
            self.SEXUAL: "Focus on intensity, chemistry, and one-to-one connections",
        }
        return descriptions[self]


class EnneagramTriad(StrEnum):
    """The three centers of intelligence in Enneagram."""

    BODY = "body"  # Types 8, 9, 1 - Anger/Gut
    HEART = "heart"  # Types 2, 3, 4 - Shame/Feeling
    HEAD = "head"  # Types 5, 6, 7 - Fear/Thinking

    @property
    def core_emotion(self) -> str:
        """Get the core emotion associated with this triad."""
        emotions = {self.BODY: "Anger", self.HEART: "Shame", self.HEAD: "Fear"}
        return emotions[self]

    @property
    def focus(self) -> str:
        """Get the primary focus of this triad."""
        focuses = {
            self.BODY: "Control and autonomy",
            self.HEART: "Identity and image",
            self.HEAD: "Security and support",
        }
        return focuses[self]


class DevelopmentLevel(IntEnum):
    """Enneagram development levels from healthy to unhealthy."""

    LEVEL_1 = 1  # Very healthy
    LEVEL_2 = 2  # Healthy
    LEVEL_3 = 3  # Average-healthy
    LEVEL_4 = 4  # Average
    LEVEL_5 = 5  # Average-unhealthy
    LEVEL_6 = 6  # Unhealthy
    LEVEL_7 = 7  # Very unhealthy
    LEVEL_8 = 8  # Severely unhealthy
    LEVEL_9 = 9  # Pathological

    @property
    def description(self) -> str:
        """Get description of this development level."""
        descriptions = {
            self.LEVEL_1: "Liberation - Very healthy",
            self.LEVEL_2: "Psychological capacity - Healthy",
            self.LEVEL_3: "Social value - Average-healthy",
            self.LEVEL_4: "Imbalance - Average",
            self.LEVEL_5: "Interpersonal control - Average-unhealthy",
            self.LEVEL_6: "Overcompensation - Unhealthy",
            self.LEVEL_7: "Violation - Very unhealthy",
            self.LEVEL_8: "Delusion and compulsion - Severely unhealthy",
            self.LEVEL_9: "Pathological destructiveness - Pathological",
        }
        return descriptions[self]

    @property
    def is_healthy(self) -> bool:
        """Check if this is a healthy level (1-3)."""
        return self <= self.LEVEL_3

    @property
    def is_average(self) -> bool:
        """Check if this is an average level (4-6)."""
        return self.LEVEL_4 <= self <= self.LEVEL_6

    @property
    def is_unhealthy(self) -> bool:
        """Check if this is an unhealthy level (7-9)."""
        return self >= self.LEVEL_7


class StatType(StrEnum):
    """D&D-style character statistics."""

    STRENGTH = "strength"
    AGILITY = "agility"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


class RelationType(StrEnum):
    """Types of relationships between characters."""

    FRIEND = "friend"
    ENEMY = "enemy"
    RIVAL = "rival"
    ALLY = "ally"
    NEUTRAL = "neutral"
    FAMILY = "family"
    MENTOR = "mentor"
    APPRENTICE = "apprentice"
    LOVER = "lover"
    UNKNOWN = "unknown"


class EventType(StrEnum):
    BIRTH = "birth"
    DEATH = "death"
    MEETING = "meeting"
    BATTLE = "battle"
    TRAGEDY = "tragedy"
    ACHIEVEMENT = "achievement"
    TRAINING = "training"
    ROMANCE = "romance"
    ADVENTURE = "adventure"
    MAJOR = "major"
    MINOR = "minor"
    GENERAL = "general"


class StorageKeys(StrEnum):
    """Keys for data serialization and storage."""

    # Character core data
    CHARACTER_ID = "character_id"
    NAME = "name"
    LEVEL = "level"
    ENNEAGRAM_TYPE = "enneagram_type"
    DEVELOPMENT_LEVEL = "development_level"
    BIOGRAPHY = "biography"
    IMAGE_PATH = "image_path"
    IMAGE_DATA = "image_data"

    # Stats
    STATS = "stats"
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

    # Enneagram
    ENNEAGRAM = "enneagram"
    MAIN_TYPE = "main_type"
    WING = "wing"
    INSTINCTUAL_STACK = "instinctual_stack"
    TYPE_AFFINITIES = "type_affinities"

    # Relationships
    RELATIONSHIPS = "relationships"
    TARGET_ID = "target_id"
    TARGET_NAME = "target_name"
    RELATIONSHIP_TYPE = "relationship_type"
    DESCRIPTION = "description"

    # Narrative
    NARRATIVE = "narrative_events"
    AFFILIATIONS = "affiliations"

    # Metadata
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    VERSION = "version"


class Theme(StrEnum):
    """Application theme options."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # Follow system theme


class FileExtension(StrEnum):
    """Supported file extensions."""

    JSON = ".json"
    HTML = ".html"
    PDF = ".pdf"
    PNG = ".png"
    JPG = ".jpg"
    JPEG = ".jpeg"


class UIConstants(IntEnum):
    """UI dimension and timing constants."""

    SIDEBAR_WIDTH = 250
    MIN_WINDOW_WIDTH = 1200
    MIN_WINDOW_HEIGHT = 800
    ANIMATION_DURATION = 300
    AUTOSAVE_INTERVAL = 30000  # 30 seconds in milliseconds
    ENNEAGRAM_WHEEL_SIZE = 400
    AFFINITY_RADAR_SIZE = 350
    IMAGE_WIDGET_SIZE = 200
    TAB_ICON_SIZE = 24
    MAX_RECENT_FILES = 10
    TOOLTIP_DELAY = 500


class ValidationLimits(IntEnum):
    """Validation limits for various fields."""

    MIN_CHARACTER_NAME_LENGTH = 1
    MAX_CHARACTER_NAME_LENGTH = 100
    MIN_CHARACTER_LEVEL = 1
    MAX_CHARACTER_LEVEL = 100
    MIN_STAT_VALUE = 1
    MAX_STAT_VALUE = 25
    MIN_DEVELOPMENT_LEVEL = 1
    MAX_DEVELOPMENT_LEVEL = 9
    MAX_BIOGRAPHY_LENGTH = 10000
    MAX_RELATIONSHIP_DESCRIPTION_LENGTH = 500


class FileConstants:
    """File and directory constants using pathlib."""

    # Application directories
    APP_NAME: Final[str] = "MedievalCharacterManager"
    CONFIG_DIR: Final[Path] = Path.home() / ".config" / APP_NAME
    DATA_DIR: Final[Path] = Path.home() / ".local" / "share" / APP_NAME
    CACHE_DIR: Final[Path] = Path.home() / ".cache" / APP_NAME

    # File names
    SETTINGS_FILE: Final[str] = "settings.json"
    CHARACTERS_FILE: Final[str] = "characters.json"
    RECENT_FILES: Final[str] = "recent.json"

    # Default file extensions
    CHARACTER_EXT: Final[str] = FileExtension.JSON
    EXPORT_EXT: Final[str] = FileExtension.HTML

    # Backup settings
    MAX_BACKUPS: Final[int] = 5
    BACKUP_SUFFIX: Final[str] = ".backup"


class ErrorCodes(IntEnum):
    """Application error codes for better error handling."""

    SUCCESS = 0
    FILE_NOT_FOUND = 1
    PERMISSION_DENIED = 2
    INVALID_FORMAT = 3
    VALIDATION_ERROR = 4
    NETWORK_ERROR = 5
    UNKNOWN_ERROR = 99


class LogLevel(IntEnum):
    """Logging levels."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Permission(IntFlag):
    """File and data permissions using IntFlag."""

    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()

    # Combined permissions
    READ_WRITE = READ | WRITE
    FULL_ACCESS = READ | WRITE | EXECUTE | DELETE


# Type aliases for commonly used combinations
CharacterData = dict[StorageKeys, str | int | dict | list]
ValidationResult = tuple[bool, str]  # (is_valid, error_message)


# Constants for default values
DEFAULT_STAT_VALUE: Final[int] = 10
DEFAULT_DEVELOPMENT_LEVEL: Final[int] = 5
DEFAULT_CHARACTER_LEVEL: Final[int] = 1
DEFAULT_ENNEAGRAM_TYPE: Final[EnneagramType] = EnneagramType.TYPE_9
