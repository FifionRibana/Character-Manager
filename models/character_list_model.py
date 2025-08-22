"""
Character list model for QML ListView.
Provides character list for sidebar navigation.
"""

from PyQt6.QtCore import QAbstractListModel, Qt, pyqtSignal, QModelIndex, pyqtSlot, pyqtProperty, QObject
from PyQt6.QtQml import qmlRegisterType, QQmlEngine
from typing import List, Optional, Any
from data.character import Character


class CharacterListModel(QAbstractListModel):
    """
    Model for character list in sidebar.
    Provides data for QML ListView component.
    """
    
    # Custom roles for QML access
    NameRole = Qt.ItemDataRole.UserRole + 1
    LevelRole = Qt.ItemDataRole.UserRole + 2
    IdRole = Qt.ItemDataRole.UserRole + 3
    HasImageRole = Qt.ItemDataRole.UserRole + 4
    
    # Signals
    characterSelected = pyqtSignal(str)  # Emit character ID
    countChanged = pyqtSignal()  # For count property
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._characters: List[Any] = []  # Will store CharacterModel objects
        self._selected_index: int = -1
        self._filter_text: str = ""
    
    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of characters."""
        return len(self._characters)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for given index and role."""
        if not index.isValid() or index.row() >= len(self._characters):
            return None
        
        character = self._characters[index.row()]
        
        # Handle both Character and CharacterModel objects
        if role == self.NameRole:
            return character.name if hasattr(character, 'name') else "Unknown"
        elif role == self.LevelRole:
            return character.level if hasattr(character, 'level') else 1
        elif role == self.IdRole:
            return character.id if hasattr(character, 'id') else str(id(character))
        elif role == self.HasImageRole:
            if hasattr(character, 'imageData'):
                return bool(character.imageData)
            elif hasattr(character, 'image_data'):
                return bool(character.image_data)
            return False
        elif role == Qt.ItemDataRole.DisplayRole:
            return character.name if hasattr(character, 'name') else "Unknown"
        
        return None
    
    def roleNames(self) -> dict:
        """Return role names for QML access."""
        return {
            self.NameRole: b'name',
            self.LevelRole: b'level',
            self.IdRole: b'characterId',
            self.HasImageRole: b'hasImage'
        }
    
    def add_character(self, character):
        """Add a character to the model."""
        self.beginInsertRows(QModelIndex(), len(self._characters), len(self._characters))
        self._characters.append(character)
        self.endInsertRows()
        self.countChanged.emit()
        
    # Alternative method names for QML compatibility
    @pyqtSlot(QObject)
    def addCharacter(self, character):
        """QML-compatible method to add character"""
        self.add_character(character)
    
    def remove_character(self, character_id: str) -> bool:
        """Remove a character by ID."""
        for i, character in enumerate(self._characters):
            # Handle both Character and CharacterModel objects
            char_id = character.id if hasattr(character, 'id') else str(id(character))
            if char_id == character_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                del self._characters[i]
                self.endRemoveRows()
                self.countChanged.emit()
                
                # Adjust selected index if needed
                if self._selected_index == i:
                    self._selected_index = -1
                elif self._selected_index > i:
                    self._selected_index -= 1
                
                return True
        return False
    
    @pyqtSlot(str)
    def removeCharacterById(self, character_id: str):
        """QML-compatible method to remove character"""
        self.remove_character(character_id)
    
    def update_character(self, character):
        """Update a character in the model."""
        for i, existing_character in enumerate(self._characters):
            existing_id = existing_character.id if hasattr(existing_character, 'id') else str(id(existing_character))
            new_id = character.id if hasattr(character, 'id') else str(id(character))
            if existing_id == new_id:
                self._characters[i] = character
                index = self.createIndex(i, 0)
                self.dataChanged.emit(index, index)
                break
    
    def clear(self):
        """Clear all characters."""
        self.beginResetModel()
        self._characters.clear()
        self._selected_index = -1
        self.endResetModel()
        self.countChanged.emit()
    
    def load_characters(self, characters: List[Any]):
        """Load a list of characters."""
        self.beginResetModel()
        self._characters = characters.copy()
        self._selected_index = 0 if characters else -1
        self.endResetModel()
        self.countChanged.emit()
    
    def get_character(self, character_id: str) -> Optional[Any]:
        """Get character by ID."""
        for character in self._characters:
            # Handle both Character and CharacterModel objects
            char_id = character.id if hasattr(character, 'id') else str(id(character))
            if char_id == character_id:
                return character
        return None
    
    @pyqtSlot(str, result=QObject)
    def getCharacterById(self, character_id: str):
        """QML-compatible method to get character"""
        return self.get_character(character_id)
    
    def get_character_by_index(self, index: int) -> Optional[Character]:
        """Get character by index."""
        if 0 <= index < len(self._characters):
            return self._characters[index]
        return None
    
    @pyqtSlot(int)
    def selectCharacter(self, index: int):
        """Select a character by index (called from QML)."""
        if 0 <= index < len(self._characters):
            self._selected_index = index
            character = self._characters[index]
            char_id = character.id if hasattr(character, 'id') else str(id(character))
            self.characterSelected.emit(char_id)
    
    @pyqtSlot(str)
    def selectCharacterById(self, character_id: str):
        """Select a character by ID (called from QML)."""
        for i, character in enumerate(self._characters):
            char_id = character.id if hasattr(character, 'id') else str(id(character))
            if char_id == character_id:
                self._selected_index = i
                self.characterSelected.emit(character_id)
                break
    
    @pyqtSlot(result=int)
    def getSelectedIndex(self) -> int:
        """Get currently selected index."""
        return self._selected_index
    
    @pyqtSlot(result=str)
    def getSelectedCharacterId(self) -> str:
        """Get currently selected character ID."""
        if 0 <= self._selected_index < len(self._characters):
            character = self._characters[self._selected_index]
            return character.id if hasattr(character, 'id') else str(id(character))
        return ""
    
    @pyqtSlot(int, result=QObject)
    def getCharacterAt(self, index: int):
        """Get character at specific index for QML"""
        if 0 <= index < len(self._characters):
            return self._characters[index]
        return None
    
    @pyqtSlot(str)
    def setFilterText(self, text: str):
        """Set filter text for character list"""
        self._filter_text = text
        # TODO: Implement actual filtering logic
        
    @pyqtProperty(int, notify=countChanged)
    def count(self) -> int:
        """Get count of characters for QML"""
        return len(self._characters)


# Register the type for QML
def register_character_list_model():
    """Register CharacterListModel for QML."""
    qmlRegisterType(CharacterListModel, 'CharacterModels', 1, 0, 'CharacterListModel')