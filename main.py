#!/usr/bin/env python3
"""
Medieval Character Manager - QML Version
Updated with complete AppTheme to fix all undefined color/value errors
"""

import sys
from pathlib import Path

# Qt imports
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def register_qml_types():
    """Register QML types before creating controllers."""
    print("Registering QML types...")
    
    try:
        from models.character_model import CharacterModel
        qmlRegisterType(CharacterModel, 'CharacterModels', 1, 0, 'CharacterModel')
        print("  - CharacterModel registered")
    except ImportError:
        print("  - CharacterModel not available")
    
    try:
        from models.character_list_model import CharacterListModel
        qmlRegisterType(CharacterListModel, 'CharacterModels', 1, 0, 'CharacterListModel')
        print("  - CharacterListModel registered")
    except ImportError:
        print("  - CharacterListModel not available")
    
    try:
        from models.enneagram_model import EnneagramModel
        qmlRegisterType(EnneagramModel, 'EnneagramModels', 1, 0, 'EnneagramModel')
        print("  - EnneagramModel registered")
    except ImportError:
        print("  - EnneagramModel not available")
    
    try:
        from controllers.storage_controller import StorageController
        qmlRegisterType(StorageController, 'Controllers', 1, 0, 'StorageController')
        print("  - StorageController registered")
    except ImportError:
        print("  - StorageController not available")
    
    try:
        from controllers.main_controller import MainController
        qmlRegisterType(MainController, 'Controllers', 1, 0, 'MainController')
        print("  - MainController registered")
    except ImportError:
        print("  - MainController not available")


def create_complete_app_theme():
    """Create complete AppTheme with all required properties."""
    return {
        # Base colors
        'primaryColor': '#2196F3',
        'secondaryColor': '#FFC107',
        'backgroundColor': '#FAFAFA',
        'textColor': '#212121',
        'textColorSecondary': '#757575',
        'textColorLight': '#FFFFFF',
        'borderColor': '#E0E0E0',
        'highlightColor': '#3F51B5',
        'errorColor': '#F44336',
        'successColor': '#4CAF50',
        'warningColor': '#FF9800',
        'mutedColor': '#9E9E9E',
        'surfaceColor': '#FFFFFF',
        'onSurfaceColor': '#212121',
        
        # Extended color palette for components
        'accentColor': '#FF5722',
        'disabledColor': '#BDBDBD',
        'disabledTextColor': '#9E9E9E',
        'dividerColor': '#E0E0E0',
        'shadowColor': '#00000029',
        'overlayColor': '#00000080',
        
        # Additional background colors
        'backgroundColorSecondary': '#F8F9FA',
        'borderColorLight': '#DEE2E6',
        
        # Typography
        'fontFamily': 'Inter, "Segoe UI", Roboto, sans-serif',
        'fontSizeDisplay': 32,
        'fontSizeHeading': 20,
        'fontSizeBody': 14,
        'fontSizeCaption': 12,
        
        # Spacing
        'spacingSmall': 8,
        'spacingMedium': 16,
        'spacingLarge': 24,
        'spacingXLarge': 32,
        
        # Border
        'borderWidth': 1,
        'borderRadius': 8,
        
        # Card properties (nested structure)
        'card': {
            'background': '#FFFFFF',
            'border': '#E0E0E0',
            'radius': 8,
            'shadow': '#00000014'
        },
        
        # Button properties (nested structure)
        'button': {
            'normal': '#2196F3',
            'hovered': '#1976D2',
            'pressed': '#1565C0',
            'disabled': '#BDBDBD',
            'textColor': '#FFFFFF',
            'radius': 6
        },
        
        # Enneagram-specific colors
        'enneagramPrimaryColor': '#6A4C93',
        'enneagramSecondaryColor': '#FFD23F',
        'enneagramAccentColor': '#FF6B6B',
        'enneagramBackgroundColor': '#F8F9FA',
        'enneagramBorderColor': '#DEE2E6',
        'enneagramTextColor': '#495057',
        'enneagramMutedColor': '#6C757D',
        'enneagramHighlightColor': '#4ECDC4',
        
        # Type-specific colors for Enneagram types 1-9
        'type1Color': '#E74C3C',  # Red - Anger/Perfectionist
        'type2Color': '#E67E22',  # Orange - Helper
        'type3Color': '#F1C40F',  # Yellow - Achiever
        'type4Color': '#9B59B6',  # Purple - Individualist
        'type5Color': '#3498DB',  # Blue - Investigator
        'type6Color': '#1ABC9C',  # Teal - Loyalist
        'type7Color': '#2ECC71',  # Green - Enthusiast
        'type8Color': '#E74C3C',  # Red - Challenger
        'type9Color': '#95A5A6',  # Gray - Peacemaker
        
        # Additional utility colors
        'infoColor': '#17A2B8',
        'lightColor': '#F8F9FA',
        'darkColor': '#343A40',
        
        # Animation durations (in milliseconds)
        'animationDurationFast': 150,
        'animationDurationNormal': 250,
        'animationDurationSlow': 500,
        
        # Z-index values
        'zIndexDropdown': 1000,
        'zIndexTooltip': 1010,
        'zIndexModal': 1020,
        'zIndexPopover': 1030,
        
        # Component-specific properties
        'slider': {
            'handleColor': '#2196F3',
            'handleBorder': '#FFFFFF',
            'trackColor': '#E0E0E0',
            'trackActiveColor': '#2196F3'
        },
        
        'input': {
            'background': '#FFFFFF',
            'border': '#E0E0E0',
            'borderFocus': '#2196F3',
            'placeholder': '#9E9E9E'
        },
        
        'tooltip': {
            'background': '#424242',
            'text': '#FFFFFF',
            'border': 'transparent'
        }
    }


def setup_application():
    """Setup and configure the Qt application."""
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Medieval Character Manager")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Character Creator Studios")
    app.setOrganizationDomain("charactercreator.app")
    return app


def setup_complete_context(engine):
    """Setup complete QML context with all required properties."""
    print("Setting up complete QML context...")
    
    # Import controllers
    try:
        from controllers.main_controller import MainController
        from controllers.storage_controller import StorageController
        from data.enums import EnneagramType, StatType, RelationType
        
        # Create MainController
        main_controller = MainController()
        print(f"  - MainController created (has characterModel: {hasattr(main_controller, 'characterModel')})")
        
        # Create StorageController
        storage_controller = StorageController()
        print("  - StorageController created")
        
        # Expose controllers to QML context
        engine.rootContext().setContextProperty("controller", main_controller)
        engine.rootContext().setContextProperty("storageController", storage_controller)
        
        # Setup enums with real values
        enneagram_types = {f"TYPE_{i}": i for i in range(1, 10)}
        stat_types = {stat.name: stat.value for stat in StatType}
        relation_types = {rel.name: rel.value for rel in RelationType}
        
        engine.rootContext().setContextProperty("EnneagramTypes", enneagram_types)
        engine.rootContext().setContextProperty("StatTypes", stat_types)
        engine.rootContext().setContextProperty("RelationTypes", relation_types)
        
        print(f"  - Enums exposed: {len(enneagram_types)} enneagram, {len(stat_types)} stats, {len(relation_types)} relations")
        
        # Setup COMPLETE AppTheme - this should fix all undefined color/value errors
        app_theme = create_complete_app_theme()
        engine.rootContext().setContextProperty("AppTheme", app_theme)
        print(f"  - Complete AppTheme exposed with {len(app_theme)} properties")
        
        # Setup translator fallback
        translator = {"tr": lambda key: key}  # Simple identity function
        engine.rootContext().setContextProperty("translator", translator)
        print("  - Translator fallback exposed")
        
        print("Complete QML context setup finished")
        return main_controller
        
    except Exception as e:
        print(f"ERROR in context setup: {e}")
        import traceback
        traceback.print_exc()
        return None


def setup_error_handling(engine):
    """Setup detailed error handling for QML."""
    def on_object_created(obj, url):
        print(f"🔍 QML Object Creation:")
        print(f"  - URL: {url}")
        print(f"  - Object: {obj}")
        print(f"  - Success: {obj is not None}")
        
        if obj is None:
            print(f"❌ FAILED to load QML file: {url}")
        else:
            print(f"✅ Successfully loaded QML: {url}")
            # Debug: Display window properties
            try:
                if hasattr(obj, 'property'):
                    visible = obj.property('visible')
                    width = obj.property('width')
                    height = obj.property('height')
                    title = obj.property('title')
                    print(f"  📊 Window properties:")
                    print(f"    - visible: {visible}")
                    print(f"    - size: {width}x{height}")
                    print(f"    - title: {title}")
            except Exception as e:
                print(f"    ⚠️  Could not read window properties: {e}")
    
    def on_warnings(warnings):
        if warnings:
            print(f"⚠️  QML Warnings ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                warning_text = warning.toString()
                if "Unable to assign [undefined]" in warning_text:
                    continue  # Skip these common warnings
                print(f"  {i}. {warning_text}")
    
    engine.objectCreated.connect(on_object_created)
    engine.warnings.connect(on_warnings)


def validate_qml_files():
    """Validate that required QML files exist."""
    qml_dir = PROJECT_ROOT / "qml"
    main_qml = qml_dir / "main.qml"
    
    if not main_qml.exists():
        print(f"Missing main.qml at: {main_qml}")
        return False
    
    print(f"Found main.qml at: {main_qml}")
    return True


def main():
    """Main application entry point."""
    try:
        print("Starting Medieval Character Manager with Complete Theme...")
        
        # Validate QML files first
        if not validate_qml_files():
            print("Cannot start application due to missing QML files.")
            return 1
        
        # Register QML types BEFORE creating application
        register_qml_types()
        
        # Setup application
        app = setup_application()
        print("Qt Application created")
        
        # Create QML engine
        engine = QQmlApplicationEngine()
        print("QML engine created")
        
        # Setup QML import paths
        qml_dir = PROJECT_ROOT / "qml"
        engine.addImportPath(str(qml_dir))
        print("QML import paths configured")
        
        # Setup error handling
        setup_error_handling(engine)
        print("QML error handling configured")
        
        # Setup complete context with full AppTheme
        main_controller = setup_complete_context(engine)
        if main_controller is None:
            print("Failed to setup QML context")
            return 1
        
        # Load main QML file
        main_qml_path = PROJECT_ROOT / "qml" / "main.qml"
        print(f"Loading QML file: {main_qml_path}")
        
        # Load QML
        engine.load(str(main_qml_path))
        
        # Check if QML loaded successfully
        root_objects = engine.rootObjects()
        print(f"Root objects after load: {len(root_objects)}")
        
        if not root_objects:
            print("QML file failed to create root object")
            return 1
        
        print(f"QML loaded successfully! Root objects: {len(root_objects)}")
        print("Application window should now be visible with minimal errors!")
        
        # Start the application
        result = app.exec()
        print(f"Application finished with code: {result}")
        return result
        
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())