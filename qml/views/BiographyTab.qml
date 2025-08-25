/**
 * BiographyTab.qml
 * Character biography and affiliations editing tab
 * Features rich text editing and dynamic affiliations management
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import "../components"
import "./tabs/biography"

import App.Styles

ScrollView {
    id: biographyTab
    
    property var characterModel
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: biographyTab.availableWidth
        spacing: AppTheme.spacing.small
        
        // Biography section
        BiographyTabBiographyPanel {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.topMargin: AppTheme.margin.small

            biography: characterModel && characterModel.biography ? characterModel.biography : ""

            onBiographyChangeRequested: function(biographyText) {
                if (characterModel) {
                    characterModel.biography = biographyText
                }
            }
        }
        
        // Affiliations section
        BiographyTabAffiliationPanel {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.bottomMargin: AppTheme.margin.small

            affiliations: characterModel && characterModel.affiliations ? characterModel.affiliations : []

            onAddAffiliationRequested: addAffiliationDialog.open()
        }
    }
    
    // Add affiliation dialog
    Dialog {
        id: addAffiliationDialog
        title: qsTr("Add Affiliation")
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.8, 400)
        height: Math.min(parent.height * 0.6, 200)
        modal: true
        
        background: Rectangle {
            color: AppTheme.card.background || "#FFFFFF"
            border.color: AppTheme.card.border || "#E0E0E0"
            border.width: 2
            radius: 8
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: AppTheme.spacing.medium || 16
            
            Text {
                text: qsTr("Enter the name of the organization or group:")
                font.family: AppTheme.fontFamily || "Inter"
                font.pixelSize: AppTheme.fontSize.medium || 14
                color: AppTheme.colors.text || "#212121"
            }
            
            TextField {
                id: affiliationNameField
                Layout.fillWidth: true
                placeholderText: qsTr("e.g., Royal Guard, Thieves' Guild, etc.")
                font.family: AppTheme.fontFamily || "Inter"
                font.pixelSize: AppTheme.fontSize.medium || 14
                
                background: Rectangle {
                    color: AppTheme.input.background || "#FFFFFF"
                    border.color: parent.activeFocus ? (AppTheme.colors.accent || "#FF5722") : (AppTheme.colors.border || "#E0E0E0")
                    border.width: parent.activeFocus ? 2 : 1
                    radius: 4
                }
                
                Keys.onReturnPressed: addAffiliationDialog.accept()
                Keys.onEnterPressed: addAffiliationDialog.accept()
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: qsTr("Cancel")
                    
                    background: Rectangle {
                        color: AppTheme.colors.background
                        border.width: AppTheme.border.medium
                        border.color: parent.enabled ? 
                               (parent.hovered ? Qt.lighter(AppTheme.colors.textSecondary, 1.1) : AppTheme.colors.textSecondary) :
                               AppTheme.colors.border
                        radius: AppTheme.radius.small
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.enabled ? AppTheme.colors.textSecondary : "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    onClicked: addAffiliationDialog.reject()
                }
                
                Button {
                    text: qsTr("Add")
                    enabled: affiliationNameField.text.trim().length > 0
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.hovered ? Qt.lighter(AppTheme.colors.accent, 1.1) : AppTheme.colors.accent) :
                               AppTheme.colors.border
                        radius: AppTheme.radius.small
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.enabled ? "white" : AppTheme.colors.textSecondary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: addAffiliationDialog.accept()
                }
            }
        }
        
        onAccepted: {
            var name = affiliationNameField.text.trim()
            if (name.length > 0) {
                addAffiliation(name)
                affiliationNameField.clear()
            }
        }
        
        onOpened: {
            affiliationNameField.forceActiveFocus()
        }
    }
    
    // Helper functions
    function getCharacterCountColor() {
        if (!characterModel || !characterModel.biography) return AppTheme.colors.textSecondary || "#757575"
        
        const count = characterModel.biography.length
        if (count > 8000) return "#e74c3c"      // Red - approaching limit
        if (count > 5000) return "#f39c12"      // Orange - getting long
        return AppTheme.colors.textSecondary || "#757575"      // Normal
    }
    
    function addAffiliation(name) {
        if (!characterModel) return

        // A copy must be done        
        let affiliations = characterModel.affiliations || []
        
        // Check for duplicates
        for (let i = 0; i < affiliations.length; i++) {
            if (affiliations[i].toLowerCase() === name.toLowerCase()) {
                return // Duplicate found, don't add
            }
        }
        
        characterModel.addAffiliation(name)
    }
    
    function removeAffiliation(name) {
        if (!characterModel) return
        
        characterModel.removeAffiliation(name)
    }
}