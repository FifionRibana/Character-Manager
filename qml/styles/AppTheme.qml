pragma Singleton
import QtQuick

QtObject {
    id: theme
    
    // Theme controller reference (will be set from C++)
    property var themeController: null
    
    // Theme mode
    property bool isDarkMode: themeController ? themeController.isDarkMode : false
    property string currentThemeName: themeController ? themeController.currentThemeName : "Light"
    
    // User preferences
    property bool animationsEnabled: true
    property bool soundEnabled: false
    property bool autoSaveEnabled: true
    property int autoSaveInterval: 5  // minutes
    property real animationSpeed: 1.0
    
    // Dynamic colors from theme controller
    readonly property var colors: QtObject {
        property color background: themeController ? themeController.colors.background : "#FFFFFF"
        property color backgroundVariant: themeController ? themeController.colors.backgroundVariant : "#F8F9FA"
        property color surface: themeController ? themeController.colors.surface : "#F5F5F5"
        property color surfaceVariant: themeController ? themeController.colors.surfaceVariant : "#E0E0E0"
        property color primary: themeController ? themeController.colors.primary : "#6200EE"
        property color primaryVariant: themeController ? themeController.colors.primaryVariant : "#3700B3"
        property color secondary: themeController ? themeController.colors.secondary : "#03DAC6"
        property color secondaryVariant: themeController ? themeController.colors.secondaryVariant : "#018786"
        property color accent: themeController ? themeController.colors.accent : "#FF5722"
        property color error: themeController ? themeController.colors.error : "#B00020"
        property color warning: themeController ? themeController.colors.warning : "#FFA000"
        property color success: themeController ? themeController.colors.success : "#4CAF50"
        property color text: themeController ? themeController.colors.text : "#212121"
        property color textSecondary: themeController ? themeController.colors.textSecondary : "#757575"
        property color textDisabled: themeController ? themeController.colors.textDisabled : "#9E9E9E"
        property color border: themeController ? themeController.colors.border : "#BDBDBD"
        property color borderLight: themeController ? themeController.colors.borderLight : "#DEE2E6"
        property color shadow: themeController ? themeController.colors.shadow : "#000000"
        property color overlay: themeController ? themeController.colors.overlay : "rgba(0, 0, 0, 0.5)"
        
        // Computed colors
        property color textOnPrimary: isDarkMode ? "#000000" : "#FFFFFF"
        property color textOnSecondary: isDarkMode ? "#000000" : "#FFFFFF"
        property color textOnAccent: "#FFFFFF"
        property color textOnError: "#FFFFFF"
        property color textOnSuccess: "#FFFFFF"
        property color textOnWarning: isDarkMode ? "#FFFFFF" : "#000000"
        
        // Hover and pressed states
        property color hoverOverlay: isDarkMode ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.05)"
        property color pressedOverlay: isDarkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)"
        
        // Special purpose colors
        property color divider: Qt.lighter(border, isDarkMode ? 1.2 : 0.8)
        property color scrollbar: isDarkMode ? "#404040" : "#CCCCCC"
        property color scrollbarHover: isDarkMode ? "#505050" : "#AAAAAA"
        property color tooltip: isDarkMode ? "#424242" : "#616161"
        property color tooltipText: "#FFFFFF"
    }

    readonly property var fontFamily: 'Inter, "Segoe UI", Roboto, sans-serif'

    readonly property var input: QtObject {
        property color background: themeController ? themeController.input.background : "#FFFFFF"
        property color border: themeController ? themeController.input.border : "#E0E0E0"
        property color borderFocus: themeController ? themeController.input.borderFocus : "#2196F3"
        property color placeholder: themeController ? themeController.input.placeholder : "#9E9E9E"
    }
    
    readonly property var card: QtObject {
        property color background: themeController ? themeController.card.background : "#FFFFFF"
        property color border: themeController ? themeController.card.border : "#E0E0E0"
    }
    
    readonly property var button: QtObject {
        property color normal: themeController ? themeController.button.normal : "#2196F3"
        property color pressed: themeController ? themeController.button.pressed : "#1976D2"
        property color hovered: themeController ? themeController.button.hovered : "#1565C0"
        property color disabled: themeController ? themeController.button.disabled : "#BDBDBD"
        
        // Destructive
        property color destructiveNormal: themeController ? themeController.button.destructiveNormal : "#FFFFFF"
        property color destructivePressed: themeController ? themeController.button.destructivePressed : "#FFFFFF"
        property color destructiveHovered: themeController ? themeController.button.destructiveHovered : "#FFFFFF"
    }

    // Spacing values from theme controller
    readonly property var spacing: QtObject {
        property int tiny: themeController ? themeController.metrics.spacing_xs : 4
        property int small: themeController ? themeController.metrics.spacing_sm : 8
        property int medium: themeController ? themeController.metrics.spacing_md : 16
        property int large: themeController ? themeController.metrics.spacing_lg : 24
        property int huge: themeController ? themeController.metrics.spacing_xl : 32
    }
    
    // Border radius values
    readonly property var radius: QtObject {
        property int small: themeController ? themeController.metrics.radius_sm : 4
        property int medium: themeController ? themeController.metrics.radius_md : 8
        property int large: themeController ? themeController.metrics.radius_lg : 16
        property int round: 9999  // For circular elements
    }
    
    // Font sizes
    readonly property var fontSize: QtObject {
        property int tiny: themeController ? themeController.metrics.font_size_xs : 10
        property int small: themeController ? themeController.metrics.font_size_sm : 12
        property int medium: themeController ? themeController.metrics.font_size_md : 14
        property int large: themeController ? themeController.metrics.font_size_lg : 18
        property int huge: themeController ? themeController.metrics.font_size_xl : 24
        property int giant: themeController ? themeController.metrics.font_size_xxl : 32
    }
    
    // Icon sizes
    readonly property var iconSize: QtObject {
        property int small: themeController ? themeController.metrics.icon_size_sm : 16
        property int medium: themeController ? themeController.metrics.icon_size_md : 24
        property int large: themeController ? themeController.metrics.icon_size_lg : 32
        property int huge: 48
        property int giant: 64
    }
    
    // Elevation (shadow depth)
    readonly property var elevation: QtObject {
        property int flat: 0
        property int low: themeController ? themeController.metrics.elevation_sm : 2
        property int medium: themeController ? themeController.metrics.elevation_md : 4
        property int high: themeController ? themeController.metrics.elevation_lg : 8
        property int highest: 16
    }
    
    // Animation durations (affected by animationSpeed)
    readonly property var animation: QtObject {
        property int instant: 0
        property int fast: animationsEnabled ? Math.round((themeController ? themeController.metrics.animation_duration_fast : 150) / animationSpeed) : 0
        property int normal: animationsEnabled ? Math.round((themeController ? themeController.metrics.animation_duration_normal : 250) / animationSpeed) : 0
        property int slow: animationsEnabled ? Math.round((themeController ? themeController.metrics.animation_duration_slow : 400) / animationSpeed) : 0
        property int slower: animationsEnabled ? Math.round(600 / animationSpeed) : 0
        
        // Easing curves
        property var easeIn: Easing.InQuad
        property var easeOut: Easing.OutQuad
        property var easeInOut: Easing.InOutQuad
        property var easeBounce: Easing.OutBounce
        property var easeElastic: Easing.OutElastic
    }
    
    // Component heights
    readonly property var height: QtObject {
        property int tiny: 24
        property int small: 32
        property int medium: 40
        property int large: 48
        property int huge: 56
    }
    
    // Opacity values
    readonly property var opacity: QtObject {
        property real disabled: 0.38
        property real hint: 0.6
        property real divider: 0.12
        property real hover: 0.08
        property real pressed: 0.16
        property real focus: 0.12
    }
    
    // Gradient definitions
    readonly property var gradients: QtObject {
        property var primary: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: colors.primary }
            GradientStop { position: 1.0; color: colors.primaryVariant }
        }
        
        property var secondary: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: colors.secondary }
            GradientStop { position: 1.0; color: colors.secondaryVariant }
        }
        
        property var accent: Gradient {
            orientation: Gradient.Vertical
            GradientStop { position: 0.0; color: Qt.lighter(colors.accent, 1.1) }
            GradientStop { position: 1.0; color: colors.accent }
        }
        
        property var surface: Gradient {
            orientation: Gradient.Vertical
            GradientStop { position: 0.0; color: colors.surface }
            GradientStop { position: 1.0; color: colors.surfaceVariant }
        }
    }
    
    // Shadow definitions
    function shadow(elevation) {
        var depth = elevation || 0
        var color = colors.shadow
        
        if (depth === 0) return "transparent"
        
        var opacity = isDarkMode ? 0.4 : 0.2
        var blur = depth * 2
        var spread = depth / 2
        
        return Qt.rgba(color.r, color.g, color.b, opacity)
    }
    
    // Helper functions
    function alpha(color, opacity) {
        return Qt.rgba(color.r, color.g, color.b, opacity)
    }
    
    function blend(color1, color2, ratio) {
        ratio = Math.max(0, Math.min(1, ratio))
        return Qt.rgba(
            color1.r * (1 - ratio) + color2.r * ratio,
            color1.g * (1 - ratio) + color2.g * ratio,
            color1.b * (1 - ratio) + color2.b * ratio,
            color1.a * (1 - ratio) + color2.a * ratio
        )
    }
    
    function contrastColor(background) {
        // Calculate relative luminance
        var r = background.r
        var g = background.g
        var b = background.b
        
        var luminance = 0.299 * r + 0.587 * g + 0.114 * b
        
        return luminance > 0.5 ? "#000000" : "#FFFFFF"
    }
    
    // Responsive helpers
    readonly property bool isMobile: Qt.platform.os === "android" || Qt.platform.os === "ios"
    readonly property bool isDesktop: !isMobile
    readonly property real scaleFactor: isMobile ? 1.2 : 1.0
    
    // Status colors
    function statusColor(status) {
        switch(status) {
            case "error": return colors.error
            case "warning": return colors.warning
            case "success": return colors.success
            case "info": return colors.primary
            default: return colors.text
        }
    }
    
    // Relationship type colors (from Phase 4)
    function relationshipColor(type) {
        switch(type) {
            case "family": return "#4CAF50"
            case "friend": return "#2196F3"
            case "romantic": return "#E91E63"
            case "rival": return "#F44336"
            case "mentor": return "#9C27B0"
            case "student": return "#00BCD4"
            case "ally": return "#8BC34A"
            case "enemy": return "#FF5722"
            case "neutral": return "#607D8B"
            default: return colors.text
        }
    }
    
    // Event type colors (from Phase 4)
    function eventTypeColor(type) {
        switch(type) {
            case "birth": return "#4CAF50"
            case "death": return "#F44336"
            case "battle": return "#FF5722"
            case "achievement": return "#FFC107"
            case "tragedy": return "#9C27B0"
            case "milestone": return "#2196F3"
            case "relationship": return "#E91E63"
            case "discovery": return "#00BCD4"
            default: return colors.primary
        }
    }
    
    // Signal for theme changes
    signal themeChanged()
    
    // Connect to theme controller signals
    Component.onCompleted: {
        if (themeController) {
            themeController.themeChanged.connect(themeChanged)
        }
    }
}