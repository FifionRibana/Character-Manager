import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ScrollView {
    id: characterEditTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: characterEditTab.availableWidth
        spacing: 24
        
        // Basic Information section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: basicInfoContent.implicitHeight + 32
            
            ColumnLayout {
                id: basicInfoContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Text {
                    text: "Basic Information"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 24
                    
                    // Character Portrait
                    ColumnLayout {
                        spacing: 8
                        
                        Text {
                            text: "Portrait"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#212121"
                        }
                        
                        Rectangle {
                            id: imageArea
                            width: 150
                            height: 150
                            radius: 8
                            color: "#f5f5f5"
                            border.color: imageDropArea.containsDrag ? "#4CAF50" : "#e0e0e0"
                            border.width: 2
                            
                            // Image display
                            Image {
                                id: characterImage
                                anchors.fill: parent
                                anchors.margins: 4
                                source: characterModel && characterModel.imageUrl ? characterModel.imageUrl : ""
                                fillMode: Image.PreserveAspectCrop
                                visible: source.toString() !== ""
                                
                                layer.enabled: true
                                layer.effect: Item {
                                    // Simple masking for rounded corners
                                }
                            }
                            
                            // Placeholder content
                            ColumnLayout {
                                anchors.centerIn: parent
                                visible: !characterImage.visible
                                spacing: 8
                                
                                Text {
                                    text: "📷"
                                    font.pixelSize: 32
                                    color: "#757575"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                
                                Text {
                                    text: "Drop image here\nor click to browse"
                                    font.pixelSize: 12
                                    color: "#757575"
                                    horizontalAlignment: Text.AlignHCenter
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                            
                            // Drop area
                            DropArea {
                                id: imageDropArea
                                anchors.fill: parent
                                
                                onDropped: function(drop) {
                                    if (drop.hasUrls) {
                                        let url = drop.urls[0]
                                        if (url.toString().match(/\.(jpg|jpeg|png|bmp|gif)$/i)) {
                                            characterImage.source = url
                                            // TODO: Convert to base64 and save to character model
                                            console.log("Image dropped:", url)
                                        }
                                    }
                                }
                            }
                            
                            // Click to browse
                            MouseArea {
                                anchors.fill: parent
                                onClicked: imageFileDialog.open()
                            }
                        }
                        
                        Button {
                            text: "Browse..."
                            Layout.alignment: Qt.AlignHCenter
                            onClicked: imageFileDialog.open()
                        }
                        
                        Button {
                            text: "Clear"
                            enabled: characterImage.visible
                            Layout.alignment: Qt.AlignHCenter
                            onClicked: {
                                characterImage.source = ""
                                // TODO: Clear from character model
                            }
                        }
                    }
                    
                    // Character Details
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 16
                        
                        // Name
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            Text {
                                text: "Character Name"
                                font.pixelSize: 14
                                font.bold: true
                                color: "#212121"
                            }
                            
                            TextField {
                                id: nameField
                                Layout.fillWidth: true
                                text: characterModel ? characterModel.name : ""
                                placeholderText: "Enter character name..."
                                font.pixelSize: 16
                                
                                background: Rectangle {
                                    color: "#ffffff"
                                    border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                                    border.width: 1
                                    radius: 4
                                }
                                
                                onTextChanged: {
                                    if (characterModel && characterModel.name !== text) {
                                        characterModel.name = text
                                    }
                                }
                            }
                        }
                        
                        // Level
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            Text {
                                text: "Level"
                                font.pixelSize: 14
                                font.bold: true
                                color: "#212121"
                            }
                            
                            RowLayout {
                                SpinBox {
                                    id: levelSpinBox
                                    from: 1
                                    to: 100
                                    value: characterModel ? characterModel.level : 1
                                    
                                    background: Rectangle {
                                        color: "#ffffff"
                                        border.color: "#e0e0e0"
                                        border.width: 1
                                        radius: 4
                                    }
                                    
                                    onValueChanged: {
                                        if (characterModel && characterModel.level !== value) {
                                            characterModel.level = value
                                        }
                                    }
                                }
                                
                                Item { Layout.fillWidth: true }
                                
                                // Level badge
                                Rectangle {
                                    width: 60
                                    height: 40
                                    radius: 20
                                    color: "#4CAF50"
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: "Lv " + (levelSpinBox.value)
                                        font.pixelSize: 12
                                        font.bold: true
                                        color: "#ffffff"
                                    }
                                }
                            }
                        }
                        
                        // Character ID (read-only)
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            Text {
                                text: "Character ID"
                                font.pixelSize: 14
                                font.bold: true
                                color: "#212121"
                            }
                            
                            TextField {
                                Layout.fillWidth: true
                                text: "ABC-123-DEF" // TODO: Get from character model
                                readOnly: true
                                font.pixelSize: 12
                                color: "#757575"
                                
                                background: Rectangle {
                                    color: "#f5f5f5"
                                    border.color: "#e0e0e0"
                                    border.width: 1
                                    radius: 4
                                }
                            }
                        }
                        
                        Item { Layout.fillHeight: true }
                    }
                }
            }
        }
        
        // Character Notes section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: notesContent.implicitHeight + 32
            
            ColumnLayout {
                id: notesContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                Text {
                    text: "Quick Notes"
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
                    text: "Quick notes, reminders, or character concepts that don't fit elsewhere."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120
                    Layout.minimumHeight: 80
                    
                    TextArea {
                        id: notesText
                        placeholderText: "Quick notes about the character..."
                        wrapMode: TextArea.WordWrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#fafafa"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                        
                        // TODO: Connect to character model notes property
                    }
                }
            }
        }
        
        // Character Metadata section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: metadataContent.implicitHeight + 32
            
            ColumnLayout {
                id: metadataContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                Text {
                    text: "Character Metadata"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 16
                    rowSpacing: 8
                    
                    Text {
                        text: "Created:"
                        font.pixelSize: 12
                        color: "#757575"
                    }
                    
                    Text {
                        text: "2024-01-15 14:30" // TODO: Get from character model
                        font.pixelSize: 12
                        color: "#212121"
                    }
                    
                    Text {
                        text: "Last Modified:"
                        font.pixelSize: 12
                        color: "#757575"
                    }
                    
                    Text {
                        text: "2024-01-20 16:45" // TODO: Get from character model
                        font.pixelSize: 12
                        color: "#212121"
                    }
                    
                    Text {
                        text: "Version:"
                        font.pixelSize: 12
                        color: "#757575"
                    }
                    
                    Text {
                        text: "1.0" // TODO: Get from character model
                        font.pixelSize: 12
                        color: "#212121"
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // File dialog for image selection
    FileDialog {
        id: imageFileDialog
        title: "Select Character Image"
        nameFilters: ["Image files (*.png *.jpg *.jpeg *.bmp *.gif)"]
        
        onAccepted: {
            characterImage.source = selectedFile
            // TODO: Convert to base64 and save to character model
            console.log("Image selected:", selectedFile)
        }
    }
}