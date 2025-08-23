"""
controllers/image_controller.py
Image controller with properly initialized properties
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Dict
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt6.QtQml import QQmlEngine
from data.character import Character
from data.enums import FileConstants, FileExtension, Language
from data.image_handler.image_loader import ImageBase64Loader, ImageData
from models.character_model import CharacterModel
from models.character_list_model import CharacterListModel
from utils.singleton import singleton
from utils.translator import get_translator, tr

from .storage_controller import StorageController


@singleton
@dataclass
class ImageController(QObject):
    """Image controller for the application"""

    # Signals
    errorOccurred: ClassVar[pyqtSignal] = pyqtSignal(str, str)

    def __post_init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, result=str)
    def load_image_to_base64(self, image_path: str) -> str:
        safe_image_path = Path(image_path.removeprefix(r"file:///"))
        try:
            image_data = ImageBase64Loader().load_image_to_base64(safe_image_path)
            return str(image_data.base64_data)
        except Exception as e:
            print(f"Failed to load image: {str(e)}")
            self.errorOccurred.emit(
                "Image load error", f"Failed to load image: {str(e)}"
            )

            return ""
