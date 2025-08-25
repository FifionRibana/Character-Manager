import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Quick Notes")

    content: ColumnLayout {
        spacing: AppTheme.spacing.small
                
        Text {
            text: qsTr("Quick notes, reminders, or character concepts that don't fit elsewhere.")
            font.pixelSize: AppTheme.fontSize.small
            color: AppTheme.colors.textSecondary
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
        
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            Layout.minimumHeight: 80
            
            TextArea {
                id: notesText
                placeholderText: qsTr("Quick notes about the character...")
                wrapMode: TextArea.WordWrap
                selectByMouse: true
                
                background: Rectangle {
                    color: AppTheme.colors.backgroundVariant
                    border.color: parent.activeFocus ? AppTheme.colors.success : AppTheme.colors.surfaceVariant
                    border.width: AppTheme.border.thin
                    radius: AppTheme.radius.small
                }
                
                // TODO: Connect to character model notes property
            }
        }
    }


}