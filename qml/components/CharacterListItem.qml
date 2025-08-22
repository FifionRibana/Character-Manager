import QtQuick 6.9
import QtQuick.Controls 6.9
import QtQuick.Layouts 6.9
import "../styles"

// import App.Styles

Rectangle {
    id: listItem
    height: 60
    color: mouseArea.containsMouse ? AppTheme.surfaceColorDark : "transparent"
    radius: AppTheme.radius.medium

    // Properties
    property string characterName: ""
    property int characterLevel: 1
    property string characterId: ""
    property bool hasImage: false

    // Signals
    signal clicked
    signal deleteRequested(string characterId)

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onClicked: function (mouse) {
            if (mouse.button === Qt.LeftButton) {
                listItem.clicked();
            } else if (mouse.button === Qt.RightButton) {
                contextMenu.popup();
            }
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: AppTheme.spacing
        spacing: AppTheme.spacing

        // Character avatar placeholder
        Rectangle {
            width: 40
            height: 40
            radius: 20
            color: hasImage ? "transparent" : AppTheme.getEnneagramColor(1)
            border.color: AppTheme.colors.border
            border.width: 1

            Text {
                anchors.centerIn: parent
                text: hasImage ? "" : (characterName.length > 0 ? characterName.charAt(0).toUpperCase() : "?")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                visible: !hasImage
            }

            // TODO: Add Image component for character portrait when hasImage is true
        }

        // Character info
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2

            Text {
                text: characterName || qsTr("Unnamed Character")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                font.bold: true
                color: AppTheme.colors.text
                elide: Text.ElideRight
                Layout.fillWidth: true
            }

            Text {
                text: qsTr("Level") + " " + characterLevel
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeSmall
                color: AppTheme.colors.textSecondary
            }
        }

        // Level indicator
        Rectangle {
            width: 24
            height: 24
            radius: 12
            color: AppTheme.primaryColor

            Text {
                anchors.centerIn: parent
                text: characterLevel.toString()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeSmall
                font.bold: true
                color: AppTheme.colors.textSecondary
            }
        }
    }

    // Context menu
    Menu {
        id: contextMenu

        MenuItem {
            text: qsTr("Delete")
            onTriggered: listItem.deleteRequested(listItem.characterId)
        }
    }
}
