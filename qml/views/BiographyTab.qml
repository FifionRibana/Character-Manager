import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ScrollView {
    id: biographyTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: biographyTab.availableWidth
        spacing: 24
        
        // Biography section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: biographyContent.implicitHeight + 32
            
            ColumnLayout {
                id: biographyContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                Text {
                    text: "Biography"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                Text {
                    text: "Character background, history, personality, goals, fears, etc."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 200
                    Layout.minimumHeight: 150
                    
                    TextArea {
                        id: biographyText
                        placeholderText: "Enter character background, history, traumatic events, personality traits, goals, fears, etc..."
                        text: characterModel ? characterModel.biography : ""
                        wrapMode: TextArea.WordWrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#fafafa"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                        
                        onTextChanged: {
                            if (characterModel && characterModel.biography !== text) {
                                characterModel.biography = text
                            }
                        }
                    }
                }
                
                // Character count
                Text {
                    text: (biographyText.text.length || 0) + " characters"
                    font.pixelSize: 10
                    color: "#757575"
                    Layout.alignment: Qt.AlignRight
                }
            }
        }
        
        // Affiliations section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: affiliationsContent.implicitHeight + 32
            
            ColumnLayout {
                id: affiliationsContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: "Affiliations"
                        font.pixelSize: 20
                        font.bold: true
                        color: "#212121"
                        Layout.fillWidth: true
                    }
                    
                    Button {
                        text: "Add Affiliation"
                        onClicked: addAffiliationDialog.open()
                        
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
                    text: "Organizations, guilds, factions, or groups the character belongs to or has ties with."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                // Affiliations list
                ListView {
                    id: affiliationsList
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.min(contentHeight, 200)
                    Layout.minimumHeight: 60
                    
                    clip: true
                    spacing: 8
                    
                    model: ListModel {
                        id: affiliationsModel
                    }
                    
                    delegate: Rectangle {
                        width: affiliationsList.width
                        height: 40
                        color: "#f5f5f5"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 4
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 8
                            
                            Rectangle {
                                width: 24
                                height: 24
                                radius: 12
                                color: "#2196F3"
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: "🏛️"
                                    font.pixelSize: 12
                                }
                            }
                            
                            Text {
                                text: model.name || ""
                                font.pixelSize: 14
                                color: "#212121"
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                            
                            Button {
                                text: "×"
                                width: 24
                                height: 24
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#F44336" : 
                                           parent.hovered ? "#FF5722" : "transparent"
                                    radius: 12
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    color: parent.parent.hovered ? "#ffffff" : "#757575"
                                    font.pixelSize: 14
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                onClicked: {
                                    affiliationsModel.remove(index)
                                    updateCharacterAffiliations()
                                }
                            }
                        }
                    }
                    
                    // Empty state
                    Text {
                        anchors.centerIn: parent
                        text: "No affiliations yet.\nClick 'Add Affiliation' to add one."
                        font.pixelSize: 12
                        color: "#757575"
                        horizontalAlignment: Text.AlignHCenter
                        visible: affiliationsList.count === 0
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // Add affiliation dialog
    Dialog {
        id: addAffiliationDialog
        title: "Add Affiliation"
        modal: true
        anchors.centerIn: parent
        width: 300
        height: 150
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12
            
            Text {
                text: "Affiliation name:"
                font.pixelSize: 14
                color: "#212121"
            }
            
            TextField {
                id: affiliationNameField
                Layout.fillWidth: true
                placeholderText: "e.g., Thieves Guild, Royal Guard, Mages Academy..."
                
                background: Rectangle {
                    color: "#ffffff"
                    border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                    border.width: 1
                    radius: 4
                }
                
                Keys.onReturnPressed: {
                    if (text.trim() !== "") {
                        addAffiliation(text.trim())
                        addAffiliationDialog.close()
                    }
                }
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Cancel"
                    onClicked: addAffiliationDialog.close()
                }
                
                Button {
                    text: "Add"
                    enabled: affiliationNameField.text.trim() !== ""
                    
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
                        if (affiliationNameField.text.trim() !== "") {
                            addAffiliation(affiliationNameField.text.trim())
                            addAffiliationDialog.close()
                        }
                    }
                }
            }
        }
        
        onOpened: {
            affiliationNameField.text = ""
            affiliationNameField.forceActiveFocus()
        }
    }
    
    // Functions
    function addAffiliation(name) {
        affiliationsModel.append({"name": name})
        updateCharacterAffiliations()
    }
    
    function updateCharacterAffiliations() {
        if (!characterModel) return
        
        // Convert model to array
        let affiliations = []
        for (let i = 0; i < affiliationsModel.count; i++) {
            affiliations.push(affiliationsModel.get(i).name)
        }
        
        // Update character model
        // Note: This assumes the character model has an affiliations property
        // You might need to implement this in your CharacterModel
        console.log("Affiliations updated:", affiliations)
    }
    
    function loadAffiliations() {
        affiliationsModel.clear()
        
        // Load from character model
        // This is a placeholder - you'll need to implement based on your data structure
        if (characterModel) {
            // Example affiliations for testing
            let exampleAffiliations = ["Thieves Guild", "City Watch", "Merchant's Association"]
            for (let affiliation of exampleAffiliations) {
                affiliationsModel.append({"name": affiliation})
            }
        }
    }
    
    Component.onCompleted: {
        loadAffiliations()
    }
    
    // Watch for character model changes
    onCharacterModelChanged: {
        if (characterModel) {
            loadAffiliations()
        }
    }
}