"""
Main application window with dynamic translation support and OS theme detection.
"""

import sys
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QToolBar, QStatusBar, QMessageBox, QFileDialog,
    QComboBox, QLabel, QApplication, QFormLayout, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QPalette

from models.character import Character
from models.enums import (
    Language, UIConstants, FileConstants, ThemeMode,
    EnneagramType, StorageKeys
)
from ui.widgets.image_drop import ImageDropWidget
from utils.translator import get_translator, tr
from utils.storage import StorageManager
from ui.widgets.character_header import CharacterHeader
from ui.widgets.sidebar import CharacterSidebar
from ui.tabs.character_tab import CharacterTab
from ui.tabs.enneagram_tab import EnneagramTab
from ui.tabs.stats_tab import StatsTab
from ui.tabs.biography_tab import BiographyTab
from ui.tabs.relationships_tab import RelationshipsTab
from ui.tabs.narrative_tab import NarrativeTab
from ui.styles import StyleManager


class MainWindow(QMainWindow):
    """Main application window with full translation support."""
    
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
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.setup_autosave()
        
        # Apply system theme
        self.apply_theme()
        
        # Load existing characters
        print("load")
        self.load_all_characters()
        print("loaded")
        
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


        self.header_layout = CharacterHeader()

        content_layout.addWidget(self.header_layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.character_tab = CharacterTab()
        self.enneagram_tab = EnneagramTab()
        self.stats_tab = StatsTab()
        self.biography_tab = BiographyTab()
        self.relationships_tab = RelationshipsTab(self.characters)
        self.narrative_tab = NarrativeTab()
        
        # Add tabs (icons will be added in retranslate_ui)
        self.tabs.addTab(self.character_tab, "")
        self.tabs.addTab(self.enneagram_tab, "")
        self.tabs.addTab(self.stats_tab, "")
        self.tabs.addTab(self.biography_tab, "")
        self.tabs.addTab(self.relationships_tab, "")
        self.tabs.addTab(self.narrative_tab, "")
        
        content_layout.addWidget(self.tabs)
        self.splitter.addWidget(content_widget)
        
        # Set splitter sizes (sidebar: 250px, content: rest)
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
        
        # Add stretch to push language selector to the right
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
        
    def setup_connections(self):
        """Connect signals and slots between components."""
        # Connect header signals
        self.header_layout.dataChanged.connect(self.on_character_modified)

        # Connect tab signals
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
        self.tabs.setTabText(0, tr("tab_character"))
        self.tabs.setTabText(1, tr("tab_enneagram"))
        self.tabs.setTabText(2, tr("tab_stats"))
        self.tabs.setTabText(3, tr("tab_biography"))
        self.tabs.setTabText(4, tr("tab_relationships"))
        self.tabs.setTabText(5, tr("tab_narrative"))
        
        # Update header
        self.header_layout.retranslate_ui()

        # Update all tabs
        self.character_tab.retranslate_ui()
        self.enneagram_tab.retranslate_ui()
        self.stats_tab.retranslate_ui()
        self.biography_tab.retranslate_ui()
        self.relationships_tab.retranslate_ui()
        self.narrative_tab.retranslate_ui()
        
        # Update sidebar
        self.sidebar.retranslate_ui()
        
        # Status bar
        if not self.status_bar.currentMessage() or self.status_bar.currentMessage() in ["Ready", "Prêt"]:
            self.status_bar.showMessage(tr("ready"))
    
    def apply_theme(self, mode: ThemeMode = ThemeMode.AUTO):
        """
        Apply theme based on mode or system settings.
        
        Args:
            mode: Theme mode to apply
        """
        if mode == ThemeMode.AUTO:
            # Detect system theme
            palette = QApplication.palette()
            window_color = palette.color(QPalette.ColorRole.Window)
            # Simple heuristic: if background is dark, use dark theme
            is_dark = window_color.lightness() < 128
            actual_mode = ThemeMode.DARK if is_dark else ThemeMode.LIGHT
        else:
            actual_mode = mode
        
        # Apply stylesheet
        stylesheet = self.style_manager.get_stylesheet(actual_mode)
        self.setStyleSheet(stylesheet)
        
    def change_language(self):
        """Handle language change from combo box."""
        language = self.language_combo.currentData()
        self.translator.set_language(language)
        
    def change_theme(self):
        """Handle theme change from combo box."""
        theme = self.theme_combo.currentData()
        self.apply_theme(theme)
        
    def new_character(self):
        """Create a new character."""
        character = Character()
        self.characters[character.id] = character
        self.sidebar.add_character(character)
        self.load_character(character)
        self.status_bar.showMessage(tr("character_created"), 3000)
        
    def delete_character(self, character_id: str):
        """
        Delete a character.
        
        Args:
            character_id: ID of character to delete
        """
        if character_id not in self.characters:
            return
        
        character = self.characters[character_id]
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            tr("delete"),
            tr("delete_confirm").format(name=character.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from storage
            self.storage.delete_character(character_id)
            
            # Remove from memory
            del self.characters[character_id]
            
            # Clear if it was current
            if self.current_character and self.current_character.id == character_id:
                self.current_character = None
                self.clear_character_display()
            
            self.status_bar.showMessage(tr("character_deleted"), 3000)
    
    def load_character(self, character: Character):
        """
        Load a character into the UI.
        
        Args:
            character: Character to load
        """
        self.current_character = character
        print("loading character")
        print(character.name, character.stats, character.level)
        
        # Basic info
        self.header_layout.load_character(character)

        print("AFTER HEADER LOAD", character.stats)

        # Update all tabs
        self.character_tab.load_character(character)
        print("LAST", character.stats)
        self.enneagram_tab.load_character(character)
        print("LAST", character.stats)
        self.stats_tab.load_character(character)
        print("LAST", character.stats)
        self.biography_tab.load_character(character)
        print("LAST", character.stats)
        self.relationships_tab.load_character(character)
        print("LAST", character.stats)
        self.narrative_tab.load_character(character)

        print("LAST", character.stats)

        
        # Update window title
        self.setWindowTitle(f"{tr('app_title')} - {character.name}")

        print("LAST", character.stats)
        
        # Emit signal
        self.characterChanged.emit(character)
        
    def clear_character_display(self):
        """Clear all character data from UI."""
        self.header_layout.clear()
        self.character_tab.clear()
        self.enneagram_tab.clear()
        self.stats_tab.clear()
        self.biography_tab.clear()
        self.relationships_tab.clear()
        self.narrative_tab.clear()
        self.setWindowTitle(tr("app_title"))
               
    def on_character_modified(self):
        """Handle character data modification from any tab."""
        if not self.current_character:
            return
        
        # Update character object
        self.header_layout.save_to_character(self.current_character)
        
        # Update character from all tabs
        self.character_tab.save_to_character(self.current_character)
        self.enneagram_tab.save_to_character(self.current_character)
        self.stats_tab.save_to_character(self.current_character)
        self.biography_tab.save_to_character(self.current_character)
        self.relationships_tab.save_to_character(self.current_character)
        self.narrative_tab.save_to_character(self.current_character)
        
        # Update timestamp
        self.current_character.updated_at = datetime.now()
        
        # Update sidebar if name changed
        self.sidebar.update_character(self.current_character)
        
    def save_current_character(self):
        """Save the current character to disk."""
        if not self.current_character:
            return
        
        try:
            self.on_character_modified()  # Ensure latest changes are captured
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
            print(f"STAT: {character.name} {character.stats} / {characters[0].stats}")
            self.characters[character.id] = character
            self.sidebar.add_character(character)
            print(f"POST/ {self.characters[character.id].stats}")
            print(f"POST/ {character.stats}")
        
        print(f"WTF: {characters[0].name} {characters[0].stats}")
        # Load first character if any exist
        if characters:
            print(f"LOAD ALL CHAR: {characters[0].stats}")
            self.load_character(characters[0])
    
    def autosave(self):
        """Automatically save all modified characters."""
        return
        if self.current_character:
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
            # TODO: Implement PDF export using reportlab
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
        # Save all characters before closing
        for character in self.characters.values():
            try:
                self.storage.save_character(character)
            except Exception as e:
                print(f"Failed to save {character.name} on close: {e}")
        
        event.accept()