"""
Enumerations for the Medieval Character Manager.
All magic numbers are replaced with meaningful enum values.
"""

from enum import StrEnum, IntEnum, auto


class Language(StrEnum):
    """Supported languages for the application."""
    ENGLISH = "en"
    FRENCH = "fr"


class EnneagramType(IntEnum):
    """The nine Enneagram personality types."""
    TYPE_1 = 1  # The Reformer
    TYPE_2 = 2  # The Helper
    TYPE_3 = 3  # The Achiever
    TYPE_4 = 4  # The Individualist
    TYPE_5 = 5  # The Investigator
    TYPE_6 = 6  # The Loyalist
    TYPE_7 = 7  # The Enthusiast
    TYPE_8 = 8  # The Challenger
    TYPE_9 = 9  # The Peacemaker


class InstinctualVariant(StrEnum):
    """Instinctual subtypes for Enneagram."""
    SELF_PRESERVATION = "sp"
    SOCIAL = "so"
    SEXUAL = "sx"


class EnneagramTriad(StrEnum):
    """The three centers of intelligence in Enneagram."""
    BODY = "body"  # Types 8, 9, 1 - Anger/Gut
    HEART = "heart"  # Types 2, 3, 4 - Shame/Feeling
    HEAD = "head"  # Types 5, 6, 7 - Fear/Thinking


class DevelopmentLevel(IntEnum):
    """Enneagram development levels from healthy to unhealthy."""
    LEVEL_1 = 1  # Liberation
    LEVEL_2 = 2  # Psychological Capacity
    LEVEL_3 = 3  # Social Value
    LEVEL_4 = 4  # Imbalance/Social Role
    LEVEL_5 = 5  # Interpersonal Control
    LEVEL_6 = 6  # Overcompensation
    LEVEL_7 = 7  # Violation
    LEVEL_8 = 8  # Obsession and Compulsion
    LEVEL_9 = 9  # Pathological Destructiveness


class StatType(StrEnum):
    """Character statistics types."""
    STRENGTH = "strength"
    AGILITY = "agility"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


class RelationType(StrEnum):
    """Types of relationships between characters."""
    FAMILY = "family"
    FRIEND = "friend"
    RIVAL = "rival"
    MENTOR = "mentor"
    STUDENT = "student"
    ALLY = "ally"
    ENEMY = "enemy"
    ROMANTIC = "romantic"
    NEUTRAL = "neutral"


class StorageKeys(StrEnum):
    """Keys for JSON serialization."""
    CHARACTER_ID = "id"
    NAME = "name"
    LEVEL = "level"
    IMAGE_DATA = "image_data"
    ENNEAGRAM = "enneagram"
    STATS = "stats"
    BIOGRAPHY = "biography"
    RELATIONSHIPS = "relationships"
    AFFILIATIONS = "affiliations"
    NARRATIVE = "narrative"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    VERSION = "version"


class UIConstants(IntEnum):
    """UI dimension constants."""
    SIDEBAR_WIDTH = 250
    MIN_WINDOW_WIDTH = 1200
    MIN_WINDOW_HEIGHT = 800
    ANIMATION_DURATION = 300
    AUTOSAVE_INTERVAL = 30000  # 30 seconds in milliseconds
    ENNEAGRAM_WHEEL_SIZE = 400
    AFFINITY_RADAR_SIZE = 350
    IMAGE_WIDGET_SIZE = 200
    TAB_ICON_SIZE = 24


class FileConstants(StrEnum):
    """File and directory constants."""
    DATA_DIR = "data"
    CHARACTERS_DIR = "characters"
    SETTINGS_FILE = "settings.json"
    FILE_EXTENSION = ".json"
    BACKUP_EXTENSION = ".bak"


class ThemeMode(StrEnum):
    """Application theme modes."""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # Follow system theme