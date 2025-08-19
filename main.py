#!/usr/bin/env python3
"""
Medieval Character Manager - QML Version (Updated)
Main entry point for the QML-based application with Phase 2 components.
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
from models.character_model import CharacterModel, register_character_model
from models.character_list_model import CharacterListModel, register_character_list_model
from models.enneagram_model import EnneagramModel, register_enneagram_model
from controllers.main_controller import MainController, register_main_controller
from controllers.storage_controller import StorageController, register_storage_controller
from utils.translator import get_translator

# Import data classes for type registration
from data.character import Character
from data.enneagram import EnneagramProfile
from data.enums import EnneagramType, StatType, RelationType


def register_data_types() -> None:
    """Register data types and enums for QML access."""
    # Register enums as uncreatable types (for constants)
    qmlRegisterType(EnneagramType, 'DataTypes', 1, 0, 'EnneagramType')
    qmlRegisterType(StatType, 'DataTypes', 1, 0, 'StatType')
    qmlRegisterType(RelationType, 'DataTypes', 1, 0, 'RelationType')


def create_app_theme_singleton(qml_engine, js_engine):
    """Create AppTheme singleton for QML."""
    # Return None since we're using a QML singleton defined in AppTheme.qml
    return None


def setup_qml_import_paths(engine: QQmlApplicationEngine) -> None:
    """
    Setup QML import paths for the application.
    
    Args:
        engine: QML application engine
    """
    qml_dir = project_root / "qml"
    
    # Add main QML directory
    engine.addImportPath(str(qml_dir))
    
    # Add specific component directories
    components_dir = qml_dir / "components"
    styles_dir = qml_dir / "styles"
    views_dir = qml_dir / "views"
    
    for directory in [components_dir, styles_dir, views_dir]:
        if directory.exists():
            engine.addImportPath(str(directory))


def register_all_types() -> None:
    """Register all types needed for QML."""
    # Register data types first
    register_data_types()
    
    # Register models
    register_character_model()
    register_character_list_model() 
    register_enneagram_model()
    
    # Register controllers
    register_main_controller()
    register_storage_controller()
    
    # Register individual models that might be used directly
    qmlRegisterType(CharacterModel, 'CharacterModels', 1, 0, 'CharacterModel')
    qmlRegisterType(EnneagramModel, 'EnneagramModels', 1, 0, 'EnneagramModel')
    qmlRegisterType(StorageController, 'Controllers', 1, 0, 'StorageController')


def setup_qml_context(engine: QQmlApplicationEngine) -> MainController:
    """
    Setup QML context properties.
    
    Args:
        engine: QML application engine
        
    Returns:
        Main controller instance
    """
    # Create and expose main controller to QML
    main_controller = MainController()
    engine.rootContext().setContextProperty("controller", main_controller)
    
    # Create and expose storage controller
    storage_controller = StorageController()
    engine.rootContext().setContextProperty("storageController", storage_controller)
    
    # Expose translator for dynamic language switching
    translator = get_translator()
    engine.rootContext().setContextProperty("translator", translator)
    
    return main_controller


def setup_error_handling(engine: QQmlApplicationEngine) -> None:
    """
    Setup error handling for QML engine.
    
    Args:
        engine: QML application engine
    """
    def on_object_created(obj, url):
        if obj is None:
            print(f"❌ Failed to load QML file: {url}")
            print("Check QML syntax and component imports.")
            sys.exit(1)
    
    def on_warnings(warnings):
        for warning in warnings:
            print(f"⚠️  QML Warning: {warning.toString()}")
    
    engine.objectCreated.connect(on_object_created)
    engine.warnings.connect(on_warnings)


def validate_qml_files() -> bool:
    """
    Validate that required QML files exist.
    
    Returns:
        True if all required files exist
    """
    qml_dir = project_root / "qml"
    required_files = [
        # Core files
        qml_dir / "main.qml",
        qml_dir / "styles" / "AppTheme.qml",
        
        # Components (Phase 1-3)
        qml_dir / "components" / "Sidebar.qml",
        qml_dir / "components" / "CharacterHeader.qml",
        qml_dir / "components" / "EnneagramWheel.qml",
        qml_dir / "components" / "AffinityRadar.qml",
        qml_dir / "components" / "StatWidget.qml",
        qml_dir / "components" / "ImageDropArea.qml",
        qml_dir / "components" / "ErrorDialog.qml",
        
        # Views
        qml_dir / "views" / "OverviewTab.qml",
        qml_dir / "views" / "TabView.qml",
        qml_dir / "views" / "EnneagramTab.qml",
        qml_dir / "views" / "StatsTab.qml",
        qml_dir / "views" / "BiographyTab.qml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required QML files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True


def setup_application_metadata() -> QGuiApplication:
    """
    Create and configure the QGuiApplication.
    
    Returns:
        Configured QGuiApplication instance
    """
    # Enable high DPI scaling
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QGuiApplication.highDpiScaleFactorRoundingPolicy()
    )
    
    # Create application
    app = QGuiApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Medieval Character Manager")
    app.setApplicationDisplayName("Medieval Character Manager")
    app.setOrganizationName("RPG Tools")
    app.setOrganizationDomain("rpgtools.local")
    app.setApplicationVersion("2.0")
    
    # Set application properties
    app.setQuitOnLastWindowClosed(True)
    
    return app


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Application exit code
    """
    print("🏰 Starting Medieval Character Manager (QML Version)...")
    
    # Validate environment
    if not validate_qml_files():
        print("❌ Cannot start application due to missing QML files.")
        return 1
    
    # Setup application
    app = setup_application_metadata()
    
    # Initialize translator early
    translator = get_translator()
    print(f"🌍 Translator initialized with language: {translator.current_language}")
    
    # Register all QML types
    print("📦 Registering QML types...")
    register_all_types()
    
    # Create QML engine
    engine = QQmlApplicationEngine()
    
    # Setup import paths
    setup_qml_import_paths(engine)
    
    # Setup context properties
    print("🔧 Setting up QML context...")
    main_controller = setup_qml_context(engine)
    
    # Setup error handling
    setup_error_handling(engine)
    
    # Load main QML file
    main_qml = project_root / "qml" / "main.qml"
    print(f"🎨 Loading main QML file: {main_qml}")
    
    engine.load(main_qml.as_uri())
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        print("❌ Failed to load QML application")
        print("Check QML syntax and imports in main.qml")
        return 1
    
    print("✅ QML application loaded successfully")
    print("🚀 Starting main event loop...")
    
    # Run application
    try:
        return app.exec()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Application error: {e}")
        return 1


def debug_mode_main() -> int:
    """
    Main function with additional debugging information.
    
    Returns:
        Application exit code
    """
    print("🐛 Running in debug mode...")
    
    # Set debug environment variables
    os.environ["QT_LOGGING_RULES"] = "qt.qml.debug=true"
    os.environ["QML_IMPORT_TRACE"] = "1"
    
    return main()


if __name__ == "__main__":
    # Check if debug mode is requested
    if "--debug" in sys.argv:
        sys.exit(debug_mode_main())
    else:
        sys.exit(main())