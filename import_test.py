#!/usr/bin/env python3
"""
Test simple pour vérifier que tous les imports fonctionnent.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enums_import():
    """Test that all required enums can be imported."""
    print("🧪 Testing enum imports...")
    
    try:
        from data.enums import (
            EnneagramType, InstinctualVariant, EnneagramTriad, DevelopmentLevel,
            StatType, RelationType, StorageKeys, ValidationLimits, UIConstants,
            DEFAULT_STAT_VALUE, DEFAULT_DEVELOPMENT_LEVEL, DEFAULT_CHARACTER_LEVEL,
            DEFAULT_ENNEAGRAM_TYPE
        )
        
        print("✅ All enum imports successful")
        
        # Test some basic enum access
        print(f"✅ EnneagramType.TYPE_9: {EnneagramType.TYPE_9}")
        print(f"✅ InstinctualVariant.SELF_PRESERVATION: {InstinctualVariant.SELF_PRESERVATION}")
        print(f"✅ ValidationLimits.DEFAULT_CHARACTER_LEVEL: {ValidationLimits.DEFAULT_CHARACTER_LEVEL}")
        print(f"✅ UIConstants.MAX_RECENT_FILES: {UIConstants.MAX_RECENT_FILES}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_character_import():
    """Test that character module can be imported."""
    print("🧪 Testing character import...")
    
    try:
        from data.character import Character, CharacterStats, Relationship, NarrativeEvent
        print("✅ Character module imports successful")
        return True
    except ImportError as e:
        print(f"❌ Character import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enneagram_import():
    """Test that enneagram module can be imported."""
    print("🧪 Testing enneagram import...")
    
    try:
        from data.enneagram import EnneagramProfile
        print("✅ Enneagram module imports successful")
        return True
    except ImportError as e:
        print(f"❌ Enneagram import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_creation():
    """Test basic object creation."""
    print("🧪 Testing basic object creation...")
    
    try:
        from data.character import Character
        from data.enums import ValidationLimits
        
        # Test character creation
        character = Character.create_default("Test Character")
        assert character.name == "Test Character"
        assert character.level == ValidationLimits.DEFAULT_CHARACTER_LEVEL
        
        print(f"✅ Character created: {character.name}, Level: {character.level}")
        return True
        
    except Exception as e:
        print(f"❌ Basic creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all import tests."""
    print("🔍 Testing All Imports")
    print("=" * 30)
    
    tests = [
        ("Enum Imports", test_enums_import),
        ("Character Import", test_character_import),
        ("Enneagram Import", test_enneagram_import),
        ("Basic Creation", test_basic_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        print()
    
    print("=" * 30)
    print(f"🏁 Import Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All imports are working correctly!")
        print("You can now run: python test_fix_verification.py")
        return True
    else:
        print("⚠️  Some imports need fixing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)