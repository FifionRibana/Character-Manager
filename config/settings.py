"""
Application settings and configuration.
"""

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class AppSettings:
    """Application settings."""
    language: str = "en"
    theme: str = "auto"
    autosave_interval: int = 30000  # milliseconds
    last_open_directory: str = ""
    window_geometry: str = ""
    
    def save(self, path: Path):
        """Save settings to file."""
        with open(path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
            
    @classmethod
    def load(cls, path: Path) -> 'AppSettings':
        """Load settings from file."""
        if path.exists():
            with open(path, 'r') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
