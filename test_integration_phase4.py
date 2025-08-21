#!/usr/bin/env python3
"""
Integration Tests for Phase 4: Relationships & Narrative

This module tests all Phase 4 functionality including relationship management,
narrative timeline, and model integrations.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtCore import QCoreApplication
from PyQt6.QtQml import QQmlApplicationEngine

# Import Phase 4 models and components
from models.relationship_model import RelationshipModel
from models.narrative_model import NarrativeModel
from data.character import Character, Relationship, NarrativeEvent
from data.enums import RelationType, StatType


class TestPhase4Models(unittest.TestCase):
    """Test Phase 4 model functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Setup Qt application for testing."""
        if not QCoreApplication.instance():
            cls.app = QCoreApplication([])
        else:
            cls.app = QCoreApplication.instance()
    
    def setUp(self):
        """Setup test fixtures."""
        self.relationship_model = RelationshipModel()
        self.narrative_model = NarrativeModel()
        
        # Create test character
        self.test_character = Character(
            id="test_char_1",
            name="Aragorn",
            age=35,
            profession="Ranger"
        )
    
    def test_relationship_model_creation(self):
        """Test RelationshipModel creation and basic properties."""
        self.assertIsInstance(self.relationship_model, RelationshipModel)
        self.assertEqual(self.relationship_model.count, 0)
        self.assertEqual(self.relationship_model.rowCount(), 0)
    
    def test_relationship_model_add_relationship(self):
        """Test adding relationships to the model."""
        # Add a relationship
        self.relationship_model.addRelationship(
            "legolas_1", "Legolas", "friend", "Loyal companion", 8
        )
        
        self.assertEqual(self.relationship_model.count, 1)
        self.assertEqual(self.relationship_model.rowCount(), 1)
        
        # Test relationship data
        index = self.relationship_model.index(0, 0)
        self.assertEqual(
            self.relationship_model.data(index, RelationshipModel.TargetNameRole), 
            "Legolas"
        )
        self.assertEqual(
            self.relationship_model.data(index, RelationshipModel.TypeRole), 
            "friend"
        )
        self.assertEqual(
            self.relationship_model.data(index, RelationshipModel.StrengthRole), 
            8
        )
        self.assertTrue(
            self.relationship_model.data(index, RelationshipModel.IsPositiveRole)
        )
    
    def test_relationship_model_remove_relationship(self):
        """Test removing relationships from the model."""
        # Add relationship first
        self.relationship_model.addRelationship(
            "saruman_1", "Saruman", "enemy", "Corrupted wizard", 9
        )
        self.assertEqual(self.relationship_model.count, 1)
        
        # Remove relationship
        success = self.relationship_model.removeRelationship("saruman_1")
        self.assertTrue(success)
        self.assertEqual(self.relationship_model.count, 0)
        
        # Try to remove non-existent relationship
        success = self.relationship_model.removeRelationship("non_existent")
        self.assertFalse(success)
    
    def test_relationship_model_update_relationship(self):
        """Test updating existing relationships."""
        # Add relationship first
        self.relationship_model.addRelationship(
            "gimli_1", "Gimli", "neutral", "Dwarf warrior", 5
        )
        
        # Update relationship
        self.relationship_model.updateRelationship(
            "gimli_1", "friend", "Trusted ally", 9
        )
        
        # Verify update
        relationship = self.relationship_model.getRelationship("gimli_1")
        self.assertIsNotNone(relationship)
        self.assertEqual(relationship["type"], "friend")
        self.assertEqual(relationship["description"], "Trusted ally")
        self.assertEqual(relationship["strength"], 9)
    
    def test_relationship_model_get_all_types(self):
        """Test getting all relationship types."""
        types = self.relationship_model.getAllRelationshipTypes()
        
        self.assertIsInstance(types, list)
        self.assertGreater(len(types), 0)
        
        # Check that each type has required fields
        for type_info in types:
            self.assertIn("value", type_info)
            self.assertIn("display", type_info)
            self.assertIn("color", type_info)
            self.assertIn("icon", type_info)
    
    def test_narrative_model_creation(self):
        """Test NarrativeModel creation and basic properties."""
        self.assertIsInstance(self.narrative_model, NarrativeModel)
        self.assertEqual(self.narrative_model.count, 0)
        self.assertEqual(self.narrative_model.rowCount(), 0)
    
    def test_narrative_model_add_event(self):
        """Test adding events to the narrative model."""
        # Add an event
        event_id = self.narrative_model.addEvent(
            "Born in Gondor", 
            "Born in the royal city", 
            "2931-03-01", 
            8, 
            ["birth", "gondor"]
        )
        
        self.assertIsInstance(event_id, str)
        self.assertEqual(self.narrative_model.count, 1)
        self.assertEqual(self.narrative_model.rowCount(), 1)
        
        # Test event data
        index = self.narrative_model.index(0, 0)
        self.assertEqual(
            self.narrative_model.data(index, NarrativeModel.TitleRole),
            "Born in Gondor"
        )
        self.assertEqual(
            self.narrative_model.data(index, NarrativeModel.ImportanceRole),
            8
        )
        self.assertIn(
            "birth",
            self.narrative_model.data(index, NarrativeModel.TagsRole)
        )
    
    def test_narrative_model_remove_event(self):
        """Test removing events from the narrative model."""
        # Add event first
        event_id = self.narrative_model.addEvent(
            "Test Event", "Test description", "", 5, []
        )
        self.assertEqual(self.narrative_model.count, 1)
        
        # Remove event
        success = self.narrative_model.removeEvent(event_id)
        self.assertTrue(success)
        self.assertEqual(self.narrative_model.count, 0)
        
        # Try to remove non-existent event
        success = self.narrative_model.removeEvent("non_existent")
        self.assertFalse(success)
    
    def test_narrative_model_update_event(self):
        """Test updating existing events."""
        # Add event first
        event_id = self.narrative_model.addEvent(
            "Original Title", "Original description", "", 5, []
        )
        
        # Update event
        self.narrative_model.updateEvent(
            event_id, "Updated Title", "Updated description", 
            "2950-01-01", 7, ["updated", "important"]
        )
        
        # Verify update
        event = self.narrative_model.getEvent(event_id)
        self.assertIsNotNone(event)
        self.assertEqual(event["title"], "Updated Title")
        self.assertEqual(event["importance"], 7)
        self.assertIn("updated", event["tags"])
    
    def test_narrative_model_get_events_by_importance(self):
        """Test filtering events by importance."""
        # Add events with different importance levels
        self.narrative_model.addEvent("Minor Event", "", "", 3, [])
        self.narrative_model.addEvent("Major Event", "", "", 9, [])
        self.narrative_model.addEvent("Normal Event", "", "", 5, [])
        
        # Get events by importance
        events = self.narrative_model.getEventsByImportance()
        self.assertEqual(len(events), 3)
        
        # Should be sorted by importance (highest first)
        self.assertEqual(events[0]["importance"], 9)
        self.assertEqual(events[1]["importance"], 5)
        self.assertEqual(events[2]["importance"], 3)
    
    def test_narrative_model_get_events_by_tag(self):
        """Test filtering events by tag."""
        # Add events with different tags
        self.narrative_model.addEvent("Battle Event", "", "", 7, ["battle", "victory"])
        self.narrative_model.addEvent("Meeting Event", "", "", 5, ["meeting", "diplomatic"])
        self.narrative_model.addEvent("Training Event", "", "", 4, ["training", "battle"])
        
        # Filter by "battle" tag
        battle_events = self.narrative_model.getEventsByTag("battle")
        self.assertEqual(len(battle_events), 2)
        
        # Filter by "diplomatic" tag
        diplomatic_events = self.narrative_model.getEventsByTag("diplomatic")
        self.assertEqual(len(diplomatic_events), 1)
        self.assertEqual(diplomatic_events[0]["title"], "Meeting Event")
    
    def test_narrative_model_get_all_tags(self):
        """Test getting all unique tags."""
        # Add events with various tags
        self.narrative_model.addEvent("Event 1", "", "", 5, ["tag1", "tag2"])
        self.narrative_model.addEvent("Event 2", "", "", 5, ["tag2", "tag3"])
        self.narrative_model.addEvent("Event 3", "", "", 5, ["tag1", "tag4"])
        
        # Get all tags
        tags = self.narrative_model.getAllTags()
        
        # Should be sorted and unique
        expected_tags = ["tag1", "tag2", "tag3", "tag4"]
        self.assertEqual(sorted(tags), expected_tags)


class TestPhase4DataClasses(unittest.TestCase):
    """Test Phase 4 data class functionality."""
    
    def test_relationship_creation(self):
        """Test Relationship dataclass creation and validation."""
        # Valid relationship
        relationship = Relationship(
            target_id="char_1",
            target_name="Frodo",
            relationship_type=RelationType.FRIEND,
            description="Brave hobbit",
            strength=8
        )
        
        self.assertEqual(relationship.target_id, "char_1")
        self.assertEqual(relationship.target_name, "Frodo")
        self.assertEqual(relationship.relationship_type, RelationType.FRIEND)
        self.assertTrue(relationship.is_positive)
        self.assertEqual(relationship.strength, 8)
    
    def test_relationship_validation(self):
        """Test Relationship validation rules."""
        # Test invalid strength
        with self.assertRaises(ValueError):
            Relationship(
                target_id="char_1",
                target_name="Invalid",
                relationship_type=RelationType.FRIEND,
                strength=15  # Invalid: > 10
            )
        
        # Test invalid name length (assuming validation exists)
        with self.assertRaises(ValueError):
            Relationship(
                target_id="char_1",
                target_name="",  # Invalid: empty name
                relationship_type=RelationType.FRIEND
            )
    
    def test_narrative_event_creation(self):
        """Test NarrativeEvent dataclass creation."""
        event = NarrativeEvent(
            title="The Battle of Helm's Deep",
            description="Defending the fortress against Saruman's army",
            date="3019-03-03",
            importance=9,
            tags=["battle", "victory", "rohan"]
        )
        
        self.assertEqual(event.title, "The Battle of Helm's Deep")
        self.assertEqual(event.importance, 9)
        self.assertIn("battle", event.tags)
        self.assertIsInstance(event.id, str)
        self.assertTrue(len(event.id) > 0)
    
    def test_narrative_event_validation(self):
        """Test NarrativeEvent validation rules."""
        # Test invalid importance
        with self.assertRaises(ValueError):
            NarrativeEvent(
                title="Invalid Event",
                importance=15  # Invalid: > 10
            )
        
        with self.assertRaises(ValueError):
            NarrativeEvent(
                title="Invalid Event",
                importance=0  # Invalid: < 1
            )
    
    def test_character_with_relationships(self):
        """Test Character with relationship management."""
        character = Character(
            id="test_char",
            name="Gandalf",
            age=2000,
            profession="Wizard"
        )
        
        # Add relationships
        character.add_relationship(
            "frodo_1", "Frodo", RelationType.MENTOR, "Teaching hobbit about the Ring"
        )
        character.add_relationship(
            "saruman_1", "Saruman", RelationType.ENEMY, "Fallen wizard"
        )
        
        self.assertEqual(character.relationship_count, 2)
        self.assertEqual(len(character.relationships), 2)
        
        # Remove relationship
        success = character.remove_relationship("frodo_1")
        self.assertTrue(success)
        self.assertEqual(character.relationship_count, 1)
        
        # Try to remove non-existent relationship
        success = character.remove_relationship("non_existent")
        self.assertFalse(success)
    
    def test_character_with_narrative_events(self):
        """Test Character with narrative event management."""
        character = Character(
            id="test_char",
            name="Aragorn",
            age=35,
            profession="King"
        )
        
        # Add narrative events
        event_id1 = character.add_narrative_event(
            "Crowned King of Gondor",
            "Restored the throne after victory over Sauron",
            "3019-05-01",
            10,
            ["coronation", "victory", "gondor"]
        )
        
        event_id2 = character.add_narrative_event(
            "Met Gandalf",
            "First encounter with the Grey Wizard",
            "2956-01-01",
            7,
            ["meeting", "mentor"]
        )
        
        self.assertEqual(len(character.narrative_events), 2)
        self.assertIsInstance(event_id1, str)
        self.assertIsInstance(event_id2, str)
        self.assertNotEqual(event_id1, event_id2)
        
        # Remove event
        success = character.remove_narrative_event(event_id1)
        self.assertTrue(success)
        self.assertEqual(len(character.narrative_events), 1)
        
        # Try to remove non-existent event
        success = character.remove_narrative_event("non_existent")
        self.assertFalse(success)


class TestPhase4Integration(unittest.TestCase):
    """Test Phase 4 integration with existing systems."""
    
    def setUp(self):
        """Setup integration test fixtures."""
        self.character = Character(
            id="integration_test",
            name="Test Character",
            age=25,
            profession="Adventurer"
        )
        
        self.relationship_model = RelationshipModel()
        self.narrative_model = NarrativeModel()
    
    def test_model_synchronization(self):
        """Test that models stay synchronized with character data."""
        # Add relationships to character
        self.character.add_relationship(
            "ally_1", "Ally", RelationType.ALLY, "Trusted companion"
        )
        self.character.add_relationship(
            "enemy_1", "Enemy", RelationType.ENEMY, "Arch nemesis"
        )
        
        # Set relationships in model
        self.relationship_model.set_relationships(self.character.relationships)
        
        # Verify synchronization
        self.assertEqual(self.relationship_model.count, 2)
        self.assertEqual(
            self.relationship_model.rowCount(), 
            self.character.relationship_count
        )
        
        # Add event to character
        event_id = self.character.add_narrative_event(
            "Epic Quest", "Saved the kingdom", "", 9, ["quest", "victory"]
        )
        
        # Set events in model
        self.narrative_model.set_events(self.character.narrative_events)
        
        # Verify synchronization
        self.assertEqual(self.narrative_model.count, 1)
        self.assertEqual(
            self.narrative_model.rowCount(),
            len(self.character.narrative_events)
        )
    
    def test_relationship_type_consistency(self):
        """Test that relationship types are consistent across components."""
        # Get types from model
        model_types = self.relationship_model.getAllRelationshipTypes()
        
        # Verify all enum values are represented
        enum_values = [rt.value for rt in RelationType]
        model_values = [rt["value"] for rt in model_types]
        
        for enum_value in enum_values:
            self.assertIn(enum_value, model_values)
    
    def test_data_serialization(self):
        """Test that Phase 4 data can be serialized/deserialized."""
        # Create relationship
        relationship = Relationship(
            target_id="ser_test",
            target_name="Serialization Test",
            relationship_type=RelationType.FRIEND,
            description="Test relationship",
            strength=7
        )
        
        # Serialize and deserialize
        data = relationship.to_dict()
        restored_relationship = Relationship.from_dict(data)
        
        self.assertEqual(relationship.target_id, restored_relationship.target_id)
        self.assertEqual(relationship.target_name, restored_relationship.target_name)
        self.assertEqual(relationship.relationship_type, restored_relationship.relationship_type)
        self.assertEqual(relationship.strength, restored_relationship.strength)
        
        # Test narrative event serialization
        event = NarrativeEvent(
            title="Test Event",
            description="Test description",
            date="2024-01-01",
            importance=8,
            tags=["test", "serialization"]
        )
        
        event_data = event.to_dict()
        restored_event = NarrativeEvent.from_dict(event_data)
        
        self.assertEqual(event.title, restored_event.title)
        self.assertEqual(event.importance, restored_event.importance)
        self.assertEqual(event.tags, restored_event.tags)


def run_phase4_tests():
    """Run all Phase 4 tests and report results."""
    print("🧪 Running Phase 4 Integration Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestPhase4Models,
        TestPhase4DataClasses,
        TestPhase4Integration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Report results
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All Phase 4 tests passed!")
        print(f"   Tests run: {result.testsRun}")
        print("🚀 Phase 4 is ready for production!")
    else:
        print("❌ Some Phase 4 tests failed!")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        
        if result.failures:
            print("\n📋 Failures:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\n🔥 Errors:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Setup Qt application for tests
    if not QCoreApplication.instance():
        app = QCoreApplication([])
    
    success = run_phase4_tests()
    sys.exit(0 if success else 1)