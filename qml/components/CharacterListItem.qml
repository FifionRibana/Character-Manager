import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../styles"

// import App.Styles

Rectangle {
    id: listItem
    height: 60
    color: mouseArea.containsMouse ? AppTheme.colors.surfaceVariant : "transparent"
    radius: AppTheme.radius.medium

    // Properties
    property string characterName: ""
    property int characterLevel: 1
    property string characterId: ""
    property bool hasImage: false
    property string imageData: ""
    property string initials: "?"
    property int enneagramType: 1

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
        anchors.margins: AppTheme.spacing.tiny
        spacing: AppTheme.spacing.tiny

        // Character avatar placeholder
        Rectangle {
            width: 40
            height: 40
            radius: 20
            color: hasImage ? "transparent" : AppTheme.enneagramColors[listItem.enneagramType - 1]
            border.color:  hasImage ? Qt.darker(AppTheme.enneagramColors[listItem.enneagramType - 1], 1.2) : AppTheme.colors.border
            border.width: hasImage ? AppTheme.border.medium : AppTheme.border.thin
            layer.enabled: true
            layer.smooth: true

            clip: true

            Text {
                anchors.centerIn: parent
                text: hasImage ? "" : listItem.initials
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                visible: !hasImage
            }
            Loader {
                active: hasImage
                anchors.fill: parent
                sourceComponent: Canvas {
                    id: canvas

                    property string imageData: hasImage ? "data:image/png;base64," + listItem.imageData : ""
                    onImageDataChanged: loadImage(imageData)
                    onImageLoaded: requestPaint()
                    onPaint: {
                        var ctx = getContext("2d")
                        ctx.clearRect(0, 0, width, height)
                        ctx.beginPath()
                        ctx.arc(width/2, height/2, width/2 - 2, 0, 2 * Math.PI)
                        ctx.clip()
                        ctx.drawImage(imageData, 0, 0, width, height)
                    }
                }
            }
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
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
            }
        }

        // Level indicator
        Rectangle {
            width: 24
            height: 24
            radius: 12
            color: AppTheme.colors.primary

            Text {
                anchors.centerIn: parent
                text: characterLevel.toString()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.small
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
