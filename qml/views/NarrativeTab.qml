import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

ScrollView {
    id: narrativeTab
    
    property var characterModel
    property var narrativeModel: characterModel ? characterModel.narrativeModel : null
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: narrativeTab.availableWidth
        spacing: 24
        
        // Header section
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: headerContent.implicitHeight + 32
            
            ColumnLayout {
                id: headerContent
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
                    text: "Chronicle important events, milestones, and story moments in your character's life."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                // Statistics row
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 24
                    
                    ColumnLayout {
                        spacing: 4
                        
                        Text {
                            text: narrativeModel ? narrativeModel.count : 0
                            font.pixelSize: 24
                            font.bold: true
                            color: "#FF9800"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Total Events"
                            font.pixelSize: 10
                            color: "#757575"
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    Rectangle {
                        width: 1
                        height: 40
                        color: "#e0e0e0"
                    }
                    
                    ColumnLayout {
                        spacing: 4
                        
                        Text {
                            text: getMajorEventCount()
                            font.pixelSize: 24
                            font.bold: true
                            color: "#3F51B5"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Major Events"
                            font.pixelSize: 10
                            color: "#757575"
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    Rectangle {
                        width: 1
                        height: 40
                        color: "#e0e0e0"
                    }
                    
                    ColumnLayout {
                        spacing: 4
                        
                        Text {
                            text: getUniqueTagCount()
                            font.pixelSize: 24
                            font.bold: true
                            color: "#9C27B0"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Tags Used"
                            font.pixelSize: 10
                            color: "#757575"
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    Item { Layout.fillWidth: true }
                }
            }
        }
        
        // View controls section
        Rectangle {
            Layout.fillWidth: true
            color: "#f8f9fa"
            border.color: "#dee2e6"
            border.width: 1
            radius: 6
            
            implicitHeight: controlsContent.implicitHeight + 16
            
            RowLayout {
                id: controlsContent
                anchors.fill: parent
                anchors.margins: 8
                spacing: 12
                
                Text {
                    text: "View:"
                    font.pixelSize: 11
                    color: "#495057"
                }
                
                ButtonGroup {
                    id: viewModeGroup
                    buttons: [timelineViewBtn, importanceViewBtn, chapterViewBtn]
                }
                
                Button {
                    id: timelineViewBtn
                    text: "Timeline"
                    checkable: true
                    checked: true
                    
                    ButtonGroup.group: viewModeGroup
                    
                    background: Rectangle {
                        color: parent.checked ? "#007bff" : 
                               (parent.pressed ? "#e9ecef" : 
                                parent.hovered ? "#f8f9fa" : "transparent")
                        border.color: "#007bff"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 10
                        color: parent.checked ? "#ffffff" : "#007bff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        setSortMode("timeline")
                    }
                }
                
                Button {
                    id: importanceViewBtn
                    text: "Importance"
                    checkable: true
                    
                    ButtonGroup.group: viewModeGroup
                    
                    background: Rectangle {
                        color: parent.checked ? "#007bff" : 
                               (parent.pressed ? "#e9ecef" : 
                                parent.hovered ? "#f8f9fa" : "transparent")
                        border.color: "#007bff"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 10
                        color: parent.checked ? "#ffffff" : "#007bff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        setSortMode("importance")
                    }
                }
                
                Button {
                    id: chapterViewBtn
                    text: "Chapter"
                    checkable: true
                    
                    ButtonGroup.group: viewModeGroup
                    
                    background: Rectangle {
                        color: parent.checked ? "#007bff" : 
                               (parent.pressed ? "#e9ecef" : 
                                parent.hovered ? "#f8f9fa" : "transparent")
                        border.color: "#007bff"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 10
                        color: parent.checked ? "#ffffff" : "#007bff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        setSortMode("chapter")
                    }
                }
                
                Rectangle {
                    width: 1
                    height: 20
                    color: "#dee2e6"
                }
                
                Text {
                    text: "Filter:"
                    font.pixelSize: 11
                    color: "#495057"
                }
                
                ComboBox {
                    id: tagFilter
                    model: getAvailableTags()
                    currentIndex: 0
                    
                    Layout.preferredWidth: 120
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: "#ced4da"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.displayText
                        font.pixelSize: 11
                        color: "#212529"
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 8
                    }
                    
                    onCurrentTextChanged: {
                        filterEventsByTag()
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Export Timeline"
                    implicitHeight: 28
                    
                    background: Rectangle {
                        color: parent.pressed ? "#28a745" : 
                               parent.hovered ? "#34ce57" : "#28a745"
                        border.width: 0
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 10
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        exportTimeline()
                    }
                }
            }
        }
        
        // Timeline section
        Rectangle {
            Layout.fillWidth: true
            Layout.minimumHeight: 400
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            // Timeline background line
            Rectangle {
                id: timelineBackgroundLine
                x: 16
                y: 20
                width: 2
                height: parent.height - 40
                color: "#e0e0e0"
                visible: timelineViewBtn.checked
            }
            
            ScrollView {
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
        if (narrativeModel) {
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
    
    function filterEventsByTag() {
        console.log("Filtering by tag:", tagFilter.currentText)
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