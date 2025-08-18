"""
Enhanced Enneagram tab with affinity sliders for each type.
"""

from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QGroupBox,
    QComboBox, QSlider, QLabel, QFormLayout, QTextBrowser,
    QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from models.character import Character
from models.enums import EnneagramType, InstinctualVariant
from ui.widgets.enneagram_wheel import EnneagramWheel
from ui.widgets.affinity_radar import AffinityRadarWidget
from utils.translator import tr


class EnneagramTabEnhanced(QWidget):
    """Enhanced Enneagram tab with affinity controls."""
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_character: Optional[Character] = None
        self.affinity_sliders: Dict[EnneagramType, QSlider] = {}
        self.affinity_labels: Dict[EnneagramType, QLabel] = {}
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Initialize the tab UI."""
        layout = QVBoxLayout(self)
        
        # Create horizontal splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Wheel and basic controls
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Middle panel - Affinity controls
        middle_panel = self.create_affinity_panel()
        main_splitter.addWidget(middle_panel)
        
        # Right panel - Radar and descriptions
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (33/33/33)
        main_splitter.setSizes([300, 300, 300])
        
        layout.addWidget(main_splitter)
        
    def create_left_panel(self) -> QWidget:
        """Create left panel with wheel and main controls."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Enneagram wheel
        self.enneagram_wheel = EnneagramWheel()
        layout.addWidget(self.enneagram_wheel)
        
        # Type configuration
        config_group = QGroupBox("Type Configuration")
        config_layout = QFormLayout(config_group)
        
        # Main type
        self.main_type_combo = QComboBox()
        for etype in EnneagramType:
            self.main_type_combo.addItem(f"Type {etype.value}", etype)
        config_layout.addRow("Main Type", self.main_type_combo)
        
        # Wing
        self.wing_combo = QComboBox()
        config_layout.addRow("Wing", self.wing_combo)
        
        # Development level
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
        
        config_layout.addRow("Development", dev_widget)
        
        layout.addWidget(config_group)
        
        # Instinctual variants
        instinct_group = QGroupBox("Instinctual Stack")
        instinct_layout = QVBoxLayout(instinct_group)
        
        self.instinct_combos = []
        for i in range(3):
            combo = QComboBox()
            for variant in InstinctualVariant:
                combo.addItem(variant.value.upper(), variant)
            self.instinct_combos.append(combo)
            
            label_text = ["Primary", "Secondary", "Tertiary"][i]
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label_text}:"))
            row.addWidget(combo)
            instinct_layout.addLayout(row)
        
        layout.addWidget(instinct_group)
        
        return widget
    
    def create_affinity_panel(self) -> QWidget:
        """Create middle panel with affinity sliders for each type."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Affinity controls group
        affinity_group = QGroupBox("Type Affinities")
        affinity_layout = QVBoxLayout(affinity_group)
        
        # Scroll area for sliders
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        sliders_widget = QWidget()
        sliders_layout = QVBoxLayout(sliders_widget)
        
        # Create slider for each type
        for etype in EnneagramType:
            # Container for each affinity control
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Type label
            type_label = QLabel(f"Type {etype.value}:")
            type_label.setMinimumWidth(60)
            container_layout.addWidget(type_label)
            
            # Slider
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(25)
            self.affinity_sliders[etype] = slider
            container_layout.addWidget(slider)
            
            # Value label
            value_label = QLabel("50%")
            value_label.setMinimumWidth(40)
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.affinity_labels[etype] = value_label
            container_layout.addWidget(value_label)
            
            sliders_layout.addWidget(container)
            
            # Connect slider to update label and data
            slider.valueChanged.connect(
                lambda v, t=etype: self.on_affinity_changed(t, v)
            )
        
        sliders_layout.addStretch()
        scroll.setWidget(sliders_widget)
        affinity_layout.addWidget(scroll)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        reset_btn = QLabel("<a href='#'>Reset All</a>")
        reset_btn.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        reset_btn.linkActivated.connect(self.reset_affinities)
        actions_layout.addWidget(reset_btn)
        
        actions_layout.addStretch()
        
        high_btn = QLabel("<a href='#'>Set High</a>")
        high_btn.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        high_btn.linkActivated.connect(lambda: self.set_all_affinities(75))
        actions_layout.addWidget(high_btn)
        
        low_btn = QLabel("<a href='#'>Set Low</a>")
        low_btn.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        low_btn.linkActivated.connect(lambda: self.set_all_affinities(25))
        actions_layout.addWidget(low_btn)
        
        affinity_layout.addLayout(actions_layout)
        
        layout.addWidget(affinity_group)
        
        return widget
    
    def create_right_panel(self) -> QWidget:
        """Create right panel with radar and descriptions."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Affinity radar
        self.affinity_radar = AffinityRadarWidget()
        layout.addWidget(self.affinity_radar)
        
        # Type description
        desc_group = QGroupBox("Type Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.type_description = QTextBrowser()
        self.type_description.setMaximumHeight(200)
        desc_layout.addWidget(self.type_description)
        
        layout.addWidget(desc_group)
        
        # Dynamics
        dynamics_group = QGroupBox("Dynamics")
        dynamics_layout = QFormLayout(dynamics_group)
        
        self.integration_label = QLabel("-")
        dynamics_layout.addRow("Integration:", self.integration_label)
        
        self.disintegration_label = QLabel("-")
        dynamics_layout.addRow("Disintegration:", self.disintegration_label)
        
        self.tritype_label = QLabel("-")
        dynamics_layout.addRow("Tritype:", self.tritype_label)
        
        layout.addWidget(dynamics_group)
        
        return widget
    
    def connect_signals(self):
        """Connect widget signals."""
        self.enneagram_wheel.typeSelected.connect(self.on_wheel_type_selected)
        self.main_type_combo.currentIndexChanged.connect(self.on_main_type_changed)
        self.wing_combo.currentIndexChanged.connect(self.on_data_changed)
        self.development_slider.valueChanged.connect(self.on_development_changed)
        
        for combo in self.instinct_combos:
            combo.currentIndexChanged.connect(self.on_instinct_changed)
    
    def retranslate_ui(self):
        """Update UI text for current language."""
        # Update type names in combo
        for i in range(self.main_type_combo.count()):
            etype = self.main_type_combo.itemData(i)
            if etype:
                type_name = tr(f"type_{etype.value}_name")
                self.main_type_combo.setItemText(i, f"Type {etype.value}: {type_name}")
        
        if self.current_character:
            self.update_type_description()
    
    def load_character(self, character: Character):
        """Load character data."""
        self.current_character = character
        
        # Block signals
        self.blockSignals(True)
        self.enneagram_wheel.blockSignals(True)
        self.main_type_combo.blockSignals(True)
        self.wing_combo.blockSignals(True)
        self.development_slider.blockSignals(True)
        
        for combo in self.instinct_combos:
            combo.blockSignals(True)
        
        # Main type
        for i in range(self.main_type_combo.count()):
            if self.main_type_combo.itemData(i) == character.enneagram.main_type:
                self.main_type_combo.setCurrentIndex(i)
                break
        
        # Wing
        self.update_wing_options()
        if character.enneagram.wing:
            for i in range(self.wing_combo.count()):
                if self.wing_combo.itemData(i) == character.enneagram.wing:
                    self.wing_combo.setCurrentIndex(i)
                    break
        
        # Development level
        self.development_slider.setValue(character.enneagram.development_level)
        
        # Instinctual stack
        for i, variant in enumerate(character.enneagram.instinctual_stack[:3]):
            for j in range(self.instinct_combos[i].count()):
                if self.instinct_combos[i].itemData(j) == variant:
                    self.instinct_combos[i].setCurrentIndex(j)
                    break
        
        # Load affinities
        for etype, slider in self.affinity_sliders.items():
            value = int(character.enneagram.type_affinities.get(etype, 0.5) * 100)
            slider.setValue(value)
            self.affinity_labels[etype].setText(f"{value}%")
        
        # Update visualizations
        self.enneagram_wheel.highlight_type(character.enneagram.main_type)
        self.affinity_radar.set_affinities(character.enneagram.type_affinities)
        
        # Update descriptions
        self.update_type_description()
        self.update_dynamics_labels()
        
        # Re-enable signals
        self.blockSignals(False)
        self.enneagram_wheel.blockSignals(False)
        self.main_type_combo.blockSignals(False)
        self.wing_combo.blockSignals(False)
        self.development_slider.blockSignals(False)
        
        for combo in self.instinct_combos:
            combo.blockSignals(False)
    
    def save_to_character(self, character: Character):
        """Save data to character."""
        if not character:
            return
        
        character.enneagram.main_type = self.main_type_combo.currentData()
        character.enneagram.wing = self.wing_combo.currentData()
        character.enneagram.development_level = self.development_slider.value()
        
        character.enneagram.instinctual_stack = [
            self.instinct_combos[i].currentData()
            for i in range(3)
        ]
        
        # Save affinities
        for etype, slider in self.affinity_sliders.items():
            character.enneagram.type_affinities[etype] = slider.value() / 100.0
        
        character.enneagram.integration_point = character.enneagram.get_integration_point()
        character.enneagram.disintegration_point = character.enneagram.get_disintegration_point()
    
    def clear(self):
        """Clear the tab."""
        self.current_character = None
        self.main_type_combo.setCurrentIndex(8)
        self.wing_combo.setCurrentIndex(0)
        self.development_slider.setValue(5)
        self.reset_affinities()
    
    def on_wheel_type_selected(self, etype: EnneagramType):
        """Handle type selection from wheel."""
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
        """Handle development level change."""
        self.development_label.setText(str(value))
        self.on_data_changed()
    
    def on_instinct_changed(self):
        """Handle instinctual variant change."""
        # Ensure no duplicates
        selected = []
        for combo in self.instinct_combos:
            variant = combo.currentData()
            if variant and variant not in selected:
                selected.append(variant)
        
        if len(selected) < 3:
            all_variants = list(InstinctualVariant)
            for variant in all_variants:
                if variant not in selected:
                    selected.append(variant)
            
            for i, variant in enumerate(selected[:3]):
                self.instinct_combos[i].blockSignals(True)
                for j in range(self.instinct_combos[i].count()):
                    if self.instinct_combos[i].itemData(j) == variant:
                        self.instinct_combos[i].setCurrentIndex(j)
                        break
                self.instinct_combos[i].blockSignals(False)
        
        self.on_data_changed()
    
    def on_affinity_changed(self, etype: EnneagramType, value: int):
        """Handle affinity slider change."""
        self.affinity_labels[etype].setText(f"{value}%")
        
        # Update radar chart
        if self.current_character:
            self.current_character.enneagram.type_affinities[etype] = value / 100.0
            self.affinity_radar.set_affinities(self.current_character.enneagram.type_affinities)
        
        self.on_data_changed()
    
    def reset_affinities(self):
        """Reset all affinities to 50%."""
        for slider in self.affinity_sliders.values():
            slider.setValue(50)
    
    def set_all_affinities(self, value: int):
        """Set all affinities to a specific value."""
        for slider in self.affinity_sliders.values():
            slider.setValue(value)
    
    def update_wing_options(self):
        """Update available wing options."""
        self.wing_combo.clear()
        self.wing_combo.addItem("No Wing", None)
        
        etype = self.main_type_combo.currentData()
        if not etype:
            return
        
        if self.current_character:
            self.current_character.enneagram.main_type = etype
            valid_wings = self.current_character.enneagram.get_valid_wings()
        else:
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
        """Update type description display."""
        etype = self.main_type_combo.currentData()
        if not etype:
            return
        
        type_name = tr(f"type_{etype.value}_name")
        type_desc = tr(f"type_{etype.value}_desc")
        
        wing = self.wing_combo.currentData()
        wing_text = f"{etype.value}w{wing.value}" if wing else str(etype.value)
        
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
        
        self.integration_label.setText(f"Type {integration.value}")
        self.disintegration_label.setText(f"Type {disintegration.value}")
        
        designation = self.current_character.enneagram.get_tritype_designation()
        if designation:
            wing_notation = self.current_character.enneagram.get_wing_notation()
            self.tritype_label.setText(f"{wing_notation} - {designation}")
        else:
            self.tritype_label.setText(self.current_character.enneagram.get_wing_notation())
    
    def on_data_changed(self):
        """Handle any data change."""
        if self.current_character:
            self.save_to_character(self.current_character)
            self.dataChanged.emit()