#!/usr/bin/env python3
"""
Integration test for Medieval Character Manager Phase 2 components.
Tests the new Enneagram and CharacterHeader functionality.
"""

import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.character import Character, CharacterStats
from data.enneagram import EnneagramProfile
from data.enums import EnneagramType, InstinctualVariant, StatType
from models.character_model import CharacterModel
from models.enneagram_model import EnneagramModel


def test_dataclass_migration() -> bool:
    """Test that migrated dataclasses work correctly."""
    print("🧪 Testing migrated dataclasses...")
    
    try:
        # Test EnneagramProfile
        enneagram = EnneagramProfile(
            main_type=EnneagramType.TYPE_9,
            wing=EnneagramType.TYPE_8,
            development_level=5
        )
        
        assert enneagram.get_wing_notation() == "9w8"
        assert enneagram.main_type.title == "The Peacemaker"
        assert enneagram.health_category == "Average"
        
        # Test Character
        character = Character(
            name="Test Character",
            level=5,
            enneagram=enneagram
        )
        
        assert character.name == "Test Character"
        assert character.level == 5
        assert character.enneagram_display == "9w8"
        
        # Test serialization
        char_dict = character.to_dict()
        restored_character = Character.from_dict(char_dict)
        
        assert restored_character.name == character.name
        assert restored_character.enneagram.get_wing_notation() == "9w8"
        
        print("✅ Dataclass migration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Dataclass migration test failed: {e}")
        return False


def test_character_model() -> bool:
    """Test CharacterModel PyQt integration."""
    print("🧪 Testing CharacterModel...")
    
    try:
        from PyQt6.QtCore import QCoreApplication
        
        # Create minimal Qt application for testing
        app = QCoreApplication([])
        
        # Create character and model
        character = Character.create_default("Test Character")
        character.enneagram.main_type = EnneagramType.TYPE_4
        character.enneagram.wing = EnneagramType.TYPE_5
        character.stats.strength = 15
        
        model = CharacterModel()
        model.set_character(character)
        
        # Test property access
        assert model.name == "Test Character"
        assert model.enneagramType == 4
        assert model.enneagramWing == 5
        assert model.enneagramNotation == "4w5"
        assert model.strength == 15
        
        # Test property setting
        model.name = "Updated Character"
        model.enneagramType = 7
        model.strength = 18
        
        assert character.name == "Updated Character"
        assert character.enneagram.main_type == EnneagramType.TYPE_7
        assert character.stats.strength == 18
        
        print("✅ CharacterModel tests passed")
        return True
        
    except Exception as e:
        print(f"❌ CharacterModel test failed: {e}")
        return False


def test_enneagram_model() -> bool:
    """Test EnneagramModel PyQt integration."""
    print("🧪 Testing EnneagramModel...")
    
    try:
        from PyQt6.QtCore import QCoreApplication
        
        # Create minimal Qt application for testing
        app = QCoreApplication([])
        
        # Create enneagram profile and model
        profile = EnneagramProfile(
            main_type=EnneagramType.TYPE_3,
            wing=EnneagramType.TYPE_2,
            development_level=4
        )
        
        model = EnneagramModel()
        model.set_profile(profile)
        
        # Test property access
        assert model.mainType == 3
        assert model.wing == 2
        assert model.wingNotation == "3w2"
        assert model.developmentLevel == 4
        
        # Test property setting
        model.mainType = 6
        model.wing = 7
        model.developmentLevel = 2
        
        assert profile.main_type == EnneagramType.TYPE_6
        assert profile.wing == EnneagramType.TYPE_7
        assert profile.development_level == 2
        
        print("✅ EnneagramModel tests passed")
        return True
        
    except Exception as e:
        print(f"❌ EnneagramModel test failed: {e}")
        return False


def test_enum_features() -> bool:
    """Test new enum features in Python 3.11."""
    print("🧪 Testing enum features...")
    
    try:
        # Test EnneagramType properties
        type_9 = EnneagramType.TYPE_9
        assert type_9.title == "The Peacemaker"
        assert type_9.integration_point == EnneagramType.TYPE_3
        assert type_9.disintegration_point == EnneagramType.TYPE_6
        
        # Test InstinctualVariant properties
        sp = InstinctualVariant.SELF_PRESERVATION
        assert sp.full_name == "Self-Preservation"
        assert "safety" in sp.description.lower()
        
        # Test StatType properties
        strength = StatType.STRENGTH
        assert strength.abbreviation == "STR"
        assert "muscle" in strength.description.lower()
        
        print("✅ Enum features tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Enum features test failed: {e}")
        return False


def test_pathlib_integration() -> bool:
    """Test pathlib integration."""
    print("🧪 Testing pathlib integration...")
    
    try:
        from data.enums import FileConstants
        
        # Test path creation
        config_dir = FileConstants.CONFIG_DIR
        assert isinstance(config_dir, Path)
        
        # Test character with image
        character = Character.create_default("Path Test")
        
        # Test image handling (without actual file)
        test_path = Path("/fake/path/image.png")
        try:
            character.set_image_from_path(test_path)
        except FileNotFoundError:
            # Expected for non-existent file
            pass
        
        print("✅ Pathlib integration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Pathlib integration test failed: {e}")
        return False


def run_all_tests() -> bool:
    """Run all integration tests."""
    print("🚀 Running Medieval Character Manager Phase 2 Integration Tests")
    print("=" * 60)
    
    tests = [
        test_dataclass_migration,
        test_character_model,
        test_enneagram_model,
        test_enum_features,
        test_pathlib_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Empty line between tests
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phase 2 components are ready.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)