"""
Image Base64 Loader Module

This module provides functionality to load image files and convert them to base64 strings.
It supports common image formats and provides type-safe operations.
"""

import base64
import mimetypes
from enum import StrEnum
from pathlib import Path
from typing import Dict, Union
import argparse

from utils.singleton import singleton

from .image_data import ImageData
from ..enums import ImageFormat


class SerializationKeys(StrEnum):
    """Keys used for serialization of image data."""
    
    FILE_PATH = "file_path"
    BASE64_DATA = "base64_data"
    MIME_TYPE = "mime_type"
    FILE_SIZE = "file_size"
    FORMAT = "format"



class ImageLoadError(Exception):
    """Custom exception raised when image loading fails."""
    pass

@singleton
class ImageBase64Loader:
    """
    A class to handle loading images and converting them to base64 strings.
    
    This class provides methods to load image files from disk and convert them
    to base64 encoded strings, along with metadata about the image.
    """
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"
    })
    
    # Maximum file size in bytes (10MB)
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    
    @classmethod
    def load_image_to_base64(cls, image_path: Union[str, Path]) -> ImageData:
        """
        Load an image file and convert it to base64.
        
        Args:
            image_path: Path to the image file (string or Path object)
            
        Returns:
            ImageData object containing the base64 string and metadata
            
        Raises:
            ImageLoadError: If the image cannot be loaded or processed
            FileNotFoundError: If the image file doesn't exist
            ValueError: If the file format is not supported
        """
        
        # Convert to Path object if needed
        path = Path(image_path) if isinstance(image_path, str) else image_path
        
        # Validate file exists
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")
        
        # Validate file is actually a file
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        # Validate file extension
        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {path.suffix}. "
                f"Supported formats: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
            )
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(
                f"File too large: {file_size} bytes. "
                f"Maximum allowed: {cls.MAX_FILE_SIZE} bytes"
            )
        
        try:
            # Read the image file in binary mode
            with path.open('rb') as image_file:
                image_content = image_file.read()
            
            # Encode to base64
            base64_encoded = base64.b64encode(image_content).decode('utf-8')
            
            # Determine MIME type
            mime_type = cls._get_mime_type(path)
            
            # Determine format
            image_format = cls._get_image_format(path)
            
            return ImageData(
                file_path=path,
                base64_data=base64_encoded,
                mime_type=mime_type,
                file_size=file_size,
                format=image_format
            )
            
        except Exception as e:
            raise ImageLoadError(f"Failed to load and encode image {path}: {str(e)}")
    
    @classmethod
    def _get_mime_type(cls, path: Path) -> str:
        """
        Get the MIME type of an image file.
        
        Args:
            path: Path to the image file
            
        Returns:
            MIME type string
        """
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type if mime_type else "application/octet-stream"
    
    @classmethod
    def _get_image_format(cls, path: Path) -> ImageFormat:
        """
        Get the image format from file extension.
        
        Args:
            path: Path to the image file
            
        Returns:
            ImageFormat enum value
        """
        extension = path.suffix.lower().lstrip('.')
        
        # Handle special case for JPEG
        if extension == "jpg":
            return ImageFormat.JPEG
        
        try:
            return ImageFormat(extension)
        except ValueError:
            # Fallback for unsupported formats
            return ImageFormat.JPEG
    
    @classmethod
    def create_data_url(cls, image_data: ImageData) -> str:
        """
        Create a data URL from ImageData.
        
        Args:
            image_data: ImageData object containing base64 data and metadata
            
        Returns:
            Data URL string that can be used in HTML/CSS
        """
        return f"data:{image_data.mime_type};base64,{image_data.base64_data}"
    
    @classmethod
    def serialize_image_data(cls, image_data: ImageData) -> Dict[str, Union[str, int]]:
        """
        Serialize ImageData to a dictionary using enum keys.
        
        Args:
            image_data: ImageData object to serialize
            
        Returns:
            Dictionary with serialized data
        """
        return {
            SerializationKeys.FILE_PATH: str(image_data.file_path),
            SerializationKeys.BASE64_DATA: image_data.base64_data,
            SerializationKeys.MIME_TYPE: image_data.mime_type,
            SerializationKeys.FILE_SIZE: image_data.file_size,
            SerializationKeys.FORMAT: image_data.format.value
        }


def main() -> None:
    """
    Main function to demonstrate usage of the ImageBase64Loader.
    """
    parser = argparse.ArgumentParser(
        description="Load an image file and convert it to base64"
    )
    parser.add_argument(
        "image_path",
        type=str,
        help="Path to the image file to convert"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional output file to save the base64 string"
    )
    parser.add_argument(
        "--data-url",
        action="store_true",
        help="Output as data URL instead of plain base64"
    )
    
    args = parser.parse_args()
    
    try:
        # Load the image
        image_data = ImageBase64Loader.load_image_to_base64(args.image_path)
        
        # Prepare output
        if args.data_url:
            output = ImageBase64Loader.create_data_url(image_data)
        else:
            output = image_data.base64_data
        
        # Output to file or console
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output, encoding='utf-8')
            print(f"Base64 data saved to: {output_path}")
        else:
            print(output)
        
        # Print metadata
        print(f"\nMetadata:", file=__import__('sys').stderr)
        print(f"File: {image_data.file_path}", file=__import__('sys').stderr)
        print(f"Format: {image_data.format.value}", file=__import__('sys').stderr)
        print(f"MIME Type: {image_data.mime_type}", file=__import__('sys').stderr)
        print(f"Size: {image_data.file_size} bytes", file=__import__('sys').stderr)
        
    except Exception as e:
        print(f"Error: {e}", file=__import__('sys').stderr)
        return


if __name__ == "__main__":
    main()


# Example usage:
if __name__ == "__example__":
    # Example of how to use the ImageBase64Loader
    
    try:
        # Load an image
        loader = ImageBase64Loader()
        image_data = loader.load_image_to_base64("example.jpg")
        
        # Get the base64 string
        base64_string = image_data.base64_data
        print(f"Base64 length: {len(base64_string)}")
        
        # Create a data URL for HTML usage
        data_url = loader.create_data_url(image_data)
        print(f"Data URL: {data_url[:100]}...")
        
        # Serialize for JSON storage
        serialized = loader.serialize_image_data(image_data)
        print(f"Serialized keys: {list(serialized.keys())}")
        
    except Exception as e:
        print(f"Example failed: {e}")