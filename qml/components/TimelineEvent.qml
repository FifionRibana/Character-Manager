import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles
import App.Types

Rectangle {
    id: timelineEvent
    
    // Properties from model
    property string eventId: ""
    property string title: ""
    property string description: ""
    property string date: ""
    property int importance: 5
    property var tags: []
    property string chapter: ""
    property string eventType: ""
    property string eventColor: "#607D8B"
    property string eventIcon:"📅"
    
    // Signals
    signal editRequested(string eventId)
    signal deleteRequested(string eventId)
    signal importanceChangeRequested(string eventId, int newImportance)
    
    // Visual properties
    width: parent.width
    height: Math.max(minHeight, contentColumn.implicitHeight + AppTheme.spacing.large)
    color: AppTheme.colors.background
    border.color: eventColor
    border.width: AppTheme.border.medium
    radius: AppTheme.radius.medium
    
    readonly property int minHeight: 100
    property bool hovered: false
    property bool isHighImportance: importance >= 7
    
    // Timeline line connection (left side)
    Rectangle {
        id: timelineLine
        x: -20
        y: parent.height / 2 - height / 2
        width: 40
        height: 2
        color: eventColor
        opacity: 0.6
    }
    
    // Timeline dot (left side)
    Rectangle {
        id: timelineDot
        x: -24
        y: parent.height / 2 - height / 2
        width: 12
        height: 12
        radius: 6
        color: eventColor
        border.color: "#ffffff"
        border.width: 2
        
        // Pulse effect for high importance events
        SequentialAnimation {
            loops: Animation.Infinite
            running: isHighImportance
            
            PropertyAnimation {
                target: timelineDot
                property: "scale"
                to: 1.2
                duration: 1000
                easing.type: Easing.InOutSine
            }
            
            PropertyAnimation {
                target: timelineDot
                property: "scale"
                to: 1.0
                duration: 1000
                easing.type: Easing.InOutSine
            }
        }
    }
    
    // Hover effects
    MouseArea {
        id: hoverArea
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: {
            parent.hovered = true
        }
        
        onExited: {
            parent.hovered = false
        }
        
        onClicked: {
            timelineEvent.editRequested(eventId)
        }
    }
    
    // Background highlight
    Rectangle {
        anchors.fill: parent
        color: eventColor
        opacity: hovered ? 0.05 : 0
        radius: parent.radius
        
        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
    
    // Main content
    ColumnLayout {
        id: contentColumn
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8
        
        // Header row
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            
            // Event icon
            Text {
                text: eventIcon
                font.pixelSize: 20
                Layout.alignment: Qt.AlignTop
            }
            
            // Title and metadata
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                // Title
                Text {
                    text: title
                    font.pixelSize: 16
                    font.bold: true
                    color: "#212121"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }
                
                // Date and chapter
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    
                    Text {
                        text: date || "Undated"
                        font.pixelSize: 11
                        color: "#757575"
                        font.italic: !date
                    }
                    
                    Rectangle {
                        width: 4
                        height: 4
                        radius: 2
                        color: "#bdbdbd"
                        visible: date && chapter
                    }
                    
                    Text {
                        text: chapter
                        font.pixelSize: 11
                        color: eventColor
                        font.bold: true
                        visible: chapter
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    // Importance indicator
                    RowLayout {
                        spacing: 2
                        
                        Repeater {
                            model: Math.min(importance, 5)
                            
                            Text {
                                text: "⭐"
                                font.pixelSize: 10
                                color: importance >= 7 ? "#FFD700" : "#FFC107"
                            }
                        }
                        
                        Text {
                            text: importance > 5 ? `+${importance - 5}` : ""
                            font.pixelSize: 9
                            color: "#FF5722"
                            font.bold: true
                            visible: importance > 5
                        }
                    }
                }
            }
            
            // Action buttons (visible on hover)
            RowLayout {
                spacing: 4
                opacity: hovered ? 1.0 : 0.3
                
                Behavior on opacity {
                    NumberAnimation { duration: 150 }
                }
                
                Button {
                    id: editButton
                    text: "✏️"
                    implicitWidth: 28
                    implicitHeight: 28
                    
                    background: Rectangle {
                        color: parent.pressed ? "#1976D2" : 
                               parent.hovered ? "#42A5F5" : "transparent"
                        radius: 14
                        border.color: "#2196F3"
                        border.width: parent.hovered ? 1 : 0
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        timelineEvent.editRequested(eventId)
                    }
                }
                
                Button {
                    id: deleteButton
                    text: "🗑️"
                    implicitWidth: 28
                    implicitHeight: 28
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C62828" : 
                               parent.hovered ? "#EF5350" : "transparent"
                        radius: 14
                        border.color: "#F44336"
                        border.width: parent.hovered ? 1 : 0
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        timelineEvent.deleteRequested(eventId)
                    }
                }
            }
        }
        
        // Description
        Text {
            text: description
            font.pixelSize: 13
            color: "#424242"
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            visible: description.length > 0
            lineHeight: 1.2
        }
        
        // Tags
        Flow {
            Layout.fillWidth: true
            spacing: 6
            visible: tags && tags.length > 0
            
            Repeater {
                model: tags || []
                
                Rectangle {
                    height: 20
                    width: tagText.implicitWidth + 12
                    color: eventColor
                    opacity: 0.15
                    radius: 10
                    border.color: eventColor
                    border.width: 1
                    
                    Text {
                        id: tagText
                        anchors.centerIn: parent
                        text: "#" + modelData
                        font.pixelSize: 9
                        color: eventColor
                        font.bold: true
                    }
                }
            }
        }
    }
    
    // Elevation shadow
    Rectangle {
        anchors.fill: parent
        anchors.topMargin: 2
        anchors.leftMargin: 1
        color: "#20000000"
        radius: parent.radius
        z: -1
        opacity: hovered ? 0.4 : 0.2
        
        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
    
    // Special highlight for very important events
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.color: "#FFD700"
        border.width: importance >= 9 ? 2 : 0
        radius: parent.radius
        opacity: 0.7
        
        Behavior on border.width {
            NumberAnimation { duration: 200 }
        }
    }
}