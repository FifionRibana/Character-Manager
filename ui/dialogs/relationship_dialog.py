"""
Dialog for adding and editing character relationships.
"""

from typing import Dict
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QTextEdit,
    QDialogButtonBox
)

from models.character import Character, Relationship
from models.enums import RelationType
from utils.translator import tr


class RelationshipDialog(QDialog):
    """Dialog for adding/editing relationships."""
    
    def __init__(self, all_characters: Dict[str, Character], current_id: str, parent=None):
        super().__init__(parent)
        self.all_characters = all_characters
        self.current_id = current_id
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle(tr("add_relationship"))
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        # Character selection
        self.character_combo = QComboBox()
        for char_id, character in self.all_characters.items():
            if char_id != self.current_id:
                self.character_combo.addItem(character.name, char_id)
        layout.addRow(tr("character"), self.character_combo)
        
        # Relationship type
        self.type_combo = QComboBox()
        for rel_type in RelationType:
            self.type_combo.addItem(tr(f"rel_{rel_type.value}"), rel_type)
        layout.addRow(tr("relationship_type"), self.type_combo)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addRow(tr("description"), self.description_edit)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def get_relationship(self) -> Relationship:
        """Get the created relationship."""
        return Relationship(
            target_id=self.character_combo.currentData(),
            target_name=self.character_combo.currentText(),
            relationship_type=self.type_combo.currentData(),
            description=self.description_edit.toPlainText()
        )
