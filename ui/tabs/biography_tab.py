"""
Biography and affiliations management tab.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox,
    QListWidget, QPushButton, QHBoxLayout, QInputDialog
)
from PyQt6.QtCore import pyqtSignal

from models.character import Character
from utils.translator import tr


class BiographyTab(QWidget):
    """Tab for character biography and affiliations."""
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        
        # Biography editor
        bio_group = QGroupBox()
        bio_layout = QVBoxLayout(bio_group)
        
        self.biography_edit = QTextEdit()
        bio_layout.addWidget(self.biography_edit)
        
        layout.addWidget(bio_group)
        
        # Affiliations
        aff_group = QGroupBox()
        aff_layout = QVBoxLayout(aff_group)
        
        self.affiliations_list = QListWidget()
        aff_layout.addWidget(self.affiliations_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.add_affiliation)
        self.remove_button = QPushButton()
        self.remove_button.clicked.connect(self.remove_affiliation)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()
        
        aff_layout.addLayout(button_layout)
        layout.addWidget(aff_group)
        
        self.biography_edit.textChanged.connect(self.on_data_changed)
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.biography_edit.setPlaceholderText(tr("biography_placeholder"))
        self.add_button.setText(tr("add_affiliation"))
        self.remove_button.setText(tr("remove"))
        
    def load_character(self, character: Character):
        """Load character data."""
        self.current_character = character

        # Block signals during loading
        self.blockSignals(True)
        
        self.biography_edit.setPlainText(character.biography)
        
        self.affiliations_list.clear()
        for affiliation in character.affiliations:
            self.affiliations_list.addItem(affiliation)
            
        # Re-enable signals
        self.blockSignals(False)
            
    def save_to_character(self, character: Character):
        """Save data to character."""
        if not character:
            return
        character.biography = self.biography_edit.toPlainText()
        
        character.affiliations = []
        for i in range(self.affiliations_list.count()):
            character.affiliations.append(self.affiliations_list.item(i).text())
            
    def clear(self):
        """Clear the tab."""
        self.current_character = None
        self.biography_edit.clear()
        self.affiliations_list.clear()
        
    def add_affiliation(self):
        """Add new affiliation."""
        text, ok = QInputDialog.getText(self, tr("add_affiliation"), tr("affiliation_name"))
        if ok and text and self.current_character:
            self.affiliations_list.addItem(text)
            self.on_data_changed()
            
    def remove_affiliation(self):
        """Remove selected affiliation."""
        current = self.affiliations_list.currentRow()
        if current >= 0:
            self.affiliations_list.takeItem(current)
            self.on_data_changed()
            
    def on_data_changed(self):
        """Handle data changes."""
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()
