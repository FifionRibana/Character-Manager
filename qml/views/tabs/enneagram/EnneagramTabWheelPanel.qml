import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    property int selectedType: 9

    property alias typeInfo: typeInfoText.text

    signal typeSelected(int type)
    signal typeHovered(int type)

    contentItem: ColumnLayout {
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

            selectedType: iCard.selectedType

            onTypeSelected: function(type) { iCard.typeSelected(type) }
            onTypeHovered: function(type) { iCard.typeHovered(type) }
        }

        // Type info display
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            color: AppTheme.colors.backgroundVariant
            border.color: AppTheme.colors.borderLight
            border.width: AppTheme.border.thin
            radius: AppTheme.radius.small

            Text {
                id: typeInfoText
                anchors.fill: parent
                anchors.margins: AppTheme.margin.small
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