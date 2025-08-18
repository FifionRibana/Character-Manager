"""
Enneagram personality configuration tab.
Provides complete Enneagram type selection and visualization.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QGroupBox,
    QComboBox, QSlider, QLabel, QFormLayout, QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal

from models.character import Character
from models.enums import EnneagramType, InstinctualVariant
from ui.widgets.enneagram_wheel import EnneagramWheel
from ui.widgets.affinity_radar import AffinityRadarWidget
from utils.translator import tr


class EnneagramTab(QWidget):
    """
    Tab for configuring character's Enneagram personality profile.
    """
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        
        # Create horizontal splitter for two-column layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Wheel and controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Radar and descriptions
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (50/50)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter)
        
    def create_left_panel(self) -> QWidget:
        """
        Create left panel with Enneagram wheel and controls.
        
        Returns:
            Left panel widget
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Enneagram wheel
        self.enneagram_wheel = EnneagramWheel()
        layout.addWidget(self.enneagram_wheel)
        
        # Type configuration group
        config_group = QGroupBox()
        config_layout = QFormLayout(config_group)
        
        # Main type selector
        self.main_type_combo = QComboBox()
        for etype in EnneagramType:
            type_name = tr(f"type_{etype.value}_name")
            self.main_type_combo.addItem(f"Type {etype.value}: {type_name}", etype)
        config_layout.addRow(tr("main_type"), self.main_type_combo)
        
        # Wing selector
        self.wing_combo = QComboBox()
        config_layout.addRow(tr("wing"), self.wing_combo)
        
        # Development level slider
        dev_widget = QWidget()
        dev_layout = QHBoxLayout(dev_widget)
        dev_layout.setContentsMargins(0, 0, 0, 0)
        
        self.development_slider = QSlider(Qt.Orientation.Horizontal)
        self.development_slider.setRange(1, 9)
        self.development_slider.setValue(5)
        self.development_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.development_slider.setTickInterval(1)
        dev_layout.addWidget(self.development_slider)
        
        self.development_label = QLabel("5")
        self.development_label.setMinimumWidth(20)
        dev_layout.addWidget(self.development_label)
        
        config_layout.addRow(tr("development_level"), dev_widget)
        
        layout.addWidget(config_group)
        
        # Instinctual variants group
        instinct_group = QGroupBox(tr("instinctual_stack"))
        instinct_layout = QVBoxLayout(instinct_group)
        
        # Three combo boxes for instinctual stacking
        self.instinct_combos = []
        for i in range(3):
            combo = QComboBox()
            for variant in InstinctualVariant:
                combo.addItem(variant.value.upper(), variant)
            self.instinct_combos.append(combo)
            
            label = QLabel(f"{i + 1}.")
            row = QHBoxLayout()
            row.addWidget(label)
            row.addWidget(combo)
            instinct_layout.addLayout(row)
        
        # Set default stack
        self.instinct_combos[0].setCurrentText("SP")
        self.instinct_combos[1].setCurrentText("SO")
        self.instinct_combos[2].setCurrentText("SX")
        
        layout.addWidget(instinct_group)
        
        return widget
    
    def create_right_panel(self) -> QWidget:
        """
        Create right panel with affinity radar and descriptions.
        
        Returns:
            Right panel widget
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Affinity radar
        self.affinity_radar = AffinityRadarWidget()
        layout.addWidget(self.affinity_radar)
        
        # Type description browser
        desc_group = QGroupBox(tr("type_description"))
        desc_layout = QVBoxLayout(desc_group)
        
        self.type_description = QTextBrowser()
        self.type_description.setMaximumHeight(250)
        self.type_description.setOpenExternalLinks(False)
        desc_layout.addWidget(self.type_description)
        
        layout.addWidget(desc_group)
        
        # Integration/Disintegration info
        dynamics_group = QGroupBox("Dynamics")
        dynamics_layout = QFormLayout(dynamics_group)
        
        self.integration_label = QLabel("-")
        dynamics_layout.addRow(tr("integration"), self.integration_label)
        
        self.disintegration_label = QLabel("-")
        dynamics_layout.addRow(tr("disintegration"), self.disintegration_label)
        
        self.tritype_label = QLabel("-")
        dynamics_layout.addRow(tr("tritype"), self.tritype_label)
        
        layout.addWidget(dynamics_group)
        
        return widget
    
    def connect_signals(self):
        """Connect widget signals to handlers."""
        # Enneagram wheel
        self.enneagram_wheel.typeSelected.connect(self.on_wheel_type_selected)
        
        # Combo boxes
        self.main_type_combo.currentIndexChanged.connect(self.on_main_type_changed)
        self.wing_combo.currentIndexChanged.connect(self.on_data_changed)
        
        # Sliders
        self.development_slider.valueChanged.connect(self.on_development_changed)
        
        # Instinctual variants
        for combo in self.instinct_combos:
            combo.currentIndexChanged.connect(self.on_instinct_changed)
    
    def retranslate_ui(self):
        """Update UI text for current language."""
        # Update combo box items
        for i in range(self.main_type_combo.count()):
            etype = self.main_type_combo.itemData(i)
            if etype:
                type_name = tr(f"type_{etype.value}_name")
                self.main_type_combo.setItemText(i, f"Type {etype.value}: {type_name}")
        
        # Update description if character loaded
        if self.current_character:
            self.update_type_description()
    
    def load_character(self, character: Character):
        """
        Load character data into the tab.
        
        Args:
            character: Character to load
        """
        self.current_character = character

        # Block signals during loading
        self.blockSignals(True)
        self.enneagram_wheel.blockSignals(True)
        # Combo boxes
        self.main_type_combo.blockSignals(True)
        self.wing_combo.blockSignals(True)
        # Sliders
        self.development_slider.blockSignals(True)
        
        # Instinctual variants
        for combo in self.instinct_combos:
            combo.currentIndexChanged.connect(self.on_instinct_changed)
    
        
        # Set main type
        for i in range(self.main_type_combo.count()):
            if self.main_type_combo.itemData(i) == character.enneagram.main_type:
                self.main_type_combo.setCurrentIndex(i)
                break
        
        # Update wing options and selection
        self.update_wing_options()
        if character.enneagram.wing:
            for i in range(self.wing_combo.count()):
                if self.wing_combo.itemData(i) == character.enneagram.wing:
                    self.wing_combo.setCurrentIndex(i)
                    break
        
        # Set development level
        self.development_slider.setValue(character.enneagram.development_level)
        
        # Set instinctual stack
        for i, variant in enumerate(character.enneagram.instinctual_stack[:3]):
            for j in range(self.instinct_combos[i].count()):
                if self.instinct_combos[i].itemData(j) == variant:
                    self.instinct_combos[i].setCurrentIndex(j)
                    break
        
        # Update visualizations
        self.enneagram_wheel.highlight_type(character.enneagram.main_type)
        self.affinity_radar.set_affinities(character.enneagram.type_affinities)
        
        # Update descriptions
        self.update_type_description()
        self.update_dynamics_labels()
        
        # Re-enable signals
        self.blockSignals(False)
        self.enneagram_wheel.blockSignals(False)
        # Combo boxes
        self.main_type_combo.blockSignals(False)
        self.wing_combo.blockSignals(False)
        # Sliders
        self.development_slider.blockSignals(False)
    
    def save_to_character(self, character: Character):
        """
        Save tab data to character.
        
        Args:
            character: Character to update
        """
        if not character:
            return
        
        # Save main type
        character.enneagram.main_type = self.main_type_combo.currentData()
        
        # Save wing
        character.enneagram.wing = self.wing_combo.currentData()
        
        # Save development level
        character.enneagram.development_level = self.development_slider.value()
        
        # Save instinctual stack
        character.enneagram.instinctual_stack = [
            self.instinct_combos[i].currentData()
            for i in range(3)
        ]
        
        # Update integration/disintegration points
        character.enneagram.integration_point = character.enneagram.get_integration_point()
        character.enneagram.disintegration_point = character.enneagram.get_disintegration_point()
    
    def clear(self):
        """Clear all data from the tab."""
        self.current_character = None
        self.main_type_combo.setCurrentIndex(8)  # Type 9
        self.wing_combo.setCurrentIndex(0)  # No wing
        self.development_slider.setValue(5)
        self.type_description.clear()
        self.integration_label.setText("-")
        self.disintegration_label.setText("-")
        self.tritype_label.setText("-")
    
    def on_wheel_type_selected(self, etype: EnneagramType):
        """
        Handle type selection from wheel.
        
        Args:
            etype: Selected Enneagram type
        """
        for i in range(self.main_type_combo.count()):
            if self.main_type_combo.itemData(i) == etype:
                self.main_type_combo.setCurrentIndex(i)
                break
    
    def on_main_type_changed(self):
        """Handle main type change."""
        etype = self.main_type_combo.currentData()
        if etype:
            self.enneagram_wheel.highlight_type(etype)
            self.update_wing_options()
            self.update_type_description()
            self.update_dynamics_labels()
            self.on_data_changed()
    
    def on_development_changed(self, value: int):
        """
        Handle development level change.
        
        Args:
            value: New development level
        """
        self.development_label.setText(str(value))
        self.on_data_changed()
    
    def on_instinct_changed(self):
        """Handle instinctual variant change."""
        # Ensure no duplicates in stack
        selected = []
        for combo in self.instinct_combos:
            variant = combo.currentData()
            if variant and variant not in selected:
                selected.append(variant)
        
        # If duplicate found, swap with unselected variant
        if len(selected) < 3:
            all_variants = list(InstinctualVariant)
            for variant in all_variants:
                if variant not in selected:
                    selected.append(variant)
            
            # Update combos
            for i, variant in enumerate(selected[:3]):
                self.instinct_combos[i].blockSignals(True)
                for j in range(self.instinct_combos[i].count()):
                    if self.instinct_combos[i].itemData(j) == variant:
                        self.instinct_combos[i].setCurrentIndex(j)
                        break
                self.instinct_combos[i].blockSignals(False)
        
        self.on_data_changed()
    
    def update_wing_options(self):
        """Update available wing options based on main type."""
        self.wing_combo.clear()
        self.wing_combo.addItem(tr("no_wing"), None)
        
        etype = self.main_type_combo.currentData()
        if not etype:
            return
        
        # Get valid wings for current type
        if self.current_character:
            self.current_character.enneagram.main_type = etype
            valid_wings = self.current_character.enneagram.get_valid_wings()
        else:
            # Calculate valid wings manually
            if etype == EnneagramType.TYPE_9:
                valid_wings = [EnneagramType.TYPE_8, EnneagramType.TYPE_1]
            elif etype == EnneagramType.TYPE_1:
                valid_wings = [EnneagramType.TYPE_9, EnneagramType.TYPE_2]
            else:
                valid_wings = [
                    EnneagramType(etype.value - 1),
                    EnneagramType(etype.value + 1)
                ]
        
        for wing_type in valid_wings:
            self.wing_combo.addItem(f"Wing {wing_type.value}", wing_type)
    
    def update_type_description(self):
        """Update the type description display."""
        etype = self.main_type_combo.currentData()
        if not etype:
            return
        
        type_name = tr(f"type_{etype.value}_name")
        type_desc = tr(f"type_{etype.value}_desc")
        
        wing = self.wing_combo.currentData()
        wing_text = f"{etype.value}w{wing.value}" if wing else str(etype.value)
        
        # Get tritype designation if applicable
        designation = ""
        if self.current_character:
            designation = self.current_character.enneagram.get_tritype_designation()
            if designation:
                designation = f" ({designation})"
        
        html = f"""
        <h3>Type {etype.value}: {type_name}</h3>
        <p><b>Wing:</b> {wing_text}{designation}</p>
        <p>{type_desc}</p>
        """
        
        self.type_description.setHtml(html)
    
    def update_dynamics_labels(self):
        """Update integration/disintegration labels."""
        if not self.current_character:
            return
        
        integration = self.current_character.enneagram.get_integration_point()
        disintegration = self.current_character.enneagram.get_disintegration_point()
        
        self.integration_label.setText(
            f"Type {integration.value}: {tr(f'type_{integration.value}_name')}"
        )
        self.disintegration_label.setText(
            f"Type {disintegration.value}: {tr(f'type_{disintegration.value}_name')}"
        )
        
        # Update tritype
        designation = self.current_character.enneagram.get_tritype_designation()
        if designation:
            wing_notation = self.current_character.enneagram.get_wing_notation()
            self.tritype_label.setText(f"{wing_notation} - {designation}")
        else:
            self.tritype_label.setText(self.current_character.enneagram.get_wing_notation())
    
    def on_data_changed(self):
        """Handle any data change in the tab."""
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()