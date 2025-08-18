"""
Updated main window with view/edit modes and overview tab.
"""

import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QToolBar, QStatusBar, QMessageBox, QFileDialog,
    QComboBox, QLabel, QApplication, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QPalette

from models.character import Character
from models.enums import (
    Language, UIConstants, FileConstants, ThemeMode,
    EnneagramType, StorageKeys
)
from utils.translator import get_translator, tr
from utils.storage import StorageManager
from ui.widgets.character_header import CharacterHeader
from ui.widgets.sidebar import CharacterSidebar
from ui.tabs.overview_tab import OverviewTab
from ui.tabs.character_tab import CharacterTab
from ui.tabs.enneagram_tab_enhanced import EnneagramTabEnhanced
from ui.tabs.stats_tab import StatsTab
from ui.tabs.biography_tab import BiographyTab
from ui.tabs.relationships_tab import RelationshipsTab
from ui.tabs.narrative_tab import NarrativeTab
from ui.styles import StyleManager


class MainWindowUpdated(QMainWindow):
    """Main window with view/edit modes."""
    
    characterChanged = pyqtSignal(Character)
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.translator = get_translator()
        self.storage = StorageManager()
        self.style_manager = StyleManager()
        
        # Character management
        self.characters: Dict[str, Character] = {}
        self.current_character: Optional[Character] = None
        
        # Edit mode state
        self.edit_mode = False
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.setup_autosave()
        
        # Apply system theme
        self.apply_theme()
        
        # Load existing characters
        self.load_all_characters()
        
        # Connect translation signal
        self.translator.languageChanged.connect(self.retranslate_ui)
        
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(tr("app_title"))
        self.setMinimumSize(UIConstants.MIN_WINDOW_WIDTH, UIConstants.MIN_WINDOW_HEIGHT)
        
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Create sidebar
        self.sidebar = CharacterSidebar()
        self.sidebar.characterSelected.connect(self.load_character)
        self.sidebar.newCharacterRequested.connect(self.new_character)
        self.sidebar.deleteCharacterRequested.connect(self.delete_character)
        self.splitter.addWidget(self.sidebar)
        
        # Create main content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Mode toggle button
        mode_layout = QHBoxLayout()
        self.mode_button = QPushButton("Switch to Edit Mode")
        self.mode_button.clicked.connect(self.toggle_mode)
        mode_layout.addStretch()
        mode_layout.addWidget(self.mode_button)
        content_layout.addLayout(mode_layout)

        self.mode_action = QAction("View Mode", self)
        self.mode_action.setCheckable(True)
        self.mode_action.toggled.connect(self.toggle_mode_from_toolbar)

        
        # Character header (only in edit mode)
        self.header_layout = CharacterHeader()
        self.header_layout.setVisible(False)  # Hidden by default (view mode)
        content_layout.addWidget(self.header_layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.overview_tab = OverviewTab()
        self.character_tab = CharacterTab()
        self.enneagram_tab = EnneagramTabEnhanced()
        self.stats_tab = StatsTab()
        self.biography_tab = BiographyTab()
        self.relationships_tab = RelationshipsTab(self.characters)
        self.narrative_tab = NarrativeTab()
        
        # Add tabs
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.character_tab, "Character")
        self.tabs.addTab(self.enneagram_tab, "Enneagram")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.biography_tab, "Biography")
        self.tabs.addTab(self.relationships_tab, "Relationships")
        self.tabs.addTab(self.narrative_tab, "Narrative")
        
        # Initially disable edit tabs
        self.set_edit_mode(False)
        
        content_layout.addWidget(self.tabs)
        self.splitter.addWidget(content_widget)
        
        # Set splitter sizes
        self.splitter.setSizes([UIConstants.SIDEBAR_WIDTH, 
                                UIConstants.MIN_WINDOW_WIDTH - UIConstants.SIDEBAR_WIDTH])
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(tr("ready"))
        
        # Apply initial translations
        self.retranslate_ui()
        
    def create_toolbar(self):
        """Create the application toolbar."""
        self.toolbar = self.addToolBar("Main")
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        
        # File actions
        self.new_action = QAction(self)
        self.new_action.triggered.connect(self.new_character)
        self.toolbar.addAction(self.new_action)
        
        self.save_action = QAction(self)
        self.save_action.triggered.connect(self.save_current_character)
        self.save_action.setShortcut("Ctrl+S")
        self.toolbar.addAction(self.save_action)
        
        self.load_action = QAction(self)
        self.load_action.triggered.connect(self.load_character_dialog)
        self.load_action.setShortcut("Ctrl+O")
        self.toolbar.addAction(self.load_action)
        
        self.toolbar.addSeparator()
        
        # Export actions
        self.export_pdf_action = QAction(self)
        self.export_pdf_action.triggered.connect(self.export_to_pdf)
        self.toolbar.addAction(self.export_pdf_action)
        
        self.export_html_action = QAction(self)
        self.export_html_action.triggered.connect(self.export_to_html)
        self.toolbar.addAction(self.export_html_action)
        
        self.toolbar.addSeparator()
        
        # Mode toggle action
        # self.mode_action = QAction("View Mode", self)
        # self.mode_action.setCheckable(True)
        # self.mode_action.toggled.connect(self.toggle_mode_from_toolbar)
        self.toolbar.addAction(self.mode_action)
        
        self.toolbar.addSeparator()
        
        # Add stretch
        spacer = QWidget()
        spacer.setSizePolicy(
            spacer.sizePolicy().horizontalPolicy(),
            spacer.sizePolicy().verticalPolicy()
        )
        self.toolbar.addWidget(spacer)
        
        # Language selector
        self.language_label = QLabel()
        self.toolbar.addWidget(self.language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", Language.ENGLISH)
        self.language_combo.addItem("Français", Language.FRENCH)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        self.language_combo.setMinimumWidth(100)
        self.toolbar.addWidget(self.language_combo)
        
        # Theme selector
        self.theme_label = QLabel()
        self.toolbar.addWidget(self.theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("", ThemeMode.LIGHT)
        self.theme_combo.addItem("", ThemeMode.DARK)
        self.theme_combo.addItem("", ThemeMode.AUTO)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setMinimumWidth(100)
        self.toolbar.addWidget(self.theme_combo)
        
        # Set current theme to AUTO by default
        self.theme_combo.setCurrentIndex(2)
        
    def toggle_mode(self):
        """Toggle between view and edit modes."""
        self.set_edit_mode(not self.edit_mode)
        
    def toggle_mode_from_toolbar(self, checked):
        """Toggle mode from toolbar action."""
        self.set_edit_mode(checked)
        
    def set_edit_mode(self, edit: bool):
        """Set the application mode."""
        self.edit_mode = edit
        
        # Update UI based on mode
        if edit:
            # Edit mode
            self.mode_button.setText("Switch to View Mode")
            self.mode_action.setText("Edit Mode")
            self.mode_action.setChecked(True)
            self.header_layout.setVisible(True)
            
            # Enable all tabs
            for i in range(1, self.tabs.count()):
                self.tabs.setTabEnabled(i, True)
            
            # Switch to character tab
            if self.tabs.currentIndex() == 0:
                self.tabs.setCurrentIndex(1)
            
            self.status_bar.showMessage("Edit Mode", 2000)
            
        else:
            # View mode
            self.mode_button.setText("Switch to Edit Mode")
            self.mode_action.setText("View Mode")
            self.mode_action.setChecked(False)
            self.header_layout.setVisible(False)
            
            # Disable edit tabs (keep overview enabled)
            for i in range(1, self.tabs.count()):
                self.tabs.setTabEnabled(i, False)
            
            # Switch to overview tab
            self.tabs.setCurrentIndex(0)
            
            # Save changes when switching to view mode
            if self.current_character:
                self.on_character_modified()
                self.save_current_character()
            
            # self.status_bar.showMessage("View Mode", 2000)
    
    def setup_connections(self):
        """Connect signals and slots."""
        # Overview tab
        self.overview_tab.editModeRequested.connect(lambda: self.set_edit_mode(True))
        
        # Header signals
        self.header_layout.dataChanged.connect(self.on_character_modified)
        
        # Tab signals
        self.character_tab.dataChanged.connect(self.on_character_modified)
        self.enneagram_tab.dataChanged.connect(self.on_character_modified)
        self.stats_tab.dataChanged.connect(self.on_character_modified)
        self.biography_tab.dataChanged.connect(self.on_character_modified)
        self.relationships_tab.dataChanged.connect(self.on_character_modified)
        self.narrative_tab.dataChanged.connect(self.on_character_modified)
        
    def setup_autosave(self):
        """Setup automatic saving timer."""
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(UIConstants.AUTOSAVE_INTERVAL)
        
    def retranslate_ui(self):
        """Update all UI text when language changes."""
        # Window title
        self.setWindowTitle(tr("app_title"))
        
        # Toolbar actions
        self.new_action.setText(tr("new_character"))
        self.save_action.setText(tr("save"))
        self.load_action.setText(tr("load"))
        self.export_pdf_action.setText(tr("export_pdf"))
        self.export_html_action.setText(tr("export_html"))
        
        # Toolbar labels
        self.language_label.setText(tr("language") + ":")
        self.theme_label.setText(tr("theme") + ":")
        
        # Theme combo items
        self.theme_combo.setItemText(0, tr("light_theme"))
        self.theme_combo.setItemText(1, tr("dark_theme"))
        self.theme_combo.setItemText(2, tr("auto_theme"))
        
        # Tab labels
        self.tabs.setTabText(0, tr("tab_overview", "Overview"))
        self.tabs.setTabText(1, tr("tab_character"))
        self.tabs.setTabText(2, tr("tab_enneagram"))
        self.tabs.setTabText(3, tr("tab_stats"))
        self.tabs.setTabText(4, tr("tab_biography"))
        self.tabs.setTabText(5, tr("tab_relationships"))
        self.tabs.setTabText(6, tr("tab_narrative"))
        
        # Update all components
        self.header_layout.retranslate_ui()
        self.overview_tab.retranslate_ui()
        self.character_tab.retranslate_ui()
        self.enneagram_tab.retranslate_ui()
        self.stats_tab.retranslate_ui()
        self.biography_tab.retranslate_ui()
        self.relationships_tab.retranslate_ui()
        self.narrative_tab.retranslate_ui()
        self.sidebar.retranslate_ui()
        
        # Status bar
        if not self.status_bar.currentMessage() or self.status_bar.currentMessage() in ["Ready", "Prêt"]:
            self.status_bar.showMessage(tr("ready"))
    
    def apply_theme(self, mode: ThemeMode = ThemeMode.AUTO):
        """Apply theme based on mode or system settings."""
        if mode == ThemeMode.AUTO:
            palette = QApplication.palette()
            window_color = palette.color(QPalette.ColorRole.Window)
            is_dark = window_color.lightness() < 128
            actual_mode = ThemeMode.DARK if is_dark else ThemeMode.LIGHT
        else:
            actual_mode = mode
        
        stylesheet = self.style_manager.get_stylesheet(actual_mode)
        self.setStyleSheet(stylesheet)
        
    def change_language(self):
        """Handle language change."""
        language = self.language_combo.currentData()
        self.translator.set_language(language)
        
    def change_theme(self):
        """Handle theme change."""
        theme = self.theme_combo.currentData()
        self.apply_theme(theme)
        
    def new_character(self):
        """Create a new character."""
        character = Character()
        self.characters[character.id] = character
        self.sidebar.add_character(character)
        self.load_character(character)
        self.set_edit_mode(True)  # Switch to edit mode for new character
        self.status_bar.showMessage(tr("character_created"), 3000)
        
    def delete_character(self, character_id: str):
        """Delete a character."""
        if character_id not in self.characters:
            return
        
        character = self.characters[character_id]
        
        reply = QMessageBox.question(
            self,
            tr("delete"),
            tr("delete_confirm").format(name=character.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_character(character_id)
            del self.characters[character_id]
            
            if self.current_character and self.current_character.id == character_id:
                self.current_character = None
                self.clear_character_display()
            
            self.status_bar.showMessage(tr("character_deleted"), 3000)
    
    def load_character(self, character: Character):
        """Load a character into the UI."""
        self.current_character = character
        
        # Load in all tabs
        self.header_layout.load_character(character)
        self.overview_tab.load_character(character)
        self.character_tab.load_character(character)
        self.enneagram_tab.load_character(character)
        self.stats_tab.load_character(character)
        self.biography_tab.load_character(character)
        self.relationships_tab.load_character(character)
        self.narrative_tab.load_character(character)
        
        self.setWindowTitle(f"{tr('app_title')} - {character.name}")
        self.characterChanged.emit(character)
        
    def clear_character_display(self):
        """Clear all character data from UI."""
        self.header_layout.clear()
        self.overview_tab.clear()
        self.character_tab.clear()
        self.enneagram_tab.clear()
        self.stats_tab.clear()
        self.biography_tab.clear()
        self.relationships_tab.clear()
        self.narrative_tab.clear()
        self.setWindowTitle(tr("app_title"))
        
    def on_character_modified(self):
        """Handle character data modification."""
        if not self.current_character:
            return
        
        # Save from all tabs
        self.header_layout.save_to_character(self.current_character)
        self.character_tab.save_to_character(self.current_character)
        self.enneagram_tab.save_to_character(self.current_character)
        self.stats_tab.save_to_character(self.current_character)
        self.biography_tab.save_to_character(self.current_character)
        self.relationships_tab.save_to_character(self.current_character)
        self.narrative_tab.save_to_character(self.current_character)
        
        # Update overview tab
        self.overview_tab.load_character(self.current_character)
        
        self.current_character.updated_at = datetime.now()
        self.sidebar.update_character(self.current_character)
        
    def save_current_character(self):
        """Save the current character to disk."""
        if not self.current_character:
            return
        
        try:
            self.on_character_modified()
            self.storage.save_character(self.current_character)
            self.status_bar.showMessage(
                f"{tr('saved')} - {self.current_character.name}", 3000
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("save_error"),
                f"{tr('save_error')}: {str(e)}"
            )
    
    def load_character_dialog(self):
        """Show dialog to load a character file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("load_character"),
            str(self.storage.characters_dir),
            tr("json_filter")
        )
        
        if file_path:
            try:
                character = self.storage.load_character_from_file(Path(file_path))
                self.characters[character.id] = character
                self.sidebar.add_character(character)
                self.load_character(character)
                self.status_bar.showMessage(
                    f"{tr('loaded')} - {character.name}", 3000
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    tr("load_error"),
                    f"{tr('load_error')}: {str(e)}"
                )
    
    def load_all_characters(self):
        """Load all characters from the data directory."""
        characters = self.storage.load_all_characters()
        for character in characters:
            self.characters[character.id] = character
            self.sidebar.add_character(character)
        
        if characters:
            self.load_character(characters[0])
    
    def autosave(self):
        """Automatically save all modified characters."""
        if self.current_character and self.edit_mode:
            self.on_character_modified()
            
        saved_count = 0
        for character in self.characters.values():
            if self.storage.needs_save(character):
                try:
                    self.storage.save_character(character)
                    saved_count += 1
                except Exception as e:
                    print(f"Autosave failed for {character.name}: {e}")
        
        if saved_count > 0:
            self.status_bar.showMessage(tr("autosaving"), 2000)
    
    def export_to_pdf(self):
        """Export current character to PDF."""
        if not self.current_character:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("export_pdf"),
            f"{self.current_character.name}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            QMessageBox.information(
                self,
                tr("export_pdf"),
                "PDF export will be implemented with reportlab library."
            )
    
    def export_to_html(self):
        """Export current character to HTML."""
        if not self.current_character:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("export_html"),
            f"{self.current_character.name}.html",
            "HTML Files (*.html)"
        )
        
        if file_path:
            try:
                self.storage.export_to_html(self.current_character, Path(file_path))
                self.status_bar.showMessage(
                    f"Exported to {Path(file_path).name}", 3000
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export: {str(e)}"
                )
    
    def closeEvent(self, event):
        """Handle application close event."""
        for character in self.characters.values():
            try:
                self.storage.save_character(character)
            except Exception as e:
                print(f"Failed to save {character.name} on close: {e}")
        
        event.accept()