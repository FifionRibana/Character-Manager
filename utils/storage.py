"""
Storage management for character data.
Handles saving/loading characters in the project directory.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from models.character import Character
from models.enums import FileConstants, StorageKeys


class StorageManager:
    """Manages character file storage in the project directory."""
    
    def __init__(self):
        """Initialize storage manager and create necessary directories."""
        # Use project directory for storage, not user home
        self.base_dir = Path(__file__).parent.parent / FileConstants.DATA_DIR
        self.characters_dir = self.base_dir / FileConstants.CHARACTERS_DIR
        
        # Create directories if they don't exist
        self.characters_dir.mkdir(parents=True, exist_ok=True)
        
        # Track last saved state for each character
        self._last_saved: Dict[str, datetime] = {}
    
    def get_character_path(self, character_id: str) -> Path:
        """
        Get the file path for a character.
        
        Args:
            character_id: Character UUID
            
        Returns:
            Path to character JSON file
        """
        return self.characters_dir / f"{character_id}{FileConstants.FILE_EXTENSION}"
    
    def save_character(self, character: Character) -> Path:
        """
        Save a character to disk.
        
        Args:
            character: Character to save
            
        Returns:
            Path to saved file
        """
        file_path = self.get_character_path(character.id)
        
        # Create backup if file exists
        if file_path.exists():
            backup_path = file_path.with_suffix(FileConstants.BACKUP_EXTENSION)
            shutil.copy2(file_path, backup_path)
        
        try:
            # Save character data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    character.to_dict(),
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str  # Handle datetime serialization
                )
            
            # Update last saved timestamp
            self._last_saved[character.id] = character.updated_at
            
            return file_path
            
        except Exception as e:
            # Restore from backup if save failed
            backup_path = file_path.with_suffix(FileConstants.BACKUP_EXTENSION)
            if backup_path.exists():
                shutil.copy2(backup_path, file_path)
            raise e
    
    def load_character(self, character_id: str) -> Optional[Character]:
        """
        Load a character by ID.
        
        Args:
            character_id: Character UUID
            
        Returns:
            Character object or None if not found
        """
        file_path = self.get_character_path(character_id)
        
        if not file_path.exists():
            return None
        
        return self.load_character_from_file(file_path)
    
    def load_character_from_file(self, file_path: Path) -> Character:
        """
        Load a character from a specific file.
        
        Args:
            file_path: Path to character JSON file
            
        Returns:
            Character object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is invalid JSON
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        character = Character.from_dict(data)
        
        # Track last saved state
        self._last_saved[character.id] = character.updated_at
        
        return character
    
    def load_all_characters(self) -> List[Character]:
        """
        Load all characters from the characters directory.
        
        Returns:
            List of all characters
        """
        characters = []
        
        for file_path in self.characters_dir.glob(f"*{FileConstants.FILE_EXTENSION}"):
            try:
                character = self.load_character_from_file(file_path)
                print(character.stats)
                characters.append(character)
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")
        
        # Sort by name for consistent ordering
        characters.sort(key=lambda c: c.name.lower())
        print(len(characters))
        
        return characters
    
    def delete_character(self, character_id: str) -> bool:
        """
        Delete a character file.
        
        Args:
            character_id: Character UUID
            
        Returns:
            True if deleted, False if not found
        """
        file_path = self.get_character_path(character_id)
        
        if file_path.exists():
            # Create backup before deletion
            backup_path = file_path.with_suffix('.deleted')
            shutil.move(str(file_path), str(backup_path))
            
            # Remove from tracking
            if character_id in self._last_saved:
                del self._last_saved[character_id]
            
            return True
        
        return False
    
    def needs_save(self, character: Character) -> bool:
        """
        Check if a character has unsaved changes.
        
        Args:
            character: Character to check
            
        Returns:
            True if character has been modified since last save
        """
        if character.id not in self._last_saved:
            return True
        
        return character.updated_at > self._last_saved[character.id]
    
    def export_to_html(self, character: Character, output_path: Path):
        """
        Export character to HTML format.
        
        Args:
            character: Character to export
            output_path: Path for HTML file
        """
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{name} - Character Sheet</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .header {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    margin: 0;
                }}
                .level {{
                    color: #666;
                    font-size: 18px;
                }}
                .section {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #444;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                }}
                .stat {{
                    text-align: center;
                    padding: 10px;
                    background: #f9f9f9;
                    border-radius: 5px;
                }}
                .stat-name {{
                    font-weight: bold;
                    color: #666;
                    font-size: 12px;
                    text-transform: uppercase;
                }}
                .stat-value {{
                    font-size: 24px;
                    color: #333;
                    font-weight: bold;
                }}
                .enneagram {{
                    background: #f0f4ff;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
                .biography {{
                    white-space: pre-wrap;
                    line-height: 1.6;
                }}
                .relationships table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .relationships th, .relationships td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                }}
                .relationships th {{
                    background: #f5f5f5;
                    font-weight: bold;
                }}
                .timeline {{
                    border-left: 3px solid #4CAF50;
                    padding-left: 20px;
                    margin-left: 10px;
                }}
                .event {{
                    margin-bottom: 20px;
                    position: relative;
                }}
                .event::before {{
                    content: '';
                    position: absolute;
                    left: -26px;
                    top: 5px;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: #4CAF50;
                }}
                .event-date {{
                    color: #666;
                    font-size: 12px;
                }}
                .event-title {{
                    font-weight: bold;
                    margin: 5px 0;
                }}
                .affiliations {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                }}
                .affiliation {{
                    background: #e3f2fd;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{name}</h1>
                <div class="level">Level {level}</div>
            </div>
            
            <div class="section">
                <h2>Enneagram Profile</h2>
                <div class="enneagram">
                    <p><strong>Main Type:</strong> Type {enneagram_type} - {enneagram_name}</p>
                    <p><strong>Wing:</strong> {wing}</p>
                    <p><strong>Development Level:</strong> {development}/9</p>
                    <p><strong>Instinctual Stack:</strong> {instincts}</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Ability Scores</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-name">Strength</div>
                        <div class="stat-value">{str}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-name">Agility</div>
                        <div class="stat-value">{agi}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-name">Constitution</div>
                        <div class="stat-value">{con}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-name">Intelligence</div>
                        <div class="stat-value">{int}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-name">Wisdom</div>
                        <div class="stat-value">{wis}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-name">Charisma</div>
                        <div class="stat-value">{cha}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Biography</h2>
                <div class="biography">{biography}</div>
            </div>
            
            {affiliations_section}
            {relationships_section}
            {narrative_section}
            
            <div style="text-align: center; color: #999; margin-top: 40px; font-size: 12px;">
                Generated on {date} • Medieval Character Manager
            </div>
        </body>
        </html>
        """
        
        # Prepare Enneagram info
        enneagram_names = {
            1: "The Reformer", 2: "The Helper", 3: "The Achiever",
            4: "The Individualist", 5: "The Investigator", 6: "The Loyalist",
            7: "The Enthusiast", 8: "The Challenger", 9: "The Peacemaker"
        }
        
        # Prepare sections
        affiliations_html = ""
        if character.affiliations:
            affiliations_list = "".join([
                f'<div class="affiliation">{aff}</div>'
                for aff in character.affiliations
            ])
            affiliations_html = f"""
            <div class="section">
                <h2>Affiliations</h2>
                <div class="affiliations">{affiliations_list}</div>
            </div>
            """
        
        relationships_html = ""
        if character.relationships:
            rows = "".join([
                f"<tr><td>{rel.target_name}</td><td>{rel.relationship_type.value}</td><td>{rel.description}</td></tr>"
                for rel in character.relationships
            ])
            relationships_html = f"""
            <div class="section relationships">
                <h2>Relationships</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Character</th>
                            <th>Type</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """
        
        narrative_html = ""
        if character.narrative_events:
            events = "".join([
                f"""
                <div class="event">
                    <div class="event-date">{event.timestamp.strftime('%Y-%m-%d')}</div>
                    <div class="event-title">{event.title}</div>
                    <div>{event.description}</div>
                </div>
                """
                for event in sorted(character.narrative_events, key=lambda e: e.timestamp)
            ])
            narrative_html = f"""
            <div class="section">
                <h2>Narrative Timeline</h2>
                <div class="timeline">{events}</div>
            </div>
            """
        
        # Format HTML
        html = html_template.format(
            name=character.name,
            level=character.level,
            enneagram_type=character.enneagram.main_type,
            enneagram_name=enneagram_names.get(character.enneagram.main_type, ""),
            wing=character.enneagram.get_wing_notation(),
            development=character.enneagram.development_level,
            instincts=" / ".join([v.value.upper() for v in character.enneagram.instinctual_stack]),
            str=character.stats.strength,
            agi=character.stats.agility,
            con=character.stats.constitution,
            int=character.stats.intelligence,
            wis=character.stats.wisdom,
            cha=character.stats.charisma,
            biography=character.biography or "No biography written yet.",
            affiliations_section=affiliations_html,
            relationships_section=relationships_html,
            narrative_section=narrative_html,
            date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)