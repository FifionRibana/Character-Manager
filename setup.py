#!/usr/bin/env python3
"""
Setup script to initialize the Medieval Character Manager project structure.
Creates all necessary directories and __init__.py files.
"""

import os
from pathlib import Path


def create_project_structure():
    """Create the complete project directory structure."""
    
    # Define project structure
    directories = [
        "data/characters",
        "config",
        "models",
        "ui/widgets",
        "ui/tabs",
        "ui/dialogs",
        "utils",
        "translations",
        "tests",
        "docs"
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create __init__.py files for Python packages
    packages = [
        "models",
        "ui",
        "ui/widgets",
        "ui/tabs", 
        "ui/dialogs",
        "utils",
        "translations"
    ]
    
    for package in packages:
        init_file = Path(package) / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Package initialization."""\n')
            print(f"✓ Created {init_file}")
    
    # Create placeholder files for missing tabs
    tab_files = {
        "ui/tabs/biography_tab.py": create_biography_tab_code(),
        "ui/tabs/relationships_tab.py": create_relationships_tab_code(),
        "ui/tabs/narrative_tab.py": create_narrative_tab_code(),
        "ui/widgets/image_drop.py": create_image_drop_code(),
        "ui/dialogs/relationship_dialog.py": create_relationship_dialog_code(),
        "config/settings.py": create_settings_code(),
        "translations/en.json": create_english_translations()
    }
    
    for filepath, content in tab_files.items():
        file_path = Path(filepath)
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            print(f"✓ Created {filepath}")
    
    print("\n✅ Project structure setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python main.py")


def create_biography_tab_code():
    """Generate biography tab code."""
    return '''"""
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
        self.biography_edit.setPlainText(character.biography)
        
        self.affiliations_list.clear()
        for affiliation in character.affiliations:
            self.affiliations_list.addItem(affiliation)
            
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
'''


def create_relationships_tab_code():
    """Generate relationships tab code."""
    return '''"""
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
        
        self.table.setRowCount(len(character.relationships))
        for i, rel in enumerate(character.relationships):
            self.table.setItem(i, 0, QTableWidgetItem(rel.target_name))
            self.table.setItem(i, 1, QTableWidgetItem(rel.relationship_type.value))
            self.table.setItem(i, 2, QTableWidgetItem(rel.description))
            
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
'''


def create_narrative_tab_code():
    """Generate narrative tab code."""
    return '''"""
Narrative timeline and events management tab.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QGroupBox,
    QLineEdit, QTextEdit, QPushButton, QFormLayout
)
from PyQt6.QtCore import pyqtSignal

from models.character import Character, NarrativeEvent
from utils.translator import tr


class NarrativeTab(QWidget):
    """Tab for managing character narrative timeline."""
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        
        # Timeline list
        self.timeline_list = QListWidget()
        layout.addWidget(self.timeline_list)
        
        # Add event group
        event_group = QGroupBox()
        event_layout = QFormLayout(event_group)
        
        self.title_edit = QLineEdit()
        event_layout.addRow(tr("event_title"), self.title_edit)
        
        self.chapter_edit = QLineEdit()
        event_layout.addRow(tr("chapter"), self.chapter_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        event_layout.addRow(tr("event_description"), self.description_edit)
        
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.add_event)
        event_layout.addRow(self.add_button)
        
        layout.addWidget(event_group)
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.add_button.setText(tr("add_event"))
        
    def load_character(self, character: Character):
        """Load character data."""
        self.current_character = character
        
        self.timeline_list.clear()
        for event in sorted(character.narrative_events, key=lambda e: e.timestamp):
            text = f"{event.timestamp.strftime('%Y-%m-%d')} - {event.title}"
            if event.chapter:
                text = f"[{event.chapter}] {text}"
            self.timeline_list.addItem(text)
            
    def save_to_character(self, character: Character):
        """Save data to character."""
        # Events are saved immediately when added
        pass
        
    def clear(self):
        """Clear the tab."""
        self.current_character = None
        self.timeline_list.clear()
        self.title_edit.clear()
        self.chapter_edit.clear()
        self.description_edit.clear()
        
    def add_event(self):
        """Add new narrative event."""
        if self.current_character and self.title_edit.text():
            self.current_character.add_narrative_event(
                self.title_edit.text(),
                self.description_edit.toPlainText(),
                self.chapter_edit.text() or None
            )
            self.load_character(self.current_character)
            self.title_edit.clear()
            self.chapter_edit.clear()
            self.description_edit.clear()
            self.dataChanged.emit()
'''


def create_image_drop_code():
    """Generate image drop widget code."""
    return '''"""
Drag and drop image widget for character portraits.
"""

import base64
from pathlib import Path
from PyQt6.QtWidgets import QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent

from utils.translator import tr


class ImageDropWidget(QLabel):
    """Widget for drag and drop image upload."""
    
    imageChanged = pyqtSignal(str)  # Emits base64 encoded image
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 200)
        self.setScaledContents(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
        """)
        self.setText(tr("drop_image"))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def mousePressEvent(self, event):
        """Open file dialog on click."""
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self, tr("select_image"), "", tr("images_filter")
            )
            if file_path:
                self.load_image(file_path)
                
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept image drag events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle dropped images."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_image(file_path)
            
    def load_image(self, file_path: str):
        """Load and display image."""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
            
            with open(file_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
                self.imageChanged.emit(image_data)
                
    def set_image_from_base64(self, data: str):
        """Load image from base64 data."""
        if data:
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(data))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.setPixmap(scaled)
'''


def create_relationship_dialog_code():
    """Generate relationship dialog code."""
    return '''"""
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
'''


def create_settings_code():
    """Generate settings configuration code."""
    return '''"""
Application settings and configuration.
"""

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class AppSettings:
    """Application settings."""
    language: str = "en"
    theme: str = "auto"
    autosave_interval: int = 30000  # milliseconds
    last_open_directory: str = ""
    window_geometry: str = ""
    
    def save(self, path: Path):
        """Save settings to file."""
        with open(path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
            
    @classmethod
    def load(cls, path: Path) -> 'AppSettings':
        """Load settings from file."""
        if path.exists():
            with open(path, 'r') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
'''


def create_english_translations():
    """Generate English translations JSON."""
    # This is already created in the main artifacts, returning empty
    return ""


if __name__ == "__main__":
    print("Medieval Character Manager - Project Setup")
    print("=" * 50)
    create_project_structure()