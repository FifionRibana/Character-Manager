pragma Singleton
import QtQuick

QtObject {
    id: theme

    // Color palette
    readonly property color primaryColor: "#4CAF50"
    readonly property color primaryColorDark: "#388E3C"
    readonly property color primaryColorLight: "#81C784"
    
    readonly property color accentColor: "#FF5722"
    readonly property color accentColorLight: "#FF8A65"
    
    readonly property color backgroundColor: "#F5F5F5"
    readonly property color surfaceColor: "#FFFFFF"
    readonly property color surfaceColorDark: "#FAFAFA"
    
    readonly property color textColor: "#212121"
    readonly property color textColorSecondary: "#757575"
    readonly property color textColorLight: "#FFFFFF"
    
    readonly property color borderColor: "#E0E0E0"
    readonly property color borderColorDark: "#BDBDBD"
    
    readonly property color errorColor: "#F44336"
    readonly property color warningColor: "#FF9800"
    readonly property color successColor: "#4CAF50"
    readonly property color infoColor: "#2196F3"
    
    readonly property color shadowColor: "#40000000"
    
    // Enneagram type colors
    readonly property var enneagramColors: [
        "#E3F2FD", // Type 1 - Light Blue
        "#F3E5F5", // Type 2 - Light Purple
        "#E8F5E8", // Type 3 - Light Green
        "#FFF3E0", // Type 4 - Light Orange
        "#E0F2F1", // Type 5 - Light Teal
        "#FCE4EC", // Type 6 - Light Pink
        "#FFFDE7", // Type 7 - Light Yellow
        "#FFEBEE", // Type 8 - Light Red
        "#F1F8E9"  // Type 9 - Light Light Green
    ]
    
    // Typography
    readonly property int fontSizeSmall: 12
    readonly property int fontSizeBody: 14
    readonly property int fontSizeSubheading: 16
    readonly property int fontSizeHeading: 18
    readonly property int fontSizeTitle: 20
    readonly property int fontSizeDisplay: 24
    
    readonly property string fontFamily: "Segoe UI"
    readonly property string fontFamilyMono: "Consolas"
    
    // Spacing
    readonly property int spacing: 8
    readonly property int spacingSmall: 4
    readonly property int spacingMedium: 12
    readonly property int spacingLarge: 16
    readonly property int spacingXLarge: 24
    
    // Dimensions
    readonly property int borderRadius: 4
    readonly property int borderRadiusLarge: 8
    readonly property int borderWidth: 1
    readonly property int borderWidthThick: 2
    
    readonly property int buttonHeight: 36
    readonly property int inputHeight: 40
    readonly property int toolbarHeight: 48
    readonly property int tabHeight: 48
    
    readonly property int sidebarWidth: 300
    readonly property int sidebarMinWidth: 250
    readonly property int sidebarMaxWidth: 400
    
    // Shadows
    readonly property int shadowOffset: 2
    readonly property int shadowBlur: 4
    readonly property int shadowSpread: 0
    
    // Animation
    readonly property int animationDuration: 200
    readonly property int animationDurationLong: 400
    readonly property int animationDurationShort: 100
    
    // Functions for dynamic colors
    function getEnneagramColor(type) {
        if (type >= 1 && type <= 9) {
            return enneagramColors[type - 1];
        }
        return surfaceColor;
    }
    
    function getStatModifierColor(modifier) {
        if (modifier > 0) return successColor;
        if (modifier < 0) return errorColor;
        return textColorSecondary;
    }
    
    function getDevelopmentLevelColor(level) {
        if (level <= 3) return successColor;
        if (level <= 6) return warningColor;
        return errorColor;
    }
    
    // Button styles
    readonly property QtObject button: QtObject {
        readonly property color normal: primaryColor
        readonly property color hovered: primaryColorDark
        readonly property color pressed: Qt.darker(primaryColorDark, 1.2)
        readonly property color disabled: borderColor
        
        readonly property color destructiveNormal: errorColor
        readonly property color destructiveHovered: Qt.darker(errorColor, 1.1)
        readonly property color destructivePressed: Qt.darker(errorColor, 1.2)
        
        readonly property color secondaryNormal: "transparent"
        readonly property color secondaryHovered: surfaceColorDark
        readonly property color secondaryPressed: borderColor
    }
    
    // Input styles
    readonly property QtObject input: QtObject {
        readonly property color background: surfaceColor
        readonly property color backgroundFocused: surfaceColor
        readonly property color border: borderColor
        readonly property color borderFocused: primaryColor
        readonly property color text: textColor
        readonly property color placeholder: textColorSecondary
    }
    
    // Card styles
    readonly property QtObject card: QtObject {
        readonly property color background: surfaceColor
        readonly property color border: borderColor
        readonly property int elevation: 2
        readonly property int radius: borderRadius
    }
    
    // Stat colors for ability scores
    function getStatColor(value) {
        if (value >= 16) return "#4CAF50";      // Green for high stats
        if (value >= 14) return "#8BC34A";      // Light green
        if (value >= 12) return "#CDDC39";      // Yellow-green
        if (value >= 10) return "#FFC107";      // Amber for average
        if (value >= 8) return "#FF9800";       // Orange for low
        return "#F44336";                       // Red for very low
    }
    
    // Relationship type colors
    readonly property var relationshipColors: ({
        "family": "#E91E63",      // Pink
        "friend": "#4CAF50",      // Green
        "rival": "#FF5722",       // Deep Orange
        "mentor": "#3F51B5",      // Indigo
        "student": "#00BCD4",     // Cyan
        "ally": "#8BC34A",        // Light Green
        "enemy": "#F44336",       // Red
        "romantic": "#E91E63",    // Pink
        "neutral": "#9E9E9E"      // Grey
    })
    
    function getRelationshipColor(type) {
        return relationshipColors[type] || textColorSecondary;
    }
}