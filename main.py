#!/usr/bin/env python3
"""
Medieval Character Manager - QML Version
Main entry point for the QML-based application.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType, qmlRegisterSingletonType
from PyQt6.QtCore import QObject, pyqtSignal

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import our models and controllers
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel, register_character_list_model
from controllers.main_controller import MainController, register_main_controller
from utils.translator import get_translator


def create_app_theme_singleton(qml_engine, js_engine):
    """Create AppTheme singleton for QML."""
    # Return None since we're using a QML singleton defined in AppTheme.qml
    return None


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QGuiApplication.highDpiScaleFactorRoundingPolicy()
    )
    
    # Create application
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Medieval Character Manager")
    app.setOrganizationName("RPG Tools")
    app.setOrganizationDomain("rpgtools.local")
    
    # Set application metadata
    app.setApplicationDisplayName("Medieval Character Manager")
    
    # Initialize translator
    translator = get_translator()
    
    # Register QML types
    register_character_list_model()
    register_main_controller()
    
    # Register individual models that might be used directly
    qmlRegisterType(CharacterModel, 'CharacterModels', 1, 0, 'CharacterModel')
    
    # Create QML engine
    engine = QQmlApplicationEngine()
    
    # Create and expose main controller to QML
    main_controller = MainController()
    engine.rootContext().setContextProperty("controller", main_controller)
    
    # Set QML import paths
    qml_dir = project_root / "qml"
    engine.addImportPath(str(qml_dir))
    
    # Add styles path
    styles_dir = qml_dir / "styles"
    engine.addImportPath(str(styles_dir))
    
    # Handle QML errors
    def on_object_created(obj, url):
        if obj is None:
            print(f"Failed to load QML file: {url}")
            sys.exit(1)
    
    def on_warnings(warnings):
        for warning in warnings:
            print(f"QML Warning: {warning.toString()}")
    
    engine.objectCreated.connect(on_object_created)
    engine.warnings.connect(on_warnings)
    
    # Load main QML file
    main_qml = qml_dir / "main.qml"
    
    if not main_qml.exists():
        print(f"Error: Could not find main.qml at {main_qml}")
        sys.exit(1)
    
    engine.load(main_qml.as_uri())
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        print("Error: Failed to load QML application")
        sys.exit(1)
    
    # Run application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())