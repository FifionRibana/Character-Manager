import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    property bool timelineView: false
    property var narrativeModel

    // Timeline background line
    Rectangle {
        id: timelineBackgroundLine
        x: 16
        y: 20
        width: AppTheme.border.medium
        height: parent.height - 40
        color: AppTheme.colors.surfaceVariant
        visible: iCard.timelineView
    }

    contentItem: ScrollView {
        anchors.fill: parent
        anchors.margins: AppTheme.margin.medium
        anchors.leftMargin: 48  // Space for timeline line
        contentWidth: availableWidth
        
        ListView {
            id: eventsList
            width: parent.width
            
            model: narrativeModel
            spacing: AppTheme.spacing.medium
            clip: true
            
            delegate: TimelineEvent {
                width: eventsList.width
                
                eventId: model ? model.id : ""
                title: model ? model.title : ""
                description: model ? model.description : ""
                date: model ? model.date : ""
                importance: model ? model.importance : 5
                tags: model ? model.tags : []
                chapter: model ? model.chapter : ""
                eventType: model ? model.eventType : ""
                eventColor: model ? model.color : "#607D8B"
                eventIcon: model ? model.icon : "📅"
                
                
                onEditRequested: function(eventId) {
                    editEvent(eventId)
                }
                
                onDeleteRequested: function(eventId) {
                    confirmDeleteEventDialog.eventId = eventId
                    confirmDeleteEventDialog.eventTitle = model.title
                    confirmDeleteEventDialog.open()
                }
            }
            
            // Empty state
            Rectangle {
                anchors.centerIn: parent
                width: 300
                height: 150
                color: "transparent"
                visible: eventsList.count === 0
                
                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: AppTheme.spacing.small
                    
                    Text {
                        text: "📅"
                        font.pixelSize: AppTheme.iconSize.huge
                        color: AppTheme.colors.backgroundVariant
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "No events yet."
                        font.pixelSize: AppTheme.fontSize.medium
                        font.bold: true
                        color: AppTheme.colors.border
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "Click 'Add Event' to start building your character's timeline.\nRecord births, meetings, adventures, tragedies, and victories."
                        font.pixelSize: AppTheme.fontSize.small
                        color: AppTheme.colors.textSecondary
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredWidth: 250
                    }
                }
            }
        }
    }
}