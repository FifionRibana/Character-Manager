#!/usr/bin/env python3
"""
Quick test script to verify the Phase 3 corrections.
"""

import sys
import json
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Global imports for all tests
from data.character import Character, CharacterStats
from data.enneagram import EnneagramProfile
from data.enums import EnneagramType, StatType, RelationType
from models.character_model import CharacterModel
from controllers.storage_controller import StorageController

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        # Test that imports are available
        assert Character is not None
        assert CharacterStats is not None
        assert EnneagramProfile is not None
        assert EnneagramType is not None
        assert StatType is not None
        assert RelationType is not None
        assert CharacterModel is not None
        assert StorageController is not None
        
        print("✅ All imports successful")
        return True
        
    except (ImportError, NameError, AssertionError) as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without PyQt signals."""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test Character creation
        character = Character.create_default("Test Character")
        character.level = 5
        character.stats.strength = 15
        character.biography = "Test biography"
        character.affiliations = ["Test Guild"]
        
        # Test relationship
        character.add_relationship(
            target_id="test_001",
            target_name="Test Friend",
            relationship_type=RelationType.FRIEND,
            description="A good friend"
        )
        
        # Test serialization
        character_dict = character.to_dict()
        character_json = json.dumps(character_dict)
        
        # Test deserialization
        restored_character = Character.from_dict(character_dict)
        
        assert restored_character.name == "Test Character"
        assert restored_character.level == 5
        assert restored_character.stats.strength == 15
        assert len(restored_character.relationships) == 1
        assert restored_character.relationships[0].relationship_type == RelationType.FRIEND
        
        print("✅ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_without_qt():
    """Test storage operations without Qt signals."""
    print("🧪 Testing storage without Qt...")
    
    try:
        # Create test character
        character = Character.create_default("Storage Test")
        character.level = 8
        character.stats.strength = 16
        
        # Manual JSON operations
        character_dict = character.to_dict()
        character_json = json.dumps(character_dict)
        
        # Test file operations manually
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = Path(f.name)
        
        try:
            # Manual save
            temp_file.write_text(character_json)
            assert temp_file.exists()
            
            # Manual load
            loaded_json = temp_file.read_text()
            loaded_data = json.loads(loaded_json)
            
            assert loaded_data['name'] == "Storage Test"
            assert loaded_data['level'] == 8
            assert loaded_data['stats']['strength'] == 16
            
            print("✅ Manual storage operations work")
            
            # Test StorageController validation
            from controllers.storage_controller import StorageController
            storage = StorageController()
            
            # Test validation method directly
            is_valid, error_msg = storage._validate_character_data(character_dict)
            assert is_valid, f"Validation failed: {error_msg}"
            
            # Test HTML generation
            html_content = storage._generate_character_html(character_dict)
            assert "Storage Test" in html_content
            assert "Level 8" in html_content
            
            print("✅ StorageController validation and HTML generation work")
            
        finally:
            temp_file.unlink(missing_ok=True)
        
        print("✅ Storage operations tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Storage operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all quick tests."""
    print("🚀 Running Quick Test for Phase 3 Fixes")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_storage_without_qt
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Quick Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All quick tests passed! Fixes are working.")
        print("You can now run: python test_integration_phase3.py")
        return True
    else:
        print("❌ Some quick tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)