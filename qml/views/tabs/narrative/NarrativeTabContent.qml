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
        width: 2
        height: parent.height - 40
        color: "#e0e0e0"
        visible: iCard.timelineView
    }

    contentItem: ScrollView {
        anchors.fill: parent
        anchors.margins: 16
        anchors.leftMargin: 48  // Space for timeline line
        contentWidth: availableWidth
        
        ListView {
            id: eventsList
            width: parent.width
            
            model: narrativeModel
            spacing: 16
            clip: true
            
            delegate: TimelineEvent {
                width: eventsList.width
                
                onEditRequested: function(eventId) {
                    editEvent(eventId)
                }
                
                onDeleteRequested: function(eventId) {
                    confirmDeleteEventDialog.eventId = eventId
                    confirmDeleteEventDialog.eventTitle = model.title
                    confirmDeleteEventDialog.open()
                }
                
                onImportanceChangeRequested: function(eventId, newImportance) {
                    if (narrativeModel) {
                        const event = narrativeModel.getEvent(eventId)
                        if (event) {
                            narrativeModel.updateEvent(
                                eventId,
                                event.title,
                                event.description,
                                event.date,
                                newImportance,
                                event.tags || []
                            )
                        }
                    }
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
                    spacing: 12
                    
                    Text {
                        text: "📅"
                        font.pixelSize: 48
                        color: "#e0e0e0"
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "No events yet."
                        font.pixelSize: 16
                        font.bold: true
                        color: "#bdbdbd"
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "Click 'Add Event' to start building your character's timeline.\nRecord births, meetings, adventures, tragedies, and victories."
                        font.pixelSize: 12
                        color: "#757575"
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