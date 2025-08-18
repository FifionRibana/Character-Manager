import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ScrollView {
    id: relationshipsTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: relationshipsTab.availableWidth
        spacing: 24
        
        // Relationships section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: relationshipsContent.implicitHeight + 32
            
            ColumnLayout {
                id: relationshipsContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: "Character Relationships"
                        font.pixelSize: 20
                        font.bold: true
                        color: "#212121"
                        Layout.fillWidth: true
                    }
                    
                    Button {
                        text: "Add Relationship"
                        onClicked: addRelationshipDialog.open()
                        
                        background: Rectangle {
                            color: parent.pressed ? "#388E3C" : 
                                   parent.hovered ? "#45A049" : "#4CAF50"
                            radius: 4
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "#ffffff"
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                Text {
                    text: "Relationships with other characters, NPCs, or important people in the character's life."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                // Relationships list
                ListView {
                    id: relationshipsList
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.min(contentHeight, 300)
                    Layout.minimumHeight: 100
                    
                    clip: true
                    spacing: 8
                    
                    model: ListModel {
                        id: relationshipsModel
                        
                        // Example data
                        ListElement {
                            name: "Aria Moonwhisper"
                            type: "friend"
                            description: "Childhood friend and trusted ally"
                        }
                        ListElement {
                            name: "Baron Aldric"
                            type: "enemy"
                            description: "Corrupt noble who wronged the character's family"
                        }
                        ListElement {
                            name: "Master Chen"
                            type: "mentor"
                            description: "Wise teacher who trained the character in combat"
                        }
                    }
                    
                    delegate: Rectangle {
                        width: relationshipsList.width
                        height: relationshipContent.implicitHeight + 16
                        color: "#f9f9f9"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 6
                        
                        RowLayout {
                            id: relationshipContent
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 12
                            
                            // Relationship type icon
                            Rectangle {
                                width: 40
                                height: 40
                                radius: 20
                                color: getRelationshipColor(model.type)
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: getRelationshipIcon(model.type)
                                    font.pixelSize: 16
                                    color: "#ffffff"
                                }
                            }
                            
                            // Relationship info
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 4
                                
                                RowLayout {
                                    Layout.fillWidth: true
                                    
                                    Text {
                                        text: model.name
                                        font.pixelSize: 14
                                        font.bold: true
                                        color: "#212121"
                                        Layout.fillWidth: true
                                    }
                                    
                                    Rectangle {
                                        height: 20
                                        width: typeText.implicitWidth + 16
                                        radius: 10
                                        color: getRelationshipColor(model.type)
                                        
                                        Text {
                                            id: typeText
                                            anchors.centerIn: parent
                                            text: capitalizeFirst(model.type)
                                            font.pixelSize: 10
                                            font.bold: true
                                            color: "#ffffff"
                                        }
                                    }
                                }
                                
                                Text {
                                    text: model.description
                                    font.pixelSize: 12
                                    color: "#757575"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                            }
                            
                            // Actions
                            ColumnLayout {
                                spacing: 4
                                
                                Button {
                                    text: "✏️"
                                    width: 28
                                    height: 28
                                    
                                    background: Rectangle {
                                        color: parent.pressed ? "#2196F3" : 
                                               parent.hovered ? "#42A5F5" : "transparent"
                                        radius: 14
                                    }
                                    
                                    onClicked: {
                                        // TODO: Open edit dialog
                                        console.log("Edit relationship:", model.name)
                                    }
                                }
                                
                                Button {
                                    text: "🗑️"
                                    width: 28
                                    height: 28
                                    
                                    background: Rectangle {
                                        color: parent.pressed ? "#F44336" : 
                                               parent.hovered ? "#EF5350" : "transparent"
                                        radius: 14
                                    }
                                    
                                    onClicked: {
                                        relationshipsModel.remove(index)
                                    }
                                }
                            }
                        }
                    }
                    
                    // Empty state
                    Text {
                        anchors.centerIn: parent
                        text: "No relationships yet.\nClick 'Add Relationship' to add one."
                        font.pixelSize: 12
                        color: "#757575"
                        horizontalAlignment: Text.AlignHCenter
                        visible: relationshipsList.count === 0
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // Add relationship dialog
    Dialog {
        id: addRelationshipDialog
        title: "Add Relationship"
        modal: true
        anchors.centerIn: parent
        width: 400
        height: 300
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12
            
            // Character name
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Character Name:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                TextField {
                    id: relationshipNameField
                    Layout.fillWidth: true
                    placeholderText: "e.g., Aria Moonwhisper, Lord Blackwood, etc."
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                        border.width: 1
                        radius: 4
                    }
                }
            }
            
            // Relationship type
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Relationship Type:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                ComboBox {
                    id: relationshipTypeCombo
                    Layout.fillWidth: true
                    
                    model: [
                        {text: "Family", value: "family"},
                        {text: "Friend", value: "friend"},
                        {text: "Rival", value: "rival"},
                        {text: "Mentor", value: "mentor"},
                        {text: "Student", value: "student"},
                        {text: "Ally", value: "ally"},
                        {text: "Enemy", value: "enemy"},
                        {text: "Romantic", value: "romantic"},
                        {text: "Neutral", value: "neutral"}
                    ]
                    
                    textRole: "text"
                    valueRole: "value"
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 4
                    }
                }
            }
            
            // Description
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Description:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80
                    
                    TextArea {
                        id: relationshipDescField
                        placeholderText: "Describe the relationship, how they met, current status, etc."
                        wrapMode: TextArea.WordWrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                    }
                }
            }
            
            // Buttons
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Cancel"
                    onClicked: addRelationshipDialog.close()
                }
                
                Button {
                    text: "Add"
                    enabled: relationshipNameField.text.trim() !== ""
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.pressed ? "#388E3C" : 
                                parent.hovered ? "#45A049" : "#4CAF50") :
                               "#e0e0e0"
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.enabled ? "#ffffff" : "#757575"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (relationshipNameField.text.trim() !== "") {
                            addRelationship(
                                relationshipNameField.text.trim(),
                                relationshipTypeCombo.currentValue,
                                relationshipDescField.text.trim()
                            )
                            addRelationshipDialog.close()
                        }
                    }
                }
            }
        }
        
        onOpened: {
            relationshipNameField.text = ""
            relationshipDescField.text = ""
            relationshipTypeCombo.currentIndex = 1 // Default to "friend"
            relationshipNameField.forceActiveFocus()
        }
    }
    
    // Helper functions
    function addRelationship(name, type, description) {
        relationshipsModel.append({
            "name": name,
            "type": type,
            "description": description
        })
        
        // TODO: Update character model
        console.log("Added relationship:", name, type, description)
    }
    
    function getRelationshipColor(type) {
        const colors = {
            "family": "#E91E63",      // Pink
            "friend": "#4CAF50",      // Green
            "rival": "#FF5722",       // Deep Orange
            "mentor": "#3F51B5",      // Indigo
            "student": "#00BCD4",     // Cyan
            "ally": "#8BC34A",        // Light Green
            "enemy": "#F44336",       // Red
            "romantic": "#E91E63",    // Pink
            "neutral": "#9E9E9E"      // Grey
        }
        return colors[type] || "#9E9E9E"
    }
    
    function getRelationshipIcon(type) {
        const icons = {
            "family": "👨‍👩‍👧‍👦",
            "friend": "😊",
            "rival": "⚔️",
            "mentor": "👨‍🏫",
            "student": "👨‍🎓",
            "ally": "🤝",
            "enemy": "💀",
            "romantic": "💕",
            "neutral": "😐"
        }
        return icons[type] || "👤"
    }
    
    function capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1)
    }
}