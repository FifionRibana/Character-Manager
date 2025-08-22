import QtQuick 6.9
import QtQuick.Controls 6.9
import QtQuick.Layouts 6.9
import "../styles"

// import App.Styles

Rectangle {
    id: sidebar
    color: AppTheme.colors.surface
    border.color: AppTheme.colors.border
    border.width: 1

    // Properties
    property alias characterListModel: characterList.model

    // Signals
    signal characterSelected(string characterId)
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
            color: AppTheme.colors.text
            Layout.alignment: Qt.AlignHCenter
        }

        // Separator
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: AppTheme.colors.border
        }

        // Character list
        ListView {
            id: characterList
            Layout.fillWidth: true
            Layout.fillHeight: true

            clip: true
            spacing: AppTheme.spacing.small

            delegate: CharacterListItem {
                width: characterList.width

                characterName: model.name || ""
                characterLevel: model.level || 1
                characterId: model.characterId || ""
                hasImage: model.hasImage || false

                onClicked: {
                    characterList.currentIndex = index;
                    sidebar.characterSelected(model.characterId || "");
                }

                onDeleteRequested: function (charId) {
                    sidebar.deleteCharacterRequested(charId);
                }
            }

            // Highlight current item
            highlight: Rectangle {
                color: AppTheme.primaryColor
                opacity: 0.3
                radius: AppTheme.radius.medium
            }

            // Empty state
            Label {
                anchors.centerIn: parent
                text: qsTr("No characters")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.textSecondary
                visible: characterList.count === 0
            }
        }

        // Button row
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.small

            Button {
                text: qsTr("New")
                Layout.fillWidth: true

                background: Rectangle {
                    color: parent.pressed ? AppTheme.button.pressed : parent.hovered ? AppTheme.button.hovered : AppTheme.button.normal
                    radius: AppTheme.radius.medium
                }

                contentItem: Text {
                    text: parent.text
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: AppTheme.colors.textSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    sidebar.newCharacterRequested();
                }
            }

            Button {
                text: qsTr("Delete")
                enabled: characterList.currentIndex >= 0
                Layout.fillWidth: true

                background: Rectangle {
                    color: parent.enabled ? (parent.pressed ? AppTheme.button.destructivePressed : parent.hovered ? AppTheme.button.destructiveHovered : AppTheme.button.destructiveNormal) : AppTheme.button.disabled
                    radius: AppTheme.radius.medium
                }

                contentItem: Text {
                    text: parent.text
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: parent.enabled ? AppTheme.colors.textSecondary : AppTheme.colors.textSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    if (characterList.currentIndex >= 0) {
                        var character = characterList.model.getCharacterAt(characterList.currentIndex);
                        if (character) {
                            sidebar.deleteCharacterRequested(character.id || "");
                        }
                    }
                }
            }
        }
    }
}
