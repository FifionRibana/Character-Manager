"""
Style and theme management for the application.
Provides light and dark themes that respect OS settings.
"""

from models.enums import ThemeMode


class StyleManager:
    """Manages application themes and stylesheets."""
    
    def __init__(self):
        """Initialize style manager with theme definitions."""
        self.themes = {
            ThemeMode.LIGHT: self._get_light_theme(),
            ThemeMode.DARK: self._get_dark_theme()
        }
    
    def get_stylesheet(self, mode: ThemeMode) -> str:
        """
        Get stylesheet for specified theme mode.
        
        Args:
            mode: Theme mode (light/dark)
            
        Returns:
            CSS stylesheet string
        """
        if mode == ThemeMode.AUTO:
            # This should be handled by the caller
            return self.themes[ThemeMode.LIGHT]
        
        return self.themes.get(mode, self.themes[ThemeMode.LIGHT])
    
    def _get_light_theme(self) -> str:
        """Get light theme stylesheet."""
        return """
        /* Light Theme */
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 5px;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 2px solid #4CAF50;
        }
        
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QPushButton#deleteButton {
            background-color: #f44336;
        }
        
        QPushButton#deleteButton:hover {
            background-color: #da190b;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-weight: bold;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            background-color: white;
        }
        
        /* List Widgets */
        QListWidget {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            outline: none;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 4px;
            margin: 2px 0;
        }
        
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QListWidget::item:hover {
            background-color: #e8f5e9;
        }
        
        /* Text Edits */
        QTextEdit, QPlainTextEdit {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
        }
        
        QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Line Edits */
        QLineEdit {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            min-height: 20px;
        }
        
        QLineEdit:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Spin Boxes */
        QSpinBox, QDoubleSpinBox {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            min-height: 20px;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Combo Boxes */
        QComboBox {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            min-height: 25px;
        }
        
        QComboBox:focus {
            border: 2px solid #4CAF50;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #666;
            margin-right: 5px;
        }
        
        /* Sliders */
        QSlider::groove:horizontal {
            height: 6px;
            background-color: #ddd;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            width: 18px;
            height: 18px;
            background-color: #4CAF50;
            border-radius: 9px;
            margin: -6px 0;
        }
        
        QSlider::handle:horizontal:hover {
            background-color: #45a049;
        }
        
        /* Tables */
        QTableWidget {
            background-color: white;
            gridline-color: #ddd;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QTableWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #f5f5f5;
            padding: 5px;
            border: none;
            border-bottom: 2px solid #ddd;
            font-weight: bold;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #f0f0f0;
            border-top: 1px solid #ddd;
        }
        
        /* Tool Bar */
        QToolBar {
            background-color: white;
            border-bottom: 1px solid #ddd;
            padding: 5px;
            spacing: 5px;
        }
        
        QToolBar QToolButton {
            background-color: transparent;
            border: none;
            padding: 5px;
            border-radius: 4px;
        }
        
        QToolBar QToolButton:hover {
            background-color: #e0e0e0;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
        
        QScrollBar:horizontal {
            background-color: #f0f0f0;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #a0a0a0;
        }
        
        /* Splitter */
        QSplitter::handle {
            background-color: #e0e0e0;
        }
        
        QSplitter::handle:hover {
            background-color: #c0c0c0;
        }
        
        /* Labels */
        QLabel {
            color: #333333;
        }
        
        /* Graphics View */
        QGraphicsView {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        """
    
    def _get_dark_theme(self) -> str:
        """Get dark theme stylesheet."""
        return """
        /* Dark Theme */
        QMainWindow {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #3c3c3c;
            background-color: #2d2d2d;
            border-radius: 5px;
        }
        
        QTabBar::tab {
            background-color: #3c3c3c;
            color: #e0e0e0;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #2d2d2d;
            border-bottom: 2px solid #4CAF50;
        }
        
        QTabBar::tab:hover {
            background-color: #464646;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #5cbf60;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QPushButton:disabled {
            background-color: #3c3c3c;
            color: #666666;
        }
        
        QPushButton#deleteButton {
            background-color: #f44336;
        }
        
        QPushButton#deleteButton:hover {
            background-color: #ff6659;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-weight: bold;
            border: 2px solid #3c3c3c;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        /* List Widgets */
        QListWidget {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 5px;
            outline: none;
            color: #e0e0e0;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 4px;
            margin: 2px 0;
        }
        
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QListWidget::item:hover {
            background-color: #3c3c3c;
        }
        
        /* Text Edits */
        QTextEdit, QPlainTextEdit, QTextBrowser {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 8px;
            color: #e0e0e0;
        }
        
        QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Line Edits */
        QLineEdit {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 8px;
            min-height: 20px;
            color: #e0e0e0;
        }
        
        QLineEdit:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Spin Boxes */
        QSpinBox, QDoubleSpinBox {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 5px;
            min-height: 20px;
            color: #e0e0e0;
        }
        
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #4CAF50;
        }
        
        /* Combo Boxes */
        QComboBox {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 5px;
            min-height: 25px;
            color: #e0e0e0;
        }
        
        QComboBox:focus {
            border: 2px solid #4CAF50;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #e0e0e0;
            margin-right: 5px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            color: #e0e0e0;
            selection-background-color: #4CAF50;
        }
        
        /* Sliders */
        QSlider::groove:horizontal {
            height: 6px;
            background-color: #3c3c3c;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            width: 18px;
            height: 18px;
            background-color: #4CAF50;
            border-radius: 9px;
            margin: -6px 0;
        }
        
        QSlider::handle:horizontal:hover {
            background-color: #5cbf60;
        }
        
        /* Tables */
        QTableWidget {
            background-color: #2d2d2d;
            gridline-color: #3c3c3c;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            color: #e0e0e0;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QTableWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #1e1e1e;
            padding: 5px;
            border: none;
            border-bottom: 2px solid #3c3c3c;
            font-weight: bold;
            color: #e0e0e0;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #1e1e1e;
            border-top: 1px solid #3c3c3c;
            color: #e0e0e0;
        }
        
        /* Tool Bar */
        QToolBar {
            background-color: #2d2d2d;
            border-bottom: 1px solid #3c3c3c;
            padding: 5px;
            spacing: 5px;
        }
        
        QToolBar QToolButton {
            background-color: transparent;
            border: none;
            padding: 5px;
            border-radius: 4px;
            color: #e0e0e0;
        }
        
        QToolBar QToolButton:hover {
            background-color: #3c3c3c;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background-color: #1e1e1e;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3c3c3c;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #4c4c4c;
        }
        
        QScrollBar:horizontal {
            background-color: #1e1e1e;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3c3c3c;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #4c4c4c;
        }
        
        /* Splitter */
        QSplitter::handle {
            background-color: #3c3c3c;
        }
        
        QSplitter::handle:hover {
            background-color: #4c4c4c;
        }
        
        /* Labels */
        QLabel {
            color: #e0e0e0;
        }
        
        /* Graphics View */
        QGraphicsView {
            background-color: #2d2d2d;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
        }
        
        /* Tool Tips */
        QToolTip {
            background-color: #3c3c3c;
            color: #e0e0e0;
            border: 1px solid #4c4c4c;
            padding: 5px;
            border-radius: 4px;
        }
        """