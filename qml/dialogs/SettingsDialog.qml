import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"
import "../styles"

Dialog {
    id: settingsDialog
    
    property var themeController: null
    property int selectedTabIndex: 0
    
    title: "Settings"
    width: 800
    height: 600
    modal: true
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Apply
    
    // Apply button handler
    onApplied: {
        applySettings()
    }
    
    // OK button handler
    onAccepted: {
        applySettings()
    }
    
    // Cancel button handler
    onRejected: {
        revertSettings()
    }
    
    function applySettings() {
        // Apply theme changes
        if (themeController && themeCombo.currentText !== themeController.currentThemeName) {
            themeController.switchTheme(themeCombo.currentText)
        }
        
        // Save other settings
        AppTheme.animationsEnabled = animationsSwitch.checked
        AppTheme.soundEnabled = soundSwitch.checked
        AppTheme.autoSaveEnabled = autoSaveSwitch.checked
        AppTheme.autoSaveInterval = autoSaveSpinBox.value
    }
    
    function revertSettings() {
        // Revert to original values
        loadCurrentSettings()
    }
    
    function loadCurrentSettings() {
        // Load current theme
        if (themeController) {
            var themes = themeController.availableThemes
            for (var i = 0; i < themes.length; i++) {
                if (themes[i].name === themeController.currentThemeName) {
                    themeCombo.currentIndex = i
                    break
                }
            }
        }
        
        // Load other settings
        animationsSwitch.checked = AppTheme.animationsEnabled
        soundSwitch.checked = AppTheme.soundEnabled
        autoSaveSwitch.checked = AppTheme.autoSaveEnabled
        autoSaveSpinBox.value = AppTheme.autoSaveInterval
    }
    
    Component.onCompleted: {
        loadCurrentSettings()
    }
    
    // Main content
    ColumnLayout {
        anchors.fill: parent
        spacing: AppTheme.spacing.medium
        
        // Tab bar for different settings categories
        TabBar {
            id: settingsTabBar
            Layout.fillWidth: true
            currentIndex: selectedTabIndex
            
            TabButton {
                text: "Appearance"
                width: implicitWidth
            }
            
            TabButton {
                text: "Behavior"
                width: implicitWidth
            }
            
            TabButton {
                text: "Data"
                width: implicitWidth
            }
            
            TabButton {
                text: "Shortcuts"
                width: implicitWidth
            }
        }
        
        // Settings content area
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: settingsTabBar.currentIndex
            
            // Appearance Tab
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: AppTheme.spacing.large
                    
                    // Theme Selection
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Theme"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Theme:"
                                    Layout.preferredWidth: 120
                                }
                                
                                ComboBox {
                                    id: themeCombo
                                    Layout.fillWidth: true
                                    model: themeController ? themeController.availableThemes.map(t => t.name) : []
                                    
                                    onCurrentTextChanged: {
                                        if (themeController) {
                                            updateThemePreview()
                                        }
                                    }
                                }
                                
                                Button {
                                    text: "Customize"
                                    enabled: themeCombo.currentText !== ""
                                    onClicked: openCustomThemeDialog()
                                }
                            }
                            
                            // Theme Preview
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 100
                                color: AppTheme.colors.surface
                                border.color: AppTheme.colors.border
                                radius: AppTheme.radius.medium
                                
                                GridLayout {
                                    anchors.fill: parent
                                    anchors.margins: AppTheme.spacing.medium
                                    columns: 4
                                    rowSpacing: AppTheme.spacing.small
                                    columnSpacing: AppTheme.spacing.small
                                    
                                    // Color preview squares
                                    Repeater {
                                        model: [
                                            { name: "Background", color: AppTheme.colors.background },
                                            { name: "Surface", color: AppTheme.colors.surface },
                                            { name: "Primary", color: AppTheme.colors.primary },
                                            { name: "Secondary", color: AppTheme.colors.secondary },
                                            { name: "Accent", color: AppTheme.colors.accent },
                                            { name: "Text", color: AppTheme.colors.text },
                                            { name: "Error", color: AppTheme.colors.error },
                                            { name: "Success", color: AppTheme.colors.success }
                                        ]
                                        
                                        delegate: Column {
                                            spacing: 2
                                            
                                            Rectangle {
                                                width: 60
                                                height: 40
                                                color: modelData.color
                                                border.color: AppTheme.colors.border
                                                radius: AppTheme.radius.small
                                            }
                                            
                                            Label {
                                                text: modelData.name
                                                font.pixelSize: 10
                                                anchors.horizontalCenter: parent.horizontalCenter
                                            }
                                        }
                                    }
                                }
                            }
                            
                            // Quick toggle
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Quick Toggle (Ctrl+Shift+T):"
                                    Layout.fillWidth: true
                                }
                                
                                Button {
                                    text: themeController && themeController.isDarkMode ? "Switch to Light" : "Switch to Dark"
                                    onClicked: {
                                        if (themeController) {
                                            themeController.toggleTheme()
                                            loadCurrentSettings()
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    // Animation Settings
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Animations"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Enable Animations:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: animationsSwitch
                                    checked: true
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                enabled: animationsSwitch.checked
                                
                                Label {
                                    text: "Animation Speed:"
                                    Layout.preferredWidth: 120
                                }
                                
                                Slider {
                                    id: animationSpeedSlider
                                    Layout.fillWidth: true
                                    from: 0.5
                                    to: 2.0
                                    value: 1.0
                                    stepSize: 0.1
                                }
                                
                                Label {
                                    text: animationSpeedSlider.value.toFixed(1) + "x"
                                    Layout.preferredWidth: 40
                                }
                            }
                        }
                    }
                    
                    // Font Settings
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Fonts"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Font Size:"
                                    Layout.preferredWidth: 120
                                }
                                
                                SpinBox {
                                    id: fontSizeSpinBox
                                    from: 10
                                    to: 20
                                    value: 14
                                    suffix: " pt"
                                }
                                
                                Button {
                                    text: "Reset"
                                    onClicked: fontSizeSpinBox.value = 14
                                }
                            }
                        }
                    }
                }
            }
            
            // Behavior Tab
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: AppTheme.spacing.large
                    
                    // General Behavior
                    GroupBox {
                        Layout.fillWidth: true
                        title: "General"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Sound Effects:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: soundSwitch
                                    checked: false
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Confirm Deletions:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: confirmDeleteSwitch
                                    checked: true
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Show Tooltips:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: tooltipsSwitch
                                    checked: true
                                }
                            }
                        }
                    }
                    
                    // Auto-save Settings
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Auto-save"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Enable Auto-save:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: autoSaveSwitch
                                    checked: true
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                enabled: autoSaveSwitch.checked
                                
                                Label {
                                    text: "Auto-save Interval:"
                                    Layout.preferredWidth: 120
                                }
                                
                                SpinBox {
                                    id: autoSaveSpinBox
                                    from: 1
                                    to: 60
                                    value: 5
                                    suffix: " min"
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                enabled: autoSaveSwitch.checked
                                
                                Label {
                                    text: "Create Backups:"
                                    Layout.fillWidth: true
                                }
                                
                                Switch {
                                    id: backupSwitch
                                    checked: true
                                }
                            }
                        }
                    }
                }
            }
            
            // Data Tab
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: AppTheme.spacing.large
                    
                    // Storage Settings
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Storage"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Data Directory:"
                                    Layout.preferredWidth: 120
                                }
                                
                                TextField {
                                    id: dataDirectoryField
                                    Layout.fillWidth: true
                                    readOnly: true
                                    text: StandardPaths.writableLocation(StandardPaths.AppDataLocation)
                                }
                                
                                Button {
                                    text: "Browse"
                                    onClicked: {
                                        folderDialog.open()
                                    }
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Label {
                                    text: "Maximum Backups:"
                                    Layout.preferredWidth: 120
                                }
                                
                                SpinBox {
                                    id: maxBackupsSpinBox
                                    from: 1
                                    to: 100
                                    value: 10
                                }
                            }
                        }
                    }
                    
                    // Import/Export
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Import/Export"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Button {
                                    text: "Export All Characters"
                                    Layout.fillWidth: true
                                    onClicked: exportAllCharacters()
                                }
                                
                                Button {
                                    text: "Import Characters"
                                    Layout.fillWidth: true
                                    onClicked: importCharacters()
                                }
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Button {
                                    text: "Export Settings"
                                    Layout.fillWidth: true
                                    onClicked: exportSettings()
                                }
                                
                                Button {
                                    text: "Import Settings"
                                    Layout.fillWidth: true
                                    onClicked: importSettings()
                                }
                            }
                        }
                    }
                    
                    // Clear Data
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Clear Data"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            Label {
                                text: "⚠️ Warning: These actions cannot be undone!"
                                color: AppTheme.colors.error
                                font.bold: true
                            }
                            
                            RowLayout {
                                Layout.fillWidth: true
                                
                                Button {
                                    text: "Clear Cache"
                                    Layout.fillWidth: true
                                    onClicked: confirmClearCache()
                                }
                                
                                Button {
                                    text: "Reset Settings"
                                    Layout.fillWidth: true
                                    onClicked: confirmResetSettings()
                                }
                                
                                Button {
                                    text: "Delete All Data"
                                    Layout.fillWidth: true
                                    palette.button: AppTheme.colors.error
                                    onClicked: confirmDeleteAllData()
                                }
                            }
                        }
                    }
                }
            }
            
            // Shortcuts Tab
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                ColumnLayout {
                    width: parent.width
                    spacing: AppTheme.spacing.large
                    
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Keyboard Shortcuts"
                        
                        GridLayout {
                            anchors.fill: parent
                            columns: 3
                            rowSpacing: AppTheme.spacing.medium
                            columnSpacing: AppTheme.spacing.large
                            
                            // Headers
                            Label {
                                text: "Action"
                                font.bold: true
                            }
                            Label {
                                text: "Shortcut"
                                font.bold: true
                            }
                            Label {
                                text: "Description"
                                font.bold: true
                            }
                            
                            // Shortcuts list
                            Repeater {
                                model: [
                                    { action: "New Character", shortcut: "Ctrl+N", description: "Create a new character" },
                                    { action: "Save", shortcut: "Ctrl+S", description: "Save current character" },
                                    { action: "Save All", shortcut: "Ctrl+Shift+S", description: "Save all characters" },
                                    { action: "Load", shortcut: "Ctrl+O", description: "Load character file" },
                                    { action: "Delete", shortcut: "Delete", description: "Delete selected item" },
                                    { action: "Overview Tab", shortcut: "Ctrl+1", description: "Switch to Overview tab" },
                                    { action: "Enneagram Tab", shortcut: "Ctrl+2", description: "Switch to Enneagram tab" },
                                    { action: "Stats Tab", shortcut: "Ctrl+3", description: "Switch to Stats tab" },
                                    { action: "Biography Tab", shortcut: "Ctrl+4", description: "Switch to Biography tab" },
                                    { action: "Relations Tab", shortcut: "Ctrl+5", description: "Switch to Relations tab" },
                                    { action: "Timeline Tab", shortcut: "Ctrl+6", description: "Switch to Timeline tab" },
                                    { action: "Toggle Theme", shortcut: "Ctrl+Shift+T", description: "Toggle dark/light theme" },
                                    { action: "Settings", shortcut: "Ctrl+,", description: "Open settings dialog" },
                                    { action: "Search", shortcut: "Ctrl+F", description: "Open search dialog" },
                                    { action: "Quit", shortcut: "Ctrl+Q", description: "Quit application" }
                                ]
                                
                                delegate: RowLayout {
                                    Layout.columnSpan: 3
                                    spacing: parent.columnSpacing
                                    
                                    Label {
                                        text: modelData.action
                                        Layout.preferredWidth: 150
                                    }
                                    
                                    Rectangle {
                                        Layout.preferredWidth: 120
                                        height: 30
                                        color: AppTheme.colors.surface
                                        border.color: AppTheme.colors.border
                                        radius: AppTheme.radius.small
                                        
                                        Label {
                                            anchors.centerIn: parent
                                            text: modelData.shortcut
                                            font.family: "monospace"
                                        }
                                    }
                                    
                                    Label {
                                        text: modelData.description
                                        Layout.fillWidth: true
                                        color: AppTheme.colors.textSecondary
                                    }
                                }
                            }
                        }
                    }
                    
                    GroupBox {
                        Layout.fillWidth: true
                        title: "Custom Shortcuts"
                        
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: AppTheme.spacing.medium
                            
                            Label {
                                text: "Custom shortcuts coming soon..."
                                color: AppTheme.colors.textSecondary
                                font.italic: true
                            }
                        }
                    }
                }
            }
        }
    }
    
    // Helper functions
    function updateThemePreview() {
        // This will be called when theme changes
        // The preview will update automatically through bindings
    }
    
    function openCustomThemeDialog() {
        // TODO: Open custom theme creation dialog
        console.log("Custom theme dialog not yet implemented")
    }
    
    function exportAllCharacters() {
        // TODO: Implement export functionality
        console.log("Export all characters")
    }
    
    function importCharacters() {
        // TODO: Implement import functionality
        console.log("Import characters")
    }
    
    function exportSettings() {
        // TODO: Implement settings export
        console.log("Export settings")
    }
    
    function importSettings() {
        // TODO: Implement settings import
        console.log("Import settings")
    }
    
    function confirmClearCache() {
        // TODO: Show confirmation dialog
        console.log("Clear cache")
    }
    
    function confirmResetSettings() {
        // TODO: Show confirmation dialog
        console.log("Reset settings")
    }
    
    function confirmDeleteAllData() {
        // TODO: Show confirmation dialog
        console.log("Delete all data")
    }
    
    // File dialog for selecting data directory
    FolderDialog {
        id: folderDialog
        title: "Select Data Directory"
        
        onAccepted: {
            dataDirectoryField.text = folder
        }
    }
}