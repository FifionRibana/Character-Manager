
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import StrEnum, IntEnum, auto
import base64

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QStackedWidget, QTabWidget,
    QTextEdit, QLineEdit, QSpinBox, QComboBox, QSlider, QGroupBox,
    QGridLayout, QScrollArea, QSplitter, QFileDialog, QMessageBox,
    QListWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QToolBar, QStatusBar,
    QDockWidget, QFormLayout, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QTextBrowser, QDialog, QDialogButtonBox, QProgressBar
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, 
    pyqtSignal, QObject, QPointF, QRectF, QSize, QThread,
    QTranslator, QLocale, QDateTime
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QFont,
    QAction, QPalette, QLinearGradient, QRadialGradient,
    QPolygonF, QImage, QDragEnterEvent, QDropEvent
)

@dataclass
class NarrativeEvent:
    """Single event in character's narrative progression."""
    timestamp: datetime
    title: str
    description: str
    chapter: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "title": self.title,
            "description": self.description,
            "chapter": self.chapter
        }
