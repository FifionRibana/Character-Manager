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
import "../styles"

ScrollView {
    id: biographyTab
    
    property var characterModel
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: biographyTab.availableWidth
        spacing: AppTheme.spacingLarge
        
        // Title section
        Text {
            text: qsTr("Biography & Affiliations")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSizeDisplay
            font.bold: true
            color: AppTheme.textColor
        }
        
        // Biography section
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: AppTheme.borderWidth
            radius: AppTheme.card.radius
            
            implicitHeight: biographyContent.implicitHeight + 2 * AppTheme.spacingLarge
            
            ColumnLayout {
                id: biographyContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacingLarge
                spacing: AppTheme.spacingMedium
                
                // Biography header
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: qsTr("Character Biography")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeHeading
                        font.bold: true
                        color: AppTheme.textColor
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        id: characterCount
                        text: (characterModel ? characterModel.biography.length : 0) + "/10000"
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeCaption
                        color: getCharacterCountColor()
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.borderColor
                }
                
                // Biography text editor
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 300
                    Layout.minimumHeight: 200
                    
                    TextArea {
                        id: biographyTextArea
                        
                        text: characterModel ? characterModel.biography : ""
                        placeholderText: qsTr("Write your character's background story, personality, goals, and history here.\n\n" +
                                            "Consider including:\n" +
                                            "• Childhood and upbringing\n" +
                                            "• Major life events\n" +
                                            "• Personality traits and quirks\n" +
                                            "• Goals and motivations\n" +
                                            "• Fears and weaknesses\n" +
                                            "• Relationships with family and friends\n" +
                                            "• Professional background or training")
                        
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeBody
                        color: AppTheme.textColor
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: AppTheme.inputBackground
                            border.color: parent.activeFocus ? AppTheme.accentColor : AppTheme.borderColor
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
                            if (characterModel && text !== characterModel.biography) {
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
                    color: AppTheme.backgroundColorSecondary
                    border.color: AppTheme.borderColorLight
                    border.width: 1
                    radius: 6
                    
                    implicitHeight: tipsContent.implicitHeight + 2 * AppTheme.spacingSmall
                    
                    RowLayout {
                        id: tipsContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacingSmall
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: "💡"
                            font.pixelSize: AppTheme.fontSizeBody
                        }
                        
                        Text {
                            text: qsTr("Tip: A good biography helps bring your character to life. Focus on their personality, motivations, and what makes them unique.")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeCaption
                            color: AppTheme.textColorSecondary
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
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: AppTheme.borderWidth
            radius: AppTheme.card.radius
            
            implicitHeight: affiliationsContent.implicitHeight + 2 * AppTheme.spacingLarge
            
            ColumnLayout {
                id: affiliationsContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacingLarge
                spacing: AppTheme.spacingMedium
                
                // Affiliations header
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: qsTr("Affiliations & Organizations")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeHeading
                        font.bold: true
                        color: AppTheme.textColor
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Button {
                        text: qsTr("Add Affiliation")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeBody
                        
                        background: Rectangle {
                            color: parent.hovered ? Qt.lighter(AppTheme.accentColor, 1.1) : AppTheme.accentColor
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
                    color: AppTheme.borderColor
                }
                
                // Affiliations list
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: AppTheme.spacingSmall
                    
                    Repeater {
                        model: characterModel ? characterModel.affiliations : []
                        
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            implicitHeight: affiliationRow.implicitHeight + 2 * AppTheme.spacingSmall
                            color: AppTheme.backgroundColorSecondary
                            border.color: AppTheme.borderColorLight
                            border.width: 1
                            radius: 6
                            
                            RowLayout {
                                id: affiliationRow
                                anchors.fill: parent
                                anchors.margins: AppTheme.spacingSmall
                                spacing: AppTheme.spacingMedium
                                
                                // Organization icon
                                Rectangle {
                                    width: 40
                                    height: 40
                                    radius: 20
                                    color: AppTheme.accentColor
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: getAffiliationIcon(modelData)
                                        font.family: AppTheme.fontFamily
                                        font.pixelSize: 20
                                        color: "white"
                                    }
                                }
                                
                                // Affiliation name
                                Text {
                                    text: modelData
                                    font.family: AppTheme.fontFamily
                                    font.pixelSize: AppTheme.fontSizeBody
                                    color: AppTheme.textColor
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
                                        font.family: AppTheme.fontFamily
                                        font.pixelSize: 16
                                        font.bold: true
                                        color: parent.hovered ? "white" : "#e74c3c"
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    
                                    onClicked: removeAffiliation(index)
                                    
                                    ToolTip {
                                        text: qsTr("Remove ") + modelData
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
                        visible: !characterModel || characterModel.affiliations.length === 0
                        color: "transparent"
                        border.color: AppTheme.borderColorLight
                        border.width: 2
                        radius: 8
                        
                        ColumnLayout {
                            anchors.centerIn: parent
                            spacing: AppTheme.spacingSmall
                            
                            Text {
                                text: "🏛️"
                                font.pixelSize: 32
                                Layout.alignment: Qt.AlignHCenter
                            }
                            
                            Text {
                                text: qsTr("No affiliations yet")
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeBody
                                color: AppTheme.textColorSecondary
                                Layout.alignment: Qt.AlignHCenter
                            }
                            
                            Text {
                                text: qsTr("Add organizations, guilds, or groups your character belongs to")
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeCaption
                                color: AppTheme.textColorSecondary
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                    }
                }
                
                // Affiliation examples
                Rectangle {
                    Layout.fillWidth: true
                    color: AppTheme.backgroundColorSecondary
                    border.color: AppTheme.borderColorLight
                    border.width: 1
                    radius: 6
                    
                    implicitHeight: examplesContent.implicitHeight + 2 * AppTheme.spacingSmall
                    
                    RowLayout {
                        id: examplesContent
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacingSmall
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: "💡"
                            font.pixelSize: AppTheme.fontSizeBody
                        }
                        
                        Text {
                            text: qsTr("Examples: Royal Guard, Thieves' Guild, Mages' College, Noble House Stark, Rangers of the North, Church of Light")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeCaption
                            color: AppTheme.textColorSecondary
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
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: 2
            radius: 8
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: AppTheme.spacingMedium
            
            Text {
                text: qsTr("Enter the name of the organization or group:")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeBody
                color: AppTheme.textColor
            }
            
            TextField {
                id: affiliationNameField
                Layout.fillWidth: true
                placeholderText: qsTr("e.g., Royal Guard, Thieves' Guild, etc.")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeBody
                
                background: Rectangle {
                    color: AppTheme.inputBackground
                    border.color: parent.activeFocus ? AppTheme.accentColor : AppTheme.borderColor
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
                               (parent.hovered ? Qt.lighter(AppTheme.accentColor, 1.1) : AppTheme.accentColor) :
                               AppTheme.borderColor
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.enabled ? "white" : AppTheme.textColorSecondary
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
        if (!characterModel) return AppTheme.textColorSecondary
        
        var count = characterModel.biography.length
        if (count > 8000) return "#e74c3c"      // Red - approaching limit
        if (count > 5000) return "#f39c12"      // Orange - getting long
        return AppTheme.textColorSecondary      // Normal
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