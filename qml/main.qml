import QtQuick 6.2
import QtQuick.Window 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import QtQuick.Dialogs 6.2
import MedievalModels 1.0
import MedievalControllers 1.0
import "components"
import "views"
import "dialogs"
import "styles"

// import App.Styles
// import App.Controllers

ApplicationWindow {
    id: mainWindow
    visible: true
    width: compactMode ? 1024 : 1280
    height: compactMode ? 600 : 800
    minimumWidth: 800
    minimumHeight: 600
    title: qsTr("Medieval Character Manager") + (controller.currentCharacter ? " - " + controller.currentCharacter.name : "")

    // Theme support
    color: AppTheme.colors.background

    // Properties
    property bool unsavedChanges: false
    property string currentFile: ""
    property bool isLoading: false
    property int autoSaveCounter: 0

    // Controllers
    MainController {
        id: controller

        onCharacterLoaded: {
            if (currentCharacter) {
                console.log("Character loaded:", currentCharacter.name);
                tabView.currentIndex = 0;
            }
        }

        onErrorOccurred: function (message) {
            errorDialog.showError("Error", message);
        }
    }

    // Auto-save timer
    Timer {
        id: autoSaveTimer
        interval: AppTheme.autoSaveInterval * 60000 // Convert minutes to milliseconds
        running: AppTheme.autoSaveEnabled && controller.currentCharacter !== null
        repeat: true

        onTriggered: {
            if (unsavedChanges && controller.currentCharacter) {
                console.log("Auto-saving character...");
                storageController.quickSave(controller.currentCharacter);
                autoSaveCounter++;
                statusBar.showMessage("Auto-saved", 2000);
            }
        }
    }

    // Global shortcuts
    Shortcut {
        sequence: "Ctrl+N"
        onActivated: controller.createNewCharacter()
    }

    Shortcut {
        sequence: "Ctrl+S"
        onActivated: saveCharacter()
    }

    Shortcut {
        sequence: "Ctrl+Shift+S"
        onActivated: saveAllCharacters()
    }

    Shortcut {
        sequence: "Ctrl+O"
        onActivated: openFileDialog.open()
    }

    Shortcut {
        sequence: "Ctrl+,"
        onActivated: openSettings()
    }

    Shortcut {
        sequence: "Ctrl+Q"
        onActivated: confirmQuit()
    }

    Shortcut {
        sequence: "Ctrl+F"
        onActivated: searchDialog.open()
    }

    Shortcut {
        sequence: "Ctrl+E"
        onActivated: openExportDialog()
    }

    Shortcut {
        sequence: "Ctrl+Shift+T"
        onActivated: {
            if (themeController) {
                themeController.toggleTheme();
            }
        }
    }

    // Tab navigation shortcuts
    Shortcut {
        sequence: "Ctrl+1"
        onActivated: tabView.currentIndex = 0
    }

    Shortcut {
        sequence: "Ctrl+2"
        onActivated: tabView.currentIndex = 1
    }

    Shortcut {
        sequence: "Ctrl+3"
        onActivated: tabView.currentIndex = 2
    }

    Shortcut {
        sequence: "Ctrl+4"
        onActivated: tabView.currentIndex = 3
    }

    Shortcut {
        sequence: "Ctrl+5"
        onActivated: tabView.currentIndex = 4
    }

    Shortcut {
        sequence: "Ctrl+6"
        onActivated: tabView.currentIndex = 5
    }

    // Menu bar
    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")

            Action {
                text: qsTr("&New Character")
                shortcut: "Ctrl+N"
                onTriggered: controller.createNewCharacter()
            }

            Action {
                text: qsTr("&Open...")
                shortcut: "Ctrl+O"
                onTriggered: openFileDialog.open()
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Save")
                shortcut: "Ctrl+S"
                enabled: controller.currentCharacter !== null
                onTriggered: saveCharacter()
            }

            Action {
                text: qsTr("Save &As...")
                shortcut: "Ctrl+Shift+S"
                enabled: controller.currentCharacter !== null
                onTriggered: saveAsDialog.open()
            }

            Action {
                text: qsTr("Save A&ll")
                enabled: controller && controller.characterList ? controller.characterList.rowCount() > 0 : false
                onTriggered: saveAllCharacters()
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Export...")
                shortcut: "Ctrl+E"
                enabled: controller.currentCharacter !== null
                onTriggered: openExportDialog()
            }

            Action {
                text: qsTr("Export &Timeline...")
                enabled: controller.currentCharacter !== null && controller && controller.currentCharacter && controller.currentCharacter.narrativeModel ? controller.currentCharacter.narrativeModel.rowCount() > 0 : false
                onTriggered: exportTimelineDialog.open()
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Settings...")
                shortcut: "Ctrl+,"
                onTriggered: openSettings()
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Quit")
                shortcut: "Ctrl+Q"
                onTriggered: confirmQuit()
            }
        }

        Menu {
            title: qsTr("&Edit")

            Action {
                text: qsTr("&Undo")
                shortcut: "Ctrl+Z"
                enabled: false // TODO: Implement undo system
            }

            Action {
                text: qsTr("&Redo")
                shortcut: "Ctrl+Y"
                enabled: false // TODO: Implement redo system
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Search...")
                shortcut: "Ctrl+F"
                onTriggered: searchDialog.open()
            }

            Action {
                text: qsTr("&Delete Character")
                shortcut: "Delete"
                enabled: controller.currentCharacter !== null
                onTriggered: confirmDeleteCharacter()
            }
        }

        Menu {
            title: qsTr("&View")

            Action {
                text: qsTr("&Toggle Theme")
                shortcut: "Ctrl+Shift+T"
                onTriggered: {
                    if (themeController) {
                        themeController.toggleTheme();
                    }
                }
            }

            MenuSeparator {}

            Action {
                text: qsTr("&Compact Mode")
                checkable: true
                checked: compactMode
                onTriggered: toggleCompactMode()
            }

            Action {
                text: qsTr("&Full Screen")
                shortcut: "F11"
                checkable: true
                checked: mainWindow.visibility === Window.FullScreen
                onTriggered: toggleFullScreen()
            }
        }

        Menu {
            title: qsTr("&Tools")

            Action {
                text: qsTr("Character &Templates...")
                onTriggered: templateDialog.open()
            }

            Action {
                text: qsTr("&Batch Export...")
                enabled: controller && controller.characterList ? controller.characterList.rowCount() > 1 : false
                onTriggered: batchExportDialog.open()
            }

            Action {
                text: qsTr("&Statistics...")
                enabled: controller && controller.characterList ? controller.characterList.rowCount() > 0 : false
                onTriggered: statisticsDialog.open()
            }
        }

        Menu {
            title: qsTr("&Help")

            Action {
                text: qsTr("&Documentation")
                shortcut: "F1"
                onTriggered: Qt.openUrlExternally("https://github.com/medieval-character-manager/docs")
            }

            Action {
                text: qsTr("&Keyboard Shortcuts")
                onTriggered: shortcutsDialog.open()
            }

            MenuSeparator {}

            Action {
                text: qsTr("&About...")
                onTriggered: aboutDialog.open()
            }
        }
    }

    // Main content
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Sidebar
        Sidebar {
            id: sidebar
            Layout.preferredWidth: compactMode ? 200 : 250
            Layout.fillHeight: true
            characterListModel: controller.characterList

            onCharacterSelected: function (characterId) {
                controller.selectCharacter(characterId);
            }

            onNewCharacterRequested: {
                controller.createNewCharacter();
            }

            onDeleteCharacterRequested: function (characterId) {
                confirmDeleteDialog.characterToDelete = characterId;
                confirmDeleteDialog.open();
            }
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

            // Character header
            CharacterHeader {
                id: characterHeader
                Layout.fillWidth: true
                Layout.preferredHeight: compactMode ? 100 : 120
                visible: controller.currentCharacter !== null
                characterModel: controller.currentCharacter

                onImageChangeRequested: function (imagePath) {
                    if (controller.currentCharacter) {
                        controller.currentCharacter.imagePath = imagePath;
                        unsavedChanges = true;
                    }
                }

                onEditModeChanged: {
                    characterHeader.editMode = !characterHeader.editMode;
                }
            }

            // Tab view
            TabView {
                id: tabView
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: controller.currentCharacter !== null
                characterModel: controller.currentCharacter

                // onDataChanged: {
                //     unsavedChanges = true
                // }
            }

            // Empty state
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: controller.currentCharacter === null

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: AppTheme.spacing.large

                    Image {
                        Layout.alignment: Qt.AlignHCenter
                        source: ""  // Image removed - was: qrc:/images/empty-state.svg
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
                        onClicked: controller.createNewCharacter()
                    }
                }
            }
        }
    }

    // Status bar
    footer: ToolBar {
        id: statusBar
        height: 30
        background: Rectangle {
            color: AppTheme.colors.surface
            border.color: AppTheme.colors.border
            border.width: 1
        }

        property string message: ""
        property Timer messageTimer: Timer {
            interval: 3000
            onTriggered: statusBar.message = ""
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
                text: statusBar.message || (unsavedChanges ? "⚠️ Unsaved changes" : "Ready")
                color: unsavedChanges && !statusBar.message ? AppTheme.colors.warning : AppTheme.colors.text
                font.pixelSize: AppTheme.fontSize.small
            }

            Item {
                Layout.fillWidth: true
            }

            // Character count
            Label {
                text: qsTr("Characters: %1").arg(controller && controller.characterList ? controller.characterList.rowCount() : 0)
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
                text: "🎨 " + (themeController ? themeController.currentThemeName : "Default")
                color: AppTheme.colors.textSecondary
                font.pixelSize: AppTheme.fontSize.small

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (themeController) {
                            themeController.toggleTheme();
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
                visible: controller.currentCharacter !== null

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: openSettings()
                }
            }
        }
    }

    // Dialogs

    ErrorDialog {
        id: errorDialog
    }

    FileDialog {
        id: openFileDialog
        title: qsTr("Open Character File")
        nameFilters: ["Character files (*.json *.chr)", "All files (*)"]
        fileMode: FileDialog.OpenFile

        onAccepted: {
            controller.loadCharacterFromFile(selectedFile);
        }
    }

    FileDialog {
        id: saveAsDialog
        title: qsTr("Save Character As")
        nameFilters: ["Character files (*.json)", "All files (*)"]
        fileMode: FileDialog.SaveFile
        defaultSuffix: "json"

        onAccepted: {
            saveCharacterToFile(selectedFile);
        }
    }

    SettingsDialog {
        id: settingsDialog
        themeController: themeController

        onAccepted: {
            statusBar.showMessage("Settings saved", 2000);
        }
    }

    MessageDialog {
        id: confirmDeleteDialog
        property string characterToDelete: ""

        title: qsTr("Delete Character")
        text: qsTr("Are you sure you want to delete this character?")
        informativeText: qsTr("This action cannot be undone.")
        buttons: MessageDialog.Yes | MessageDialog.No

        onAccepted: {
            if (characterToDelete) {
                controller.deleteCharacter(characterToDelete);
                characterToDelete = "";
            }
        }
    }

    MessageDialog {
        id: confirmQuitDialog
        title: qsTr("Quit Application")
        text: unsavedChanges ? qsTr("You have unsaved changes. Do you want to save before quitting?") : qsTr("Are you sure you want to quit?")
        buttons: unsavedChanges ? (MessageDialog.Save | MessageDialog.Discard | MessageDialog.Cancel) : (MessageDialog.Yes | MessageDialog.No)

        onAccepted: {
            if (unsavedChanges) {
                saveAllCharacters();
            }
            Qt.quit();
        }

        onRejected: {
            Qt.quit();
        }
    }

    Dialog {
        id: exportDialog
        title: qsTr("Export Character")
        width: 600
        height: 500
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel

        property var exportOptions: ({})

        ColumnLayout {
            anchors.fill: parent
            spacing: AppTheme.spacing.medium

            Label {
                text: qsTr("Export Format:")
                font.bold: true
            }

            ComboBox {
                id: exportFormatCombo
                Layout.fillWidth: true
                model: ["PDF", "HTML", "Markdown", "JSON", "Plain Text"]
            }

            GroupBox {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: qsTr("Export Options")

                ColumnLayout {
                    anchors.fill: parent

                    CheckBox {
                        id: includeOverviewCheck
                        text: qsTr("Include Overview")
                        checked: true
                    }

                    CheckBox {
                        id: includeEnneagramCheck
                        text: qsTr("Include Enneagram")
                        checked: true
                    }

                    CheckBox {
                        id: includeStatsCheck
                        text: qsTr("Include Statistics")
                        checked: true
                    }

                    CheckBox {
                        id: includeBiographyCheck
                        text: qsTr("Include Biography")
                        checked: true
                    }

                    CheckBox {
                        id: includeRelationshipsCheck
                        text: qsTr("Include Relationships")
                        checked: true
                    }

                    CheckBox {
                        id: includeTimelineCheck
                        text: qsTr("Include Timeline")
                        checked: true
                    }

                    CheckBox {
                        id: includeImagesCheck
                        text: qsTr("Include Images")
                        checked: true
                    }

                    CheckBox {
                        id: darkThemeCheck
                        text: qsTr("Use Dark Theme")
                        checked: AppTheme.isDarkMode
                        visible: exportFormatCombo.currentText === "HTML"
                    }
                }
            }
        }

        onAccepted: {
            var options = {
                "include_overview": includeOverviewCheck.checked,
                "include_enneagram": includeEnneagramCheck.checked,
                "include_stats": includeStatsCheck.checked,
                "include_biography": includeBiographyCheck.checked,
                "include_relationships": includeRelationshipsCheck.checked,
                "include_timeline": includeTimelineCheck.checked,
                "include_images": includeImagesCheck.checked,
                "dark_theme": darkThemeCheck.checked
            };

            var format = exportFormatCombo.currentText.toLowerCase();
            if (format === "plain text")
                format = "text";

            var filepath = exportController.exportCharacter(controller.currentCharacter, format, options);

            if (filepath) {
                statusBar.showMessage("Exported to: " + filepath, 5000);
            }
        }
    }

    // Helper functions

    function saveCharacter() {
        if (controller.currentCharacter) {
            if (currentFile) {
                saveCharacterToFile(currentFile);
            } else {
                saveAsDialog.open();
            }
        }
    }

    function saveCharacterToFile(filepath) {
        if (controller.currentCharacter && storageController) {
            var success = storageController.saveCharacter(controller.currentCharacter, filepath);
            if (success) {
                currentFile = filepath;
                unsavedChanges = false;
                statusBar.showMessage("Character saved", 2000);
            } else {
                errorDialog.showError("Save Error", "Failed to save character to file");
            }
        }
    }

    function saveAllCharacters() {
        var savedCount = 0;
        for (var i = 0; i < controller.characterList.rowCount(); i++) {
            var character = controller.characterList.getCharacterAt(i);
            if (character && storageController.quickSave(character)) {
                savedCount++;
            }
        }
        statusBar.showMessage(qsTr("Saved %1 characters").arg(savedCount), 3000);
        unsavedChanges = false;
    }

    function openSettings() {
        settingsDialog.open();
    }

    function openExportDialog() {
        if (controller.currentCharacter) {
            exportDialog.open();
        }
    }

    function confirmQuit() {
        if (unsavedChanges) {
            confirmQuitDialog.open();
        } else {
            Qt.quit();
        }
    }

    function confirmDeleteCharacter() {
        if (controller.currentCharacter) {
            confirmDeleteDialog.characterToDelete = controller.currentCharacter.id;
            confirmDeleteDialog.open();
        }
    }

    function toggleCompactMode() {
        mainWindow.width = compactMode ? 1280 : 1024;
        mainWindow.height = compactMode ? 800 : 600;
    }

    function toggleFullScreen() {
        if (mainWindow.visibility === Window.FullScreen) {
            mainWindow.showNormal();
        } else {
            mainWindow.showFullScreen();
        }
    }

    // Initialize theme
    Component.onCompleted: {
        // Set theme controller reference in AppTheme
        if (themeController) {
            AppTheme.themeController = themeController;
        }

        console.log("Medieval Character Manager - Phase 5 initialized");
        console.log("Theme:", themeController ? themeController.currentThemeName : "Default");
        console.log("Debug mode:", debugMode);
        console.log("Compact mode:", compactMode);
    }
}
