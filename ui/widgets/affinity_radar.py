"""
Radar chart widget for displaying Enneagram type affinities.
"""

import math
from typing import Dict
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QFont

from models.enums import EnneagramType, UIConstants


class AffinityRadarWidget(QWidget):
    """
    Radar/Spider chart for visualizing affinities with all Enneagram types.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize with neutral affinities
        self.affinities: Dict[EnneagramType, float] = {
            t: 0.5 for t in EnneagramType
        }
        
        # Set size constraints
        self.setMinimumSize(UIConstants.AFFINITY_RADAR_SIZE, UIConstants.AFFINITY_RADAR_SIZE)
        self.setMaximumSize(UIConstants.AFFINITY_RADAR_SIZE, UIConstants.AFFINITY_RADAR_SIZE)
        
        # Color scheme
        self.colors = {
            'background': QColor(250, 250, 250),
            'grid': QColor(200, 200, 200),
            'grid_major': QColor(150, 150, 150),
            'axis': QColor(100, 100, 100),
            'fill': QColor(100, 150, 255, 50),
            'stroke': QColor(100, 150, 255),
            'text': QColor(50, 50, 50),
            'center': QColor(255, 100, 100)
        }
        
    def set_affinities(self, affinities: Dict[EnneagramType, float]):
        """
        Update affinity values and redraw.
        
        Args:
            affinities: Dictionary mapping types to affinity values (0.0 to 1.0)
        """
        self.affinities = affinities
        self.update()
    
    def paintEvent(self, event):
        """Paint the radar chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget dimensions
        rect = self.rect()
        width = rect.width()
        height = rect.height()
        center_x = width / 2
        center_y = height / 2
        max_radius = min(width, height) / 2 - 30  # Leave margin for labels
        
        # Clear background
        painter.fillRect(rect, self.colors['background'])
        
        # Draw concentric circles (grid)
        num_circles = 5
        for i in range(1, num_circles + 1):
            radius = max_radius * i / num_circles
            pen = QPen(self.colors['grid_major'] if i == num_circles else self.colors['grid'], 
                      1 if i < num_circles else 2)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
            
            # Draw percentage labels
            if i < num_circles:
                percentage = i * 20  # 20%, 40%, 60%, 80%
                painter.setPen(QPen(self.colors['text']))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(
                    int(center_x + 5),
                    int(center_y - radius - 5),
                    f"{percentage}%"
                )
        
        # Type order (Type 9 at top, going clockwise)
        type_order = [9, 1, 2, 3, 4, 5, 6, 7, 8]
        num_types = len(type_order)
        
        # Draw axes and labels
        painter.setPen(QPen(self.colors['axis'], 1))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        axis_points = []
        for i, type_num in enumerate(type_order):
            # Calculate angle (starting from top, going clockwise)
            angle = -90 + (i * 360 / num_types)
            rad = math.radians(angle)
            
            # End point of axis
            x = center_x + max_radius * math.cos(rad)
            y = center_y + max_radius * math.sin(rad)
            axis_points.append((x, y, EnneagramType(type_num)))
            
            # Draw axis line
            painter.setPen(QPen(self.colors['axis'], 1, Qt.PenStyle.DashLine))
            painter.drawLine(QPointF(center_x, center_y), QPointF(x, y))
            
            # Draw type label
            label_offset = 20
            label_x = center_x + (max_radius + label_offset) * math.cos(rad)
            label_y = center_y + (max_radius + label_offset) * math.sin(rad)
            
            painter.setPen(QPen(self.colors['text']))
            painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            
            # Center the text around the point
            text_rect = QRectF(label_x - 15, label_y - 10, 30, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(type_num))
        
        # Draw affinity polygon
        affinity_points = []
        for i, type_num in enumerate(type_order):
            angle = -90 + (i * 360 / num_types)
            rad = math.radians(angle)
            
            # Get affinity value (0.0 to 1.0)
            etype = EnneagramType(type_num)
            affinity = self.affinities.get(etype, 0.5)
            affinity = max(0.0, min(1.0, affinity))  # Clamp to valid range
            
            # Calculate point position based on affinity
            radius = max_radius * affinity
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            affinity_points.append(QPointF(x, y))
        
        # Draw filled polygon
        polygon = QPolygonF(affinity_points)
        painter.setPen(QPen(self.colors['stroke'], 2))
        painter.setBrush(QBrush(self.colors['fill']))
        painter.drawPolygon(polygon)
        
        # Draw points at vertices
        painter.setPen(QPen(self.colors['stroke'], 1))
        painter.setBrush(QBrush(self.colors['stroke']))
        for point in affinity_points:
            painter.drawEllipse(point, 4, 4)
        
        # Draw center point
        painter.setPen(QPen(self.colors['center'], 2))
        painter.setBrush(QBrush(self.colors['center']))
        painter.drawEllipse(QPointF(center_x, center_y), 3, 3)
        
        # Draw legend
        self.draw_legend(painter, rect)
    
    def draw_legend(self, painter: QPainter, rect: QRectF):
        """
        Draw a small legend explaining the chart.
        
        Args:
            painter: QPainter instance
            rect: Widget rectangle
        """
        painter.setFont(QFont("Arial", 9))
        painter.setPen(QPen(self.colors['text']))
        
        legend_text = "Affinity with Types (0-100%)"
        text_rect = QRectF(10, rect.height() - 25, 200, 20)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, legend_text)
    
    def get_affinity_for_type(self, etype: EnneagramType) -> float:
        """
        Get affinity value for a specific type.
        
        Args:
            etype: Enneagram type
            
        Returns:
            Affinity value (0.0 to 1.0)
        """
        return self.affinities.get(etype, 0.5)
    
    def set_affinity_for_type(self, etype: EnneagramType, value: float):
        """
        Set affinity value for a specific type.
        
        Args:
            etype: Enneagram type
            value: Affinity value (0.0 to 1.0)
        """
        self.affinities[etype] = max(0.0, min(1.0, value))
        self.update()
    
    def reset_affinities(self):
        """Reset all affinities to neutral (0.5)."""
        self.affinities = {t: 0.5 for t in EnneagramType}
        self.update()