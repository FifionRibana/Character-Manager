"""
Drag and drop image widget for character portraits.
"""

import base64
from pathlib import Path
from PyQt6.QtWidgets import QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent

from utils.translator import tr


class ImageDropWidget(QLabel):
    """Widget for drag and drop image upload."""
    
    imageChanged = pyqtSignal(str)  # Emits base64 encoded image
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 200)
        self.setScaledContents(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
        """)
        self.setText(tr("drop_image"))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def mousePressEvent(self, event):
        """Open file dialog on click."""
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self, tr("select_image"), "", tr("images_filter")
            )
            if file_path:
                self.load_image(file_path)
                
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept image drag events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle dropped images."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_image(file_path)
            
    def load_image(self, file_path: str):
        """Load and display image."""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
            
            with open(file_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
                self.imageChanged.emit(image_data)
                
    def set_image_from_base64(self, data: str):
        """Load image from base64 data."""
        if data:
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(data))
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.setPixmap(scaled)
