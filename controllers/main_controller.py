"""
controllers/main_controller.py - FIXED
Main controller with properly initialized properties
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt6.QtQml import QQmlEngine
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel


class MainController(QObject):
    """Main controller for the application"""
    
    # Signals
    characterLoaded = pyqtSignal()
    characterCreated = pyqtSignal()
    characterDeleted = pyqtSignal()
    errorOccurred = pyqtSignal(str)
    
    # Property changed signals
    currentCharacterChanged = pyqtSignal()
    characterListChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize models - IMPORTANT: These must not be None
        self._character_list = CharacterListModel(self)
        self._current_character = None  # Can be None initially
        
        # Set QML ownership to prevent garbage collection
        QQmlEngine.setObjectOwnership(self._character_list, QQmlEngine.ObjectOwnership.CppOwnership)
    
    # Character List property - ALWAYS returns a valid model
    @pyqtProperty(CharacterListModel, notify=characterListChanged)
    def characterList(self):
        """Get the character list model"""
        return self._character_list
    
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
    
    @pyqtSlot()
    def createNewCharacter(self):
        """Create a new character"""
        try:
            # Create new character model
            new_character = CharacterModel(self)
            new_character.name = "New Character"
            new_character.level = 1
            
            # Add to list
            self._character_list.addCharacter(new_character)
            
            # Set as current
            self.currentCharacter = new_character
            
            self.characterCreated.emit()
            
        except Exception as e:
            self.errorOccurred.emit(f"Failed to create character: {str(e)}")
    
    @pyqtSlot(str)
    def selectCharacter(self, character_id):
        """Select a character by ID"""
        try:
            character = self._character_list.getCharacterById(character_id)
            if character:
                self.currentCharacter = character
            else:
                self.errorOccurred.emit(f"Character not found: {character_id}")
        except Exception as e:
            self.errorOccurred.emit(f"Failed to select character: {str(e)}")
    
    @pyqtSlot(str)
    def deleteCharacter(self, character_id):
        """Delete a character by ID"""
        try:
            # If it's the current character, clear it
            if self._current_character and self._current_character.id == character_id:
                self.currentCharacter = None
            
            # Remove from list
            self._character_list.removeCharacterById(character_id)
            
            self.characterDeleted.emit()
            
        except Exception as e:
            self.errorOccurred.emit(f"Failed to delete character: {str(e)}")
    
    @pyqtSlot(str)
    def loadCharacterFromFile(self, file_path):
        """Load a character from a file"""
        try:
            # TODO: Implement file loading
            self.errorOccurred.emit("File loading not yet implemented")
        except Exception as e:
            self.errorOccurred.emit(f"Failed to load character: {str(e)}")
    
    @pyqtSlot(str)
    def filterCharacters(self, search_text):
        """Filter the character list"""
        try:
            self._character_list.setFilterText(search_text)
        except Exception as e:
            self.errorOccurred.emit(f"Failed to filter characters: {str(e)}")
    
    def load_character_file(self, file_path):
        """Python method to load a character file (called from main.py)"""
        self.loadCharacterFromFile(file_path)