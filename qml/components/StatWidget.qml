/**
 * StatWidget.qml
 * Reusable component for displaying and editing individual character stats
 * Features interactive editing, D&D modifiers, and visual feedback
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: statWidget
    
    // Public properties
    property string statName: "Stat"
    property string statAbbreviation: "STR"
    property string statDescription: "Stat description"
    property int statValue: 10
    property int minValue: 1
    property int maxValue: 25
    property bool editMode: true
    
    // Visual properties
    property real animationDuration: 200
    
    // Signals
    signal valueChanged(int newValue)
    signal valueIncreased()
    signal valueDecreased()
    
    // Computed properties
    readonly property int modifier: Math.floor((statValue - 10) / 2)
    readonly property string modifierText: modifier >= 0 ? "+" + modifier : modifier.toString()
    readonly property color statColor: getStatColor(statValue)
    readonly property color modifierColor: getModifierColor(modifier)
    
    // Widget styling
    color: AppTheme.card.background
    border.color: AppTheme.card.border
    border.width: AppTheme.borderWidth
    radius: AppTheme.card.radius
    
    implicitWidth: 220
    implicitHeight: 160
    
    // Hover effect
    Rectangle {
        anchors.fill: parent
        color: AppTheme.accentColor
        opacity: parent.hovered ? 0.05 : 0
        radius: parent.radius
        
        Behavior on opacity {
            NumberAnimation { duration: animationDuration }
        }
    }
    
    // Mouse area for hover detection
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.NoButton // Don't consume clicks
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: AppTheme.spacingMedium
        spacing: AppTheme.spacingSmall
        
        // Header section
        RowLayout {
            Layout.fillWidth: true
            
            // Stat name and abbreviation
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                
                Text {
                    text: statName
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeHeading
                    font.bold: true
                    color: AppTheme.textColor
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }
                
                Text {
                    text: statAbbreviation
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeCaption
                    color: AppTheme.textColorSecondary
                    font.bold: true
                }
            }
            
            // Decrease button
            Button {
                implicitWidth: 32
                implicitHeight: 32
                enabled: editMode && statValue > minValue
                
                background: Rectangle {
                    radius: 16
                    color: parent.enabled ? 
                           (parent.pressed ? Qt.darker("#e74c3c", 1.2) : 
                            parent.hovered ? Qt.lighter("#e74c3c", 1.1) : "#e74c3c") :
                           AppTheme.borderColor
                    
                    Behavior on color {
                        ColorAnimation { duration: animationDuration }
                    }
                }
                
                contentItem: Text {
                    text: "−"
                    font.family: AppTheme.fontFamily
                    font.pixelSize: 18
                    font.bold: true
                    color: parent.enabled ? "white" : AppTheme.textColorSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    if (statValue > minValue) {
                        valueChanged(statValue - 1)
                        valueDecreased()
                    }
                }
                
                ToolTip {
                    text: qsTr("Decrease ") + statName
                    visible: parent.hovered && parent.enabled
                    delay: 500
                }
            }
        }
        
        // Value display section
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            color: statColor
            border.color: Qt.darker(statColor, 1.2)
            border.width: 2
            radius: 8
            
            // Subtle gradient effect
            Rectangle {
                anchors.fill: parent
                anchors.margins: 2
                color: "transparent"
                border.color: "white"
                border.width: 1
                radius: 6
                opacity: 0.3
            }
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 8
                
                // Main stat value
                Text {
                    text: statValue.toString()
                    font.family: AppTheme.fontFamily
                    font.pixelSize: 28
                    font.bold: true
                    color: "white"
                    Layout.alignment: Qt.AlignCenter
                }
                
                Rectangle {
                    width: 1
                    Layout.fillHeight: true
                    color: "white"
                    opacity: 0.5
                }
                
                // Modifier display
                ColumnLayout {
                    Layout.alignment: Qt.AlignCenter
                    spacing: 2
                    
                    Text {
                        text: qsTr("MOD")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeCaption
                        color: "white"
                        opacity: 0.8
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: modifierText
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeHeading
                        font.bold: true
                        color: "white"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
            
            // Click to edit (SpinBox overlay)
            SpinBox {
                id: spinBox
                anchors.fill: parent
                from: minValue
                to: maxValue
                value: statValue
                visible: false
                
                background: Rectangle {
                    color: AppTheme.inputBackground
                    border.color: AppTheme.accentColor
                    border.width: 2
                    radius: 8
                }
                
                onValueChanged: {
                    if (value !== statWidget.statValue) {
                        statWidget.valueChanged(value)
                    }
                }
                
                Keys.onReturnPressed: visible = false
                Keys.onEnterPressed: visible = false
                Keys.onEscapePressed: {
                    value = statWidget.statValue
                    visible = false
                }
                
                onVisibleChanged: {
                    if (visible) {
                        forceActiveFocus()
                    }
                }
            }
            
            // Click area for direct editing
            MouseArea {
                anchors.fill: parent
                enabled: editMode
                
                onDoubleClicked: {
                    spinBox.visible = true
                    spinBox.forceActiveFocus()
                }
            }
        }
        
        // Bottom section
        RowLayout {
            Layout.fillWidth: true
            
            // Increase button
            Button {
                implicitWidth: 32
                implicitHeight: 32
                enabled: editMode && statValue < maxValue
                
                background: Rectangle {
                    radius: 16
                    color: parent.enabled ? 
                           (parent.pressed ? Qt.darker("#2ecc71", 1.2) : 
                            parent.hovered ? Qt.lighter("#2ecc71", 1.1) : "#2ecc71") :
                           AppTheme.borderColor
                    
                    Behavior on color {
                        ColorAnimation { duration: animationDuration }
                    }
                }
                
                contentItem: Text {
                    text: "+"
                    font.family: AppTheme.fontFamily
                    font.pixelSize: 18
                    font.bold: true
                    color: parent.enabled ? "white" : AppTheme.textColorSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    if (statValue < maxValue) {
                        valueChanged(statValue + 1)
                        valueIncreased()
                    }
                }
                
                ToolTip {
                    text: qsTr("Increase ") + statName
                    visible: parent.hovered && parent.enabled
                    delay: 500
                }
            }
            
            Item { Layout.fillWidth: true }
            
            // Range indicator
            Text {
                text: minValue + "–" + maxValue
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeCaption
                color: AppTheme.textColorSecondary
                font.italic: true
            }
        }
    }
    
    // Tooltip for description
    ToolTip {
        id: descriptionTooltip
        text: statDescription
        visible: mouseArea.containsMouse && !spinBox.visible
        delay: 1000
        timeout: 5000
    }
    
    // Visual feedback animations
    SequentialAnimation {
        id: increaseAnimation
        PropertyAnimation {
            target: statWidget
            property: "scale"
            to: 1.05
            duration: animationDuration / 2
            easing.type: Easing.OutCubic
        }
        PropertyAnimation {
            target: statWidget
            property: "scale"
            to: 1.0
            duration: animationDuration / 2
            easing.type: Easing.InCubic
        }
    }
    
    SequentialAnimation {
        id: decreaseAnimation
        PropertyAnimation {
            target: statWidget
            property: "scale"
            to: 0.95
            duration: animationDuration / 2
            easing.type: Easing.OutCubic
        }
        PropertyAnimation {
            target: statWidget
            property: "scale"
            to: 1.0
            duration: animationDuration / 2
            easing.type: Easing.InCubic
        }
    }
    
    // Connect animations to value changes
    onValueIncreased: increaseAnimation.start()
    onValueDecreased: decreaseAnimation.start()
    
    // Helper functions
    function getStatColor(value) {
        // Color coding based on stat value
        if (value >= 18) return "#8e44ad"      // Epic (purple)
        if (value >= 16) return "#2ecc71"      // Excellent (green)
        if (value >= 14) return "#3498db"      // Good (blue)
        if (value >= 12) return "#f39c12"      // Above average (orange)
        if (value >= 10) return "#95a5a6"      // Average (gray)
        if (value >= 8) return "#e67e22"       // Below average (dark orange)
        return "#e74c3c"                       // Poor (red)
    }
    
    function getModifierColor(modifier) {
        if (modifier > 0) return "#2ecc71"     // Positive - green
        if (modifier < 0) return "#e74c3c"     // Negative - red
        return "#95a5a6"                       // Zero - gray
    }
    
    function getStatDescription(value) {
        if (value >= 18) return qsTr("Legendary")
        if (value >= 16) return qsTr("Exceptional")
        if (value >= 14) return qsTr("Very Good")
        if (value >= 12) return qsTr("Good")
        if (value >= 10) return qsTr("Average")
        if (value >= 8) return qsTr("Below Average")
        return qsTr("Poor")
    }
}