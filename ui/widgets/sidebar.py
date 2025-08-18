"""
Sidebar widget for character list and navigation.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from models.character import Character
from models.enums import UIConstants
from utils.translator import tr


class CharacterSidebar(QWidget):
    """
    Sidebar widget displaying character list with quick navigation.
    """
    
    # Signals
    characterSelected = pyqtSignal(Character)
    newCharacterRequested = pyqtSignal()
    deleteCharacterRequested = pyqtSignal(str)  # character_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.characters = {}  # id -> Character mapping
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the sidebar UI."""
        # Set fixed width
        self.setMaximumWidth(UIConstants.SIDEBAR_WIDTH)
        self.setMinimumWidth(UIConstants.SIDEBAR_WIDTH)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title section
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Character list
        self.character_list = QListWidget()
        self.character_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.character_list.itemClicked.connect(self.on_character_clicked)
        self.character_list.setAlternatingRowColors(True)
        layout.addWidget(self.character_list)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        # New character button
        self.new_button = QPushButton()
        self.new_button.clicked.connect(self.newCharacterRequested.emit)
        self.new_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.new_button)
        
        # Delete character button
        self.delete_button = QPushButton()
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.setObjectName("deleteButton")  # For styling
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        
        # Apply initial translations
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.title_label.setText(tr("characters"))
        self.new_button.setText(tr("new"))
        self.delete_button.setText(tr("delete_btn"))
        
        # Update tooltips
        self.new_button.setToolTip(tr("new_character"))
        self.delete_button.setToolTip(tr("delete"))
        
    def add_character(self, character: Character):
        """
        Add a character to the sidebar.
        
        Args:
            character: Character to add
        """
        # Store character reference
        self.characters[character.id] = character
        
        # Create list item
        item = QListWidgetItem(character.name)
        item.setData(Qt.ItemDataRole.UserRole, character.id)
        
        # Add icon based on level (optional enhancement)
        if character.level >= 10:
            item.setToolTip(f"Level {character.level} - Veteran")
        elif character.level >= 5:
            item.setToolTip(f"Level {character.level} - Experienced")
        else:
            item.setToolTip(f"Level {character.level} - Novice")
        
        self.character_list.addItem(item)
        
        # Auto-select if it's the first character
        if self.character_list.count() == 1:
            self.character_list.setCurrentItem(item)
            print(f"CHAR: {character.stats}")
            self.characterSelected.emit(character)
    
    def update_character(self, character: Character):
        """
        Update character display in the list.
        
        Args:
            character: Updated character
        """
        # Update stored reference
        self.characters[character.id] = character
        
        # Find and update list item
        for i in range(self.character_list.count()):
            item = self.character_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == character.id:
                item.setText(character.name)
                item.setToolTip(f"Level {character.level}")
                break
    
    def remove_character(self, character_id: str):
        """
        Remove a character from the sidebar.
        
        Args:
            character_id: ID of character to remove
        """
        # Remove from storage
        if character_id in self.characters:
            del self.characters[character_id]
        
        # Remove from list
        for i in range(self.character_list.count()):
            item = self.character_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == character_id:
                self.character_list.takeItem(i)
                break
    
    def get_selected_character(self) -> Optional[Character]:
        """
        Get the currently selected character.
        
        Returns:
            Selected character or None
        """
        current_item = self.character_list.currentItem()
        if current_item:
            character_id = current_item.data(Qt.ItemDataRole.UserRole)
            return self.characters.get(character_id)
        return None
    
    def select_character(self, character_id: str):
        """
        Select a character in the list.
        
        Args:
            character_id: ID of character to select
        """
        for i in range(self.character_list.count()):
            item = self.character_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == character_id:
                self.character_list.setCurrentItem(item)
                break
    
    def clear(self):
        """Clear all characters from the sidebar."""
        self.character_list.clear()
        self.characters.clear()
    
    def on_character_clicked(self, item: QListWidgetItem):
        """
        Handle character selection from list.
        
        Args:
            item: Clicked list item
        """
        character_id = item.data(Qt.ItemDataRole.UserRole)
        if character_id in self.characters:
            self.characterSelected.emit(self.characters[character_id])
    
    def on_delete_clicked(self):
        """Handle delete button click."""
        character = self.get_selected_character()
        if character:
            self.deleteCharacterRequested.emit(character.id)
            self.remove_character(character.id)
    
    def get_character_count(self) -> int:
        """
        Get the number of characters in the sidebar.
        
        Returns:
            Number of characters
        """
        return len(self.characters)
    
    def get_all_characters(self) -> list:
        """
        Get all characters in the sidebar.
        
        Returns:
            List of all characters
        """
        return list(self.characters.values())