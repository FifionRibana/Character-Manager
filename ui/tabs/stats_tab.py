"""
Character statistics configuration tab.
Manages RPG ability scores.
"""

from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QGroupBox,
    QSpinBox, QLabel, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from models.character import Character
from models.enums import StatType
from utils.translator import tr


class StatsTab(QWidget):
    """
    Tab for configuring character ability scores.
    """
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.stat_spinners: Dict[StatType, QSpinBox] = {}
        self.stat_modifiers: Dict[StatType, QLabel] = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Main stats group
        self.stats_group = QGroupBox()
        stats_layout = QGridLayout(self.stats_group)
        stats_layout.setSpacing(15)
        
        # Define stat configuration
        stat_configs = [
            (StatType.STRENGTH, 0, 0),
            (StatType.AGILITY, 0, 1),
            (StatType.CONSTITUTION, 0, 2),
            (StatType.INTELLIGENCE, 1, 0),
            (StatType.WISDOM, 1, 1),
            (StatType.CHARISMA, 1, 2),
        ]
        
        # Create stat controls
        for stat_type, row, col in stat_configs:
            # Create container for each stat
            stat_widget = QWidget()
            stat_layout = QVBoxLayout(stat_widget)
            stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Stat name label
            name_label = QLabel()
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setBold(True)
            name_label.setFont(font)
            name_label.setObjectName(f"stat_label_{stat_type.value}")
            stat_layout.addWidget(name_label)
            
            # Spinner container
            spinner_container = QHBoxLayout()
            spinner_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Stat value spinner
            spinner = QSpinBox()
            spinner.setRange(1, 20)
            spinner.setValue(10)
            spinner.setMinimumWidth(60)
            spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spinner.valueChanged.connect(self.on_stat_changed)
            self.stat_spinners[stat_type] = spinner
            spinner_container.addWidget(spinner)
            
            # Modifier label (D&D style)
            modifier_label = QLabel("(+0)")
            modifier_label.setMinimumWidth(40)
            modifier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stat_modifiers[stat_type] = modifier_label
            spinner_container.addWidget(modifier_label)
            
            stat_layout.addLayout(spinner_container)
            
            # Add to grid
            stats_layout.addWidget(stat_widget, row, col)
        
        layout.addWidget(self.stats_group)
        
        # Stats summary group
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout(summary_group)
        
        # Total points
        self.total_points_label = QLabel("Total Points: 60 / 60")
        self.total_points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.total_points_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        summary_layout.addWidget(separator)
        
        # Point buy info
        info_label = QLabel(
            "Standard array: 15, 14, 13, 12, 10, 8\n"
            "Point buy range: 8-15 (27 points)\n"
            "Heroic: All stats start at 10"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        summary_layout.addWidget(info_label)
        
        layout.addWidget(summary_group)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        # Apply initial translations
        self.retranslate_ui()
        
    def retranslate_ui(self):
        """Update UI text for current language."""
        self.stats_group.setTitle(tr("ability_scores"))
        
        # Update stat labels
        for stat_type in StatType:
            label = self.findChild(QLabel, f"stat_label_{stat_type.value}")
            if label:
                label.setText(tr(stat_type.value))
        
        # Update total points
        self.update_total_points()
        
    def load_character(self, character: Character):
        """
        Load character data into the tab.
        
        Args:
            character: Character to load
        """
        self.current_character = character

        # Block signals during loading
        self.blockSignals(True)
        
        # Block signals during loading
        for spinner in self.stat_spinners.values():
            spinner.blockSignals(True)
        
        # Load stat values
        for stat_type, spinner in self.stat_spinners.items():
            value = getattr(character.stats, stat_type.value)
            spinner.setValue(value)
            self.update_modifier(stat_type, value)
        
        # Re-enable signals
        for spinner in self.stat_spinners.values():
            spinner.blockSignals(False)
        
        # Re-enable signals
        self.blockSignals(False)
        
        # Update summary
        self.update_total_points()
        
    def save_to_character(self, character: Character):
        """
        Save tab data to character.
        
        Args:
            character: Character to update
        """
        if not character:
            return
        
        # Save all stat values
        for stat_type, spinner in self.stat_spinners.items():
            setattr(character.stats, stat_type.value, spinner.value())
    
    def clear(self):
        """Clear all data from the tab."""
        self.current_character = None
        
        # Reset all spinners to 10
        for spinner in self.stat_spinners.values():
            spinner.blockSignals(True)
            spinner.setValue(10)
            spinner.blockSignals(False)
        
        # Reset modifiers
        for stat_type in self.stat_modifiers:
            self.update_modifier(stat_type, 10)
        
        self.update_total_points()
    
    def on_stat_changed(self):
        """Handle stat value change."""
        # Update modifier for changed stat
        sender = self.sender()
        for stat_type, spinner in self.stat_spinners.items():
            if spinner == sender:
                self.update_modifier(stat_type, spinner.value())
                break
        
        # Update total
        self.update_total_points()
        
        # Emit change signal
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()
    
    def update_modifier(self, stat_type: StatType, value: int):
        """
        Update the modifier label for a stat (D&D 5e style).
        
        Args:
            stat_type: The stat type
            value: The stat value
        """
        # Calculate D&D 5e modifier
        modifier = (value - 10) // 2
        
        # Format with + or - sign
        if modifier >= 0:
            modifier_text = f"(+{modifier})"
        else:
            modifier_text = f"({modifier})"
        
        # Update label
        if stat_type in self.stat_modifiers:
            self.stat_modifiers[stat_type].setText(modifier_text)
            
            # Color code based on modifier
            if modifier > 0:
                self.stat_modifiers[stat_type].setStyleSheet("color: green;")
            elif modifier < 0:
                self.stat_modifiers[stat_type].setStyleSheet("color: red;")
            else:
                self.stat_modifiers[stat_type].setStyleSheet("")
    
    def update_total_points(self):
        """Update the total points display."""
        total = sum(spinner.value() for spinner in self.stat_spinners.values())
        
        # Standard point buy total is 27 points for values 8-15
        # But we're using a simpler system where 10 is baseline
        baseline = 60  # 6 stats * 10 each
        
        self.total_points_label.setText(f"Total Points: {total} / {baseline}")
        
        # Color code based on total
        if total > baseline:
            self.total_points_label.setStyleSheet("color: blue; font-weight: bold;")
        elif total < baseline:
            self.total_points_label.setStyleSheet("color: orange;")
        else:
            self.total_points_label.setStyleSheet("color: green;")
    
    def apply_standard_array(self):
        """Apply D&D 5e standard array (15, 14, 13, 12, 10, 8)."""
        standard_array = [15, 14, 13, 12, 10, 8]
        
        for i, (stat_type, spinner) in enumerate(self.stat_spinners.items()):
            if i < len(standard_array):
                spinner.setValue(standard_array[i])
        
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()
    
    def randomize_stats(self):
        """Roll random stats (4d6 drop lowest method)."""
        import random
        
        for spinner in self.stat_spinners.values():
            # Roll 4d6, drop lowest
            rolls = sorted([random.randint(1, 6) for _ in range(4)])
            value = sum(rolls[1:])  # Sum the highest 3
            spinner.setValue(value)
        
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()