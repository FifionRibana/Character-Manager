"""
Main controller for the QML application.
Orchestrates models and business logic.
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt6.QtQml import qmlRegisterType
from typing import Optional, Dict
from pathlib import Path

from models.character import Character
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel
from utils.storage import StorageManager
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
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize storage and translation
        self.storage = StorageManager()
        self.translator = get_translator()
        
        # Create models
        self.character_model = CharacterModel(self)
        self.character_list_model = CharacterListModel(self)
        
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
    
    # Character management methods
    @pyqtSlot()
    def newCharacter(self):
        """Create a new character."""
        try:
            character = Character()
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
            
            # Remove from storage
            self.storage.delete_character(character_id)
            
            # Remove from memory and model
            del self._characters[character_id]
            self.character_list_model.remove_character(character_id)
            
            # Clear if it was current character
            if self._current_character and self._current_character.id == character_id:
                self._current_character = None
                self.character_model.clear()
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
        self.character_model.load_character(character)
        self.characterLoaded.emit()
        
        self.statusChanged.emit(f"Loaded {character.name}")
    
    @pyqtSlot()
    def save_current_character(self):
        """Save the current character."""
        if not self._current_character:
            return
        
        try:
            self.storage.save_character(self._current_character)
            self.character_list_model.update_character(self._current_character)
            self.characterSaved.emit(self._current_character.name)
            self.statusChanged.emit(f"Saved {self._current_character.name}")
            
        except Exception as e:
            self.errorOccurred.emit("Save Error", f"Failed to save character: {str(e)}")
    
    @pyqtSlot(str, result=bool)
    def loadCharacterFile(self, file_path: str) -> bool:
        """Load a character from file path."""
        try:
            character = self.storage.load_character_from_file(Path(file_path))
            self._characters[character.id] = character
            self.character_list_model.add_character(character)
            
            # Select the loaded character
            self.character_list_model.selectCharacterById(character.id)
            self.load_character_by_id(character.id)
            
            self.statusChanged.emit(f"Loaded {character.name}")
            return True
            
        except Exception as e:
            self.errorOccurred.emit("Load Error", f"Failed to load character: {str(e)}")
            return False
    
    def load_all_characters(self):
        """Load all characters from storage."""
        try:
            characters = self.storage.load_all_characters()
            
            # Store in dictionary
            for character in characters:
                self._characters[character.id] = character
            
            # Load into list model
            self.character_list_model.load_characters(characters)
            
            # Load first character if any
            if characters:
                self.load_character_by_id(characters[0].id)
            
        except Exception as e:
            self.errorOccurred.emit("Load Error", f"Failed to load characters: {str(e)}")
    
    @pyqtSlot(str, str, result=bool)
    def exportCharacter(self, character_id: str, file_path: str) -> bool:
        """Export character to HTML."""
        try:
            if character_id not in self._characters:
                return False
            
            character = self._characters[character_id]
            self.storage.export_to_html(character, Path(file_path))
            self.statusChanged.emit(f"Exported {character.name}")
            return True
            
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
        from data.enums import Language
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