"""
controllers/main_controller.py
Main controller with properly initialized properties
"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt6.QtQml import QQmlEngine
from data.character import Character
from data.enums import FileConstants, FileExtension, Language
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel
from utils.singleton import singleton
from utils.translator import get_translator, tr

from .storage_controller import StorageController


@singleton
@dataclass
class MainController(QObject):
    """Main controller for the application"""

    # Signals
    characterLoaded: ClassVar[pyqtSignal] = pyqtSignal()
    characterCreated: ClassVar[pyqtSignal] = pyqtSignal()
    characterDeleted: ClassVar[pyqtSignal] = pyqtSignal()
    characterSaved: ClassVar[pyqtSignal] = pyqtSignal(str)
    errorOccurred: ClassVar[pyqtSignal] = pyqtSignal(str, str)
    statusChanged: ClassVar[pyqtSignal] = pyqtSignal(str)

    # Property changed signals
    currentCharacterChanged: ClassVar[pyqtSignal] = pyqtSignal()
    characterListChanged: ClassVar[pyqtSignal] = pyqtSignal()

    editModeChanged: ClassVar[pyqtSignal] = pyqtSignal()

    # Initialize models - IMPORTANT: These must not be None
    _character_list_model: CharacterListModel = field(
        init=False, default_factory=lambda: CharacterListModel()
    )
    _current_character: CharacterModel = field(
        init=False, default=None
    )  # Can be None initially

    _edit_mode: bool = field(init=False, default=False)

    def __post_init__(self):
        QObject.__init__(self)

        # Set QML ownership to prevent garbage collection
        # QQmlEngine.setObjectOwnership(
        #     self._character_list_model, QQmlEngine.ObjectOwnership.CppOwnership
        # )

    # Character List property - ALWAYS returns a valid model
    @pyqtProperty(CharacterListModel, notify=characterListChanged)
    def characterListModel(self):
        """Get the character list model"""
        return self._character_list_model

    # Current Character property - can be None
    @pyqtProperty(CharacterModel, notify=currentCharacterChanged)
    def currentCharacter(self):
        """Get the current character model"""
        return self._current_character

    @currentCharacter.setter
    def currentCharacter(self, character):
        """Set the current character model"""
        if self._current_character != character:
            self._current_character = character
            self.currentCharacterChanged.emit()
            if character:
                self.characterLoaded.emit()

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

    ### SLOTS ###

    @pyqtSlot()
    def create_new_character(self):
        """Create a new character"""
        try:
            print("Create a new character")
            # Create new character model
            new_character = CharacterModel(_character=Character.create_default())

            # Add to list
            self._character_list_model.add_character(new_character)

            # Set as current
            self.currentCharacter = new_character

            self.characterCreated.emit()

            print(f"New character created: {new_character.name}")

        except Exception as e:
            print(f"Failed to create character: {str(e)}")
            self.errorOccurred.emit(f"Failed to create character: {str(e)}")

    @pyqtSlot(str)
    def select_character(self, character_id):
        """Select a character by ID"""
        try:
            character = self._character_list_model.get_character(character_id)
            if character:
                self.currentCharacter = character
            else:
                self.errorOccurred.emit(f"Character not found: {character_id}")
        except Exception as e:
            self.errorOccurred.emit(f"Failed to select character: {str(e)}")

    @pyqtSlot(str)
    def delete_character(self, character_id):
        """Delete a character by ID"""
        try:
            # If it's the current character, clear it
            if self._current_character and self._current_character.id == character_id:
                self.currentCharacter = None

            # Remove from list
            self._character_list_model.remove_character(character_id)

            self.characterDeleted.emit()

        except Exception as e:
            self.errorOccurred.emit(f"Failed to delete character: {str(e)}")

    @pyqtSlot()
    def save_current_character(self):
        """Save the current character using StorageController."""
        print("Saving triggered")
        if not self._current_character:
            return

        try:
            # Convert character to JSON using the proper storage controller method
            character_dict = self._current_character.get_character().to_dict()
            character_json = self._dict_to_json_string(character_dict)

            # Generate safe file path
            safe_name = self._make_safe_filename(self._current_character.name)
            file_path = FileConstants.DATA_DIR / f"{safe_name}{FileExtension.JSON.value}"

            # Save using storage controller
            success = StorageController().save_character(character_json, str(file_path))

            if success:
                self._character_list_model.update_character(self._current_character)
                self.characterSaved.emit(self._current_character.name)
                self.statusChanged.emit(f"Saved {self._current_character.name}")

        except Exception as e:
            self.errorOccurred.emit("Save Error", f"Failed to save character: {str(e)}")

    def _dict_to_json_string(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to JSON string."""
        import json

        return json.dumps(data, indent=2, default=str)

    def _make_safe_filename(self, name: str) -> str:
        """Create a safe filename from character name."""
        return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()

    @pyqtSlot(str)
    def load_character_from_file(self, file_path):
        """Load a character from a file"""
        try:
            # TODO: Implement file loading
            self.errorOccurred.emit("File loading not yet implemented")
        except Exception as e:
            self.errorOccurred.emit(f"Failed to load character: {str(e)}")

    @pyqtSlot(str)
    def filter_characters(self, search_text):
        """Filter the character list"""
        try:
            # For now, just emit a signal - filtering will be handled in the model
            # self._character_list_model.setFilterText(search_text)
            pass  # TODO: Implement filtering
        except Exception as e:
            self.errorOccurred.emit(f"Failed to filter characters: {str(e)}")

    def load_character_file(self, file_path):
        """Python method to load a character file (called from main.py)"""
        self.load_character_from_file(file_path)

    @pyqtSlot()
    def toggleEditMode(self):
        """Toggle edit mode."""
        self.editMode = not self.editMode

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
