"""
Interactive Enneagram wheel widget with proper sizing and animations.
No scrolling required - adapts to available space.
"""

import math
from typing import Dict, Tuple, Optional
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient

from models.enums import EnneagramType, UIConstants


class EnneagramWheel(QGraphicsView):
    """
    Interactive Enneagram wheel visualization.
    Type 9 is positioned at the top (12 o'clock).
    """
    
    typeSelected = pyqtSignal(EnneagramType)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configure view
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set fixed size to prevent scrolling
        self.setMinimumSize(UIConstants.ENNEAGRAM_WHEEL_SIZE, UIConstants.ENNEAGRAM_WHEEL_SIZE)
        self.setMaximumSize(UIConstants.ENNEAGRAM_WHEEL_SIZE, UIConstants.ENNEAGRAM_WHEEL_SIZE)
        
        # Initialize scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Wheel parameters
        self.center_x = 0
        self.center_y = 0
        self.radius = 120  # Smaller radius to fit better
        self.node_radius = 20
        
        # Storage for graphical elements
        self.type_items: Dict[EnneagramType, Tuple[QGraphicsEllipseItem, QGraphicsTextItem]] = {}
        self.connection_lines: Dict[Tuple[EnneagramType, EnneagramType], QGraphicsLineItem] = {}
        self.selected_type = EnneagramType.TYPE_9
        
        # Colors for better visual hierarchy
        self.colors = {
            'background': QColor(250, 250, 250),
            'wheel': QColor(200, 200, 200),
            'node_default': QColor(255, 255, 255),
            'node_selected': QColor(100, 150, 255),
            'node_hover': QColor(150, 180, 255),
            'integration': QColor(100, 200, 100, 120),
            'disintegration': QColor(200, 100, 100, 120),
            'text': QColor(50, 50, 50)
        }
        
        self.setup_wheel()
        
    def setup_wheel(self):
        """Create the Enneagram wheel with 9 points."""
        self.scene.clear()
        
        # Set scene rect to match view size
        view_rect = QRectF(-200, -200, 400, 400)
        self.scene.setSceneRect(view_rect)
        self.setSceneRect(view_rect)
        
        # Background
        self.scene.setBackgroundBrush(QBrush(self.colors['background']))
        
        # Draw outer circle
        pen = QPen(self.colors['wheel'], 2)
        self.scene.addEllipse(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.radius * 2,
            self.radius * 2,
            pen,
            QBrush(Qt.BrushStyle.NoBrush)
        )
        
        # Draw inner connecting lines (the enneagram figure)
        self.draw_enneagram_figure()
        
        # Position and create type nodes
        positions = self.calculate_type_positions()
        
        for etype, (x, y) in positions.items():
            # Create gradient for node
            gradient = QRadialGradient(x, y, self.node_radius)
            gradient.setColorAt(0, self.colors['node_default'])
            gradient.setColorAt(1, self.colors['node_default'].darker(110))
            
            # Circle for type
            circle = self.scene.addEllipse(
                x - self.node_radius,
                y - self.node_radius,
                self.node_radius * 2,
                self.node_radius * 2,
                QPen(self.colors['wheel'], 2),
                QBrush(gradient)
            )
            circle.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
            circle.setData(0, etype)  # Store type in item data
            circle.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Text label
            text = self.scene.addText(str(etype.value))
            text.setPos(x - 8, y - 10)
            text.setDefaultTextColor(self.colors['text'])
            font = QFont("Arial", 12, QFont.Weight.Bold)
            text.setFont(font)
            
            self.type_items[etype] = (circle, text)
        
        # Draw integration/disintegration lines
        self.draw_connections()
        
        # Highlight default selection
        self.highlight_type(self.selected_type)
        
    def calculate_type_positions(self) -> Dict[EnneagramType, Tuple[float, float]]:
        """
        Calculate positions for each Enneagram type on the wheel.
        Type 9 is at the top (12 o'clock position).
        """
        positions = {}
        
        # Type order clockwise from top
        type_order = [9, 1, 2, 3, 4, 5, 6, 7, 8]
        
        for i, type_num in enumerate(type_order):
            # Start at -90 degrees (top) and go clockwise
            angle = -90 + (i * 40)  # 360/9 = 40 degrees apart
            rad = math.radians(angle)
            x = self.center_x + self.radius * math.cos(rad)
            y = self.center_y + self.radius * math.sin(rad)
            positions[EnneagramType(type_num)] = (x, y)
        
        return positions
    
    def draw_enneagram_figure(self):
        """Draw the internal lines of the enneagram figure."""
        # The classic enneagram figure connections
        connections = [
            (9, 3), (3, 6), (6, 9),  # Inner triangle
            (1, 4), (4, 2), (2, 8), (8, 5), (5, 7), (7, 1)  # Hexad
        ]
        
        positions = self.calculate_type_positions()
        pen = QPen(self.colors['wheel'].lighter(120), 1, Qt.PenStyle.SolidLine)
        
        for from_num, to_num in connections:
            from_type = EnneagramType(from_num)
            to_type = EnneagramType(to_num)
            x1, y1 = positions[from_type]
            x2, y2 = positions[to_type]
            
            line = self.scene.addLine(x1, y1, x2, y2, pen)
            line.setZValue(-1)  # Put behind nodes
    
    def draw_connections(self):
        """Draw integration and disintegration arrows."""
        # Integration lines (growth direction)
        integrations = {
            EnneagramType.TYPE_1: EnneagramType.TYPE_7,
            EnneagramType.TYPE_2: EnneagramType.TYPE_4,
            EnneagramType.TYPE_3: EnneagramType.TYPE_6,
            EnneagramType.TYPE_4: EnneagramType.TYPE_1,
            EnneagramType.TYPE_5: EnneagramType.TYPE_8,
            EnneagramType.TYPE_6: EnneagramType.TYPE_9,
            EnneagramType.TYPE_7: EnneagramType.TYPE_5,
            EnneagramType.TYPE_8: EnneagramType.TYPE_2,
            EnneagramType.TYPE_9: EnneagramType.TYPE_3
        }
        
        positions = self.calculate_type_positions()
        
        # Draw subtle integration lines
        for from_type, to_type in integrations.items():
            x1, y1 = positions[from_type]
            x2, y2 = positions[to_type]
            
            # Offset slightly to not overlap with main figure
            pen = QPen(self.colors['integration'], 2, Qt.PenStyle.DashLine)
            line = self.scene.addLine(x1, y1, x2, y2, pen)
            line.setZValue(-2)  # Put behind everything
            line.setVisible(False)  # Hidden by default
            self.connection_lines[(from_type, to_type)] = line
    
    def highlight_type(self, etype: EnneagramType, animate: bool = True):
        """
        Highlight the selected type with animation.
        
        Args:
            etype: The Enneagram type to highlight
            animate: Whether to animate the highlight
        """
        # Reset all types
        for type_enum, (circle, text) in self.type_items.items():
            if type_enum == etype:
                # Highlight selected
                gradient = QRadialGradient(circle.rect().center(), self.node_radius)
                gradient.setColorAt(0, self.colors['node_selected'])
                gradient.setColorAt(1, self.colors['node_selected'].darker(120))
                circle.setBrush(QBrush(gradient))
                circle.setPen(QPen(self.colors['node_selected'].darker(150), 3))
                text.setDefaultTextColor(QColor(255, 255, 255))
            else:
                # Reset to default
                gradient = QRadialGradient(circle.rect().center(), self.node_radius)
                gradient.setColorAt(0, self.colors['node_default'])
                gradient.setColorAt(1, self.colors['node_default'].darker(110))
                circle.setBrush(QBrush(gradient))
                circle.setPen(QPen(self.colors['wheel'], 2))
                text.setDefaultTextColor(self.colors['text'])
        
        # Show/hide integration lines
        for (from_type, to_type), line in self.connection_lines.items():
            line.setVisible(from_type == etype or to_type == etype)
        
        self.selected_type = etype
        self.typeSelected.emit(etype)
    
    def mousePressEvent(self, event):
        """Handle mouse clicks on types."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get item at click position
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())
            
            if item and isinstance(item, QGraphicsEllipseItem):
                etype = item.data(0)
                if etype:
                    self.highlight_type(etype)
        
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """Handle resize events to fit content."""
        super().resizeEvent(event)
        # Ensure the scene fits in the view
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)