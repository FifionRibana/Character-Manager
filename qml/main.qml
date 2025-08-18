import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "components"
import "views"

ApplicationWindow {
    id: mainWindow
    width: 1200
    height: 800
    minimumWidth: 1000
    minimumHeight: 700
    visible: true
    title: controller.hasCharacter ? 
           "Medieval Character Manager - " + controller.getCurrentCharacterName() :
           "Medieval Character Manager"

    // Error dialog
    MessageDialog {
        id: errorDialog
        buttons: MessageDialog.Ok
    }

    // File dialogs
    FileDialog {
        id: loadDialog
        title: "Load Character"
        nameFilters: ["JSON files (*.json)"]
        onAccepted: {
            let path = selectedFile.toString()
            if (path.startsWith("file://")) {
                path = path.substring(7) // Remove file:// prefix
            }
            controller.loadCharacterFile(path)
        }
    }

    FileDialog {
        id: exportDialog
        title: "Export Character"
        fileMode: FileDialog.SaveFile
        nameFilters: ["HTML files (*.html)"]
        onAccepted: {
            let path = selectedFile.toString()
            if (path.startsWith("file://")) {
                path = path.substring(7) // Remove file:// prefix
            }
            controller.exportCharacter(
                controller.getCurrentCharacterId(),
                path
            )
        }
    }

    // Menu bar
    menuBar: MenuBar {
        Menu {
            title: "File"
            
            Action {
                text: "New Character"
                shortcut: "Ctrl+N"
                onTriggered: controller.newCharacter()
            }
            
            MenuSeparator {}
            
            Action {
                text: "Load Character"
                shortcut: "Ctrl+O"
                onTriggered: loadDialog.open()
            }
            
            Action {
                text: "Save Character"
                shortcut: "Ctrl+S"
                enabled: controller.hasCharacter
                onTriggered: controller.save_current_character()
            }
            
            MenuSeparator {}
            
            Action {
                text: "Export to HTML"
                enabled: controller.hasCharacter
                onTriggered: exportDialog.open()
            }
            
            MenuSeparator {}
            
            Action {
                text: "Quit"
                shortcut: "Ctrl+Q"
                onTriggered: Qt.quit()
            }
        }
        
        Menu {
            title: "Edit"
            
            Action {
                text: controller.editMode ? "View Mode" : "Edit Mode"
                shortcut: "Ctrl+E"
                onTriggered: controller.toggleEditMode()
            }
        }
    }

    // Tool bar
    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            
            ToolButton {
                text: "New"
                onClicked: controller.newCharacter()
            }
            
            ToolButton {
                text: "Save"
                enabled: controller.hasCharacter
                onClicked: controller.save_current_character()
            }
            
            ToolButton {
                text: "Load"
                onClicked: loadDialog.open()
            }
            
            ToolSeparator {}
            
            ToolButton {
                text: "Export"
                enabled: controller.hasCharacter
                onClicked: exportDialog.open()
            }
            
            Item { Layout.fillWidth: true }
            
            // Edit mode toggle
            Switch {
                text: "Edit Mode"
                checked: controller.editMode
                onToggled: controller.editMode = checked
            }
        }
    }

    // Main content
    SplitView {
        id: splitView
        anchors.fill: parent
        orientation: Qt.Horizontal
        
        // Sidebar
        Rectangle {
            SplitView.minimumWidth: 250
            SplitView.preferredWidth: 300
            SplitView.maximumWidth: 400
            
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 8

                // Title
                Text {
                    text: "Characters"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                    Layout.alignment: Qt.AlignHCenter
                }

                // Separator
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }

                // Character list
                ListView {
                    id: characterList
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    
                    model: controller.characterListModel
                    clip: true
                    spacing: 4
                    
                    delegate: Rectangle {
                        width: characterList.width
                        height: 60
                        color: mouseArea.containsMouse ? "#f5f5f5" : "transparent"
                        radius: 4
                        
                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            
                            onClicked: {
                                characterList.currentIndex = index
                                if (controller.characterListModel) {
                                    controller.characterListModel.selectCharacter(index)
                                }
                            }
                        }
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 8
                            
                            // Avatar
                            Rectangle {
                                width: 40
                                height: 40
                                radius: 20
                                color: "#e3f2fd"
                                border.color: "#e0e0e0"
                                border.width: 1
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: model.name ? model.name.charAt(0).toUpperCase() : "?"
                                    font.pixelSize: 18
                                    font.bold: true
                                    color: "#212121"
                                }
                            }
                            
                            // Info
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 2
                                
                                Text {
                                    text: model.name || "Unnamed Character"
                                    font.pixelSize: 14
                                    font.bold: true
                                    color: "#212121"
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                }
                                
                                Text {
                                    text: "Level " + (model.level || 1)
                                    font.pixelSize: 12
                                    color: "#757575"
                                }
                            }
                            
                            // Level badge
                            Rectangle {
                                width: 24
                                height: 24
                                radius: 12
                                color: "#4CAF50"
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: (model.level || 1).toString()
                                    font.pixelSize: 12
                                    font.bold: true
                                    color: "#ffffff"
                                }
                            }
                        }
                    }
                    
                    // Highlight
                    highlight: Rectangle {
                        color: "#4CAF50"
                        opacity: 0.3
                        radius: 4
                    }
                    
                    // Empty state
                    Label {
                        anchors.centerIn: parent
                        text: "No characters"
                        color: "#757575"
                        visible: characterList.count === 0
                    }
                }

                // Buttons
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 4

                    Button {
                        text: "New"
                        Layout.fillWidth: true
                        onClicked: controller.newCharacter()
                    }

                    Button {
                        text: "Delete"
                        enabled: characterList.currentIndex >= 0
                        Layout.fillWidth: true
                        onClicked: {
                            console.log("Delete not implemented yet")
                        }
                    }
                }
            }
        }
        
        // Main content area
        Rectangle {
            id: contentArea
            SplitView.fillWidth: true
            color: "#f5f5f5"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10
                
                // Character header (only in edit mode)
                Rectangle {
                    Layout.fillWidth: true
                    height: 80
                    visible: controller.editMode
                    color: "#ffffff"
                    border.color: "#e0e0e0"
                    border.width: 1
                    radius: 4
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 16
                        
                        // Image placeholder
                        Rectangle {
                            width: 60
                            height: 60
                            radius: 8
                            color: "#f5f5f5"
                            border.color: "#e0e0e0"
                            border.width: 1
                            
                            Text {
                                anchors.centerIn: parent
                                text: "📷"
                                font.pixelSize: 24
                            }
                        }
                        
                        // Character info
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 4
                            
                            TextField {
                                text: controller.characterModel ? controller.characterModel.name : ""
                                font.pixelSize: 18
                                font.bold: true
                                placeholderText: "Character Name"
                                Layout.fillWidth: true
                                
                                onTextChanged: {
                                    if (controller.characterModel && controller.characterModel.name !== text) {
                                        controller.characterModel.name = text
                                    }
                                }
                            }
                            
                            RowLayout {
                                Text {
                                    text: "Level:"
                                    font.pixelSize: 14
                                    color: "#757575"
                                }
                                
                                SpinBox {
                                    from: 1
                                    to: 100
                                    value: controller.characterModel ? controller.characterModel.level : 1
                                    
                                    onValueChanged: {
                                        if (controller.characterModel && controller.characterModel.level !== value) {
                                            controller.characterModel.level = value
                                        }
                                    }
                                }
                                
                                Item { Layout.fillWidth: true }
                            }
                        }
                    }
                }
                
                // Tab view
                TabBar {
                    id: tabBar
                    Layout.fillWidth: true
                    
                    TabButton { text: "Overview" }
                    TabButton { text: "Character"; enabled: controller.editMode; visible: controller.editMode }
                    TabButton { text: "Enneagram"; enabled: controller.editMode; visible: controller.editMode }
                    TabButton { text: "Stats"; enabled: controller.editMode; visible: controller.editMode }
                    TabButton { text: "Biography"; enabled: controller.editMode; visible: controller.editMode }
                    TabButton { text: "Relationships"; enabled: controller.editMode; visible: controller.editMode }
                    TabButton { text: "Narrative"; enabled: controller.editMode; visible: controller.editMode }
                }
                
                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: tabBar.currentIndex
                    
                    // Overview tab
                    Rectangle {
                        color: "#ffffff"
                        
                        ScrollView {
                            anchors.fill: parent
                            anchors.margins: 16
                            
                            ColumnLayout {
                                width: parent.width
                                spacing: 16
                                
                                // Edit mode button
                                Button {
                                    text: "Enter Edit Mode"
                                    Layout.alignment: Qt.AlignRight
                                    visible: !controller.editMode && controller.hasCharacter
                                    onClicked: controller.editMode = true
                                }
                                
                                // Character info
                                Text {
                                    text: "Character: " + (controller.characterModel ? controller.characterModel.name : "No character loaded")
                                    font.pixelSize: 18
                                    font.bold: true
                                }
                                
                                Text {
                                    text: "Level: " + (controller.characterModel ? controller.characterModel.level : "?")
                                    font.pixelSize: 14
                                    color: "#757575"
                                }
                                
                                // Basic stats display
                                Text {
                                    text: "Stats:"
                                    font.pixelSize: 16
                                    font.bold: true
                                }
                                
                                GridLayout {
                                    columns: 3
                                    columnSpacing: 16
                                    rowSpacing: 8
                                    
                                    Text { text: "STR: " + (controller.characterModel ? controller.characterModel.strength : 10) }
                                    Text { text: "AGI: " + (controller.characterModel ? controller.characterModel.agility : 10) }
                                    Text { text: "CON: " + (controller.characterModel ? controller.characterModel.constitution : 10) }
                                    Text { text: "INT: " + (controller.characterModel ? controller.characterModel.intelligence : 10) }
                                    Text { text: "WIS: " + (controller.characterModel ? controller.characterModel.wisdom : 10) }
                                    Text { text: "CHA: " + (controller.characterModel ? controller.characterModel.charisma : 10) }
                                }
                                
                                Item { Layout.fillHeight: true }
                            }
                        }
                    }
                    
                    // Real edit tabs
                    Loader {
                        source: "views/CharacterEditTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                    
                    Loader {
                        source: "views/EnneagramTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                    
                    Loader {
                        source: "views/StatsTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                    
                    Loader {
                        source: "views/BiographyTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                    
                    Loader {
                        source: "views/RelationshipsTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                    
                    Loader {
                        source: "views/NarrativeTab.qml"
                        onLoaded: {
                            if (item) {
                                item.characterModel = Qt.binding(function() { return controller.characterModel })
                            }
                        }
                    }
                }
            }
        }
    }

    // Status bar
    footer: Rectangle {
        id: statusBar
        height: 30
        color: "#ffffff"
        border.color: "#e0e0e0"
        border.width: 1
        
        property string message: "Ready"
        
        function showMessage(msg) {
            message = msg
            statusTimer.restart()
        }
        
        Text {
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            text: statusBar.message
            color: "#212121"
        }
        
        Timer {
            id: statusTimer
            interval: 3000
            onTriggered: statusBar.message = "Ready"
        }
    }

    Component.onCompleted: {
        // Connect controller signals
        controller.errorOccurred.connect(function(title, message) {
            errorDialog.title = title
            errorDialog.text = message
            errorDialog.open()
        })
        
        controller.statusChanged.connect(function(message) {
            statusBar.showMessage(message)
        })
        
        console.log("Medieval Character Manager started")
    }
}