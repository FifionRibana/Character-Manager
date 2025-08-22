/**
 * BiographyTab.qml
 * Character biography and affiliations editing tab
 * Features rich text editing and dynamic affiliations management
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"
// import "../styles"
import App.Styles

ScrollView {
    id: biographyTab
    
    property var characterModel
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: biographyTab.availableWidth
        spacing: AppTheme.spacing.large || 24
        
        // Title section
        Text {
            text: qsTr("Biography & Affiliations")
            font.family: AppTheme.fontFamily || "Inter"
            font.pixelSize: AppTheme.fontSize.tiny || 32
            font.bold: true
            color: AppTheme.colors.text || "#212121"
        }
        
        // Biography section
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.card.background || "#FFFFFF"
            border.color: AppTheme.card.border || "#E0E0E0"
            border.width: AppTheme.borderWidth || 1
            radius: AppTheme.radius.medium || 8
            
            implicitHeight: biographyContent.implicitHeight + 2 * (AppTheme.spacing.large || 24)
            
            ColumnLayout {
                id: biographyContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.large || 24
                spacing: AppTheme.spacing.medium || 16
                
                // Biography header
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: qsTr("Character Biography")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: AppTheme.colors.text || "#212121"
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        id: characterCount
                        text: (characterModel && characterModel.biography ? characterModel.biography.length : 0) + "/10000"
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.small || 12
                        color: getCharacterCountColor()
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.colors.border || "#E0E0E0"
                }
                
                // Biography text editor
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 300
                    Layout.minimumHeight: 200
                    
                    TextArea {
                        id: biographyTextArea
                        
                        text: characterModel && characterModel.biography ? characterModel.biography : ""
                        placeholderText: qsTr("Write your character's background story, personality, goals, and history here.\n\n" +
                                            "Consider including:\n" +
                                            "• Childhood and upbringing\n" +
                                            "• Major life events\n" +
                                            "• Personality traits and quirks\n" +
                                            "• Goals and motivations\n" +
                                            "• Fears and weaknesses\n" +
                                            "• Relationships with family and friends\n" +
                                            "• Professional background or training")
                        
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.medium || 14
                        color: AppTheme.colors.text || "#212121"
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: AppTheme.input.background || "#FFFFFF"
                            border.color: parent.activeFocus ? (AppTheme.colors.accent || "#FF5722") : (AppTheme.colors.border || "#E0E0E0")
                            border.width: parent.activeFocus ? 2 : 1
                            radius: 6
                            
                            Behavior on border.color {
                                ColorAnimation { duration: 150 }
                            }
                            
                            Behavior on border.width {
                                NumberAnimation { duration: 150 }
                            }
                        }
                        
                        onTextChanged: {
                            if (characterModel && text !== (characterModel.biography || "")) {
                                // Throttle updates to avoid excessive property changes
                                saveTimer.restart()
                            }
                        }
                        
                        // Auto-save timer
                        Timer {
                            id: saveTimer
                            interval: 500
                            onTriggered: {
                                if (characterModel) {
                                    characterModel.biography = biographyTextArea.text
                                }
                            }
                        }
                    }
                }
                
                // Writing tips
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.colors.backgroundVariant || "#F8F9FA"
                    border.color: AppTheme.colors.borderLight || "#DEE2E6"
                    border.width: 1
                    radius: 6
                    
                    implicitHeight: tipsContent.implicitHeight + 2 * (AppTheme.spacing.small || 8)
                    
                    RowLayout {
                        id: tipsContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.small || 8
                        spacing: AppTheme.spacing.small || 8
                        
                        Text {
                            text: "💡"
                            font.pixelSize: AppTheme.fontSize.medium || 14
                        }
                        
                        Text {
                            text: qsTr("Tip: A good biography helps bring your character to life. Focus on their personality, motivations, and what makes them unique.")
                            font.family: AppTheme.fontFamily || "Inter"
                            font.pixelSize: AppTheme.fontSize.small || 12
                            color: AppTheme.colors.textSecondary || "#757575"
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
        
        // Affiliations section
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.card.background || "#FFFFFF"
            border.color: AppTheme.card.border || "#E0E0E0"
            border.width: AppTheme.borderWidth || 1
            radius: AppTheme.radius.medium || 8
            
            implicitHeight: affiliationsContent.implicitHeight + 2 * (AppTheme.spacing.large || 24)
            
            ColumnLayout {
                id: affiliationsContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.large || 24
                spacing: AppTheme.spacing.medium || 16
                
                // Affiliations header
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: qsTr("Affiliations & Organizations")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: AppTheme.colors.text || "#212121"
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Button {
                        text: qsTr("Add Affiliation")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.medium || 14
                        
                        background: Rectangle {
                            color: parent.hovered ? Qt.lighter(AppTheme.colors.accent || "#FF5722", 1.1) : (AppTheme.colors.accent || "#FF5722")
                            radius: 6
                            
                            Behavior on color {
                                ColorAnimation { duration: 150 }
                            }
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: addAffiliationDialog.open()
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.colors.border || "#E0E0E0"
                }
                
                // Affiliations list
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: AppTheme.spacing.small || 8
                    
                    Repeater {
                        model: characterModel && characterModel.affiliations ? characterModel.affiliations : []
                        
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            implicitHeight: affiliationRow.implicitHeight + 2 * (AppTheme.spacing.small || 8)
                            color: AppTheme.colors.backgroundVariant || "#F8F9FA"
                            border.color: AppTheme.colors.borderLight || "#DEE2E6"
                            border.width: 1
                            radius: 6
                            
                            RowLayout {
                                id: affiliationRow
                                anchors.fill: parent
                                anchors.margins: AppTheme.spacing.small || 8
                                spacing: AppTheme.spacing.medium || 16
                                
                                // Organization icon
                                Rectangle {
                                    width: 40
                                    height: 40
                                    radius: 20
                                    color: AppTheme.colors.accent || "#FF5722"
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: getAffiliationIcon(modelData || "")
                                        font.family: AppTheme.fontFamily || "Inter"
                                        font.pixelSize: 20
                                        color: "white"
                                    }
                                }
                                
                                // Affiliation name
                                Text {
                                    text: modelData || ""
                                    font.family: AppTheme.fontFamily || "Inter"
                                    font.pixelSize: AppTheme.fontSize.medium || 14
                                    color: AppTheme.colors.text || "#212121"
                                    Layout.fillWidth: true
                                    elide: Text.ElideRight
                                }
                                
                                // Remove button
                                Button {
                                    text: "×"
                                    implicitWidth: 32
                                    implicitHeight: 32
                                    
                                    background: Rectangle {
                                        radius: 16
                                        color: parent.hovered ? "#e74c3c" : "transparent"
                                        border.color: "#e74c3c"
                                        border.width: 1
                                        
                                        Behavior on color {
                                            ColorAnimation { duration: 150 }
                                        }
                                    }
                                    
                                    contentItem: Text {
                                        text: parent.text
                                        font.family: AppTheme.fontFamily || "Inter"
                                        font.pixelSize: 16
                                        font.bold: true
                                        color: parent.hovered ? "white" : "#e74c3c"
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    
                                    onClicked: removeAffiliation(index)
                                    
                                    ToolTip {
                                        text: qsTr("Remove ") + (modelData || "")
                                        visible: parent.hovered
                                        delay: 500
                                    }
                                }
                            }
                        }
                    }
                    
                    // Empty state
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: 100
                        visible: !characterModel || !characterModel.affiliations || characterModel.affiliations.length === 0
                        color: "transparent"
                        border.color: AppTheme.colors.borderLight || "#DEE2E6"
                        border.width: 2
                        radius: 8
                        
                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: AppTheme.spacing.small || 8
                            
                            Text {
                                text: "🏛️"
                                font.pixelSize: 32
                                Layout.alignment: Qt.AlignHCenter
                            }
                            
                            Text {
                                text: qsTr("No affiliations yet")
                                font.family: AppTheme.fontFamily || "Inter"
                                font.pixelSize: AppTheme.fontSize.medium || 14
                                color: AppTheme.colors.textSecondary || "#757575"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            
                            Text {
                                text: qsTr("Add organizations, guilds, or groups your character belongs to")
                                font.family: AppTheme.fontFamily || "Inter"
                                font.pixelSize: AppTheme.fontSize.small || 12
                                color: AppTheme.colors.textSecondary || "#757575"
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }
                }
                
                // Affiliation examples
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.colors.backgroundVariant || "#F8F9FA"
                    border.color: AppTheme.colors.borderLight || "#DEE2E6"
                    border.width: 1
                    radius: 6
                    
                    implicitHeight: examplesContent.implicitHeight + 2 * (AppTheme.spacing.small || 8)
                    
                    RowLayout {
                        id: examplesContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.small || 8
                        spacing: AppTheme.spacing.small || 8
                        
                        Text {
                            text: "💡"
                            font.pixelSize: AppTheme.fontSize.medium || 14
                        }
                        
                        Text {
                            text: qsTr("Examples: Royal Guard, Thieves' Guild, Mages' College, Noble House Stark, Rangers of the North, Church of Light")
                            font.family: AppTheme.fontFamily || "Inter"
                            font.pixelSize: AppTheme.fontSize.small || 12
                            color: AppTheme.colors.textSecondary || "#757575"
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
    }
    
    // Add affiliation dialog
    Dialog {
        id: addAffiliationDialog
        title: qsTr("Add Affiliation")
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.8, 400)
        height: Math.min(parent.height * 0.6, 200)
        modal: true
        
        background: Rectangle {
            color: AppTheme.card.background || "#FFFFFF"
            border.color: AppTheme.card.border || "#E0E0E0"
            border.width: 2
            radius: 8
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: AppTheme.spacing.medium || 16
            
            Text {
                text: qsTr("Enter the name of the organization or group:")
                font.family: AppTheme.fontFamily || "Inter"
                font.pixelSize: AppTheme.fontSize.medium || 14
                color: AppTheme.colors.text || "#212121"
            }
            
            TextField {
                id: affiliationNameField
                Layout.fillWidth: true
                placeholderText: qsTr("e.g., Royal Guard, Thieves' Guild, etc.")
                font.family: AppTheme.fontFamily || "Inter"
                font.pixelSize: AppTheme.fontSize.medium || 14
                
                background: Rectangle {
                    color: AppTheme.input.background || "#FFFFFF"
                    border.color: parent.activeFocus ? (AppTheme.colors.accent || "#FF5722") : (AppTheme.colors.border || "#E0E0E0")
                    border.width: parent.activeFocus ? 2 : 1
                    radius: 4
                }
                
                Keys.onReturnPressed: addAffiliationDialog.accept()
                Keys.onEnterPressed: addAffiliationDialog.accept()
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: qsTr("Cancel")
                    onClicked: addAffiliationDialog.reject()
                }
                
                Button {
                    text: qsTr("Add")
                    enabled: affiliationNameField.text.trim().length > 0
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.hovered ? Qt.lighter(AppTheme.colors.accent || "#FF5722", 1.1) : (AppTheme.colors.accent || "#FF5722")) :
                               (AppTheme.colors.border || "#E0E0E0")
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.enabled ? "white" : (AppTheme.colors.textSecondary || "#757575")
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: addAffiliationDialog.accept()
                }
            }
        }
        
        onAccepted: {
            var name = affiliationNameField.text.trim()
            if (name.length > 0) {
                addAffiliation(name)
                affiliationNameField.clear()
            }
        }
        
        onOpened: {
            affiliationNameField.forceActiveFocus()
        }
    }
    
    // Helper functions
    function getCharacterCountColor() {
        if (!characterModel || !characterModel.biography) return AppTheme.colors.textSecondary || "#757575"
        
        var count = characterModel.biography.length
        if (count > 8000) return "#e74c3c"      // Red - approaching limit
        if (count > 5000) return "#f39c12"      // Orange - getting long
        return AppTheme.colors.textSecondary || "#757575"      // Normal
    }
    
    function getAffiliationIcon(affiliation) {
        var lower = affiliation.toLowerCase()
        
        // Organization type detection
        if (lower.includes("guild")) return "🔨"
        if (lower.includes("guard") || lower.includes("watch")) return "🛡️"
        if (lower.includes("church") || lower.includes("temple")) return "⛪"
        if (lower.includes("mage") || lower.includes("magic")) return "🔮"
        if (lower.includes("noble") || lower.includes("house")) return "👑"
        if (lower.includes("ranger") || lower.includes("forest")) return "🏹"
        if (lower.includes("merchant") || lower.includes("trade")) return "💰"
        if (lower.includes("academy") || lower.includes("school")) return "📚"
        if (lower.includes("order") || lower.includes("knight")) return "⚔️"
        
        // Default icon
        return "🏛️"
    }
    
    function addAffiliation(name) {
        if (!characterModel) return
        
        var affiliations = characterModel.affiliations || []
        
        // Check for duplicates
        for (var i = 0; i < affiliations.length; i++) {
            if (affiliations[i].toLowerCase() === name.toLowerCase()) {
                return // Duplicate found, don't add
            }
        }
        
        affiliations.push(name)
        characterModel.affiliations = affiliations
    }
    
    function removeAffiliation(index) {
        if (!characterModel) return
        
        var affiliations = characterModel.affiliations || []
        affiliations.splice(index, 1)
        characterModel.affiliations = affiliations
    }
}