import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Character Biography")

    property string biography: ""
    property int biographyLength: 0

    signal biographyChangeRequested(string biographyText)

    buttons: Text {
        id: characterCount
        text: iCard.biographyLength + "/10000"
        font.family: AppTheme.fontFamily
        font.pixelSize: AppTheme.fontSize.small
        color: getCharacterCountColor()
        verticalAlignment: Text.AlignVCenter
    }

    content: ColumnLayout {
        spacing: AppTheme.spacing.small
        
        // Biography text editor
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 300
            Layout.minimumHeight: 200
            
            TextArea {
                id: biographyTextArea
                
                text: iCard.biography
                placeholderText: qsTr("Write your character's background story, personality, goals, and history here.\n\n" +
                                    "Consider including:\n" +
                                    "• Childhood and upbringing\n" +
                                    "• Major life events\n" +
                                    "• Personality traits and quirks\n" +
                                    "• Goals and motivations\n" +
                                    "• Fears and weaknesses\n" +
                                    "• Relationships with family and friends\n" +
                                    "• Professional background or training")
                
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                wrapMode: TextArea.Wrap
                selectByMouse: true
                
                background: Rectangle {
                    color: AppTheme.input.background
                    border.color: parent.activeFocus ? (AppTheme.colors.accent) : (AppTheme.colors.border)
                    border.width: parent.activeFocus ? 2 : 1
                    radius: 6
                    
                    Behavior on border.color {
                        ColorAnimation { duration: 150 }
                    }
                    
                    Behavior on border.width {
                        NumberAnimation { duration: 150 }
                    }
                }
                
                onTextChanged: {
                    if (text !== iCard.biography) {
                        iCard.biographyLength = biographyTextArea.text.length
                        // Throttle updates to avoid excessive property changes
                        saveTimer.restart()
                    }
                }
                
                // Auto-save timer
                Timer {
                    id: saveTimer
                    interval: 500
                    onTriggered: iCard.biographyChangeRequested(biographyTextArea.text)
                }
            }
        }
        
        // Writing tips
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.colors.backgroundVariant
            border.color: AppTheme.colors.borderLight
            border.width: 1
            radius: 6
            
            implicitHeight: tipsContent.implicitHeight + AppTheme.spacing.medium
            
            RowLayout {
                id: tipsContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.small
                spacing: AppTheme.spacing.small
                
                Text {
                    text: "💡"
                    font.pixelSize: AppTheme.fontSize.medium
                }
                
                Text {
                    text: qsTr("Tip: A good biography helps bring your character to life. Focus on their personality, motivations, and what makes them unique.")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
            }
        }
    }
}