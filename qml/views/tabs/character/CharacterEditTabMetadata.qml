import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"


TabHeaderCard {
    id: iCard

    title: qsTr("Character Metadata")

    content: ColumnLayout {
        spacing: AppTheme.spacing.small
        
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