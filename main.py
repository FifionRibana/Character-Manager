import argparse
import os
from pathlib import Path
import sys

from PyQt6.QtCore import (
    QObject,
    QUrl,
    QCoreApplication,
    qInstallMessageHandler,
    QtMsgType,
)
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import (
    QQmlApplicationEngine,
    qmlRegisterType,
    qmlRegisterSingletonType,
    qmlRegisterSingletonInstance,
)

from controllers.image_controller import ImageController
from controllers.main_controller import MainController
from controllers.storage_controller import StorageController
from controllers.theme_controller import ThemeController
from models.character_model import CharacterModel


def qml_message_handler(msg_type, context, msg):
    """Custom handler for QML messages to help debug"""
    type_str = {
        QtMsgType.QtDebugMsg: "Debug",
        QtMsgType.QtInfoMsg: "Info",
        QtMsgType.QtWarningMsg: "Warning",
        QtMsgType.QtCriticalMsg: "Critical",
        QtMsgType.QtFatalMsg: "Fatal",
    }.get(msg_type, "Unknown")

    if context.file:
        print(f"QML {type_str}: {msg} [{context.file}:{context.line}]")
    else:
        print(f"QML {type_str}: {msg}")


def register_qml_types() -> bool:
    """Register all Python types for QML access"""
    try:
        qmlRegisterType(CharacterModel, "App.Types", 1, 0, "CharacterModel")
        print(f"✓ CharacterModel singleton registered")
        return True
    except Exception as e:
        print(f"ERROR: Failed to register App types: {e}")
        return False


def setup_application() -> QGuiApplication:
    """Setup and configure the Qt application"""

    # Set application metadata
    QCoreApplication.setOrganizationName("MedievalCharacterManager")
    QCoreApplication.setOrganizationDomain("medieval-character-manager.local")
    QCoreApplication.setApplicationName("Medieval Character Manager")
    QCoreApplication.setApplicationVersion("2.5.0-Phase5")

    # Set Qt Quick Controls style to avoid customization warnings
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

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
        "--debug", action="store_true", help="Enable debug mode with verbose output"
    )

    parser.add_argument(
        "--theme",
        choices=["light", "dark", "system"],
        default="system",
        help="Set the initial theme (default: system)",
    )

    parser.add_argument(
        "--data-dir", type=Path, help="Custom data directory for character files"
    )

    parser.add_argument(
        "--load", type=Path, help="Load a specific character file on startup"
    )

    parser.add_argument(
        "--no-animations",
        action="store_true",
        help="Disable all animations for better performance",
    )

    parser.add_argument(
        "--compact",
        action="store_true",
        help="Start in compact mode for smaller screens",
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
        "styles/AppTheme.qml",
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


def register_app_theme_singleton() -> bool:
    """Register the AppTheme singleton - FIXED"""

    qml_dir = Path(__file__).parent / "qml"
    app_theme_file = qml_dir / "styles" / "AppTheme.qml"

    if not app_theme_file.exists():
        print(f"ERROR: AppTheme.qml not found at {app_theme_file}")
        return False

    # Create proper file URL
    file_url = QUrl.fromLocalFile(str(app_theme_file))

    try:
        # Register the singleton with the correct URL format
        qmlRegisterSingletonType(file_url, "App.Styles", 1, 0, "AppTheme")
        print(f"✓ AppTheme singleton registered from {app_theme_file}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to register AppTheme singleton: {e}")
        return False


def register_app_controller_singleton() -> bool:
    try:
        qmlRegisterSingletonInstance(
            "App.Controllers",
            1,
            0,
            "ImageController",
            ImageController(),
        )
        print(f"✓ ImageController singleton registered")

        qmlRegisterSingletonInstance(
            "App.Controllers", 1, 0, "MainController", MainController()
        )
        print(f"✓ MainController singleton registered")

        qmlRegisterSingletonInstance(
            "App.Controllers",
            1,
            0,
            "StorageController",
            StorageController(),
        )
        print(f"✓ StorageController singleton registered")

        qmlRegisterSingletonInstance(
            "App.Controllers",
            1,
            0,
            "ThemeController",
            ThemeController(),
        )
        print(f"✓ ThemeController singleton registered")

        return True
    except Exception as e:
        print(f"ERROR: Failed to register App controller singletons: {e}")
        return False


def main() -> int:
    """Main application entry point"""

    # Parse command line arguments
    args = parse_arguments()

    if args.debug:
        print("Medieval Character Manager - Phase 5")
        print("Debug mode enabled")
        # Install custom message handler for better QML debugging
        qInstallMessageHandler(qml_message_handler)

    # Verify QML files exist
    if not verify_qml_files():
        print("ERROR: Cannot start application - missing QML files")
        print("Please ensure all QML files are present in the qml/ directory")
        return 1

    # Setup application
    app = setup_application()

    # Create QML engine
    engine = QQmlApplicationEngine()

    # Add QML import paths BEFORE setting context and loading QML
    qml_dir = Path(__file__).parent / "qml"
    engine.addImportPath(str(qml_dir))

    if args.debug:
        print("\nQML Import paths:")
        for path in engine.importPathList():
            print(f"  - {path}")

    # Register QML types
    if not register_qml_types():
        print("WARNING: App.Types registration failed")

    # Register AppTheme singleton BEFORE setting context
    if not register_app_theme_singleton():
        print("WARNING: AppTheme singleton registration failed")
        # Continue anyway, as it might work with relative imports

    if not register_app_controller_singleton():
        print("WARNING: App.Controller singletons registration failed")

    # Setup engine context (properties must be set BEFORE loading QML)
    # setup_engine_context(engine, args)

    # Load main QML file
    main_qml = qml_dir / "main.qml"

    if args.debug:
        print(f"\nLoading main QML from: {main_qml}")

    engine.load(QUrl.fromLocalFile(str(main_qml)))

    # Check if loading was successful
    if not engine.rootObjects():
        print("ERROR: Failed to load main.qml")
        print(f"Attempted to load: {main_qml}")
        return 1

    if args.debug:
        print("\n✓ Application started successfully")
        print(f"  Theme: {args.theme}")
        print(f"  Data directory: {args.data_dir or 'default'}")
        print(f"  Animations: {'disabled' if args.no_animations else 'enabled'}")
        print(f"  Mode: {'compact' if args.compact else 'normal'}")

    # Run application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
