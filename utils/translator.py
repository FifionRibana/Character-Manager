"""
Translation management system for dynamic language switching.
Allows changing language without restarting the application.
"""

import json
from pathlib import Path
from typing import Dict, Optional
from PyQt6.QtCore import QObject, pyqtSignal
from models.enums import Language


class TranslationManager(QObject):
    """Manages application translations and language switching."""
    
    # Signal emitted when language changes
    languageChanged = pyqtSignal(Language)
    
    def __init__(self):
        super().__init__()
        self.current_language = Language.ENGLISH
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all translation files."""
        translations_dir = Path(__file__).parent.parent / "translations"
        
        for lang in Language:
            file_path = translations_dir / f"{lang.value}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang.value] = json.load(f)
            else:
                # Create default English translations if file doesn't exist
                if lang == Language.ENGLISH:
                    self.translations[lang.value] = self._get_default_translations()
                else:
                    self.translations[lang.value] = {}
    
    def set_language(self, language: Language):
        """Change the current language."""
        if language != self.current_language:
            self.current_language = language
            self.languageChanged.emit(language)
    
    def tr(self, key: str, default: Optional[str] = None) -> str:
        """
        Translate a key to the current language.
        
        Args:
            key: Translation key
            default: Default value if translation not found
            
        Returns:
            Translated string or default value
        """
        translations = self.translations.get(self.current_language.value, {})
        return translations.get(key, default or key)
    
    def _get_default_translations(self) -> Dict[str, str]:
        """Get default English translations."""
        return {
            # Main window
            "app_title": "Medieval Character Manager",
            "file": "File",
            "edit": "Edit",
            "view": "View",
            "help": "Help",
            
            # Actions
            "new_character": "New Character",
            "save": "Save",
            "save_as": "Save As",
            "load": "Load",
            "export_pdf": "Export PDF",
            "export_html": "Export HTML",
            "delete": "Delete",
            "quit": "Quit",
            
            # Sidebar
            "characters": "Characters",
            "new": "New",
            "delete_btn": "Delete",
            
            # Character fields
            "name": "Name",
            "level": "Level",
            "drop_image": "Drop image here\nor click to browse",
            
            # Tabs
            "tab_enneagram": "Enneagram",
            "tab_stats": "Stats",
            "tab_biography": "Biography",
            "tab_relationships": "Relationships",
            "tab_narrative": "Narrative",
            
            # Enneagram
            "main_type": "Main Type",
            "wing": "Wing",
            "no_wing": "No Wing",
            "development_level": "Development Level",
            "instinctual_stack": "Instinctual Stack (Primary to Tertiary)",
            "integration": "Integration",
            "disintegration": "Disintegration",
            "type_description": "Type Description",
            "tritype": "Tritype",
            
            # Enneagram types
            "type_1_name": "The Reformer",
            "type_2_name": "The Helper",
            "type_3_name": "The Achiever",
            "type_4_name": "The Individualist",
            "type_5_name": "The Investigator",
            "type_6_name": "The Loyalist",
            "type_7_name": "The Enthusiast",
            "type_8_name": "The Challenger",
            "type_9_name": "The Peacemaker",
            
            "type_1_desc": "Principled, purposeful, self-controlled, and perfectionistic.",
            "type_2_desc": "Generous, demonstrative, people-pleasing, and possessive.",
            "type_3_desc": "Adaptable, excelling, driven, and image-conscious.",
            "type_4_desc": "Expressive, dramatic, self-absorbed, and temperamental.",
            "type_5_desc": "Perceptive, innovative, secretive, and isolated.",
            "type_6_desc": "Engaging, responsible, anxious, and suspicious.",
            "type_7_desc": "Spontaneous, versatile, acquisitive, and scattered.",
            "type_8_desc": "Self-confident, decisive, willful, and confrontational.",
            "type_9_desc": "Receptive, reassuring, complacent, and resigned.",
            
            # Stats
            "ability_scores": "Ability Scores",
            "strength": "Strength",
            "agility": "Agility",
            "constitution": "Constitution",
            "intelligence": "Intelligence",
            "wisdom": "Wisdom",
            "charisma": "Charisma",
            
            # Biography
            "biography_placeholder": "Enter character background, history, traumatic events, etc...",
            "affiliations": "Affiliations",
            "add_affiliation": "Add Affiliation",
            "remove": "Remove",
            "affiliation_name": "Affiliation name:",
            
            # Relationships
            "character": "Character",
            "type": "Type",
            "description": "Description",
            "add_relationship": "Add Relationship",
            "relationship_type": "Relationship Type",
            
            # Relationship types
            "rel_family": "Family",
            "rel_friend": "Friend",
            "rel_rival": "Rival",
            "rel_mentor": "Mentor",
            "rel_student": "Student",
            "rel_ally": "Ally",
            "rel_enemy": "Enemy",
            "rel_romantic": "Romantic",
            "rel_neutral": "Neutral",
            
            # Narrative
            "add_event": "Add Event",
            "event_title": "Title",
            "chapter": "Chapter",
            "event_description": "Description",
            "timeline": "Timeline",
            
            # Messages
            "ready": "Ready",
            "saved": "Saved",
            "loaded": "Loaded",
            "character_created": "New character created",
            "character_deleted": "Character deleted",
            "delete_confirm": "Delete {name}?",
            "save_error": "Failed to save character",
            "load_error": "Failed to load character",
            "autosaving": "Autosaving...",
            
            # Dialogs
            "select_image": "Select Character Image",
            "images_filter": "Images (*.png *.jpg *.jpeg *.bmp *.gif)",
            "json_filter": "JSON Files (*.json)",
            "load_character": "Load Character",
            "export_location": "Export Location",
            
            # Settings
            "language": "Language",
            "theme": "Theme",
            "light_theme": "Light",
            "dark_theme": "Dark",
            "auto_theme": "Auto (System)",
        }


# Global translator instance
_translator = None


def get_translator() -> TranslationManager:
    """Get the global translator instance."""
    global _translator
    if _translator is None:
        _translator = TranslationManager()
    return _translator


def tr(key: str, default: Optional[str] = None) -> str:
    """
    Convenience function for translation.
    
    Args:
        key: Translation key
        default: Default value if translation not found
        
    Returns:
        Translated string
    """
    return get_translator().tr(key, default)