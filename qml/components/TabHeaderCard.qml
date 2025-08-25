import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

Card {
    id: iCard

    verticalPadding: AppTheme.padding.small
    horizontalPadding: AppTheme.padding.medium

    property alias title: iTitle.text
    property alias buttons: iButtonRow.sourceComponent
    property alias content: iContent.sourceComponent

    // Rectangle {
    //     color: "red"
    //     opacity: 0.3
    //     anchors.fill: parent
    // }
    // Rectangle {
    //     color: "green"
    //     opacity: 0.3
    //     width: iRow.width
    //     height: iRow.height
    //     x: iRow.x + parent.leftPadding
    //     y: iRow.y + parent.topPadding
    // }

    contentItem: ColumnLayout {
        id: headerContent
        spacing: AppTheme.spacing.small
        
        RowLayout {
            id: iRow
            Layout.fillWidth: true
            Layout.preferredHeight: AppTheme.spacing.huge
            
            Text {
                id: iTitle
                text: qsTr("Header title")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter
            }

            Item { Layout.fillWidth: true }
            
            Loader {
                id: iButtonRow
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
            }
        }
        
        HorizontalSeparator { Layout.fillWidth: true }

        Loader {
            id: iContent
            Layout.fillWidth: true
        }
    }
}