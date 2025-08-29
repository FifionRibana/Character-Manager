import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import App.Styles

import "./tabs/character"

ScrollView {
    id: characterEditTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: characterEditTab.availableWidth
        spacing: AppTheme.spacing.small
        
        // Character Notes section
        CharacterEditTabNotes {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.topMargin: AppTheme.margin.small

            quickNotes: characterModel && characterModel.quickNotes ? characterModel.quickNotes : ""

            onQuickNotesChangeRequested: function(quickNotesText) {
                if (characterModel) {
                    characterModel.quickNotes = quickNotesText
                }
            }
        }
        
        // Character Metadata section
        CharacterEditTabMetadata {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.bottomMargin: AppTheme.margin.small
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
}