"""
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

        # Block signals during loading
        self.blockSignals(True)
        
        self.timeline_list.clear()
        for event in sorted(character.narrative_events, key=lambda e: e.timestamp):
            text = f"{event.timestamp.strftime('%Y-%m-%d')} - {event.title}"
            if event.chapter:
                text = f"[{event.chapter}] {text}"
            self.timeline_list.addItem(text)
            
        # Re-enable signals
        self.blockSignals(False)
            
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
