import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import App.Styles
import App.Controllers

import "./components"
import "./views"

ApplicationWindow {
    id: iMainWindow
    visible: true
    width: 1280
    height: 800
    minimumWidth: 800
    minimumHeight: 600
    title: qsTr("Character Manager")

    // Theme support
    color: AppTheme.colors.background
    
    // Properties
    property bool unsavedChanges: false
    property string currentFile: ""
    property bool isLoading: false
    property int autoSaveCounter: 0
    property bool editMode: MainController.editMode

    Component.onCompleted: console.log("Result", ImageController.test_method())

    Connections {
        target: ImageController
        function onErrorOccurred(label, message) {
            errorDialog.showError(label, message)
        }
    }

    Connections {
        target: MainController
        function onErrorOccurred(label, message) {
            errorDialog.showError(label, message)
        }
    }
    
    // Global shortcuts
    // Shortcut {
    //     sequence: "Ctrl+N"
    //     onActivated: MainController.create_new_character()
    // }

    // Shortcut {
    //     sequence: "Ctrl+S"
    //     onActivated: MainController.save_current_character()
    // }

    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")

            Action {
                text: qsTr("&New Character")
                shortcut: "Ctrl+N"
                onTriggered: MainController.create_new_character()
            }
            Action {
                text: qsTr("&Open...")
                shortcut: "Ctrl+O"
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Save")
                shortcut: "Ctrl+S"
                onTriggered: MainController.save_current_character()
            }
            Action {
                text: qsTr("Save &As...")
                shortcut: "Ctrl+Shift+S"
            }
            Action {
                text: qsTr("Save A&ll")
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Export...")
                shortcut: "Ctrl+E"
            }
            Action {
                text: qsTr("Export &Timeline...")
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Settings...")
                shortcut: "Ctrl+,"
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Quit")
                shortcut: "Ctrl+Q"
            }
        }

        Menu {
            title: qsTr("&Edit")

            Action {
                text: qsTr("&Undo")
                shortcut: "Ctrl+Z"
                enabled: false
            }
            Action {
                text: qsTr("&Redo")
                shortcut: "Ctrl+Y"
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Search...")
                shortcut: "Ctrl+F"
            }
            Action {
                text: qsTr("&Delete character")
            }
        }

        Menu {
            title: qsTr("&View")

            Action {
                text: qsTr("&Toggle Theme")
                shortcut: "Ctrl+Shift+T"
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Full Screen")
                shortcut: "F11"
            }
        }

        Menu {
            title: qsTr("&Tools")
            
            Action {
                text: qsTr("Character &Templates...")
            }

            Action {
                text: qsTr("&Batch Export...")
            }

            Action {
                text: qsTr("&Statistics...")
            }
        }
        
        Menu {
            title: qsTr("&Help")

            Action {
                text: qsTr("&Documentation")
                shortcut: "F1"
            }

            Action {
                text: qsTr("&Keyboard Shortcuts")
            }

            MenuSeparator {}

            Action {
                text: qsTr("&About...")
            }
        }
    }

    // Main content
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Sidebar
        Sidebar {
            id: iSidebar
            Layout.preferredWidth: 250
            Layout.fillHeight: true

            characterListModel: MainController.characterListModel
            

        }

        // Divider
        Rectangle {
            Layout.preferredWidth: 1
            Layout.fillHeight: true
            color: AppTheme.colors.border
        }

        // Main content area
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            // Empty State
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: MainController.currentCharacter === null

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: AppTheme.spacing.large

                    Image {
                        Layout.alignment: Qt.AlignHCenter
                        source: ""
                        sourceSize.width: 200
                        sourceSize.height: 200
                        opacity: 0.3
                    }

                    Label {
                        Layout.alignment: Qt.AlignHCenter
                        text: qsTr("No Character Selected")
                        font.pixelSize: AppTheme.fontSize.huge
                        color: AppTheme.colors.textSecondary
                    }

                    Label {
                        Layout.alignment: Qt.AlignHCenter
                        text: qsTr("Create a new character or select one from the sidebar")
                        font.pixelSize: AppTheme.fontSize.medium
                        color: AppTheme.colors.textDisabled
                    }

                    Button {
                        Layout.alignment: Qt.AlignHCenter
                        text: qsTr("Create New Character")
                        highlighted: true
                        onClicked: MainController.create_new_character()
                    }
                }
            }

            // Character header
            CharacterHeader {
                Layout.fillWidth: true
                Layout.preferredHeight: 160
                visible: MainController.currentCharacter !== null //&& !iMainWindow.editMode
                characterModel: MainController.currentCharacter
                editMode: iMainWindow.editMode
            }

            OverviewTab {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: MainController.currentCharacter !== null && !iMainWindow.editMode
                characterModel: MainController.currentCharacter
            }

            // Tab view
            TabView {
                id: iTabView
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: MainController.currentCharacter !== null && iMainWindow.editMode
                characterModel: MainController.currentCharacter
            }


            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: iTabView.currentIndex
                visible: MainController.currentCharacter !== null && iMainWindow.editMode

                CharacterEditTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    characterModel: MainController.currentCharacter
                }
                
                EnneagramTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    characterModel: MainController.currentCharacter
                }
                
                StatsTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    characterModel: MainController.currentCharacter
                }
                
                BiographyTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    characterModel: MainController.currentCharacter
                }
                
                RelationshipsTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    // characterModel: MainController.currentCharacter
                }
                
                NarrativeTab {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    // characterModel: MainController.currentCharacter
                }
            }
        }
    }

    footer: ToolBar {
        id: iStatusBar
        height: 30
        background: Rectangle {
            color: AppTheme.colors.surface
            border.color: AppTheme.colors.border
            border.width: AppTheme.border.thin
        }
        
        property string message: ""
        property Timer messageTimer: Timer {
            interval: 3000
            onTriggered: iStatusBar.message = ""
        }

        function showMessage(text, duration) {
            message = text;
            if (duration > 0) {
                messageTimer.interval = duration;
                messageTimer.restart();
            }
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.small

            // Status message
            Label {
                text: iStatusBar.message || (unsavedChanges ? "⚠️ Unsaved changes" : "Ready")
                color: unsavedChanges && !iStatusBar.message ? AppTheme.colors.warning : AppTheme.colors.text
                font.pixelSize: AppTheme.fontSize.small
            }

            Item {
                Layout.fillWidth: true
            }

            // Character count
            Label {
                text: qsTr("Characters: %1").arg(MainController && MainController.characterListModel ? MainController.characterListModel.rowCount() : 0)
                color: AppTheme.colors.textSecondary
                font.pixelSize: AppTheme.fontSize.small
            }

            Rectangle {
                width: 1
                height: parent.height - 4
                color: AppTheme.colors.border
            }

            // Current theme
            Label {
                text: "🎨 " + (ThemeController ? ThemeController.currentThemeName : "Default")
                color: AppTheme.colors.textSecondary
                font.pixelSize: AppTheme.fontSize.small

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (ThemeController) {
                            ThemeController.toggle_theme();
                        }
                    }
                }
            }

            Rectangle {
                width: 1
                height: parent.height - 4
                color: AppTheme.colors.border
            }

            // Auto-save indicator
            Label {
                text: AppTheme.autoSaveEnabled ? "💾 Auto-save ON" : "💾 Auto-save OFF"
                color: AppTheme.autoSaveEnabled ? AppTheme.colors.success : AppTheme.colors.textDisabled
                font.pixelSize: AppTheme.fontSize.small
                visible: MainController.currentCharacter !== null

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    // onClicked: openSettings()
                }
            }
        }
    }

    // Dialogs

    ErrorDialog {
        id: errorDialog
    }
}