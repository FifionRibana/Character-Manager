#!/usr/bin/env python3
"""
Main controller for the QML application.
Orchestrates models and business logic.
Fixed version with corrected imports for your project structure.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import asdict

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt6.QtQml import qmlRegisterType

# CORRECTED IMPORTS for your project structure
from data.character import Character  # NOT models.character
from data.enneagram import EnneagramProfile
from data.enums import EnneagramType, StatType, RelationType, Language

# Import models
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel

# Use StorageController instead of StorageManager
from controllers.storage_controller import StorageController

# Translator with corrected import
from utils.translator import get_translator, tr


class MainController(QObject):
    """
    Main application controller.
    Manages character data, storage, and coordinates between models.
    """
    
    # Signals
    characterLoaded = pyqtSignal()
    characterSaved = pyqtSignal(str)  # character name
    errorOccurred = pyqtSignal(str, str)  # title, message
    statusChanged = pyqtSignal(str)  # status message
    editModeChanged = pyqtSignal()
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        
        # Initialize storage controller and translation
        self.storage = StorageController(self)  # Use StorageController, not StorageManager
        self.translator = get_translator()
        
        # Create models
        self.character_model = CharacterModel()
        self.character_list_model = CharacterListModel()
        
        # Application state
        self._edit_mode: bool = False
        self._characters: Dict[str, Character] = {}
        self._current_character: Optional[Character] = None
        
        # Connect signals
        self.character_list_model.characterSelected.connect(self.load_character_by_id)
        
        # Load characters on startup
        self.load_all_characters()
    
    # Properties exposed to QML
    @pyqtProperty(CharacterModel, constant=True)
    def characterModel(self) -> CharacterModel:
        """Get the character model for QML."""
        return self.character_model
    
    @pyqtProperty(CharacterListModel, constant=True)
    def characterListModel(self) -> CharacterListModel:
        """Get the character list model for QML."""
        return self.character_list_model
    
    @pyqtProperty(bool, notify=editModeChanged)
    def editMode(self) -> bool:
        """Get current edit mode state."""
        return self._edit_mode
    
    @editMode.setter
    def editMode(self, value: bool):
        """Set edit mode state."""
        if self._edit_mode != value:
            self._edit_mode = value
            self.editModeChanged.emit()
            
            if not value and self._current_character:
                # Auto-save when leaving edit mode
                self.save_current_character()
    
    @pyqtProperty(bool, notify=characterLoaded)
    def hasCharacter(self) -> bool:
        """Check if a character is currently loaded."""
        return self._current_character is not None
    
    @pyqtProperty(str, notify=characterLoaded)
    def currentCharacterName(self) -> str:
        """Get current character name."""
        return self._current_character.name if self._current_character else ""
    
    # Character management methods
    @pyqtSlot()
    def newCharacter(self):
        """Create a new character."""
        try:
            character = Character.create_default("New Character")
            self._characters[character.id] = character
            self.character_list_model.add_character(character)
            
            # Select the new character
            self.character_list_model.selectCharacterById(character.id)
            self.load_character_by_id(character.id)
            
            # Switch to edit mode
            self.editMode = True
            
            self.statusChanged.emit(tr("character_created"))
            
        except Exception as e:
            self.errorOccurred.emit("Error", f"Failed to create character: {str(e)}")
    
    @pyqtSlot(str)
    def deleteCharacter(self, character_id: str):
        """Delete a character by ID."""
        try:
            if character_id not in self._characters:
                return
            
            character = self._characters[character_id]
            
            # Remove from memory and model
            del self._characters[character_id]
            self.character_list_model.remove_character(character_id)
            
            # Clear if it was current character
            if self._current_character and self._current_character.id == character_id:
                self._current_character = None
                self.character_model.set_character(None)
                self.characterLoaded.emit()
            
            self.statusChanged.emit(tr("character_deleted"))
            
        except Exception as e:
            self.errorOccurred.emit("Error", f"Failed to delete character: {str(e)}")
    
    @pyqtSlot(str)
    def load_character_by_id(self, character_id: str):
        """Load a character by ID."""
        if character_id not in self._characters:
            return
        
        character = self._characters[character_id]
        self._current_character = character
        self.character_model.set_character(character)
        self.characterLoaded.emit()
        
        self.statusChanged.emit(f"Loaded {character.name}")
    
    @pyqtSlot()
    def save_current_character(self):
        """Save the current character using StorageController."""
        if not self._current_character:
            return
        
        try:
            # Convert character to JSON using the proper storage controller method
            character_dict = self._current_character.to_dict()
            character_json = self._dict_to_json_string(character_dict)
            
            # Generate safe file path
            safe_name = self._make_safe_filename(self._current_character.name)
            file_path = Path.cwd() / f"{safe_name}.json"
            
            # Save using storage controller
            success = self.storage.save_character(character_json, str(file_path))
            
            if success:
                self.character_list_model.update_character(self._current_character)
                self.characterSaved.emit(self._current_character.name)
                self.statusChanged.emit(f"Saved {self._current_character.name}")
            else:
                self.errorOccurred.emit("Save Error", "Failed to save character")
                
        except Exception as e:
            self.errorOccurred.emit("Save Error", f"Failed to save character: {str(e)}")
    
    def _dict_to_json_string(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to JSON string."""
        import json
        return json.dumps(data, indent=2, default=str)
    
    def _make_safe_filename(self, name: str) -> str:
        """Create a safe filename from character name."""
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    @pyqtSlot(str, result=bool)
    def loadCharacterFile(self, file_path: str) -> bool:
        """Load a character from file path using StorageController."""
        try:
            # Load using storage controller
            character_json = self.storage.load_character(file_path)
            
            if character_json:
                # Parse JSON and create character
                import json
                character_dict = json.loads(character_json)
                character = Character.from_dict(character_dict)
                
                # Store and load
                self._characters[character.id] = character
                self.character_list_model.add_character(character)
                
                # Select the loaded character
                self.character_list_model.selectCharacterById(character.id)
                self.load_character_by_id(character.id)
                
                self.statusChanged.emit(f"Loaded {character.name}")
                return True
            else:
                self.errorOccurred.emit("Load Error", "Failed to load character file")
                return False
                
        except Exception as e:
            self.errorOccurred.emit("Load Error", f"Failed to load character: {str(e)}")
            return False
    
    def load_all_characters(self):
        """Load all characters from recent files."""
        try:
            # Get recent files from storage controller
            recent_files = self.storage.get_recent_files()
            
            loaded_count = 0
            for file_path in recent_files[:5]:  # Load max 5 recent files
                if self.loadCharacterFile(file_path):
                    loaded_count += 1
            
            if loaded_count > 0:
                self.statusChanged.emit(f"Loaded {loaded_count} characters")
                
                # Load first character if available
                if self._characters:
                    first_character_id = next(iter(self._characters.keys()))
                    self.load_character_by_id(first_character_id)
            
        except Exception as e:
            self.errorOccurred.emit("Load Error", f"Failed to load characters: {str(e)}")
    
    @pyqtSlot(str, str, result=bool)
    def exportCharacter(self, character_id: str, file_path: str) -> bool:
        """Export character to HTML using StorageController."""
        try:
            if character_id not in self._characters:
                return False
            
            character = self._characters[character_id]
            character_dict = character.to_dict()
            character_json = self._dict_to_json_string(character_dict)
            
            success = self.storage.export_character_html(character_json, file_path)
            
            if success:
                self.statusChanged.emit(f"Exported {character.name}")
                return True
            else:
                self.errorOccurred.emit("Export Error", "Failed to export character")
                return False
                
        except Exception as e:
            self.errorOccurred.emit("Export Error", f"Failed to export: {str(e)}")
            return False
    
    # Translation support
    @pyqtSlot(str, result=str)
    def translate(self, key: str) -> str:
        """Translate a key to current language."""
        return tr(key)
    
    @pyqtSlot(str)
    def setLanguage(self, language_code: str):
        """Set application language."""
        try:
            language = Language(language_code)
            self.translator.set_language(language)
        except ValueError:
            pass  # Invalid language code
    
    # Utility methods
    @pyqtSlot(result=str)
    def getCurrentCharacterId(self) -> str:
        """Get current character ID."""
        return self._current_character.id if self._current_character else ""
    
    @pyqtSlot(result=str)
    def getCurrentCharacterName(self) -> str:
        """Get current character name."""
        return self._current_character.name if self._current_character else ""
    
    @pyqtSlot()
    def toggleEditMode(self):
        """Toggle edit mode."""
        self.editMode = not self.editMode


# Register the type for QML
def register_main_controller():
    """Register MainController for QML."""
    qmlRegisterType(MainController, 'Controllers', 1, 0, 'MainController')


if __name__ == "__main__":
    # Simple test
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    controller = MainController()
    print("MainController created successfully")
    print(f"Has character: {controller.hasCharacter}")
    print(f"Edit mode: {controller.editMode}")