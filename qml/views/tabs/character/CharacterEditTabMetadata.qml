import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"


Card {
    id: iCard

    implicitHeight: metadataContent.implicitHeight + AppTheme.spacing.huge

    contentItem: ColumnLayout {
        id: metadataContent
        spacing: AppTheme.spacing.medium
        anchors.fill: parent
        anchors.margins: AppTheme.margin.medium
        
        Text {
            text: qsTr("Character Metadata")
            font.pixelSize: AppTheme.fontSize.large
            font.bold: true
            color: AppTheme.colors.text
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: AppTheme.border.thin
            color: AppTheme.card.border
        }
        
        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 16
            rowSpacing: 8
            
            Text {
                text: qsTr("Created:")
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
            }
            
            Text {
                text: qsTr("2024-01-15 14:30") // TODO: Get from character model
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.text
            }
            
            Text {
                text: qsTr("Last Modified:")
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
            }
            
            Text {
                text: qsTr("2024-01-20 16:45") // TODO: Get from character model
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.text
            }
            
            Text {
                text: qsTr("Version:")
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
            }
            
            Text {
                text: qsTr("1.0") // TODO: Get from character model
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.text
            }
        }
    }

}