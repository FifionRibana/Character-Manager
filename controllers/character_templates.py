"""
Character Templates Controller for Medieval Character Manager
Provides pre-defined character archetypes and templates for quick creation
"""

import json
from dataclasses import dataclass, field, asdict
from enum import StrEnum
from pathlib import Path
from typing import Dict, List, Optional, Any

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty

from data.character import Character
from data.enums import Archetype, Affinity, Gender, EnneagramType, Wing, Instinct


class TemplateCategory(StrEnum):
    """Categories for character templates"""
    HERO = "hero"
    VILLAIN = "villain"
    SUPPORT = "support"
    NEUTRAL = "neutral"
    CUSTOM = "custom"


@dataclass
class CharacterTemplate:
    """Character template definition"""
    id: str
    name: str
    category: TemplateCategory
    description: str
    
    # Basic attributes
    archetype: Archetype
    age_range: tuple[int, int] = (20, 40)
    gender_preference: Optional[Gender] = None
    
    # Personality traits
    enneagram_type: Optional[EnneagramType] = None
    enneagram_wing: Optional[Wing] = None
    enneagram_instinct: Optional[Instinct] = None
    
    # Stats template (0-10 scale)
    stat_template: Dict[str, int] = field(default_factory=dict)
    
    # Affinity preferences
    affinity_preferences: List[Affinity] = field(default_factory=list)
    
    # Biography templates
    background_template: str = ""
    personality_template: str = ""
    motivations_template: str = ""
    goals_template: str = ""
    conflicts_template: str = ""
    
    # Common relationships
    suggested_relationships: List[Dict[str, str]] = field(default_factory=list)
    
    # Starting events for timeline
    starting_events: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    author: str = "System"
    version: str = "1.0.0"
    custom: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary for storage"""
        data = asdict(self)
        data["archetype"] = self.archetype.value if self.archetype else None
        data["category"] = self.category.value
        data["gender_preference"] = self.gender_preference.value if self.gender_preference else None
        data["enneagram_type"] = self.enneagram_type.value if self.enneagram_type else None
        data["enneagram_wing"] = self.enneagram_wing.value if self.enneagram_wing else None
        data["enneagram_instinct"] = self.enneagram_instinct.value if self.enneagram_instinct else None
        data["affinity_preferences"] = [a.value for a in self.affinity_preferences]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterTemplate":
        """Create template from dictionary"""
        # Convert enums back
        if data.get("archetype"):
            data["archetype"] = Archetype(data["archetype"])
        if data.get("category"):
            data["category"] = TemplateCategory(data["category"])
        if data.get("gender_preference"):
            data["gender_preference"] = Gender(data["gender_preference"])
        if data.get("enneagram_type"):
            data["enneagram_type"] = EnneagramType(data["enneagram_type"])
        if data.get("enneagram_wing"):
            data["enneagram_wing"] = Wing(data["enneagram_wing"])
        if data.get("enneagram_instinct"):
            data["enneagram_instinct"] = Instinct(data["enneagram_instinct"])
        if data.get("affinity_preferences"):
            data["affinity_preferences"] = [Affinity(a) for a in data["affinity_preferences"]]
        
        return cls(**data)


class CharacterTemplateController(QObject):
    """
    Controller for managing character templates
    Provides built-in templates and custom template management
    """
    
    # Signals
    templatesChanged = pyqtSignal()
    templateApplied = pyqtSignal(str)  # template_id
    templateCreated = pyqtSignal(str)  # template_id
    templateDeleted = pyqtSignal(str)  # template_id
    
    def __init__(self, parent: Optional[QObject] = None):
        """Initialize template controller with built-in templates"""
        super().__init__(parent)
        
        self._templates: Dict[str, CharacterTemplate] = {}
        self._custom_templates_path = Path.home() / ".medieval_character_manager" / "templates"
        
        # Initialize built-in templates
        self._init_builtin_templates()
        
        # Load custom templates
        self._load_custom_templates()
    
    def _init_builtin_templates(self) -> None:
        """Initialize built-in character templates"""
        
        # Noble Knight Template
        knight = CharacterTemplate(
            id="noble_knight",
            name="Noble Knight",
            category=TemplateCategory.HERO,
            description="A valiant knight sworn to protect the innocent",
            archetype=Archetype.HERO,
            age_range=(25, 35),
            enneagram_type=EnneagramType.ONE,
            enneagram_wing=Wing.TWO,
            enneagram_instinct=Instinct.SOCIAL,
            stat_template={
                "strength": 8,
                "dexterity": 6,
                "constitution": 7,
                "intelligence": 5,
                "wisdom": 6,
                "charisma": 7,
                "combat_skill": 9,
                "magic_power": 2,
                "stealth": 3,
                "diplomacy": 6
            },
            affinity_preferences=[Affinity.LAWFUL, Affinity.GOOD],
            background_template="Born into nobility, {name} was trained from youth in the arts of combat and chivalry.",
            personality_template="Honor-bound and courageous, with a strong sense of justice and duty to protect the weak.",
            motivations_template="To uphold the knightly code, protect the innocent, and bring justice to the land.",
            goals_template="Become a legendary hero whose deeds inspire future generations.",
            conflicts_template="Struggles between personal desires and sworn oaths of duty.",
            suggested_relationships=[
                {"type": "mentor", "name": "Veteran Knight Commander", "description": "Taught the ways of chivalry"},
                {"type": "ally", "name": "Fellow Knights", "description": "Brothers and sisters in arms"},
                {"type": "romantic", "name": "Noble's Child", "description": "Forbidden love across social boundaries"}
            ],
            starting_events=[
                {"date": "Age 7", "title": "Page Training Begins", "type": "milestone"},
                {"date": "Age 14", "title": "Becomes Squire", "type": "milestone"},
                {"date": "Age 21", "title": "Knighted", "type": "achievement"}
            ],
            tags=["combat", "nobility", "honor", "hero"]
        )
        self._templates[knight.id] = knight
        
        # Dark Sorcerer Template
        sorcerer = CharacterTemplate(
            id="dark_sorcerer",
            name="Dark Sorcerer",
            category=TemplateCategory.VILLAIN,
            description="A powerful mage who has delved too deep into forbidden magic",
            archetype=Archetype.MAGE,
            age_range=(30, 50),
            enneagram_type=EnneagramType.FIVE,
            enneagram_wing=Wing.FOUR,
            enneagram_instinct=Instinct.SELF_PRESERVATION,
            stat_template={
                "strength": 3,
                "dexterity": 5,
                "constitution": 4,
                "intelligence": 9,
                "wisdom": 7,
                "charisma": 6,
                "combat_skill": 2,
                "magic_power": 10,
                "stealth": 6,
                "diplomacy": 4
            },
            affinity_preferences=[Affinity.CHAOTIC, Affinity.EVIL],
            background_template="Once a promising scholar, {name} discovered ancient tomes that corrupted their soul.",
            personality_template="Brilliant but twisted, consumed by the pursuit of forbidden knowledge and power.",
            motivations_template="To unlock the ultimate secrets of magic, regardless of the cost.",
            goals_template="Achieve immortality and reshape the world according to their dark vision.",
            conflicts_template="The remnants of humanity fighting against the corruption of dark magic.",
            suggested_relationships=[
                {"type": "enemy", "name": "Former Mentor", "description": "Betrayed and left for dead"},
                {"type": "student", "name": "Dark Apprentice", "description": "Teaching forbidden arts"},
                {"type": "rival", "name": "Court Wizard", "description": "Competing for magical supremacy"}
            ],
            starting_events=[
                {"date": "Age 15", "title": "Enters Magic Academy", "type": "milestone"},
                {"date": "Age 25", "title": "Discovers Dark Tome", "type": "discovery"},
                {"date": "Age 30", "title": "First Dark Ritual", "type": "tragedy"}
            ],
            tags=["magic", "villain", "knowledge", "corruption"]
        )
        self._templates[sorcerer.id] = sorcerer
        
        # Cunning Rogue Template
        rogue = CharacterTemplate(
            id="cunning_rogue",
            name="Cunning Rogue",
            category=TemplateCategory.NEUTRAL,
            description="A skilled thief and spy who lives in the shadows",
            archetype=Archetype.ROGUE,
            age_range=(20, 30),
            enneagram_type=EnneagramType.SEVEN,
            enneagram_wing=Wing.EIGHT,
            enneagram_instinct=Instinct.SELF_PRESERVATION,
            stat_template={
                "strength": 5,
                "dexterity": 9,
                "constitution": 5,
                "intelligence": 7,
                "wisdom": 6,
                "charisma": 8,
                "combat_skill": 6,
                "magic_power": 2,
                "stealth": 10,
                "diplomacy": 7
            },
            affinity_preferences=[Affinity.CHAOTIC, Affinity.NEUTRAL],
            background_template="Growing up on the streets, {name} learned to survive through wit and cunning.",
            personality_template="Charming and quick-witted, always looking for the next opportunity.",
            motivations_template="Freedom, wealth, and the thrill of the perfect heist.",
            goals_template="Pull off the greatest heist in history and retire in luxury.",
            conflicts_template="Loyalty to the guild versus personal gain.",
            suggested_relationships=[
                {"type": "ally", "name": "Thieves Guild", "description": "Fellow rogues and contacts"},
                {"type": "rival", "name": "City Guard Captain", "description": "Cat and mouse game"},
                {"type": "friend", "name": "Tavern Owner", "description": "Information broker"}
            ],
            starting_events=[
                {"date": "Age 10", "title": "First Theft", "type": "milestone"},
                {"date": "Age 16", "title": "Joins Thieves Guild", "type": "achievement"},
                {"date": "Age 22", "title": "Big Score", "type": "achievement"}
            ],
            tags=["stealth", "thief", "cunning", "neutral"]
        )
        self._templates[rogue.id] = rogue
        
        # Wise Sage Template
        sage = CharacterTemplate(
            id="wise_sage",
            name="Wise Sage",
            category=TemplateCategory.SUPPORT,
            description="An elderly scholar with vast knowledge and wisdom",
            archetype=Archetype.SAGE,
            age_range=(50, 70),
            enneagram_type=EnneagramType.NINE,
            enneagram_wing=Wing.ONE,
            enneagram_instinct=Instinct.SOCIAL,
            stat_template={
                "strength": 2,
                "dexterity": 3,
                "constitution": 3,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 6,
                "combat_skill": 1,
                "magic_power": 7,
                "stealth": 2,
                "diplomacy": 8
            },
            affinity_preferences=[Affinity.LAWFUL, Affinity.NEUTRAL],
            background_template="After decades of study, {name} has become a repository of ancient knowledge.",
            personality_template="Patient and wise, preferring to guide others rather than act directly.",
            motivations_template="To preserve knowledge and guide the next generation.",
            goals_template="Complete the great work - a comprehensive tome of all knowledge.",
            conflicts_template="The burden of knowledge versus the desire for peace.",
            suggested_relationships=[
                {"type": "mentor", "name": "Young Heroes", "description": "Guiding the next generation"},
                {"type": "friend", "name": "Fellow Scholars", "description": "Academic colleagues"},
                {"type": "student", "name": "Eager Apprentice", "description": "Passing on knowledge"}
            ],
            starting_events=[
                {"date": "Age 20", "title": "Completes Studies", "type": "achievement"},
                {"date": "Age 35", "title": "Great Discovery", "type": "discovery"},
                {"date": "Age 50", "title": "Becomes Master", "type": "achievement"}
            ],
            tags=["wisdom", "knowledge", "mentor", "support"]
        )
        self._templates[sage.id] = sage
        
        # Brave Warrior Template
        warrior = CharacterTemplate(
            id="brave_warrior",
            name="Brave Warrior",
            category=TemplateCategory.HERO,
            description="A fierce warrior who lives for battle and glory",
            archetype=Archetype.WARRIOR,
            age_range=(25, 40),
            enneagram_type=EnneagramType.EIGHT,
            enneagram_wing=Wing.SEVEN,
            enneagram_instinct=Instinct.SEXUAL,
            stat_template={
                "strength": 10,
                "dexterity": 6,
                "constitution": 9,
                "intelligence": 4,
                "wisdom": 5,
                "charisma": 6,
                "combat_skill": 10,
                "magic_power": 1,
                "stealth": 2,
                "diplomacy": 3
            },
            affinity_preferences=[Affinity.CHAOTIC, Affinity.GOOD],
            background_template="Born in the northern tribes, {name} was raised to be a warrior from birth.",
            personality_template="Fierce and proud, with an unbreakable will and loyalty to companions.",
            motivations_template="To die gloriously in battle and earn a place in the warrior's afterlife.",
            goals_template="Become the greatest warrior of the age.",
            conflicts_template="The call of battle versus the needs of peace.",
            suggested_relationships=[
                {"type": "ally", "name": "Battle Brothers", "description": "Warriors who fight alongside"},
                {"type": "rival", "name": "Enemy Champion", "description": "Worthy opponent"},
                {"type": "romantic", "name": "Shield Maiden", "description": "Equal in battle and love"}
            ],
            starting_events=[
                {"date": "Age 13", "title": "First Battle", "type": "battle"},
                {"date": "Age 18", "title": "Earns Name", "type": "achievement"},
                {"date": "Age 25", "title": "Legendary Duel", "type": "battle"}
            ],
            tags=["combat", "warrior", "strength", "glory"]
        )
        self._templates[warrior.id] = warrior
    
    def _load_custom_templates(self) -> None:
        """Load custom templates from user directory"""
        if not self._custom_templates_path.exists():
            self._custom_templates_path.mkdir(parents=True, exist_ok=True)
            return
        
        for template_file in self._custom_templates_path.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template = CharacterTemplate.from_dict(template_data)
                    template.custom = True
                    self._templates[template.id] = template
            except Exception as e:
                print(f"Error loading custom template {template_file}: {e}")
    
    @pyqtSlot(str, result=Character)
    def applyTemplate(self, template_id: str) -> Optional[Character]:
        """
        Apply a template to create a new character
        
        Args:
            template_id: ID of the template to apply
            
        Returns:
            New Character instance with template applied
        """
        if template_id not in self._templates:
            return None
        
        template = self._templates[template_id]
        
        # Create new character
        character = Character(name="New " + template.name)
        
        # Apply basic attributes
        character.archetype = template.archetype.value if template.archetype else ""
        
        # Random age within range
        import random
        character.age = random.randint(*template.age_range)
        
        # Apply gender if specified
        if template.gender_preference:
            character.gender = template.gender_preference.value
        
        # Apply enneagram
        if template.enneagram_type:
            character.enneagram.core_type = template.enneagram_type
        if template.enneagram_wing:
            character.enneagram.wing = template.enneagram_wing
        if template.enneagram_instinct:
            character.enneagram.instinct = template.enneagram_instinct
        
        # Apply stats
        for stat_name, value in template.stat_template.items():
            if hasattr(character.stats, stat_name):
                setattr(character.stats, stat_name, value)
        
        # Apply affinities
        if template.affinity_preferences:
            character.affinities = [a.value for a in template.affinity_preferences]
        
        # Apply biography templates (replace {name} placeholder)
        character.background = template.background_template.replace("{name}", character.name)
        character.personality = template.personality_template.replace("{name}", character.name)
        character.motivations = template.motivations_template.replace("{name}", character.name)
        character.goals = template.goals_template.replace("{name}", character.name)
        character.conflicts = template.conflicts_template.replace("{name}", character.name)
        
        # Note: Relationships and events should be added through their respective models
        # after character creation
        
        self.templateApplied.emit(template_id)
        return character
    
    @pyqtSlot(Character, str, result=bool)
    def createTemplateFromCharacter(self, character: Character, template_name: str) -> bool:
        """
        Create a custom template from an existing character
        
        Args:
            character: Character to use as template base
            template_name: Name for the new template
            
        Returns:
            True if template was created successfully
        """
        try:
            # Generate template ID
            template_id = template_name.lower().replace(" ", "_")
            
            # Create template from character
            template = CharacterTemplate(
                id=template_id,
                name=template_name,
                category=TemplateCategory.CUSTOM,
                description=f"Custom template based on {character.name}",
                archetype=Archetype(character.archetype) if character.archetype else Archetype.HERO,
                age_range=(max(character.age - 5, 18), character.age + 5),
                gender_preference=Gender(character.gender) if character.gender else None,
                enneagram_type=character.enneagram.core_type,
                enneagram_wing=character.enneagram.wing,
                enneagram_instinct=character.enneagram.instinct,
                stat_template={
                    "strength": character.stats.strength,
                    "dexterity": character.stats.dexterity,
                    "constitution": character.stats.constitution,
                    "intelligence": character.stats.intelligence,
                    "wisdom": character.stats.wisdom,
                    "charisma": character.stats.charisma,
                    "combat_skill": character.stats.combat_skill,
                    "magic_power": character.stats.magic_power,
                    "stealth": character.stats.stealth,
                    "diplomacy": character.stats.diplomacy
                },
                affinity_preferences=[Affinity(a) for a in character.affinities if a],
                background_template=character.background or "",
                personality_template=character.personality or "",
                motivations_template=character.motivations or "",
                goals_template=character.goals or "",
                conflicts_template=character.conflicts or "",
                custom=True
            )
            
            # Save template
            self._templates[template_id] = template
            
            # Save to file
            template_file = self._custom_templates_path / f"{template_id}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template.to_dict(), f, indent=2)
            
            self.templateCreated.emit(template_id)
            self.templatesChanged.emit()
            return True
            
        except Exception as e:
            print(f"Error creating template: {e}")
            return False
    
    @pyqtSlot(str, result=bool)
    def deleteTemplate(self, template_id: str) -> bool:
        """
        Delete a custom template
        
        Args:
            template_id: ID of template to delete
            
        Returns:
            True if deletion was successful
        """
        if template_id not in self._templates:
            return False
        
        template = self._templates[template_id]
        
        # Can only delete custom templates
        if not template.custom:
            return False
        
        # Delete file
        template_file = self._custom_templates_path / f"{template_id}.json"
        if template_file.exists():
            template_file.unlink()
        
        # Remove from memory
        del self._templates[template_id]
        
        self.templateDeleted.emit(template_id)
        self.templatesChanged.emit()
        return True
    
    @pyqtProperty('QVariantList', notify=templatesChanged)
    def availableTemplates(self) -> List[Dict[str, Any]]:
        """Get list of available templates with metadata"""
        return [
            {
                "id": template.id,
                "name": template.name,
                "category": template.category.value,
                "description": template.description,
                "custom": template.custom,
                "tags": template.tags
            }
            for template in self._templates.values()
        ]
    
    @pyqtSlot(str, result='QVariant')
    def getTemplate(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get full template data by ID"""
        if template_id in self._templates:
            return self._templates[template_id].to_dict()
        return None
    
    @pyqtSlot(str, result='QVariantList')
    def getTemplatesByCategory(self, category: str) -> List[Dict[str, Any]]:
        """Get templates filtered by category"""
        try:
            cat = TemplateCategory(category)
            return [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "custom": t.custom
                }
                for t in self._templates.values()
                if t.category == cat
            ]
        except ValueError:
            return []
    
    @pyqtSlot(str, result='QVariantList')
    def searchTemplates(self, search_term: str) -> List[Dict[str, Any]]:
        """Search templates by name, description, or tags"""
        search_lower = search_term.lower()
        results = []
        
        for template in self._templates.values():
            if (search_lower in template.name.lower() or
                search_lower in template.description.lower() or
                any(search_lower in tag for tag in template.tags)):
                
                results.append({
                    "id": template.id,
                    "name": template.name,
                    "category": template.category.value,
                    "description": template.description,
                    "custom": template.custom
                })
        
        return results