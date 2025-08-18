
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
class EnneagramProfile:
    """Complete Enneagram personality profile."""
    main_type: EnneagramType = EnneagramType.TYPE_9
    wing: Optional[EnneagramType] = None
    instinctual_stack: List[InstinctualVariant] = field(default_factory=lambda: [
        InstinctualVariant.SELF_PRESERVATION,
        InstinctualVariant.SOCIAL,
        InstinctualVariant.SEXUAL
    ])
    development_level: int = 5  # 1-9, with 1 being healthiest
    integration_point: Optional[EnneagramType] = None
    disintegration_point: Optional[EnneagramType] = None
    type_affinities: Dict[EnneagramType, float] = field(default_factory=lambda: {
        t: 0.5 for t in EnneagramType
    })
    
    def get_wing_notation(self) -> str:
        """Return the wing notation (e.g., '9w8' or '9w1')."""
        if self.wing:
            return f"{self.main_type}w{self.wing}"
        return str(self.main_type)
    
    def get_tritype_designation(self) -> str:
        """Return alpha/beta/gamma/mu designation based on wing."""
        if not self.wing:
            return ""
        
        # This is a simplified version - you can expand the logic
        if self.main_type == EnneagramType.TYPE_9:
            if self.wing == EnneagramType.TYPE_8:
                return "alpha"  # 9w8
            elif self.wing == EnneagramType.TYPE_1:
                return "mu"  # 9w1
        
        # Add more type-specific designations as needed
        return ""
