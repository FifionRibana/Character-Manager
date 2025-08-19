#!/usr/bin/env python3
"""
Debug script to find and fix Character test errors.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enum_access():
    """Test enum access with correct enums."""
    print("🧪 Testing enum access...")
    
    try:
        from data.enums import ValidationLimits, RelationType, StorageKeys, UIConstants
        
        # ✅ Correction: MAX_RECENT_FILES est dans UIConstants, pas ValidationLimits
        print(f"✅ MAX_RECENT_FILES: {UIConstants.MAX_RECENT_FILES}")
        print(f"✅ MIN_CHARACTER_LEVEL: {ValidationLimits.MIN_CHARACTER_LEVEL}")
        print(f"✅ MAX_CHARACTER_LEVEL: {ValidationLimits.MAX_CHARACTER_LEVEL}")
        print(f"✅ FRIEND: {RelationType.FRIEND}")
        print(f"✅ CHARACTER_ID: {StorageKeys.CHARACTER_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enum test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_character_creation():
    """Test basic character creation with proper validation."""
    print("🧪 Testing character creation...")
    
    try:
        from data.character import Character, CharacterStats
        from data.enums import RelationType, ValidationLimits
        
        # Test basic creation
        character = Character.create_default("Test Character")
        print(f"✅ Basic creation: {character.name}")
        
        # ✅ S'assurer que le niveau est valide avant les tests
        character.level = ValidationLimits.DEFAULT_CHARACTER_LEVEL  # ou 1
        
        # Test relationship addition
        character.add_relationship(
            target_id="test_001",
            target_name="Test Friend",
            relationship_type=RelationType.FRIEND,
            description="A good friend"
        )
        print(f"✅ Relationship added: {len(character.relationships)}")
        
        # Test validation - Empty name
        try:
            test_char = Character.create_default("Valid Name")
            test_char.name = ""
            test_char._validate_core_data()
            print("❌ Empty name validation failed")
            return False
        except ValueError as e:
            print(f"✅ Empty name validation: {e}")
        
        # Test validation - Invalid level
        try:
            test_char = Character.create_default("Valid Name")
            test_char.level = 0  # Invalid level
            test_char._validate_core_data()
            print("❌ Invalid level validation failed")
            return False
        except ValueError as e:
            print(f"✅ Invalid level validation: {e}")
        
        # ✅ Reset to valid values before serialization test
        character.name = "Test Character"
        character.level = 1  # Valid level
        
        # Test serialization
        character_dict = character.to_dict()
        print(f"✅ Serialization: {len(character_dict)} keys")
        
        # ✅ Debug: Print the level being serialized
        print(f"🔍 Serialized level: {character_dict.get('level', 'NOT_FOUND')}")
        
        # Test deserialization
        restored = Character.from_dict(character_dict)
        print(f"✅ Deserialization: {restored.name}")
        
        # Verify round-trip serialization
        assert restored.name == character.name
        assert restored.level == character.level
        assert len(restored.relationships) == len(character.relationships)
        print("✅ Round-trip serialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Character test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run debug tests."""
    print("🔍 Debug Character Tests")
    print("=" * 30)
    
    success = True
    success &= test_enum_access()
    print()
    success &= test_character_creation()
    
    print()
    print("=" * 30)
    if success:
        print("✅ All debug tests passed")
    else:
        print("❌ Some debug tests failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)