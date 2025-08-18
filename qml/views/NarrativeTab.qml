import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ScrollView {
    id: narrativeTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: narrativeTab.availableWidth
        spacing: 24
        
        // Timeline section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: timelineContent.implicitHeight + 32
            
            ColumnLayout {
                id: timelineContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                RowLayout {
                    Layout.fillWidth: true
                    
                    Text {
                        text: "Character Timeline"
                        font.pixelSize: 20
                        font.bold: true
                        color: "#212121"
                        Layout.fillWidth: true
                    }
                    
                    Button {
                        text: "Add Event"
                        onClicked: addEventDialog.open()
                        
                        background: Rectangle {
                            color: parent.pressed ? "#388E3C" : 
                                   parent.hovered ? "#45A049" : "#4CAF50"
                            radius: 4
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "#ffffff"
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                Text {
                    text: "Important events, milestones, and story moments in the character's life."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                // Timeline list
                ListView {
                    id: timelineList
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.min(contentHeight, 400)
                    Layout.minimumHeight: 200
                    
                    clip: true
                    spacing: 16
                    
                    model: ListModel {
                        id: eventsModel
                        
                        // Example data
                        ListElement {
                            title: "Character Birth"
                            date: "1995-03-15"
                            chapter: "Origins"
                            description: "Born in a small village to humble farmers."
                            eventType: "birth"
                        }
                        ListElement {
                            title: "Tragedy Strikes"
                            date: "2010-07-22"
                            chapter: "The Dark Years"
                            description: "Family home destroyed in a mysterious fire. Parents missing, presumed dead."
                            eventType: "tragedy"
                        }
                        ListElement {
                            title: "Mentor Found"
                            date: "2012-09-03"
                            chapter: "Training"
                            description: "Discovered by Master Chen, begins training in the ancient arts."
                            eventType: "meeting"
                        }
                        ListElement {
                            title: "First Adventure"
                            date: "2018-04-10"
                            chapter: "Current Campaign"
                            description: "Joined a group of adventurers to explore the Whispering Caves."
                            eventType: "adventure"
                        }
                    }
                    
                    delegate: Rectangle {
                        width: timelineList.width
                        height: eventContent.implicitHeight + 24
                        color: "transparent"
                        
                        // Timeline line
                        Rectangle {
                            id: timelineLine
                            x: 30
                            y: 0
                            width: 3
                            height: parent.height
                            color: "#e0e0e0"
                            visible: index < timelineList.count - 1
                        }
                        
                        // Event dot
                        Rectangle {
                            id: eventDot
                            x: 22
                            y: 20
                            width: 18
                            height: 18
                            radius: 9
                            color: getEventColor(model.eventType)
                            border.color: "#ffffff"
                            border.width: 2
                            
                            Text {
                                anchors.centerIn: parent
                                text: getEventIcon(model.eventType)
                                font.pixelSize: 8
                                color: "#ffffff"
                            }
                        }
                        
                        // Event content
                        Rectangle {
                            id: eventContent
                            anchors.left: eventDot.right
                            anchors.leftMargin: 16
                            anchors.right: parent.right
                            anchors.rightMargin: 8
                            anchors.top: parent.top
                            anchors.topMargin: 8
                            
                            height: eventLayout.implicitHeight + 16
                            color: "#f9f9f9"
                            border.color: "#e0e0e0"
                            border.width: 1
                            radius: 6
                            
                            ColumnLayout {
                                id: eventLayout
                                anchors.fill: parent
                                anchors.margins: 12
                                spacing: 6
                                
                                // Event header
                                RowLayout {
                                    Layout.fillWidth: true
                                    
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 2
                                        
                                        Text {
                                            text: model.title
                                            font.pixelSize: 14
                                            font.bold: true
                                            color: "#212121"
                                        }
                                        
                                        RowLayout {
                                            Text {
                                                text: formatDate(model.date)
                                                font.pixelSize: 10
                                                color: "#757575"
                                            }
                                            
                                            Rectangle {
                                                height: 16
                                                width: chapterText.implicitWidth + 12
                                                radius: 8
                                                color: "#2196F3"
                                                visible: model.chapter !== ""
                                                
                                                Text {
                                                    id: chapterText
                                                    anchors.centerIn: parent
                                                    text: model.chapter
                                                    font.pixelSize: 9
                                                    font.bold: true
                                                    color: "#ffffff"
                                                }
                                            }
                                        }
                                    }
                                    
                                    // Actions
                                    RowLayout {
                                        spacing: 4
                                        
                                        Button {
                                            text: "✏️"
                                            width: 24
                                            height: 24
                                            
                                            background: Rectangle {
                                                color: parent.pressed ? "#2196F3" : 
                                                       parent.hovered ? "#42A5F5" : "transparent"
                                                radius: 12
                                            }
                                            
                                            onClicked: {
                                                // TODO: Open edit dialog
                                                console.log("Edit event:", model.title)
                                            }
                                        }
                                        
                                        Button {
                                            text: "🗑️"
                                            width: 24
                                            height: 24
                                            
                                            background: Rectangle {
                                                color: parent.pressed ? "#F44336" : 
                                                       parent.hovered ? "#EF5350" : "transparent"
                                                radius: 12
                                            }
                                            
                                            onClicked: {
                                                eventsModel.remove(index)
                                            }
                                        }
                                    }
                                }
                                
                                // Event description
                                Text {
                                    text: model.description
                                    font.pixelSize: 12
                                    color: "#212121"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }
                    
                    // Empty state
                    ColumnLayout {
                        anchors.centerIn: parent
                        visible: timelineList.count === 0
                        spacing: 8
                        
                        Text {
                            text: "📅"
                            font.pixelSize: 48
                            color: "#e0e0e0"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "No events yet.\nClick 'Add Event' to start building your character's timeline."
                            font.pixelSize: 12
                            color: "#757575"
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // Add event dialog
    Dialog {
        id: addEventDialog
        title: "Add Timeline Event"
        modal: true
        anchors.centerIn: parent
        width: 450
        height: 400
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12
            
            // Event title
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Event Title:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                TextField {
                    id: eventTitleField
                    Layout.fillWidth: true
                    placeholderText: "e.g., First Adventure, Meeting the Mentor, The Great Battle..."
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                        border.width: 1
                        radius: 4
                    }
                }
            }
            
            // Date and Chapter
            RowLayout {
                Layout.fillWidth: true
                spacing: 12
                
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    
                    Text {
                        text: "Date:"
                        font.pixelSize: 14
                        color: "#212121"
                    }
                    
                    TextField {
                        id: eventDateField
                        Layout.fillWidth: true
                        placeholderText: "YYYY-MM-DD"
                        text: getCurrentDate()
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                    }
                }
                
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    
                    Text {
                        text: "Chapter (Optional):"
                        font.pixelSize: 14
                        color: "#212121"
                    }
                    
                    TextField {
                        id: eventChapterField
                        Layout.fillWidth: true
                        placeholderText: "e.g., Origins, Training, Current Campaign..."
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                    }
                }
            }
            
            // Event type
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Event Type:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                ComboBox {
                    id: eventTypeCombo
                    Layout.fillWidth: true
                    
                    model: [
                        {text: "Birth/Origin", value: "birth"},
                        {text: "Meeting/Encounter", value: "meeting"},
                        {text: "Achievement/Success", value: "achievement"},
                        {text: "Tragedy/Loss", value: "tragedy"},
                        {text: "Adventure/Quest", value: "adventure"},
                        {text: "Training/Learning", value: "training"},
                        {text: "Battle/Conflict", value: "battle"},
                        {text: "Discovery", value: "discovery"},
                        {text: "Other", value: "other"}
                    ]
                    
                    textRole: "text"
                    valueRole: "value"
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 4
                    }
                }
            }
            
            // Description
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Description:"
                    font.pixelSize: 14
                    color: "#212121"
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    
                    TextArea {
                        id: eventDescField
                        placeholderText: "Describe what happened, who was involved, and how it affected the character..."
                        wrapMode: TextArea.WordWrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                            border.width: 1
                            radius: 4
                        }
                    }
                }
            }
            
            // Buttons
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Cancel"
                    onClicked: addEventDialog.close()
                }
                
                Button {
                    text: "Add Event"
                    enabled: eventTitleField.text.trim() !== "" && eventDescField.text.trim() !== ""
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.pressed ? "#388E3C" : 
                                parent.hovered ? "#45A049" : "#4CAF50") :
                               "#e0e0e0"
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.enabled ? "#ffffff" : "#757575"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (eventTitleField.text.trim() !== "" && eventDescField.text.trim() !== "") {
                            addEvent(
                                eventTitleField.text.trim(),
                                eventDateField.text.trim(),
                                eventChapterField.text.trim(),
                                eventDescField.text.trim(),
                                eventTypeCombo.currentValue
                            )
                            addEventDialog.close()
                        }
                    }
                }
            }
        }
        
        onOpened: {
            eventTitleField.text = ""
            eventDateField.text = getCurrentDate()
            eventChapterField.text = ""
            eventDescField.text = ""
            eventTypeCombo.currentIndex = 0
            eventTitleField.forceActiveFocus()
        }
    }
    
    // Helper functions
    function addEvent(title, date, chapter, description, eventType) {
        eventsModel.append({
            "title": title,
            "date": date,
            "chapter": chapter,
            "description": description,
            "eventType": eventType
        })
        
        // Sort events by date (most recent first)
        // Note: This is a simplified sort - in a real app you'd want proper date sorting
        
        // TODO: Update character model
        console.log("Added event:", title, date, eventType)
    }
    
    function getCurrentDate() {
        let now = new Date()
        return now.getFullYear() + "-" + 
               String(now.getMonth() + 1).padStart(2, '0') + "-" + 
               String(now.getDate()).padStart(2, '0')
    }
    
    function formatDate(dateStr) {
        if (!dateStr) return ""
        
        let date = new Date(dateStr)
        if (isNaN(date.getTime())) return dateStr
        
        return date.toLocaleDateString("en-US", {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })
    }
    
    function getEventColor(eventType) {
        const colors = {
            "birth": "#4CAF50",        // Green
            "meeting": "#2196F3",      // Blue
            "achievement": "#FF9800",  // Orange
            "tragedy": "#F44336",      // Red
            "adventure": "#9C27B0",    // Purple
            "training": "#00BCD4",     // Cyan
            "battle": "#795548",       // Brown
            "discovery": "#FFEB3B",    // Yellow
            "other": "#9E9E9E"         // Grey
        }
        return colors[eventType] || "#9E9E9E"
    }
    
    function getEventIcon(eventType) {
        const icons = {
            "birth": "🌟",
            "meeting": "👤",
            "achievement": "🏆",
            "tragedy": "💔",
            "adventure": "⚔️",
            "training": "📚",
            "battle": "⚔️",
            "discovery": "🔍",
            "other": "📝"
        }
        return icons[eventType] || "📝"
    }
}