"""
Theme Controller for Medieval Character Manager
Manages application themes (dark/light) with persistence
"""

import json
from dataclasses import dataclass, field, asdict
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Dict, Any, Optional, List
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QSettings
from PyQt6.QtGui import QColor

from data.enums import FileConstants, StorageKeys, ThemeMode
from utils.singleton import singleton


class ColorRole(StrEnum):
    """Color roles in the theme system"""

    BACKGROUND = "background"
    BACKGROUND_VARIANT = "backgroundVariant"
    SURFACE = "surface"
    SURFACE_VARIANT = "surfaceVariant"
    PRIMARY = "primary"
    PRIMARY_VARIANT = "primaryVariant"
    SECONDARY = "secondary"
    SECONDARY_VARIANT = "secondaryVariant"
    ACCENT = "accent"
    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    TEXT = "text"
    TEXT_SECONDARY = "textSecondary"
    TEXT_DISABLED = "textDisabled"
    BORDER = "border"
    BORDER_LIGHT = "borderLight"
    SHADOW = "shadow"
    OVERLAY = "overlay"
    CARD = "card"


@dataclass
class CardColors:
    background: str = "#FFFFFF"
    border: str = "#E0E0E0"


@dataclass
class ThemeColors:
    """Theme color palette definition"""

    background: str = "#FFFFFF"
    background_variant: str = "#F8F9FA"
    surface: str = "#F5F5F5"
    surface_variant: str = "#E0E0E0"
    primary: str = "#6200EE"
    primary_variant: str = "#3700B3"
    secondary: str = "#03DAC6"
    secondary_variant: str = "#018786"
    accent: str = "#FF5722"
    error: str = "#B00020"
    warning: str = "#FFA000"
    success: str = "#4CAF50"
    text: str = "#212121"
    text_secondary: str = "#757575"
    text_disabled: str = "#9E9E9E"
    border: str = "#BDBDBD"
    border_light: str = "#DEE2E6"
    shadow: str = "#000000"
    overlay: str = "rgba(0, 0, 0, 0.5)"

    card: CardColors = field(default_factory=CardColors)

    def to_dict(self) -> Dict[str, str]:
        """Convert colors to dictionary for QML"""
        return {
            ColorRole.BACKGROUND: self.background,
            ColorRole.BACKGROUND_VARIANT: self.background_variant,
            ColorRole.SURFACE: self.surface,
            ColorRole.SURFACE_VARIANT: self.surface_variant,
            ColorRole.PRIMARY: self.primary,
            ColorRole.PRIMARY_VARIANT: self.primary_variant,
            ColorRole.SECONDARY: self.secondary,
            ColorRole.SECONDARY_VARIANT: self.secondary_variant,
            ColorRole.ACCENT: self.accent,
            ColorRole.ERROR: self.error,
            ColorRole.WARNING: self.warning,
            ColorRole.SUCCESS: self.success,
            ColorRole.TEXT: self.text,
            ColorRole.TEXT_SECONDARY: self.text_secondary,
            ColorRole.TEXT_DISABLED: self.text_disabled,
            ColorRole.BORDER: self.border,
            ColorRole.BORDER_LIGHT: self.border_light,
            ColorRole.SHADOW: self.shadow,
            ColorRole.OVERLAY: self.overlay,
            ColorRole.CARD: {
                ColorRole.BACKGROUND: self.card.background,
                ColorRole.BORDER: self.card.border,
            },
        }


@dataclass
class ThemeMetrics:
    """Theme spacing and sizing metrics"""

    border_xs: int = 1
    border_md: int = 2
    border_xl: int = 4

    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 16
    spacing_lg: int = 24
    spacing_xl: int = 32

    margin_xs: int = 4
    margin_sm: int = 8
    margin_md: int = 16
    margin_lg: int = 24
    margin_xl: int = 32

    padding_xs: int = 4
    padding_sm: int = 8
    padding_md: int = 16
    padding_lg: int = 24
    padding_xl: int = 32

    radius_xs: int = 2
    radius_sm: int = 4
    radius_md: int = 8
    radius_lg: int = 16

    font_size_xs: int = 10
    font_size_sm: int = 12
    font_size_md: int = 14
    font_size_lg: int = 18
    font_size_tt: int = 20
    font_size_xl: int = 24
    font_size_xxl: int = 32

    icon_size_sm: int = 16
    icon_size_md: int = 24
    icon_size_lg: int = 32

    elevation_sm: int = 2
    elevation_md: int = 4
    elevation_lg: int = 8

    animation_duration_fast: int = 150
    animation_duration_normal: int = 250
    animation_duration_slow: int = 400


@dataclass
class Theme:
    """Complete theme definition"""

    name: str
    mode: ThemeMode
    colors: ThemeColors = field(default_factory=ThemeColors)
    metrics: ThemeMetrics = field(default_factory=ThemeMetrics)
    custom: bool = False

    @classmethod
    def light_theme(cls) -> "Theme":
        """Factory method for default light theme"""
        return cls(
            name=ThemeMode.LIGHT.value,
            mode=ThemeMode.LIGHT,
            colors=ThemeColors(
                background="#FFFFFF",
                background_variant="#F8F9FA",
                surface="#F5F5F5",
                surface_variant="#E0E0E0",
                primary="#6200EE",
                primary_variant="#3700B3",
                secondary="#03DAC6",
                secondary_variant="#018786",
                accent="#FF5722",
                error="#B00020",
                warning="#FFA000",
                success="#4CAF50",
                text="#212121",
                text_secondary="#757575",
                text_disabled="#9E9E9E",
                border="#BDBDBD",
                border_light="#DEE2E6",
                shadow="#000000",
                overlay="rgba(0, 0, 0, 0.5)",
            ),
        )

    @classmethod
    def dark_theme(cls) -> "Theme":
        """Factory method for default dark theme"""
        return cls(
            name=ThemeMode.DARK.value,
            mode=ThemeMode.DARK,
            colors=ThemeColors(
                background="#121212",
                background_variant="#191919",
                surface="#1E1E1E",
                surface_variant="#2C2C2C",
                primary="#BB86FC",
                primary_variant="#7F39FB",
                secondary="#03DAC6",
                secondary_variant="#00A896",
                accent="#FF6B35",
                error="#CF6679",
                warning="#FFB74D",
                success="#81C784",
                text="#FFFFFF",
                text_secondary="#B3B3B3",
                text_disabled="#666666",
                border="#404040",
                border_light="#282828",
                shadow="#000000",
                overlay="rgba(255, 255, 255, 0.1)",
            ),
        )


@singleton
@dataclass
class ThemeController(QObject):
    """
    Controller for managing application themes
    Provides theme switching, persistence, and custom theme support
    """

    # Signals
    themeChanged: ClassVar[pyqtSignal] = pyqtSignal()
    currentThemeNameChanged: ClassVar[pyqtSignal] = pyqtSignal()
    isDarkModeChanged: ClassVar[pyqtSignal] = pyqtSignal()
    colorsChanged: ClassVar[pyqtSignal] = pyqtSignal()

    _settings: QSettings = field(
        init=False, default_factory=lambda: QSettings("CharacterManager", "Themes")
    )
    _themes: Dict[str, Theme] = field(init=False, default_factory=dict)
    _current_theme: Optional[Theme] = field(init=False, default=None)
    _custom_themes_path: Path = field(init=False, default=FileConstants.THEME_DIR)

    def __post_init__(self):
        """Initialize theme controller with default themes"""
        QObject.__init__(self)

        # Initialize default themes
        self._init_default_themes()

        # Load custom themes
        self._load_custom_themes()

        # Load saved theme preference
        self._load_theme_preference()

    def _init_default_themes(self) -> None:
        """Initialize built-in themes"""
        light = Theme.light_theme()
        dark = Theme.dark_theme()

        self._themes[light.name] = light
        self._themes[dark.name] = dark

    def _load_custom_themes(self) -> None:
        """Load custom themes from user directory"""
        if not self._custom_themes_path.exists():
            self._custom_themes_path.mkdir(parents=True, exist_ok=True)
            return

        for theme_file in self._custom_themes_path.glob("*.json"):
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
                    theme = self._deserialize_theme(theme_data)
                    if theme:
                        theme.custom = True
                        self._themes[theme.name] = theme
            except Exception as e:
                print(f"Error loading custom theme {theme_file}: {e}")

    def _load_theme_preference(self) -> None:
        """Load saved theme preference from settings"""
        saved_theme = self._settings.value(
            StorageKeys.CURRENT_THEME.value, ThemeMode.LIGHT.value
        )
        if saved_theme in self._themes:
            self._current_theme = self._themes[saved_theme]
        else:
            self._current_theme = self._themes[ThemeMode.LIGHT.value]

        self.themeChanged.emit()

    def _save_theme_preference(self) -> None:
        """Save current theme preference to settings"""
        if self._current_theme:
            self._settings.setValue("current_theme", self._current_theme.name)

    def _serialize_theme(self, theme: Theme) -> Dict[str, Any]:
        """Serialize theme to dictionary for storage"""
        return {
            StorageKeys.THEME_NAME.value: theme.name,
            StorageKeys.THEME_MODE.value: theme.mode.value,
            StorageKeys.THEME_COLORS.value: asdict(theme.colors),
            StorageKeys.THEME_METRICS.value: asdict(theme.metrics),
            StorageKeys.THEME_CUSTOM_FLAG.value: theme.custom,
        }

    def _deserialize_theme(self, data: Dict[str, Any]) -> Optional[Theme]:
        """Deserialize theme from dictionary"""
        try:
            return Theme(
                name=data[StorageKeys.THEME_NAME.value],
                mode=ThemeMode(data[StorageKeys.THEME_MODE.value]),
                colors=ThemeColors(**data.get(StorageKeys.THEME_COLORS.value, {})),
                metrics=ThemeMetrics(**data.get(StorageKeys.THEME_METRICS.value, {})),
                custom=data.get(StorageKeys.THEME_CUSTOM_FLAG.value, False),
            )
        except Exception as e:
            print(f"Error deserializing theme: {e}")
            return None

    # Public methods

    def switch_theme(self, theme_name: str) -> bool:
        """
        Switch to a different theme

        Args:
            theme_name: Name of the theme to switch to

        Returns:
            True if switch was successful
        """
        if theme_name not in self._themes:
            return False

        self._current_theme = self._themes[theme_name]
        self._save_theme_preference()

        self.themeChanged.emit()
        self.currentThemeNameChanged.emit()
        self.isDarkModeChanged.emit()
        self.colorsChanged.emit()

        return True

    @pyqtSlot()
    def toggle_theme(self) -> None:
        """Toggle between light and dark theme"""
        if self._current_theme and self._current_theme.mode == ThemeMode.DARK:
            self.switch_theme(ThemeMode.LIGHT.value)
        else:
            self.switch_theme(ThemeMode.DARK.value)

    def create_custom_theme(
        self, name: str, base_theme: str, colors: Dict[str, str]
    ) -> bool:
        """
        Create a custom theme based on existing theme

        Args:
            name: Name for the custom theme
            base_theme: Name of theme to use as base
            colors: Dictionary of color overrides

        Returns:
            True if creation was successful
        """
        if base_theme not in self._themes:
            return False

        base = self._themes[base_theme]
        custom_colors = ThemeColors(**asdict(base.colors))

        # Apply color overrides
        for role, color in colors.items():
            if hasattr(
                custom_colors,
                role.replace(ColorRole.BACKGROUND, ColorRole.BACKGROUND.value),
            ):
                setattr(
                    custom_colors,
                    role.replace(ColorRole.BACKGROUND, ColorRole.BACKGROUND.value),
                    color,
                )

        custom_theme = Theme(
            name=name,
            mode=ThemeMode.CUSTOM,
            colors=custom_colors,
            metrics=base.metrics,
            custom=True,
        )

        self._themes[name] = custom_theme

        # Save to file
        theme_file = self._custom_themes_path / f"{name}.json"
        with open(theme_file, "w", encoding="utf-8") as f:
            json.dump(self._serialize_theme(custom_theme), f, indent=2)

        return True

    def delete_custom_theme(self, name: str) -> bool:
        """
        Delete a custom theme

        Args:
            name: Name of the custom theme to delete

        Returns:
            True if deletion was successful
        """
        if name not in self._themes or not self._themes[name].custom:
            return False

        # Delete file
        theme_file = self._custom_themes_path / f"{name}.json"
        if theme_file.exists():
            theme_file.unlink()

        # Remove from memory
        del self._themes[name]

        # Switch to default if this was current
        if self._current_theme and self._current_theme.name == name:
            self.switch_theme(ThemeMode.LIGHT.value)

        return True

    def get_available_themes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self._themes.keys())

    # Qt Properties

    @pyqtProperty(str, notify=currentThemeNameChanged)
    def currentThemeName(self) -> str:
        """Current theme name property"""
        return (
            self._current_theme.name if self._current_theme else ThemeMode.LIGHT.value
        )

    @pyqtProperty(bool, notify=isDarkModeChanged)
    def isDarkMode(self) -> bool:
        """Check if current theme is dark mode"""
        return (
            self._current_theme.mode == ThemeMode.DARK if self._current_theme else False
        )

    @pyqtProperty("QVariant", notify=colorsChanged)
    def colors(self) -> Dict[str, str]:
        """Get current theme colors as dictionary"""
        if self._current_theme:
            return self._current_theme.colors.to_dict()
        return ThemeColors().to_dict()

    @pyqtProperty("QVariant", notify=themeChanged)
    def metrics(self) -> Dict[str, int]:
        """Get current theme metrics as dictionary"""
        if self._current_theme:
            return asdict(self._current_theme.metrics)
        return asdict(ThemeMetrics())

    @pyqtProperty("QVariantList", notify=themeChanged)
    def availableThemes(self) -> List[Dict[str, Any]]:
        """Get list of available themes with metadata"""
        return [
            {"name": theme.name, "mode": theme.mode.value, "custom": theme.custom}
            for theme in self._themes.values()
        ]
