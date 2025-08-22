/**
 * EnneagramTab.qml
 * Complete Enneagram personality editing tab
 * Includes EnneagramWheel and all psychological aspects
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
// import "../styles"
import App.Styles

ScrollView {
    id: enneagramTab
    
    property var characterModel
    property alias selectedType: enneagramWheel.selectedType
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: enneagramTab.availableWidth
        spacing: AppTheme.spacing.large
        
        // Title section
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: qsTr("Enneagram Profile")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.tiny
                font.bold: true
                color: AppTheme.colors.text
            }
            
            Item { Layout.fillWidth: true }
            
            // Quick help button
            Button {
                text: "?"
                implicitWidth: 32
                implicitHeight: 32
                font.bold: true
                
                background: Rectangle {
                    radius: 16
                    color: AppTheme.colors.accent
                    opacity: parent.hovered ? 0.8 : 0.6
                    
                    Behavior on opacity {
                        NumberAnimation { duration: 150 }
                    }
                }
                
                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: helpPopup.open()
            }
        }
        
        // Main content
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.large
            
            // Left panel - Enneagram Wheel
            Rectangle {
                Layout.preferredWidth: 480
                Layout.preferredHeight: 480
                Layout.alignment: Qt.AlignTop
                
                color: AppTheme.card.background
                border.color: AppTheme.card.border
                border.width: AppTheme.borderWidth
                radius: AppTheme.radius.medium
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: AppTheme.spacing.medium
                    spacing: AppTheme.spacing.medium
                    
                    // Wheel title
                    Text {
                        text: qsTr("Enneagram Wheel")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.large
                        font.bold: true
                        color: AppTheme.colors.text
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    // The wheel component
                    EnneagramWheel {
                        id: enneagramWheel
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.minimumWidth: 400
                        Layout.minimumHeight: 400
                        
                        selectedType: characterModel && characterModel.enneagramType !== undefined ? 
                                    characterModel.enneagramType : 9
                        
                        onTypeSelected: function(type) {
                            if (characterModel) {
                                characterModel.enneagramType = type
                                updateWingOptions()
                            }
                        }
                        
                        onTypeHovered: function(type) {
                            if (type > 0) {
                                typeInfoText.text = getTypeDescription(type)
                            } else {
                                typeInfoText.text = qsTr("Hover over a type to see its description")
                            }
                        }
                    }
                    
                    // Type info display
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 60
                        color: AppTheme.colors.backgroundVariant || "#F8F9FA"
                        border.color: AppTheme.colors.borderLight || "#DEE2E6"
                        border.width: 1
                        radius: 6
                        
                        Text {
                            id: typeInfoText
                            anchors.fill: parent
                            anchors.margins: 12
                            text: qsTr("Hover over a type to see its description")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            wrapMode: Text.WordWrap
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
            
            // Right panel - Controls and details
            ColumnLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
                spacing: AppTheme.spacing.medium
                
                // Core Type Information
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.card.background
                    border.color: AppTheme.card.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.radius.medium
                    
                    implicitHeight: coreTypeContent.implicitHeight + 2 * AppTheme.spacing.medium
                    
                    ColumnLayout {
                        id: coreTypeContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.small
                        
                        Text {
                            text: qsTr("Core Type")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.large
                            font.bold: true
                            color: AppTheme.colors.text
                        }
                        
                        Rectangle {
                            Layout.fillWidth: true
                            height: 1
                            color: AppTheme.colors.border
                        }
                        
                        Text {
                            text: qsTr("Selected Type") + ": " + 
                                  getTypeName(enneagramWheel.selectedType)
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.text
                            font.bold: true
                        }
                        
                        Text {
                            text: getTypeTitle(enneagramWheel.selectedType)
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            font.italic: true
                        }
                    }
                }
                
                // Wing Selection
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.card.background
                    border.color: AppTheme.card.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.radius.medium
                    
                    implicitHeight: wingContent.implicitHeight + 2 * AppTheme.spacing.medium
                    
                    ColumnLayout {
                        id: wingContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.small
                        
                        Text {
                            text: qsTr("Wing")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.large
                            font.bold: true
                            color: AppTheme.colors.text
                        }
                        
                        ComboBox {
                            id: wingComboBox
                            Layout.fillWidth: true
                            
                            model: wingModel
                            textRole: "text"
                            valueRole: "value"
                            
                            background: Rectangle {
                                color: AppTheme.input.background
                                border.color: AppTheme.colors.border
                                border.width: 1
                                radius: 4
                            }
                            
                            onCurrentValueChanged: {
                                if (characterModel && currentValue !== undefined) {
                                    characterModel.enneagramWing = currentValue
                                }
                            }
                        }
                        
                        Text {
                            id: wingNotationText
                            text: getWingNotation()
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            font.bold: true
                            color: AppTheme.colors.accent
                            visible: wingComboBox.currentValue > 0
                        }
                    }
                }
                
                // Instinctual Variant
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.card.background
                    border.color: AppTheme.card.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.radius.medium
                    
                    implicitHeight: instinctContent.implicitHeight + 2 * AppTheme.spacing.medium
                    
                    ColumnLayout {
                        id: instinctContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.small
                        
                        Text {
                            text: qsTr("Instinctual Variant")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.large
                            font.bold: true
                            color: AppTheme.colors.text
                        }
                        
                        Text {
                            text: qsTr("Primary instinct (most developed)")
                            font.family: AppTheme.fontFamily || "Inter"
                            font.pixelSize: AppTheme.fontSize.small || 12
                            color: AppTheme.colors.textSecondary
                        }
                        
                        ComboBox {
                            id: instinctComboBox
                            Layout.fillWidth: true
                            
                            model: [
                                {text: qsTr("Self-Preservation (SP)"), value: "sp"},
                                {text: qsTr("Social (SO)"), value: "so"},
                                {text: qsTr("Sexual/One-to-One (SX)"), value: "sx"}
                            ]
                            
                            textRole: "text"
                            valueRole: "value"
                            
                            background: Rectangle {
                                color: AppTheme.input.background
                                border.color: AppTheme.colors.border
                                border.width: 1
                                radius: 4
                            }
                            
                            onCurrentValueChanged: {
                                if (characterModel && currentValue !== undefined) {
                                    characterModel.instinctualVariant = currentValue
                                }
                            }
                        }
                    }
                }
                
                // Development Level
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.card.background
                    border.color: AppTheme.card.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.radius.medium
                    
                    implicitHeight: developmentContent.implicitHeight + 2 * AppTheme.spacing.medium
                    
                    ColumnLayout {
                        id: developmentContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.small
                        
                        Text {
                            text: qsTr("Development Level")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.large
                            font.bold: true
                            color: AppTheme.colors.text
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            
                            Text {
                                text: qsTr("Healthy")
                                font.family: AppTheme.fontFamily || "Inter"
                                font.pixelSize: AppTheme.fontSize.small || 12
                                color: "#2ecc71"
                            }
                            
                            Slider {
                                id: developmentSlider
                                Layout.fillWidth: true
                                from: 1
                                to: 9
                                value: characterModel && characterModel.developmentLevel !== undefined ? 
                                      characterModel.developmentLevel : 5
                                stepSize: 1
                                snapMode: Slider.SnapAlways
                                
                                onValueChanged: {
                                    if (characterModel && value !== undefined) {
                                        characterModel.developmentLevel = value
                                    }
                                }
                                
                                background: Rectangle {
                                    x: developmentSlider.leftPadding
                                    y: developmentSlider.topPadding + developmentSlider.availableHeight / 2 - height / 2
                                    implicitWidth: 200
                                    implicitHeight: 4
                                    width: developmentSlider.availableWidth
                                    height: implicitHeight
                                    radius: 2
                                    color: AppTheme.colors.border
                                    
                                    Rectangle {
                                        width: developmentSlider.visualPosition * parent.width
                                        height: parent.height
                                        color: getDevelopmentColor(developmentSlider.value)
                                        radius: 2
                                    }
                                }
                                
                                handle: Rectangle {
                                    x: developmentSlider.leftPadding + developmentSlider.visualPosition * (developmentSlider.availableWidth - width)
                                    y: developmentSlider.topPadding + developmentSlider.availableHeight / 2 - height / 2
                                    implicitWidth: 20
                                    implicitHeight: 20
                                    radius: 10
                                    color: getDevelopmentColor(developmentSlider.value)
                                    border.color: AppTheme.colors.border
                                    border.width: 2
                                }
                            }
                            
                            Text {
                                text: qsTr("Unhealthy")
                                font.family: AppTheme.fontFamily || "Inter"
                                font.pixelSize: AppTheme.fontSize.small || 12
                                color: "#e74c3c"
                            }
                        }
                        
                        Text {
                            text: qsTr("Level") + " " + Math.round(developmentSlider.value) + 
                                  " - " + getDevelopmentLevelName(Math.round(developmentSlider.value))
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.text
                            font.bold: true
                        }
                    }
                }
                
                // Integration/Disintegration info
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.card.background
                    border.color: AppTheme.card.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.radius.medium
                    
                    implicitHeight: connectionContent.implicitHeight + 2 * AppTheme.spacing.medium
                    
                    ColumnLayout {
                        id: connectionContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.small
                        
                        Text {
                            text: qsTr("Connections")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.large
                            font.bold: true
                            color: AppTheme.colors.text
                        }
                        
                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            columnSpacing: AppTheme.spacing.medium
                            rowSpacing: AppTheme.spacing.small
                            
                            Text {
                                text: qsTr("Integration (Growth):")
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.medium
                                color: AppTheme.colors.textSecondary
                            }
                            
                            Text {
                                text: qsTr("Type") + " " + getIntegrationPoint(enneagramWheel.selectedType)
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.medium
                                color: "#2ecc71"
                                font.bold: true
                            }
                            
                            Text {
                                text: qsTr("Disintegration (Stress):")
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.medium
                                color: AppTheme.colors.textSecondary
                            }
                            
                            Text {
                                text: qsTr("Type") + " " + getDisintegrationPoint(enneagramWheel.selectedType)
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.medium
                                color: "#e74c3c"
                                font.bold: true
                            }
                        }
                        
                        Text {
                            text: qsTr("Green arrows show growth direction, red arrows show stress direction")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.small || 12
                            color: AppTheme.colors.textSecondary
                            font.italic: true
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
    }
    
    // Wing model for ComboBox
    ListModel {
        id: wingModel
        
        ListElement { text: "No Wing"; value: 0 }
        // Will be populated based on selected type
    }
    
    // Help popup
    Popup {
        id: helpPopup
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.8, 600)
        height: Math.min(parent.height * 0.8, 500)
        modal: true
        focus: true
        
        background: Rectangle {
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: 2
            radius: 8
        }
        
        ScrollView {
            anchors.fill: parent
            anchors.margins: 20
            
            Text {
                width: helpPopup.width - 40
                text: getEnneagramHelp()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                wrapMode: Text.WordWrap
            }
        }
    }
    
    // Functions
    function updateWingOptions() {
        wingModel.clear()
        wingModel.append({text: qsTr("No Wing"), value: 0})
        
        var type = enneagramWheel.selectedType
        var leftWing = type === 1 ? 9 : type - 1
        var rightWing = type === 9 ? 1 : type + 1
        
        wingModel.append({text: qsTr("Wing") + " " + leftWing, value: leftWing})
        wingModel.append({text: qsTr("Wing") + " " + rightWing, value: rightWing})
    }
    
    function getWingNotation() {
        if (wingComboBox.currentValue <= 0) return ""
        return enneagramWheel.selectedType + "w" + wingComboBox.currentValue
    }
    
    function getTypeName(type) {
        var names = {
            1: qsTr("Type 1"), 2: qsTr("Type 2"), 3: qsTr("Type 3"),
            4: qsTr("Type 4"), 5: qsTr("Type 5"), 6: qsTr("Type 6"),
            7: qsTr("Type 7"), 8: qsTr("Type 8"), 9: qsTr("Type 9")
        }
        return names[type] || qsTr("Unknown")
    }
    
    function getTypeTitle(type) {
        var titles = {
            1: qsTr("The Reformer"), 2: qsTr("The Helper"), 3: qsTr("The Achiever"),
            4: qsTr("The Individualist"), 5: qsTr("The Investigator"), 6: qsTr("The Loyalist"),
            7: qsTr("The Enthusiast"), 8: qsTr("The Challenger"), 9: qsTr("The Peacemaker")
        }
        return titles[type] || ""
    }
    
    function getTypeDescription(type) {
        var descriptions = {
            1: qsTr("Rational, idealistic, principled, purposeful, self-controlled, and perfectionistic."),
            2: qsTr("Caring, interpersonal, demonstrative, generous, people-pleasing, and possessive."),
            3: qsTr("Success-oriented, pragmatic, adaptive, driven, image-conscious, and hostility."),
            4: qsTr("Sensitive, introspective, expressive, dramatic, self-absorbed, and temperamental."),
            5: qsTr("Intense, cerebral, perceptive, innovative, secretive, and isolated."),
            6: qsTr("Committed, security-oriented, engaging, responsible, anxious, and suspicious."),
            7: qsTr("Spontaneous, versatile, acquisitive, scattered, enthusiastic, and escapist."),
            8: qsTr("Self-confident, decisive, willful, confrontational, controlling, and intense."),
            9: qsTr("Receptive, reassuring, complacent, resigned, passive-aggressive, and stubborn.")
        }
        return descriptions[type] || ""
    }
    
    function getIntegrationPoint(type) {
        var integrations = {1: 7, 2: 4, 3: 6, 4: 1, 5: 8, 6: 9, 7: 5, 8: 2, 9: 3}
        return integrations[type] || 0
    }
    
    function getDisintegrationPoint(type) {
        var disintegrations = {1: 4, 2: 8, 3: 9, 4: 2, 5: 7, 6: 3, 7: 1, 8: 5, 9: 6}
        return disintegrations[type] || 0
    }
    
    function getDevelopmentColor(level) {
        if (level <= 3) return "#2ecc71"      // Healthy - Green
        if (level <= 6) return "#f39c12"     // Average - Orange
        return "#e74c3c"                     // Unhealthy - Red
    }
    
    function getDevelopmentLevelName(level) {
        var names = {
            1: qsTr("Liberation"), 2: qsTr("Psychological Capacity"), 3: qsTr("Social Value"),
            4: qsTr("Imbalance"), 5: qsTr("Interpersonal Control"), 6: qsTr("Overcompensation"),
            7: qsTr("Violation"), 8: qsTr("Obsession"), 9: qsTr("Pathological")
        }
        return names[level] || ""
    }
    
    function getEnneagramHelp() {
        return qsTr("The Enneagram is a powerful personality system that describes nine distinct patterns of thinking, feeling, and acting.\n\n") +
               qsTr("• Click on numbers around the wheel to select your core type\n") +
               qsTr("• Choose a wing (adjacent type that influences your core type)\n") +
               qsTr("• Select your instinctual variant (primary life focus)\n") +
               qsTr("• Set your development level (psychological health)\n\n") +
               qsTr("The colored lines show integration (growth) and disintegration (stress) patterns between types.")
    }
    
    // Initialize when character changes
    onCharacterModelChanged: {
        if (characterModel) {
            enneagramWheel.selectedType = characterModel.enneagramType || 9
            updateWingOptions()
        }
    }
    
    Component.onCompleted: {
        updateWingOptions()
    }
}