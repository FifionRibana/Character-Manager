#!/usr/bin/env python3
"""
Medieval Character Manager - Main Entry Point
A modern RPG character sheet application with Enneagram personality system.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window_updated import MainWindowUpdated
# from ui.main_window import MainWindow
from utils.translator import get_translator


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Medieval Character Manager")
    app.setOrganizationName("RPG Tools")
    app.setOrganizationDomain("rpgtools.local")
    
    # Set application metadata
    app.setApplicationDisplayName("Medieval Character Manager")
    app.setDesktopFileName("medieval-character-manager")
    
    # Initialize translator (creates translation files if needed)
    translator = get_translator()
    
    # Create and show main window
    window = MainWindowUpdated()
    # window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()