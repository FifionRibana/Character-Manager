
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

from .enums import StorageKeys, EnneagramType, InstinctualVariant, StatType, RelationType

@dataclass
class Relationship:
    """Relationship between two characters."""
    target_id: str
    target_name: str
    relationship_type: RelationType
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize relationship to dictionary."""
        return {
            "target_id": self.target_id,
            "target_name": self.target_name,
            "type": self.relationship_type,
            "description": self.description
        }
