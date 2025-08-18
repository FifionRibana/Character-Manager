"""
Biography and affiliations management tab.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QGroupBox,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QInputDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
)
from PyQt6.QtCore import pyqtSignal

from models.character import Character
from ui.widgets.image_drop import ImageDropWidget
from utils.translator import tr


class CharacterHeader(QWidget):
    """Tab for character biography and affiliations."""

    dataChanged = pyqtSignal()
    imageChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.image_data = ""
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Initialize the tab UI."""

        layout = QHBoxLayout(self)

        # Image
        self.image_widget = ImageDropWidget()
        layout.addWidget(self.image_widget)

        # Basic info
        info_layout = QFormLayout()

        self.name_edit = QLineEdit()
        info_layout.addRow("Name:", self.name_edit)

        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 100)
        info_layout.addRow("Level:", self.level_spin)

        layout.addLayout(info_layout, 1)

        self.retranslate_ui()

    def connect_signals(self):
        self.image_widget.imageChanged.connect(self.on_image_changed)
        self.name_edit.textChanged.connect(self.on_data_changed)
        self.level_spin.valueChanged.connect(self.on_data_changed)

    def disconnect_signals(self):
        self.image_widget.imageChanged.disconnect(self.on_image_changed)
        self.name_edit.textChanged.disconnect(self.on_data_changed)
        self.level_spin.valueChanged.disconnect(self.on_data_changed)


    def retranslate_ui(self):
        """Update UI text for current language."""
        pass

    def load_character(self, character: Character):
        """Load character data."""
        self.current_character = character
        print(character.level)

        # Block signals during loading
        self.blockSignals(True)
        self.name_edit.blockSignals(True)
        self.level_spin.blockSignals(True)
        self.image_widget.blockSignals(True)

        # Basic info
        self.name_edit.setText(character.name)
        self.level_spin.setValue(character.level)
        print(character.level)

        # Image
        if character.image_data:
            self.image_widget.set_image_from_base64(character.image_data)

        # Re-enable signals
        self.blockSignals(False)
        self.name_edit.blockSignals(False)
        self.level_spin.blockSignals(False)
        self.image_widget.blockSignals(False)

    def save_to_character(self, character: Character):
        """Save data to character."""
        if not character:
            return

        character.name = self.name_edit.text()
        character.level = self.level_spin.value()

        if self.current_character:
            character.image_data = self.current_character.image_data

    def clear(self):
        """Clear the tab."""
        self.current_character = None
        self.name_edit.clear()
        self.level_spin.clear()
        self.image_widget.clear()

    def on_image_changed(self, image_data: str):
        """Handle image change."""
        if self.current_character:
            self.current_character.image_data = image_data

    def on_data_changed(self):
        """Handle data changes."""
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()
