"""
Export Controller for Medieval Character Manager
Handles exporting characters to various formats (PDF, HTML, JSON, Markdown)
"""

import json
import base64
from dataclasses import asdict
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Optional, Dict, Any, List
from io import BytesIO

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QFont, QColor
from PyQt6.QtPrintSupport import QPrinter

# Optional imports for advanced features
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class ExportFormat(StrEnum):
    """Available export formats"""
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    TEXT = "text"
    CSV = "csv"  # For timeline events
    
    
class ExportOptions(StrEnum):
    """Export content options"""
    INCLUDE_OVERVIEW = "include_overview"
    INCLUDE_ENNEAGRAM = "include_enneagram"
    INCLUDE_STATS = "include_stats"
    INCLUDE_BIOGRAPHY = "include_biography"
    INCLUDE_RELATIONSHIPS = "include_relationships"
    INCLUDE_TIMELINE = "include_timeline"
    INCLUDE_IMAGES = "include_images"
    COMPACT_FORMAT = "compact_format"
    DARK_THEME = "dark_theme"


class ExportController(QObject):
    """
    Controller for exporting character data to various formats
    Supports PDF, HTML, Markdown, JSON, and plain text
    """
    
    # Signals
    exportStarted = pyqtSignal(str)  # format
    exportProgress = pyqtSignal(int)  # percentage
    exportCompleted = pyqtSignal(str, str)  # format, filepath
    exportFailed = pyqtSignal(str, str)  # format, error
    
    def __init__(self, parent: Optional[QObject] = None):
        """Initialize export controller"""
        super().__init__(parent)
        
        self._current_export: Optional[Dict[str, Any]] = None
        self._export_dir = Path.home() / "Documents" / "MedievalCharacters"
        self._export_dir.mkdir(parents=True, exist_ok=True)
    
    @pyqtSlot(QObject, str, 'QVariant', result=str)
    def exportCharacter(self, character_model: QObject, format_type: str, 
                       options: Dict[str, bool]) -> str:
        """
        Export a character to specified format
        
        Args:
            character_model: CharacterModel QObject
            format_type: Export format from ExportFormat enum
            options: Dictionary of export options
            
        Returns:
            Path to exported file or empty string on failure
        """
        try:
            self.exportStarted.emit(format_type)
            
            # Prepare character data
            character_data = self._extract_character_data(character_model)
            
            # Generate filename
            safe_name = self._sanitize_filename(character_data.get("name", "character"))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export based on format
            if format_type == ExportFormat.PDF:
                filepath = self._export_to_pdf(character_data, safe_name, timestamp, options)
            elif format_type == ExportFormat.HTML:
                filepath = self._export_to_html(character_data, safe_name, timestamp, options)
            elif format_type == ExportFormat.MARKDOWN:
                filepath = self._export_to_markdown(character_data, safe_name, timestamp, options)
            elif format_type == ExportFormat.JSON:
                filepath = self._export_to_json(character_data, safe_name, timestamp, options)
            elif format_type == ExportFormat.TEXT:
                filepath = self._export_to_text(character_data, safe_name, timestamp, options)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
            
            self.exportCompleted.emit(format_type, str(filepath))
            return str(filepath)
            
        except Exception as e:
            self.exportFailed.emit(format_type, str(e))
            return ""
    
    @pyqtSlot('QVariantList', str, result=str)
    def exportMultipleCharacters(self, character_models: List[QObject], 
                                format_type: str) -> str:
        """
        Export multiple characters to a single file or archive
        
        Args:
            character_models: List of CharacterModel QObjects
            format_type: Export format
            
        Returns:
            Path to exported file/archive
        """
        try:
            self.exportStarted.emit(format_type)
            
            # Extract data for all characters
            all_characters = [
                self._extract_character_data(model) 
                for model in character_models
            ]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == ExportFormat.JSON:
                # Export all to single JSON
                filepath = self._export_dir / f"all_characters_{timestamp}.json"
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(all_characters, f, indent=2, ensure_ascii=False)
            else:
                # Create archive with individual files
                # TODO: Implement archive creation
                raise NotImplementedError("Archive export not yet implemented")
            
            self.exportCompleted.emit(format_type, str(filepath))
            return str(filepath)
            
        except Exception as e:
            self.exportFailed.emit(format_type, str(e))
            return ""
    
    @pyqtSlot(QObject, str, result=str)
    def exportTimeline(self, narrative_model: QObject, format_type: str) -> str:
        """
        Export timeline/narrative events to specified format
        
        Args:
            narrative_model: NarrativeModel QObject
            format_type: Export format (CSV, JSON, HTML)
            
        Returns:
            Path to exported file
        """
        try:
            self.exportStarted.emit(f"timeline_{format_type}")
            
            # Extract timeline data
            events = self._extract_timeline_data(narrative_model)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == ExportFormat.CSV:
                filepath = self._export_timeline_csv(events, timestamp)
            elif format_type == ExportFormat.JSON:
                filepath = self._export_timeline_json(events, timestamp)
            elif format_type == ExportFormat.HTML:
                filepath = self._export_timeline_html(events, timestamp)
            else:
                raise ValueError(f"Unsupported timeline export format: {format_type}")
            
            self.exportCompleted.emit(f"timeline_{format_type}", str(filepath))
            return str(filepath)
            
        except Exception as e:
            self.exportFailed.emit(f"timeline_{format_type}", str(e))
            return ""
    
    # Private export methods
    
    def _export_to_pdf(self, data: Dict[str, Any], name: str, 
                      timestamp: str, options: Dict[str, bool]) -> Path:
        """Export character data to PDF format"""
        filepath = self._export_dir / f"{name}_{timestamp}.pdf"
        
        # Create printer
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageSize(QPrinter.PageSize.A4)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(str(filepath))
        
        # Create document
        document = QTextDocument()
        cursor = QTextCursor(document)
        
        # Title
        title_format = QTextCharFormat()
        title_format.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        cursor.insertText(data.get("name", "Character"), title_format)
        cursor.insertBlock()
        cursor.insertBlock()
        
        # Include sections based on options
        if options.get(ExportOptions.INCLUDE_OVERVIEW, True):
            self._add_overview_section(cursor, data)
            self.exportProgress.emit(20)
        
        if options.get(ExportOptions.INCLUDE_ENNEAGRAM, True):
            self._add_enneagram_section(cursor, data)
            self.exportProgress.emit(40)
        
        if options.get(ExportOptions.INCLUDE_STATS, True):
            self._add_stats_section(cursor, data)
            self.exportProgress.emit(60)
        
        if options.get(ExportOptions.INCLUDE_BIOGRAPHY, True):
            self._add_biography_section(cursor, data)
            self.exportProgress.emit(70)
        
        if options.get(ExportOptions.INCLUDE_RELATIONSHIPS, True):
            self._add_relationships_section(cursor, data)
            self.exportProgress.emit(85)
        
        if options.get(ExportOptions.INCLUDE_TIMELINE, True):
            self._add_timeline_section(cursor, data)
            self.exportProgress.emit(95)
        
        # Print to PDF
        document.print(printer)
        self.exportProgress.emit(100)
        
        return filepath
    
    def _export_to_html(self, data: Dict[str, Any], name: str, 
                       timestamp: str, options: Dict[str, bool]) -> Path:
        """Export character data to HTML format"""
        filepath = self._export_dir / f"{name}_{timestamp}.html"
        
        # Build HTML content
        html_parts = [self._get_html_header(data.get("name", "Character"), options)]
        
        if options.get(ExportOptions.INCLUDE_OVERVIEW, True):
            html_parts.append(self._get_html_overview(data))
        
        if options.get(ExportOptions.INCLUDE_ENNEAGRAM, True):
            html_parts.append(self._get_html_enneagram(data))
        
        if options.get(ExportOptions.INCLUDE_STATS, True):
            html_parts.append(self._get_html_stats(data))
        
        if options.get(ExportOptions.INCLUDE_BIOGRAPHY, True):
            html_parts.append(self._get_html_biography(data))
        
        if options.get(ExportOptions.INCLUDE_RELATIONSHIPS, True):
            html_parts.append(self._get_html_relationships(data))
        
        if options.get(ExportOptions.INCLUDE_TIMELINE, True):
            html_parts.append(self._get_html_timeline(data))
        
        html_parts.append(self._get_html_footer())
        
        # Write HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))
        
        self.exportProgress.emit(100)
        return filepath
    
    def _export_to_markdown(self, data: Dict[str, Any], name: str, 
                           timestamp: str, options: Dict[str, bool]) -> Path:
        """Export character data to Markdown format"""
        filepath = self._export_dir / f"{name}_{timestamp}.md"
        
        md_parts = []
        
        # Title
        md_parts.append(f"# {data.get('name', 'Character')}\n")
        md_parts.append(f"*Exported on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        # Overview
        if options.get(ExportOptions.INCLUDE_OVERVIEW, True):
            md_parts.append("\n## Overview\n")
            md_parts.append(f"- **Level:** {data.get('level', 1)}")
            md_parts.append(f"- **Affiliations:** {', '.join(data.get('affiliations', [])) or 'None'}")
            md_parts.append(f"- **Tags:** {', '.join(data.get('tags', [])) or 'None'}")
            if data.get('biography'):
                md_parts.append(f"\n### Biography\n{data['biography']}")
            if data.get('notes'):
                md_parts.append(f"\n### Notes\n{data['notes']}")
        
        # Enneagram
        if options.get(ExportOptions.INCLUDE_ENNEAGRAM, True) and "enneagram" in data:
            md_parts.append("\n## Enneagram\n")
            ennea = data["enneagram"]
            md_parts.append(f"- **Core Type:** {ennea.get('core_type', 'Unknown')}")
            md_parts.append(f"- **Wing:** {ennea.get('wing', 'None')}")
            md_parts.append(f"- **Instinct:** {ennea.get('instinct', 'Unknown')}")
        
        # Stats
        if options.get(ExportOptions.INCLUDE_STATS, True) and "stats" in data:
            md_parts.append("\n## Statistics\n")
            for stat, value in data["stats"].items():
                md_parts.append(f"- **{stat.replace('_', ' ').title()}:** {value}/10")
        
        # Biography
        if options.get(ExportOptions.INCLUDE_BIOGRAPHY, True):
            md_parts.append("\n## Biography\n")
            
            if data.get("biography"):
                md_parts.append(f"{data['biography']}\n")
            
            if data.get("notes"):
                md_parts.append(f"### Additional Notes\n{data['notes']}\n")
            
            if data.get("affiliations"):
                md_parts.append(f"### Affiliations\n")
                for affiliation in data["affiliations"]:
                    md_parts.append(f"- {affiliation}")
        
        # Relationships
        if options.get(ExportOptions.INCLUDE_RELATIONSHIPS, True) and "relationships" in data:
            md_parts.append("\n## Relationships\n")
            for rel in data["relationships"]:
                md_parts.append(f"### {rel['target_name']} ({rel['type'].title()})")
                md_parts.append(f"- **Strength:** {rel['strength']}/10")
                if rel.get('description'):
                    md_parts.append(f"- {rel['description']}")
        
        # Timeline
        if options.get(ExportOptions.INCLUDE_TIMELINE, True) and "timeline" in data:
            md_parts.append("\n## Timeline\n")
            for event in data["timeline"]:
                md_parts.append(f"### {event['date']} - {event['title']}")
                if event.get('description'):
                    md_parts.append(event['description'])
                if event.get('tags'):
                    md_parts.append(f"*Tags: {', '.join(event['tags'])}*")
                md_parts.append("")
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_parts))
        
        self.exportProgress.emit(100)
        return filepath
    
    def _export_to_json(self, data: Dict[str, Any], name: str, 
                       timestamp: str, options: Dict[str, bool]) -> Path:
        """Export character data to JSON format"""
        filepath = self._export_dir / f"{name}_{timestamp}.json"
        
        # Filter data based on options
        export_data = {"name": data.get("name", "Character")}
        
        if options.get(ExportOptions.INCLUDE_OVERVIEW, True):
            for key in ["level", "affiliations", "tags"]:
                if key in data:
                    export_data[key] = data[key]
        
        if options.get(ExportOptions.INCLUDE_ENNEAGRAM, True) and "enneagram" in data:
            export_data["enneagram"] = data["enneagram"]
        
        if options.get(ExportOptions.INCLUDE_STATS, True) and "stats" in data:
            export_data["stats"] = data["stats"]
        
        if options.get(ExportOptions.INCLUDE_BIOGRAPHY, True):
            for key in ["biography", "notes", "affiliations", "tags"]:
                if key in data:
                    export_data[key] = data[key]
        
        if options.get(ExportOptions.INCLUDE_RELATIONSHIPS, True) and "relationships" in data:
            export_data["relationships"] = data["relationships"]
        
        if options.get(ExportOptions.INCLUDE_TIMELINE, True) and "timeline" in data:
            export_data["timeline"] = data["timeline"]
        
        # Add metadata
        export_data["_metadata"] = {
            "exported_at": datetime.now().isoformat(),
            "version": "2.0.0",
            "format": "MedievalCharacterManager"
        }
        
        # Write JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.exportProgress.emit(100)
        return filepath
    
    def _export_to_text(self, data: Dict[str, Any], name: str, 
                       timestamp: str, options: Dict[str, bool]) -> Path:
        """Export character data to plain text format"""
        filepath = self._export_dir / f"{name}_{timestamp}.txt"
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"CHARACTER: {data.get('name', 'Unknown')}")
        lines.append("=" * 60)
        lines.append("")
        
        # Add sections
        if options.get(ExportOptions.INCLUDE_OVERVIEW, True):
            lines.append("OVERVIEW")
            lines.append("-" * 20)
            lines.append(f"Level: {data.get('level', 1)}")
            lines.append(f"Affiliations: {', '.join(data.get('affiliations', [])) or 'None'}")
            lines.append(f"Tags: {', '.join(data.get('tags', [])) or 'None'}")
            lines.append("")
        
        # Additional sections...
        # (Similar to markdown but simpler formatting)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self.exportProgress.emit(100)
        return filepath
    
    def _export_timeline_csv(self, events: List[Dict[str, Any]], timestamp: str) -> Path:
        """Export timeline events to CSV format"""
        import csv
        
        filepath = self._export_dir / f"timeline_{timestamp}.csv"
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['date', 'title', 'type', 'importance', 'description', 'tags']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for event in events:
                writer.writerow({
                    'date': event.get('date', ''),
                    'title': event.get('title', ''),
                    'type': event.get('type', ''),
                    'importance': event.get('importance', 5),
                    'description': event.get('description', ''),
                    'tags': ', '.join(event.get('tags', []))
                })
        
        return filepath
    
    def _export_timeline_json(self, events: List[Dict[str, Any]], timestamp: str) -> Path:
        """Export timeline events to JSON format"""
        filepath = self._export_dir / f"timeline_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timeline": events,
                "_metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_events": len(events)
                }
            }, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _export_timeline_html(self, events: List[Dict[str, Any]], timestamp: str) -> Path:
        """Export timeline events to HTML format"""
        filepath = self._export_dir / f"timeline_{timestamp}.html"
        
        html = self._get_html_header("Character Timeline", {})
        html += "<div class='timeline'>\n"
        
        for event in events:
            html += f"""
            <div class='timeline-event'>
                <div class='event-date'>{event.get('date', 'Unknown')}</div>
                <div class='event-content'>
                    <h3>{event.get('title', 'Untitled')}</h3>
                    <p>{event.get('description', '')}</p>
                    <div class='event-tags'>{', '.join(event.get('tags', []))}</div>
                </div>
            </div>
            """
        
        html += "</div>\n"
        html += self._get_html_footer()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    # Helper methods
    
    def _extract_character_data(self, character_model: QObject) -> Dict[str, Any]:
        """Extract character data from CharacterModel QObject"""
        # Access the internal character object directly
        if hasattr(character_model, '_character'):
            char = character_model._character
            
            # Build data dictionary with actual Character attributes
            data = {
                "name": char.name if hasattr(char, 'name') else "Unknown",
                "level": char.level if hasattr(char, 'level') else 1,
                "biography": char.biography if hasattr(char, 'biography') else "",
                "notes": char.notes if hasattr(char, 'notes') else "",
                "affiliations": char.affiliations if hasattr(char, 'affiliations') else [],
                "tags": char.tags if hasattr(char, 'tags') else [],
            }
            
            # Add stats if present
            if hasattr(char, 'stats'):
                data["stats"] = {
                    "strength": char.stats.strength,
                    "agility": char.stats.agility,
                    "constitution": char.stats.constitution,
                    "intelligence": char.stats.intelligence,
                    "wisdom": char.stats.wisdom,
                    "charisma": char.stats.charisma
                }
            
            # Add enneagram if present
            if hasattr(char, 'enneagram'):
                data["enneagram"] = {
                    "core_type": char.enneagram.core_type.value if char.enneagram.core_type else None,
                    "wing": char.enneagram.wing.value if char.enneagram.wing else None,
                    "instinct": char.enneagram.instinct.value if char.enneagram.instinct else None
                }
            
            # Add relationships if present
            if hasattr(char, 'relationships'):
                data["relationships"] = char.relationships
            elif hasattr(char_model, 'relationshipModel'):
                # Try to get from relationship model
                data["relationships"] = []
            
            # Add timeline/narrative events if present
            if hasattr(char, 'narrative_events'):
                data["timeline"] = [
                    {
                        "date": event.date,
                        "title": event.title,
                        "description": event.description,
                        "importance": event.importance,
                        "tags": event.tags,
                        "type": "event"
                    }
                    for event in char.narrative_events
                ]
            elif hasattr(char, 'timeline'):
                data["timeline"] = char.timeline
            
            return data
        else:
            # Fallback: try to get properties directly from model
            return {
                "name": character_model.property("name") if character_model else "Unknown",
                "level": character_model.property("level") if character_model else 1,
                "biography": character_model.property("biography") if character_model else "",
                "notes": character_model.property("notes") if character_model else "",
            }
    
    def _extract_timeline_data(self, narrative_model: QObject) -> List[Dict[str, Any]]:
        """Extract timeline data from NarrativeModel QObject"""
        # Check if the model has internal narrative events
        if hasattr(narrative_model, '_events'):
            return narrative_model._events
        elif hasattr(narrative_model, 'events'):
            return narrative_model.events
        else:
            # Return empty list if no events found
            return []
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename for safe file system usage"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name[:50]  # Limit length
    
    def _get_html_header(self, title: str, options: Dict[str, bool]) -> str:
        """Generate HTML header with styles"""
        dark_mode = options.get(ExportOptions.DARK_THEME, False)
        
        bg_color = "#1e1e1e" if dark_mode else "#ffffff"
        text_color = "#ffffff" if dark_mode else "#000000"
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: {bg_color};
            color: {text_color};
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        h1, h2, h3 {{
            color: {text_color};
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: {'#2a2a2a' if dark_mode else '#f5f5f5'};
            border-radius: 8px;
        }}
        .stat-bar {{
            background: {'#444' if dark_mode else '#ddd'};
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 5px 0;
        }}
        .stat-fill {{
            background: #4CAF50;
            height: 100%;
            transition: width 0.3s;
        }}
    </style>
</head>
<body>
        """
    
    def _get_html_footer(self) -> str:
        """Generate HTML footer"""
        return """
</body>
</html>
        """
    
    def _get_html_overview(self, data: Dict[str, Any]) -> str:
        """Generate HTML overview section"""
        return f"""
<div class="section">
    <h2>Overview</h2>
    <p><strong>Name:</strong> {data.get('name', 'Unknown')}</p>
    <p><strong>Level:</strong> {data.get('level', 1)}</p>
    <p><strong>Affiliations:</strong> {', '.join(data.get('affiliations', [])) or 'None'}</p>
    <p><strong>Tags:</strong> {', '.join(data.get('tags', [])) or 'None'}</p>
</div>
        """
    
    def _get_html_enneagram(self, data: Dict[str, Any]) -> str:
        """Generate HTML enneagram section"""
        if "enneagram" not in data:
            return ""
        
        ennea = data["enneagram"]
        return f"""
<div class="section">
    <h2>Enneagram</h2>
    <p><strong>Core Type:</strong> {ennea.get('core_type', 'Unknown')}</p>
    <p><strong>Wing:</strong> {ennea.get('wing', 'None')}</p>
    <p><strong>Instinct:</strong> {ennea.get('instinct', 'Unknown')}</p>
</div>
        """
    
    def _get_html_stats(self, data: Dict[str, Any]) -> str:
        """Generate HTML stats section"""
        if "stats" not in data:
            return ""
        
        html = '<div class="section"><h2>Statistics</h2>'
        
        for stat, value in data["stats"].items():
            percentage = (value / 10) * 100
            html += f"""
            <div>
                <label>{stat.replace('_', ' ').title()}: {value}/10</label>
                <div class="stat-bar">
                    <div class="stat-fill" style="width: {percentage}%"></div>
                </div>
            </div>
            """
        
        html += '</div>'
        return html
    
    def _get_html_biography(self, data: Dict[str, Any]) -> str:
        """Generate HTML biography section"""
        html = '<div class="section"><h2>Biography</h2>'
        
        if data.get("biography"):
            html += f"<p>{data['biography']}</p>"
        
        if data.get("notes"):
            html += f"<h3>Notes</h3><p>{data['notes']}</p>"
        
        if data.get("affiliations"):
            html += "<h3>Affiliations</h3><ul>"
            for affiliation in data.get("affiliations", []):
                html += f"<li>{affiliation}</li>"
            html += "</ul>"
        
        html += '</div>'
        return html
    
    def _get_html_relationships(self, data: Dict[str, Any]) -> str:
        """Generate HTML relationships section"""
        if "relationships" not in data or not data["relationships"]:
            return ""
        
        html = '<div class="section"><h2>Relationships</h2>'
        
        for rel in data["relationships"]:
            html += f"""
            <div style="margin-bottom: 15px;">
                <strong>{rel['target_name']}</strong> ({rel['type'].title()})
                <br>Strength: {rel['strength']}/10
                {f"<br>{rel['description']}" if rel.get('description') else ""}
            </div>
            """
        
        html += '</div>'
        return html
    
    def _get_html_timeline(self, data: Dict[str, Any]) -> str:
        """Generate HTML timeline section"""
        if "timeline" not in data or not data["timeline"]:
            return ""
        
        html = '<div class="section"><h2>Timeline</h2>'
        
        for event in data["timeline"]:
            html += f"""
            <div style="margin-bottom: 20px;">
                <strong>{event['date']}</strong> - {event['title']}
                {f"<br>{event['description']}" if event.get('description') else ""}
                {f"<br><em>Tags: {', '.join(event['tags'])}</em>" if event.get('tags') else ""}
            </div>
            """
        
        html += '</div>'
        return html
    
    # Document building helpers for PDF
    
    def _add_overview_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add overview section to PDF document"""
        # Section header
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Overview", header_format)
        cursor.insertBlock()
        
        # Content
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        cursor.insertText(f"Name: {data.get('name', 'Unknown')}\n", normal_format)
        cursor.insertText(f"Level: {data.get('level', 1)}\n", normal_format)
        cursor.insertText(f"Affiliations: {', '.join(data.get('affiliations', [])) or 'None'}\n", normal_format)
        cursor.insertText(f"Tags: {', '.join(data.get('tags', [])) or 'None'}\n", normal_format)
        cursor.insertBlock()
    
    def _add_enneagram_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add enneagram section to PDF document"""
        if "enneagram" not in data:
            return
        
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Enneagram", header_format)
        cursor.insertBlock()
        
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        ennea = data["enneagram"]
        cursor.insertText(f"Core Type: {ennea.get('core_type', 'Unknown')}\n", normal_format)
        cursor.insertText(f"Wing: {ennea.get('wing', 'None')}\n", normal_format)
        cursor.insertText(f"Instinct: {ennea.get('instinct', 'Unknown')}\n", normal_format)
        cursor.insertBlock()
    
    def _add_stats_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add stats section to PDF document"""
        if "stats" not in data:
            return
        
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Statistics", header_format)
        cursor.insertBlock()
        
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        for stat, value in data["stats"].items():
            cursor.insertText(f"{stat.replace('_', ' ').title()}: {value}/10\n", normal_format)
        cursor.insertBlock()
    
    def _add_biography_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add biography section to PDF document"""
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Biography", header_format)
        cursor.insertBlock()
        
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        if data.get("biography"):
            cursor.insertText(f"{data['biography']}\n\n", normal_format)
        
        if data.get("notes"):
            cursor.insertText("Notes:\n", normal_format)
            cursor.insertText(f"{data['notes']}\n\n", normal_format)
        
        if data.get("affiliations"):
            cursor.insertText("Affiliations:\n", normal_format)
            for affiliation in data.get("affiliations", []):
                cursor.insertText(f"• {affiliation}\n", normal_format)
        
        cursor.insertBlock()
    
    def _add_relationships_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add relationships section to PDF document"""
        if "relationships" not in data or not data["relationships"]:
            return
        
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Relationships", header_format)
        cursor.insertBlock()
        
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        for rel in data["relationships"]:
            cursor.insertText(f"{rel['target_name']} ({rel['type'].title()})\n", normal_format)
            cursor.insertText(f"Strength: {rel['strength']}/10\n", normal_format)
            if rel.get('description'):
                cursor.insertText(f"{rel['description']}\n", normal_format)
            cursor.insertBlock()
    
    def _add_timeline_section(self, cursor: QTextCursor, data: Dict[str, Any]) -> None:
        """Add timeline section to PDF document"""
        if "timeline" not in data or not data["timeline"]:
            return
        
        header_format = QTextCharFormat()
        header_format.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cursor.insertText("Timeline", header_format)
        cursor.insertBlock()
        
        normal_format = QTextCharFormat()
        normal_format.setFont(QFont("Arial", 11))
        
        for event in data["timeline"]:
            cursor.insertText(f"{event['date']} - {event['title']}\n", normal_format)
            if event.get('description'):
                cursor.insertText(f"{event['description']}\n", normal_format)
            if event.get('tags'):
                cursor.insertText(f"Tags: {', '.join(event['tags'])}\n", normal_format)
            cursor.insertBlock()