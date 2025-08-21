import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

ScrollView {
    id: relationshipsTab
    
    property var characterModel
    property var relationshipModel: characterModel ? characterModel.relationshipModel : null
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: relationshipsTab.availableWidth
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
                        text: "Character Relationships"
                        font.pixelSize: 20
                        font.bold: true
                        color: "#212121"
                        Layout.fillWidth: true
                    }
                    
                    Button {
                        text: "Add Relationship"
                        onClicked: addRelationshipDialog.open()
                        
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
                    text: "Manage connections between characters. Each relationship includes type, description, and strength."
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
                            text: relationshipModel ? relationshipModel.count : 0
                            font.pixelSize: 24
                            font.bold: true
                            color: "#4CAF50"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Total Relations"
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
                            text: getPositiveRelationshipCount()
                            font.pixelSize: 24
                            font.bold: true
                            color: "#2196F3"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Positive"
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
                            text: getNegativeRelationshipCount()
                            font.pixelSize: 24
                            font.bold: true
                            color: "#F44336"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Negative"
                            font.pixelSize: 10
                            color: "#757575"
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    Item { Layout.fillWidth: true }
                }
            }
        }
        
        // Filter section
        Rectangle {
            Layout.fillWidth: true
            color: "#f8f9fa"
            border.color: "#dee2e6"
            border.width: 1
            radius: 6
            
            implicitHeight: filterContent.implicitHeight + 16
            
            RowLayout {
                id: filterContent
                anchors.fill: parent
                anchors.margins: 8
                spacing: 12
                
                Text {
                    text: "Filter by:"
                    font.pixelSize: 11
                    color: "#495057"
                }
                
                ComboBox {
                    id: relationshipTypeFilter
                    model: getAllRelationshipTypes()
                    textRole: "display"
                    valueRole: "value"
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
                    
                    onCurrentValueChanged: {
                        filterRelationships()
                    }
                }
                
                Text {
                    text: "Search:"
                    font.pixelSize: 11
                    color: "#495057"
                }
                
                TextField {
                    id: searchField
                    placeholderText: "Character name..."
                    Layout.preferredWidth: 150
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: "#ced4da"
                        border.width: 1
                        radius: 4
                    }
                    
                    onTextChanged: {
                        filterRelationships()
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Clear Filters"
                    implicitHeight: 28
                    
                    background: Rectangle {
                        color: parent.pressed ? "#e9ecef" : 
                               parent.hovered ? "#f8f9fa" : "transparent"
                        border.color: "#6c757d"
                        border.width: 1
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 10
                        color: "#6c757d"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        relationshipTypeFilter.currentIndex = 0
                        searchField.text = ""
                    }
                }
            }
        }
        
        // Relationships list
        Rectangle {
            Layout.fillWidth: true
            Layout.minimumHeight: 300
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            ListView {
                id: relationshipsList
                anchors.fill: parent
                anchors.margins: 16
                
                model: relationshipModel
                spacing: 12
                clip: true
                
                delegate: RelationshipWidget {
                    width: relationshipsList.width
                    
                    onEditRequested: function(targetId) {
                        editRelationship(targetId)
                    }
                    
                    onDeleteRequested: function(targetId) {
                        confirmDeleteDialog.targetId = targetId
                        confirmDeleteDialog.targetName = model.targetName
                        confirmDeleteDialog.open()
                    }
                    
                    onStrengthChangeRequested: function(targetId, newStrength) {
                        if (relationshipModel) {
                            relationshipModel.updateRelationship(
                                targetId, 
                                model.type, 
                                model.description, 
                                newStrength
                            )
                        }
                    }
                }
                
                // Empty state
                Rectangle {
                    anchors.centerIn: parent
                    width: 200
                    height: 120
                    color: "transparent"
                    visible: relationshipsList.count === 0
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 8
                        
                        Text {
                            text: "🤝"
                            font.pixelSize: 48
                            color: "#e0e0e0"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "No relationships yet.\nClick 'Add Relationship' to start building your character's social network."
                            font.pixelSize: 12
                            color: "#757575"
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }
    }
    
    // Add relationship dialog
    Dialog {
        id: addRelationshipDialog
        title: "Add New Relationship"
        modal: true
        anchors.centerIn: parent
        
        width: Math.min(400, parent.width * 0.9)
        height: Math.min(350, parent.height * 0.8)
        
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
            
            // Character name
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Character Name *"
                    font.pixelSize: 12
                    font.bold: true
                    color: "#212121"
                }
                
                TextField {
                    id: relationshipNameField
                    Layout.fillWidth: true
                    placeholderText: "Enter character name..."
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
                        border.width: 2
                        radius: 4
                    }
                }
            }
            
            // Relationship type
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                
                Text {
                    text: "Relationship Type *"
                    font.pixelSize: 12
                    font.bold: true
                    color: "#212121"
                }
                
                ComboBox {
                    id: relationshipTypeCombo
                    Layout.fillWidth: true
                    model: getAllRelationshipTypes()
                    textRole: "display"
                    valueRole: "value"
                    currentIndex: 1 // Default to "friend"
                    
                    background: Rectangle {
                        color: "#ffffff"
                        border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
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
                    
                    TextArea {
                        id: relationshipDescField
                        placeholderText: "Describe the relationship, how they met, their history together..."
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        
                        background: Rectangle {
                            color: "#ffffff"
                            border.color: parent.activeFocus ? "#4CAF50" : "#e0e0e0"
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
                    onClicked: addRelationshipDialog.close()
                    
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
                    text: "Add Relationship"
                    enabled: relationshipNameField.text.trim() !== ""
                    
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
                        if (relationshipNameField.text.trim() !== "") {
                            addRelationship(
                                relationshipNameField.text.trim(),
                                relationshipTypeCombo.currentValue,
                                relationshipDescField.text.trim()
                            )
                            addRelationshipDialog.close()
                        }
                    }
                }
            }
        }
        
        onOpened: {
            relationshipNameField.text = ""
            relationshipDescField.text = ""
            relationshipTypeCombo.currentIndex = 1 // Default to "friend"
            relationshipNameField.forceActiveFocus()
        }
    }
    
    // Confirm delete dialog
    Dialog {
        id: confirmDeleteDialog
        title: "Confirm Deletion"
        modal: true
        anchors.centerIn: parent
        
        property string targetId: ""
        property string targetName: ""
        
        ColumnLayout {
            spacing: 16
            
            Text {
                text: `Are you sure you want to remove the relationship with "${confirmDeleteDialog.targetName}"?`
                wrapMode: Text.WordWrap
                Layout.preferredWidth: 300
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Cancel"
                    onClicked: confirmDeleteDialog.close()
                }
                
                Button {
                    text: "Remove"
                    
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
                        if (relationshipModel) {
                            relationshipModel.removeRelationship(confirmDeleteDialog.targetId)
                        }
                        confirmDeleteDialog.close()
                    }
                }
            }
        }
    }
    
    // Helper functions
    function addRelationship(name, type, description) {
        if (relationshipModel) {
            relationshipModel.addRelationship(
                generateId(name),  // Generate a simple ID
                name,
                type,
                description,
                5  // Default strength
            )
        }
    }
    
    function editRelationship(targetId) {
        if (relationshipModel) {
            const relationship = relationshipModel.getRelationship(targetId)
            if (relationship) {
                relationshipNameField.text = relationship.target_name
                relationshipDescField.text = relationship.description
                
                // Find and set the relationship type
                const types = getAllRelationshipTypes()
                for (let i = 0; i < types.length; i++) {
                    if (types[i].value === relationship.type) {
                        relationshipTypeCombo.currentIndex = i
                        break
                    }
                }
                
                addRelationshipDialog.title = "Edit Relationship"
                addRelationshipDialog.open()
            }
        }
    }
    
    function getAllRelationshipTypes() {
        if (relationshipModel) {
            return relationshipModel.getAllRelationshipTypes()
        }
        
        // Fallback types
        return [
            { value: "all", display: "All Types", color: "#9E9E9E", icon: "👥" },
            { value: "family", display: "Family", color: "#E91E63", icon: "👨‍👩‍👧‍👦" },
            { value: "friend", display: "Friend", color: "#4CAF50", icon: "😊" },
            { value: "rival", display: "Rival", color: "#FF5722", icon: "⚔️" },
            { value: "mentor", display: "Mentor", color: "#3F51B5", icon: "👨‍🏫" },
            { value: "student", display: "Student", color: "#00BCD4", icon: "👨‍🎓" },
            { value: "ally", display: "Ally", color: "#8BC34A", icon: "🤝" },
            { value: "enemy", display: "Enemy", color: "#F44336", icon: "💀" },
            { value: "romantic", display: "Romantic", color: "#E91E63", icon: "💕" },
            { value: "neutral", display: "Neutral", color: "#9E9E9E", icon: "😐" }
        ]
    }
    
    function getPositiveRelationshipCount() {
        // TODO: Implement counting logic
        return 0
    }
    
    function getNegativeRelationshipCount() {
        // TODO: Implement counting logic  
        return 0
    }
    
    function filterRelationships() {
        // TODO: Implement filtering logic
        console.log("Filtering relationships:", relationshipTypeFilter.currentValue, searchField.text)
    }
    
    function generateId(name) {
        return name.toLowerCase().replace(/\s+/g, '_') + '_' + Date.now()
    }
}