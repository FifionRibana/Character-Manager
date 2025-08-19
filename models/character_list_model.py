"""
Character list model for QML ListView.
Provides character list for sidebar navigation.
"""

from PyQt6.QtCore import QAbstractListModel, Qt, pyqtSignal, QModelIndex, pyqtSlot
from PyQt6.QtQml import qmlRegisterType
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
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._characters: List[Character] = []
        self._selected_index: int = -1
    
    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of characters."""
        return len(self._characters)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for given index and role."""
        if not index.isValid() or index.row() >= len(self._characters):
            return None
        
        character = self._characters[index.row()]
        
        if role == self.NameRole:
            return character.name
        elif role == self.LevelRole:
            return character.level
        elif role == self.IdRole:
            return character.id
        elif role == self.HasImageRole:
            return bool(character.image_data)
        elif role == Qt.ItemDataRole.DisplayRole:
            return character.name
        
        return None
    
    def roleNames(self) -> dict:
        """Return role names for QML access."""
        return {
            self.NameRole: b'name',
            self.LevelRole: b'level',
            self.IdRole: b'characterId',
            self.HasImageRole: b'hasImage'
        }
    
    def add_character(self, character: Character):
        """Add a character to the model."""
        self.beginInsertRows(QModelIndex(), len(self._characters), len(self._characters))
        self._characters.append(character)
        self.endInsertRows()
    
    def remove_character(self, character_id: str) -> bool:
        """Remove a character by ID."""
        for i, character in enumerate(self._characters):
            if character.id == character_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                del self._characters[i]
                self.endRemoveRows()
                
                # Adjust selected index if needed
                if self._selected_index == i:
                    self._selected_index = -1
                elif self._selected_index > i:
                    self._selected_index -= 1
                
                return True
        return False
    
    def update_character(self, character: Character):
        """Update a character in the model."""
        for i, existing_character in enumerate(self._characters):
            if existing_character.id == character.id:
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
    
    def load_characters(self, characters: List[Character]):
        """Load a list of characters."""
        self.beginResetModel()
        self._characters = characters.copy()
        self._selected_index = 0 if characters else -1
        self.endResetModel()
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """Get character by ID."""
        for character in self._characters:
            if character.id == character_id:
                return character
        return None
    
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
            self.characterSelected.emit(character.id)
    
    @pyqtSlot(str)
    def selectCharacterById(self, character_id: str):
        """Select a character by ID (called from QML)."""
        for i, character in enumerate(self._characters):
            if character.id == character_id:
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
            return self._characters[self._selected_index].id
        return ""


# Register the type for QML
def register_character_list_model():
    """Register CharacterListModel for QML."""
    qmlRegisterType(CharacterListModel, 'CharacterModels', 1, 0, 'CharacterListModel')