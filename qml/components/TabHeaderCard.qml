import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

Card {
    id: iCard

    implicitHeight: headerContent.implicitHeight + AppTheme.spacing.huge
    verticalPadding: AppTheme.padding.small
    horizontalPadding: AppTheme.padding.medium

    property alias title: iTitle.text
    property alias buttons: iButtonRow.sourceComponent
    property alias content: iContent.sourceComponent

    contentItem: ColumnLayout {
        id: headerContent
        spacing: AppTheme.spacing.small
        
        RowLayout {
            Layout.fillWidth: true
            Layout.minimumHeight: AppTheme.spacing.huge
            
            Text {
                id: iTitle
                text: qsTr("Header title")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                Layout.fillWidth: true
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