"""
Character relationships management tab.
"""

from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import pyqtSignal

from models.character import Character, Relationship
from models.enums import RelationType
from utils.translator import tr


class RelationshipsTab(QWidget):
    """Tab for managing character relationships."""
    
    dataChanged = pyqtSignal()
    
    def __init__(self, all_characters: Dict[str, Character], parent=None):
        super().__init__(parent)
        self.all_characters = all_characters
        self.current_character: Optional[Character] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        
        # Relationships table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.add_relationship)
        self.remove_button = QPushButton()
        self.remove_button.clicked.connect(self.remove_relationship)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.table.setHorizontalHeaderLabels([
            tr("character"), tr("type"), tr("description")
        ])
        self.add_button.setText(tr("add_relationship"))
        self.remove_button.setText(tr("remove"))
        
    def load_character(self, character: Character):
        """Load character data."""
        self.current_character = character

        # Block signals during loading
        self.blockSignals(True)
        
        self.table.setRowCount(len(character.relationships))
        for i, rel in enumerate(character.relationships):
            self.table.setItem(i, 0, QTableWidgetItem(rel.target_name))
            self.table.setItem(i, 1, QTableWidgetItem(rel.relationship_type.value))
            self.table.setItem(i, 2, QTableWidgetItem(rel.description))
            
        # Re-enable signals
        self.blockSignals(False)

    def save_to_character(self, character: Character):
        """Save data to character."""
        # Relationships are saved immediately when added/removed
        pass
        
    def clear(self):
        """Clear the tab."""
        self.current_character = None
        self.table.setRowCount(0)
        
    def add_relationship(self):
        """Add new relationship."""
        # This would open a dialog - simplified for now
        if self.current_character:
            self.on_data_changed()
            
    def remove_relationship(self):
        """Remove selected relationship."""
        current_row = self.table.currentRow()
        if current_row >= 0 and self.current_character:
            del self.current_character.relationships[current_row]
            self.load_character(self.current_character)
            self.on_data_changed()
            
    def on_data_changed(self):
        """Handle data changes."""
        if self.current_character:
            self.dataChanged.emit()
