

from dataclasses import dataclass
from pathlib import Path

from data.enums import ImageFormat

@dataclass
class ImageData:
    """
    Data class representing an image and its base64 encoded content.
    
    Attributes:
        file_path: Path to the source image file
        base64_data: Base64 encoded string of the image content
        mime_type: MIME type of the image
        file_size: Size of the image file in bytes
        format: Image format (extension)
    """
    
    file_path: Path
    base64_data: str
    mime_type: str
    file_size: int
    format: ImageFormat