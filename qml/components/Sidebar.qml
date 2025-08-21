import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: sidebar
    color: AppTheme.surfaceColor
    border.color: AppTheme.borderColor
    border.width: 1

    // Properties
    property alias characterListModel: characterList.model
    
    // Signals
    signal characterSelected()
    signal newCharacterRequested()
    signal deleteCharacterRequested(string characterId)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: AppTheme.spacing
        spacing: AppTheme.spacing

        // Title
        Text {
            text: qsTr("Characters")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSizeTitle
            font.bold: true
            color: AppTheme.textColor
            Layout.alignment: Qt.AlignHCenter
        }

        // Separator
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: AppTheme.borderColor
        }

        // Character list
        ListView {
            id: characterList
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            clip: true
            spacing: AppTheme.spacingSmall
            
            delegate: CharacterListItem {
                width: characterList.width
                
                characterName: model.name || ""
                characterLevel: model.level || 1
                characterId: model.characterId || ""
                hasImage: model.hasImage || false
                
                onClicked: {
                    characterList.currentIndex = index
                    if (characterListModel && characterListModel.selectCharacter) {
                        characterListModel.selectCharacter(index)
                    }
                }
                
                onDeleteRequested: function(charId) {
                    sidebar.deleteCharacterRequested(charId)
                }
            }
            
            // Highlight current item
            highlight: Rectangle {
                color: AppTheme.primaryColor
                opacity: 0.3
                radius: AppTheme.borderRadius
            }
            
            // Empty state
            Label {
                anchors.centerIn: parent
                text: qsTr("No characters")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeBody
                color: AppTheme.textColorSecondary
                visible: characterList.count === 0
            }
        }

        // Button row
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacingSmall

            Button {
                text: qsTr("New")
                Layout.fillWidth: true
                
                background: Rectangle {
                    color: parent.pressed ? AppTheme.button.pressed :
                           parent.hovered ? AppTheme.button.hovered :
                           AppTheme.button.normal
                    radius: AppTheme.borderRadius
                }
                
                contentItem: Text {
                    text: parent.text
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeBody
                    color: AppTheme.textColorLight
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    // Connect to controller later
                    console.log("New character clicked")
                }
            }

            Button {
                text: qsTr("Delete")
                enabled: characterList.currentIndex >= 0
                Layout.fillWidth: true
                
                background: Rectangle {
                    color: parent.enabled ? 
                           (parent.pressed ? AppTheme.button.destructivePressed :
                            parent.hovered ? AppTheme.button.destructiveHovered :
                            AppTheme.button.destructiveNormal) :
                           AppTheme.button.disabled
                    radius: AppTheme.borderRadius
                }
                
                contentItem: Text {
                    text: parent.text
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeBody
                    color: parent.enabled ? AppTheme.textColorLight : AppTheme.textColorSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    if (characterList.currentIndex >= 0) {
                        // Simplified for now - just log
                        console.log("Delete character clicked")
                    }
                }
            }
        }
    }
}