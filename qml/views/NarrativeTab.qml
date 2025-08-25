import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import "../components"
import "./tabs/narrative"

Item {
    id: narrativeTab
    
    property var characterModel
    property var narrativeModel: characterModel ? characterModel.narrativeModel : null
    
    // contentWidth: availableWidth
    
    ColumnLayout {
        anchors.fill: parent
        spacing: AppTheme.spacing.small
        
        // Header section
        NarrativeTabHeader {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.topMargin: AppTheme.margin.small

            eventCount: narrativeModel ? narrativeModel.count : 0

            majorEventCount: getMajorEventCount()
            uniqueEventCount: getUniqueTagCount()

            onAddEventRequested: addEventDialog.open()
        }
        
        // View controls section
        NarrativeTabFilter {
            id: iNarrativeTabFilter
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small

            availableTags: getAvailableTags()

            onSortModeChangeRequested: function(sortMode) { setSortMode(sortMode) }

            onFilterEventsByTagRequested: function(tag) { filterEventsByTag(tag) }
            onExportTimelineRequested: exportTimeline()
        }
        

        // Timeline section
        NarrativeTabContent {
            Layout.fillWidth: true
            Layout.fillHeight: true
            // Layout.minimumHeight: 400

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.bottomMargin: AppTheme.margin.small

            narrativeModel: narrativeTab.narrativeModel
            timelineView: iNarrativeTabFilter.timelineMode

            onEventEditRequested: function(eventId) { editEvent(eventId) }
            onEventDeleteRequested: function(eventId) {
                confirmDeleteEventDialog.eventId = eventId
                confirmDeleteEventDialog.eventTitle = model.title
                confirmDeleteEventDialog.open()
            }
        }
    }
    
    // Add/Edit Event Dialog
    Dialog {
        id: addEventDialog
        title: "Add New Event"
        modal: true
        anchors.centerIn: parent
        
        width: Math.min(500, parent.width * 0.9)
        height: Math.min(600, parent.height * 0.9)
        
        property bool isEditing: false
        property string editingEventId: ""
        
        background: Rectangle {
            color: "#ffffff"
            radius: 8
            border.color: "#e0e0e0"
            border.width: 1
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16
            
            // Event title
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Event Title *"
                    font.pixelSize: 12
                    font.bold: true
                    color: "#212121"
                }
                
                TextField {
                    id: eventTitleField
                    Layout.fillWidth: true
                    placeholderText: "Enter event title..."
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#FF9800" : "#e0e0e0"
                        border.width: 2
                        radius: 4
                    }
                }
            }
            
            // Date and importance row
            RowLayout {
                Layout.fillWidth: true
                spacing: 16
                
                // Date
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    
                    Text {
                        text: "Date"
                        font.pixelSize: 12
                        font.bold: true
                        color: "#212121"
                    }
                    
                    TextField {
                        id: eventDateField
                        Layout.fillWidth: true
                        placeholderText: "YYYY-MM-DD or Age 25..."
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#FF9800" : "#e0e0e0"
                            border.width: 2
                            radius: 4
                        }
                    }
                }
                
                // Importance
                ColumnLayout {
                    Layout.preferredWidth: 100
                    spacing: 4
                    
                    Text {
                        text: "Importance"
                        font.pixelSize: 12
                        font.bold: true
                        color: "#212121"
                    }
                    
                    RowLayout {
                        SpinBox {
                            id: importanceSpinBox
                            from: 1
                            to: 10
                            value: 5
                            
                            background: Rectangle {
                                color: "#ffffff"
                                border.color: "#e0e0e0"
                                border.width: 2
                                radius: 4
                            }
                        }
                        
                        Text {
                            text: getImportanceLabel(importanceSpinBox.value)
                            font.pixelSize: 10
                            color: "#757575"
                            Layout.preferredWidth: 60
                        }
                    }
                }
            }
            
            // Tags
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Tags (comma-separated)"
                    font.pixelSize: 12
                    font.bold: true
                    color: "#212121"
                }
                
                TextField {
                    id: eventTagsField
                    Layout.fillWidth: true
                    placeholderText: "adventure, combat, meeting, tragedy..."
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#FF9800" : "#e0e0e0"
                        border.width: 2
                        radius: 4
                    }
                }
            }
            
            // Description
            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 4
                
                Text {
                    text: "Description"
                    font.pixelSize: 12
                    font.bold: true
                    color: "#212121"
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.minimumHeight: 120
                    
                    TextArea {
                        id: eventDescriptionField
                        placeholderText: "Describe what happened, who was involved, and why it was significant..."
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#FF9800" : "#e0e0e0"
                            border.width: 2
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
                    
                    background: Rectangle {
                        color: parent.pressed ? "#f5f5f5" : 
                               parent.hovered ? "#eeeeee" : "transparent"
                        border.color: "#bdbdbd"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#757575"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Button {
                    text: addEventDialog.isEditing ? "Update Event" : "Add Event"
                    enabled: eventTitleField.text.trim() !== ""
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.pressed ? "#F57C00" : 
                                parent.hovered ? "#FFB74D" : "#FF9800") :
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
                        if (eventTitleField.text.trim() !== "") {
                            if (addEventDialog.isEditing) {
                                updateEvent()
                            } else {
                                addNewEvent()
                            }
                            addEventDialog.close()
                        }
                    }
                }
            }
        }
        
        onOpened: {
            if (!isEditing) {
                eventTitleField.text = ""
                eventDateField.text = ""
                eventDescriptionField.text = ""
                eventTagsField.text = ""
                importanceSpinBox.value = 5
            }
            eventTitleField.forceActiveFocus()
        }
    }
    
    // Confirm delete dialog
    Dialog {
        id: confirmDeleteEventDialog
        title: "Confirm Deletion"
        modal: true
        anchors.centerIn: parent
        
        property string eventId: ""
        property string eventTitle: ""
        
        ColumnLayout {
            spacing: 16
            
            Text {
                text: `Are you sure you want to delete the event "${confirmDeleteEventDialog.eventTitle}"?`
                wrapMode: Text.WordWrap
                Layout.preferredWidth: 300
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Cancel"
                    onClicked: confirmDeleteEventDialog.close()
                }
                
                Button {
                    text: "Delete"
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C62828" : 
                               parent.hovered ? "#EF5350" : "#F44336"
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#ffffff"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (narrativeModel) {
                            narrativeModel.removeEvent(confirmDeleteEventDialog.eventId)
                        }
                        confirmDeleteEventDialog.close()
                    }
                }
            }
        }
    }
    
    // Helper functions
    function addNewEvent() {
        print("Add new event")
        if (narrativeModel) {
            print("add event (narrative model is here)")
            const tags = eventTagsField.text
                .split(',')
                .map(tag => tag.trim())
                .filter(tag => tag.length > 0)
            
            narrativeModel.addEvent(
                eventTitleField.text.trim(),
                eventDescriptionField.text.trim(),
                eventDateField.text.trim(),
                importanceSpinBox.value,
                tags
            )
        }
    }
    
    function updateEvent() {
        if (narrativeModel && addEventDialog.editingEventId) {
            const tags = eventTagsField.text
                .split(',')
                .map(tag => tag.trim())
                .filter(tag => tag.length > 0)
            
            narrativeModel.updateEvent(
                addEventDialog.editingEventId,
                eventTitleField.text.trim(),
                eventDescriptionField.text.trim(),
                eventDateField.text.trim(),
                importanceSpinBox.value,
                tags
            )
        }
    }
    
    function editEvent(eventId) {
        if (narrativeModel) {
            const event = narrativeModel.getEvent(eventId)
            if (event) {
                addEventDialog.isEditing = true
                addEventDialog.editingEventId = eventId
                addEventDialog.title = "Edit Event"
                
                eventTitleField.text = event.title
                eventDateField.text = event.date
                eventDescriptionField.text = event.description
                importanceSpinBox.value = event.importance
                eventTagsField.text = (event.tags || []).join(', ')
                
                addEventDialog.open()
            }
        }
    }
    
    function setSortMode(mode) {
        console.log("Setting sort mode:", mode)
        // TODO: Implement different sorting modes
    }
    
    function filterEventsByTag(tag) {
        console.log("Filtering by tag:", )
        // TODO: Implement tag filtering
    }
    
    function exportTimeline() {
        console.log("Exporting timeline...")
        // TODO: Implement timeline export
    }
    
    function getAvailableTags() {
        if (narrativeModel) {
            const tags = narrativeModel.getAllTags()
            return ["All Tags"].concat(tags)
        }
        return ["All Tags"]
    }
    
    function getMajorEventCount() {
        // TODO: Count events with importance >= 7
        return 0
    }
    
    function getUniqueTagCount() {
        if (narrativeModel) {
            return narrativeModel.getAllTags().length
        }
        return 0
    }
    
    function getImportanceLabel(value) {
        const labels = {
            1: "Trivial", 2: "Minor", 3: "Small", 4: "Moderate", 5: "Average",
            6: "Notable", 7: "Important", 8: "Major", 9: "Critical", 10: "Epic"
        }
        return labels[value] || "Unknown"
    }
}