"""
Character overview tab - read-only summary view.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QGridLayout, QScrollArea, QFrame, QPushButton, QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from models.character import Character
from models.enums import StatType
from utils.translator import tr


class OverviewTab(QWidget):
    """Read-only overview of character information."""
    
    editModeRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the overview UI."""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Edit mode button
        self.edit_button = QPushButton("Enter Edit Mode")
        self.edit_button.clicked.connect(self.editModeRequested.emit)
        layout.addWidget(self.edit_button)
        
        # Character portrait and basic info
        header_group = QGroupBox("Character")
        header_layout = QHBoxLayout(header_group)
        
        self.portrait_label = QLabel()
        self.portrait_label.setMinimumSize(150, 150)
        self.portrait_label.setMaximumSize(150, 150)
        self.portrait_label.setScaledContents(True)
        self.portrait_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
        """)
        header_layout.addWidget(self.portrait_label)
        
        info_layout = QVBoxLayout()
        
        self.name_label = QLabel()
        name_font = QFont()
        name_font.setPointSize(18)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        info_layout.addWidget(self.name_label)
        
        self.level_label = QLabel()
        info_layout.addWidget(self.level_label)
        
        info_layout.addStretch()
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_group)
        
        # Stats summary
        stats_group = QGroupBox("Ability Scores")
        stats_layout = QGridLayout(stats_group)
        
        self.stat_labels = {}
        stat_positions = [
            (StatType.STRENGTH, 0, 0),
            (StatType.AGILITY, 0, 1),
            (StatType.CONSTITUTION, 0, 2),
            (StatType.INTELLIGENCE, 1, 0),
            (StatType.WISDOM, 1, 1),
            (StatType.CHARISMA, 1, 2),
        ]
        
        for stat_type, row, col in stat_positions:
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            name = QLabel(tr(stat_type.value))
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(name)
            
            value_label = QLabel("10")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_font = QFont()
            value_font.setPointSize(16)
            value_font.setBold(True)
            value_label.setFont(value_font)
            self.stat_labels[stat_type] = value_label
            container_layout.addWidget(value_label)
            
            modifier = QLabel("(+0)")
            modifier.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stat_labels[f"{stat_type}_mod"] = modifier
            container_layout.addWidget(modifier)
            
            stats_layout.addWidget(container, row, col)
        
        layout.addWidget(stats_group)
        
        # Enneagram summary
        enn_group = QGroupBox("Enneagram Profile")
        enn_layout = QVBoxLayout(enn_group)
        
        self.enneagram_summary = QLabel()
        enn_layout.addWidget(self.enneagram_summary)
        
        layout.addWidget(enn_group)
        
        # Biography summary
        bio_group = QGroupBox("Biography")
        bio_layout = QVBoxLayout(bio_group)
        
        self.biography_browser = QTextBrowser()
        self.biography_browser.setMaximumHeight(150)
        bio_layout.addWidget(self.biography_browser)
        
        layout.addWidget(bio_group)
        
        # Affiliations
        self.affiliations_group = QGroupBox("Affiliations")
        self.affiliations_layout = QHBoxLayout(self.affiliations_group)
        layout.addWidget(self.affiliations_group)
        
        # Relationships summary
        rel_group = QGroupBox("Relationships")
        rel_layout = QVBoxLayout(rel_group)
        
        self.relationships_summary = QLabel("No relationships")
        rel_layout.addWidget(self.relationships_summary)
        
        layout.addWidget(rel_group)
        
        # Recent narrative events
        narrative_group = QGroupBox("Recent Events")
        narrative_layout = QVBoxLayout(narrative_group)
        
        self.recent_events = QLabel("No recent events")
        narrative_layout.addWidget(self.recent_events)
        
        layout.addWidget(narrative_group)
        
        layout.addStretch()
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.edit_button.setText(tr("edit_mode", "Enter Edit Mode"))
        
    def load_character(self, character: Character):
        """Load character data for overview."""
        self.current_character = character
        
        # Basic info
        self.name_label.setText(character.name)
        self.level_label.setText(f"Level {character.level}")
        
        # Portrait
        if character.image_data:
            pixmap = character.get_image_pixmap()
            if pixmap:
                self.portrait_label.setPixmap(pixmap)
        else:
            self.portrait_label.setText("No Image")
            self.portrait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Stats
        for stat_type, label in self.stat_labels.items():
            if isinstance(stat_type, StatType):
                value = getattr(character.stats, stat_type.value)
                label.setText(str(value))
                
                # Modifier
                mod = (value - 10) // 2
                mod_label = self.stat_labels.get(f"{stat_type}_mod")
                if mod_label:
                    mod_text = f"(+{mod})" if mod >= 0 else f"({mod})"
                    mod_label.setText(mod_text)
                    if mod > 0:
                        mod_label.setStyleSheet("color: green;")
                    elif mod < 0:
                        mod_label.setStyleSheet("color: red;")
                    else:
                        mod_label.setStyleSheet("")
        
        # Enneagram
        enn_text = f"""
        <b>Type {character.enneagram.main_type.value}</b>: {tr(f'type_{character.enneagram.main_type.value}_name')}<br>
        <b>Wing:</b> {character.enneagram.get_wing_notation()}<br>
        <b>Development Level:</b> {character.enneagram.development_level}/9<br>
        <b>Instinctual Stack:</b> {'/'.join([v.value.upper() for v in character.enneagram.instinctual_stack[:3]])}
        """
        self.enneagram_summary.setText(enn_text)
        
        # Biography
        if character.biography:
            self.biography_browser.setPlainText(character.biography[:500] + "..." if len(character.biography) > 500 else character.biography)
        else:
            self.biography_browser.setPlainText("No biography written.")
        
        # Affiliations
        # Clear existing
        while self.affiliations_layout.count():
            item = self.affiliations_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if character.affiliations:
            for affiliation in character.affiliations[:5]:  # Show first 5
                label = QLabel(affiliation)
                label.setStyleSheet("""
                    QLabel {
                        background-color: #e3f2fd;
                        padding: 5px 10px;
                        border-radius: 15px;
                    }
                """)
                self.affiliations_layout.addWidget(label)
        else:
            self.affiliations_layout.addWidget(QLabel("No affiliations"))
        
        self.affiliations_layout.addStretch()
        
        # Relationships
        if character.relationships:
            rel_text = f"{len(character.relationships)} relationships:\n"
            for rel in character.relationships[:3]:  # Show first 3
                rel_text += f"• {rel.target_name} ({rel.relationship_type.value})\n"
            if len(character.relationships) > 3:
                rel_text += f"... and {len(character.relationships) - 3} more"
            self.relationships_summary.setText(rel_text)
        else:
            self.relationships_summary.setText("No relationships")
        
        # Recent events
        if character.narrative_events:
            sorted_events = sorted(character.narrative_events, key=lambda e: e.timestamp, reverse=True)
            events_text = "Recent events:\n"
            for event in sorted_events[:3]:  # Show 3 most recent
                events_text += f"• {event.timestamp.strftime('%Y-%m-%d')}: {event.title}\n"
            self.recent_events.setText(events_text)
        else:
            self.recent_events.setText("No recent events")
    
    def save_to_character(self, character: Character):
        """Overview tab is read-only, nothing to save."""
        pass
    
    def clear(self):
        """Clear the overview."""
        self.name_label.setText("")
        self.level_label.setText("")
        self.portrait_label.clear()
        self.biography_browser.clear()
        self.enneagram_summary.setText("")
        self.relationships_summary.setText("No relationships")
        self.recent_events.setText("No recent events")