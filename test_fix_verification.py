#!/usr/bin/env python3
"""
Script de vérification des corrections des erreurs de debug.
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enums_fixed():
    """Test that enums are accessible correctly."""
    print("🧪 Testing corrected enum access...")
    
    try:
        from data.enums import ValidationLimits, RelationType, StorageKeys, UIConstants
        
        # ✅ Correction: MAX_RECENT_FILES est dans UIConstants
        print(f"✅ UIConstants.MAX_RECENT_FILES: {UIConstants.MAX_RECENT_FILES}")
        print(f"✅ ValidationLimits.MIN_CHARACTER_LEVEL: {ValidationLimits.MIN_CHARACTER_LEVEL}")
        print(f"✅ ValidationLimits.MAX_CHARACTER_LEVEL: {ValidationLimits.MAX_CHARACTER_LEVEL}")
        print(f"✅ ValidationLimits.DEFAULT_CHARACTER_LEVEL: {ValidationLimits.DEFAULT_CHARACTER_LEVEL}")
        print(f"✅ RelationType.FRIEND: {RelationType.FRIEND}")
        print(f"✅ StorageKeys.CHARACTER_ID: {StorageKeys.CHARACTER_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enum test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_character_serialization_fixed():
    """Test that character serialization/deserialization works."""
    print("🧪 Testing corrected character serialization...")
    
    try:
        from data.character import Character
        from data.enums import RelationType, ValidationLimits, StorageKeys  # ✅ Import ajouté
        
        # Test 1: Basic creation with valid level
        character = Character.create_default("Test Character")
        character.level = ValidationLimits.DEFAULT_CHARACTER_LEVEL  # Ensure valid level
        
        print(f"✅ Character created: {character.name}, Level: {character.level}")
        
        # Test 2: Add a relationship
        character.add_relationship(
            target_id="test_001",
            target_name="Test Friend",
            relationship_type=RelationType.FRIEND,
            description="A good friend"
        )
        print(f"✅ Relationship added: {len(character.relationships)}")
        
        # ✅ Test stats pour s'assurer que les noms sont corrects
        character.stats.strength = 16
        character.stats.agility = 12  # ✅ Utilise agility, pas dexterity
        print(f"✅ Stats updated: STR {character.stats.strength}, AGI {character.stats.agility}")
        
        # Test 3: Serialize
        character_dict = character.to_dict()
        print(f"✅ Serialization successful: {len(character_dict)} keys")
        print(f"🔍 Serialized level: {character_dict.get(StorageKeys.LEVEL.value)}")
        
        # Test 4: Validate serialized data manually
        level_value = character_dict.get(StorageKeys.LEVEL.value)
        if not ValidationLimits.MIN_CHARACTER_LEVEL <= level_value <= ValidationLimits.MAX_CHARACTER_LEVEL:
            print(f"❌ Invalid level in serialized data: {level_value}")
            return False
        
        # ✅ Test stats dans les données sérialisées
        stats_data = character_dict.get(StorageKeys.STATS.value, {})
        if "strength" not in stats_data or "agility" not in stats_data:
            print(f"❌ Missing stats in serialized data")
            return False
        print(f"🔍 Serialized stats - STR: {stats_data.get('strength')}, AGI: {stats_data.get('agility')}")
        
        # Test 5: Deserialize
        restored = Character.from_dict(character_dict)
        print(f"✅ Deserialization successful: {restored.name}, Level: {restored.level}")
        
        # Test 6: Verify data integrity
        assert restored.name == character.name, f"Name mismatch: {restored.name} != {character.name}"
        assert restored.level == character.level, f"Level mismatch: {restored.level} != {character.level}"
        assert len(restored.relationships) == len(character.relationships), "Relationship count mismatch"
        
        # ✅ Vérifier les stats restaurées
        assert restored.stats.strength == character.stats.strength, f"Strength mismatch: {restored.stats.strength} != {character.stats.strength}"
        assert restored.stats.agility == character.stats.agility, f"Agility mismatch: {restored.stats.agility} != {character.stats.agility}"
        print(f"✅ Stats verification: STR {restored.stats.strength}, AGI {restored.stats.agility}")
        
        print("✅ Round-trip serialization successful")
        
        # Test 7: Test JSON round-trip
        json_str = json.dumps(character_dict)
        json_dict = json.loads(json_str)
        json_restored = Character.from_dict(json_dict)
        
        assert json_restored.name == character.name, "JSON round-trip failed"
        assert json_restored.stats.strength == character.stats.strength, "JSON stats round-trip failed"
        print("✅ JSON round-trip successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Character serialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_edge_cases():
    """Test validation edge cases."""
    print("🧪 Testing validation edge cases...")
    
    try:
        from data.character import Character
        from data.enums import ValidationLimits
        
        # Test 1: Empty name validation
        try:
            test_char = Character.create_default("Valid Name")
            test_char.name = ""
            test_char._validate_core_data()
            print("❌ Empty name validation should have failed")
            return False
        except ValueError as e:
            print(f"✅ Empty name validation works: {e}")
        
        # Test 2: Invalid level validation
        try:
            test_char = Character.create_default("Valid Name")
            test_char.level = 0  # Invalid level
            test_char._validate_core_data()
            print("❌ Invalid level validation should have failed")
            return False
        except ValueError as e:
            print(f"✅ Invalid level validation works: {e}")
        
        # Test 3: Valid level validation
        try:
            test_char = Character.create_default("Valid Name")
            test_char.level = ValidationLimits.DEFAULT_CHARACTER_LEVEL
            test_char._validate_core_data()
            print("✅ Valid level validation works")
        except ValueError as e:
            print(f"❌ Valid level validation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Validation edge cases test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification tests."""
    print("🔧 Running Fix Verification Tests")
    print("=" * 40)
    
    tests = [
        ("Enum Access", test_enums_fixed),
        ("Character Serialization", test_character_serialization_fixed),
        ("Validation Edge Cases", test_validation_edge_cases),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All fixes are working correctly!")
        print("You can now run your original debug_character_test.py")
        return True
    else:
        print("⚠️  Some fixes need more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)