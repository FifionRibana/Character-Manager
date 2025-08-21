#!/usr/bin/env python3
"""
Medieval Character Manager - Main Application Entry Point
Phase 5: Polish & Features Update
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QObject, QUrl, QCoreApplication
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType, qmlRegisterSingletonType

# Import all models
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel
from models.enneagram_model import EnneagramModel
from models.relationship_model import RelationshipModel, RelationType
from models.narrative_model import NarrativeModel, EventType

# Import all controllers
from controllers.main_controller import MainController
from controllers.storage_controller import StorageController
from controllers.theme_controller import ThemeController, ThemeMode
from controllers.export_controller import ExportController, ExportFormat

# Import data structures
from data.enums import (
    Archetype, Affinity, Gender, CharacterStatus,
    EnneagramType, Wing, Instinct, TriadCenter,
    StatCategory
)


def register_qml_types() -> None:
    """Register all Python types for QML access"""
    
    # Register models
    qmlRegisterType(CharacterModel, "MedievalModels", 1, 0, "CharacterModel")
    qmlRegisterType(CharacterListModel, "MedievalModels", 1, 0, "CharacterListModel")
    qmlRegisterType(EnneagramModel, "MedievalModels", 1, 0, "EnneagramModel")
    qmlRegisterType(RelationshipModel, "MedievalModels", 1, 0, "RelationshipModel")
    qmlRegisterType(NarrativeModel, "MedievalModels", 1, 0, "NarrativeModel")
    
    # Register controllers
    qmlRegisterType(MainController, "MedievalControllers", 1, 0, "MainController")
    qmlRegisterType(StorageController, "MedievalControllers", 1, 0, "StorageController")
    qmlRegisterType(ThemeController, "MedievalControllers", 1, 0, "ThemeController")
    qmlRegisterType(ExportController, "MedievalControllers", 1, 0, "ExportController")
    
    # Register enums - make them available to QML
    qmlRegisterType(Archetype, "MedievalEnums", 1, 0, "Archetype")
    qmlRegisterType(Affinity, "MedievalEnums", 1, 0, "Affinity")
    qmlRegisterType(Gender, "MedievalEnums", 1, 0, "Gender")
    qmlRegisterType(CharacterStatus, "MedievalEnums", 1, 0, "CharacterStatus")
    qmlRegisterType(EnneagramType, "MedievalEnums", 1, 0, "EnneagramType")
    qmlRegisterType(Wing, "MedievalEnums", 1, 0, "Wing")
    qmlRegisterType(Instinct, "MedievalEnums", 1, 0, "Instinct")
    qmlRegisterType(TriadCenter, "MedievalEnums", 1, 0, "TriadCenter")
    qmlRegisterType(StatCategory, "MedievalEnums", 1, 0, "StatCategory")
    qmlRegisterType(RelationType, "MedievalEnums", 1, 0, "RelationType")
    qmlRegisterType(EventType, "MedievalEnums", 1, 0, "EventType")
    qmlRegisterType(ThemeMode, "MedievalEnums", 1, 0, "ThemeMode")
    qmlRegisterType(ExportFormat, "MedievalEnums", 1, 0, "ExportFormat")


def create_app_theme_singleton(engine: QQmlApplicationEngine) -> QObject:
    """Create AppTheme singleton with theme controller"""
    theme_controller = ThemeController()
    
    # Register the theme controller to be accessible from QML
    engine.rootContext().setContextProperty("themeController", theme_controller)
    
    return theme_controller


def setup_application() -> QGuiApplication:
    """Setup and configure the Qt application"""
    
    # Set application metadata
    QCoreApplication.setOrganizationName("MedievalCharacterManager")
    QCoreApplication.setOrganizationDomain("medieval-character-manager.local")
    QCoreApplication.setApplicationName("Medieval Character Manager")
    QCoreApplication.setApplicationVersion("2.5.0-Phase5")
    
    # Create application
    app = QGuiApplication(sys.argv)
    
    # Set application icon if available
    icon_path = Path(__file__).parent / "resources" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    return app


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Medieval Character Manager - RPG Character Creation Tool"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose output"
    )
    
    parser.add_argument(
        "--theme",
        choices=["light", "dark", "system"],
        default="system",
        help="Set the initial theme (default: system)"
    )
    
    parser.add_argument(
        "--data-dir",
        type=Path,
        help="Custom data directory for character files"
    )
    
    parser.add_argument(
        "--load",
        type=Path,
        help="Load a specific character file on startup"
    )
    
    parser.add_argument(
        "--no-animations",
        action="store_true",
        help="Disable all animations for better performance"
    )
    
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Start in compact mode for smaller screens"
    )
    
    return parser.parse_args()


def verify_qml_files() -> bool:
    """Verify that all required QML files exist"""
    
    qml_dir = Path(__file__).parent / "qml"
    
    required_files = [
        "main.qml",
        "components/qmldir",
        "components/Sidebar.qml",
        "components/CharacterHeader.qml",
        "components/EnneagramWheel.qml",
        "components/AffinityRadar.qml",
        "components/StatWidget.qml",
        "components/ImageDropArea.qml",
        "components/ErrorDialog.qml",
        "components/RelationshipWidget.qml",
        "components/TimelineEvent.qml",
        "views/OverviewTab.qml",
        "views/TabView.qml",
        "views/EnneagramTab.qml",
        "views/StatsTab.qml",
        "views/BiographyTab.qml",
        "views/RelationshipsTab.qml",
        "views/NarrativeTab.qml",
        "dialogs/SettingsDialog.qml",
        "styles/AppTheme.qml"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = qml_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("ERROR: Missing required QML files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    return True


def setup_engine_context(engine: QQmlApplicationEngine, args: argparse.Namespace) -> None:
    """Setup QML engine context properties"""
    
    context = engine.rootContext()
    
    # Create and register controllers
    main_controller = MainController()
    storage_controller = StorageController()
    theme_controller = ThemeController()
    export_controller = ExportController()
    
    # Set initial theme based on arguments
    if args.theme == "dark":
        theme_controller.switch_theme("Dark")
    elif args.theme == "light":
        theme_controller.switch_theme("Light")
    
    # Set custom data directory if provided
    if args.data_dir:
        storage_controller.set_data_directory(args.data_dir)
    
    # Register controllers as context properties
    context.setContextProperty("mainController", main_controller)
    context.setContextProperty("storageController", storage_controller)
    context.setContextProperty("themeController", theme_controller)
    context.setContextProperty("exportController", export_controller)
    
    # Set debug mode
    context.setContextProperty("debugMode", args.debug)
    
    # Set animation preferences
    context.setContextProperty("animationsDisabled", args.no_animations)
    
    # Set compact mode
    context.setContextProperty("compactMode", args.compact)
    
    # Provide enum values for QML
    context.setContextProperty("Archetype", {
        name: value.value for name, value in Archetype.__members__.items()
    })
    context.setContextProperty("Affinity", {
        name: value.value for name, value in Affinity.__members__.items()
    })
    
    context.setContextProperty("RelationType", {
        name: value.value for name, value in RelationType.__members__.items()
    })
    context.setContextProperty("EventType", {
        name: value.value for name, value in EventType.__members__.items()
    })
    context.setContextProperty("ExportFormat", {
        name: value.value for name, value in ExportFormat.__members__.items()
    })
    
    # Load character file if specified
    if args.load and args.load.exists():
        main_controller.load_character_file(str(args.load))


def main() -> int:
    """Main application entry point"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    if args.debug:
        print("Medieval Character Manager - Phase 5")
        print("Debug mode enabled")
    
    # Verify QML files exist
    if not verify_qml_files():
        print("ERROR: Cannot start application - missing QML files")
        print("Please ensure all QML files are present in the qml/ directory")
        return 1
    
    # Setup application
    app = setup_application()
    
    # Register QML types
    register_qml_types()
    
    # Create QML engine
    engine = QQmlApplicationEngine()
    
    # Setup engine context
    setup_engine_context(engine, args)
    
    # Add QML import paths
    qml_dir = Path(__file__).parent / "qml"
    engine.addImportPath(str(qml_dir))
    engine.addImportPath(str(qml_dir / "components"))
    engine.addImportPath(str(qml_dir / "views"))
    engine.addImportPath(str(qml_dir / "dialogs"))
    engine.addImportPath(str(qml_dir / "styles"))
    
    # Load main QML file
    main_qml = qml_dir / "main.qml"
    engine.load(QUrl.fromLocalFile(str(main_qml)))
    
    # Check if loading was successful
    if not engine.rootObjects():
        print("ERROR: Failed to load main.qml")
        print(f"Attempted to load: {main_qml}")
        return 1
    
    if args.debug:
        print("Application started successfully")
        print(f"Theme: {args.theme}")
        print(f"Data directory: {args.data_dir or 'default'}")
        print(f"Animations: {'disabled' if args.no_animations else 'enabled'}")
        print(f"Mode: {'compact' if args.compact else 'normal'}")
    
    # Run application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())