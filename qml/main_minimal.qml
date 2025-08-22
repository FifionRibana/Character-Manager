import QtQuick 6.2
import QtQuick.Window 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.2
import MedievalModels 1.0
import MedievalControllers 1.0

// Test with different import styles for AppTheme
// Option 1: Relative import
import "./styles"
// Option 2: Module import (if singleton is registered)
// import App.Styles 1.0

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 1024
    height: 600
    title: "Test - Compact Mode Issue"
    
    // Test if properties from context are accessible
    Component.onCompleted: {
        console.log("=== Context Properties Test ===")
        console.log("compactMode exists:", typeof compactMode !== 'undefined')
        console.log("compactMode value:", typeof compactMode !== 'undefined' ? compactMode : "UNDEFINED")
        console.log("debugMode exists:", typeof debugMode !== 'undefined')
        console.log("themeController exists:", typeof themeController !== 'undefined')
        console.log("AppTheme exists:", typeof AppTheme !== 'undefined')
        
        // Test if AppTheme properties are accessible
        if (typeof AppTheme !== 'undefined') {
            console.log("AppTheme.colors exists:", typeof AppTheme.colors !== 'undefined')
            console.log("AppTheme.spacing exists:", typeof AppTheme.spacing !== 'undefined')
        }
    }
    
    // Create a property to test with
    property bool testCompactMode: false
    
    menuBar: MenuBar {
        Menu {
            title: "&Test Menu"
            
            // Test 1: Direct boolean value - Should always work
            Action {
                text: "Test 1 - Direct Value"
                checkable: true
                checked: false
                onTriggered: console.log("Test 1 triggered")
            }
            
            // Test 2: Local property binding - Should work
            Action {
                text: "Test 2 - Local Property"
                checkable: true
                checked: mainWindow.testCompactMode
                onTriggered: {
                    console.log("Test 2 triggered")
                    mainWindow.testCompactMode = !mainWindow.testCompactMode
                }
            }
            
            // Test 3: Context property with ternary - Safe approach
            Action {
                text: "Test 3 - Safe Context Property"
                checkable: true
                checked: typeof compactMode !== 'undefined' ? compactMode : false
                onTriggered: console.log("Test 3 triggered")
            }
            
            // Test 4: Direct context property - This is where the error occurs
            Action {
                text: "Test 4 - Direct Context Property"
                checkable: true
                // Comment/uncomment this line to test the error
                // checked: compactMode
                checked: false  // Use safe default for now
                onTriggered: console.log("Test 4 triggered")
            }
        }
    }
    
    // Main content to show diagnostic info
    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        
        Text {
            text: "Diagnostic Information"
            font.pixelSize: 24
            font.bold: true
        }
        
        // Show context property status
        GridLayout {
            columns: 2
            columnSpacing: 20
            rowSpacing: 10
            
            Text { text: "compactMode:" }
            Text { 
                text: typeof compactMode !== 'undefined' ? String(compactMode) : "UNDEFINED"
                color: typeof compactMode !== 'undefined' ? "green" : "red"
            }
            
            Text { text: "debugMode:" }
            Text { 
                text: typeof debugMode !== 'undefined' ? String(debugMode) : "UNDEFINED"
                color: typeof debugMode !== 'undefined' ? "green" : "red"
            }
            
            Text { text: "themeController:" }
            Text { 
                text: typeof themeController !== 'undefined' ? "EXISTS" : "UNDEFINED"
                color: typeof themeController !== 'undefined' ? "green" : "red"
            }
            
            Text { text: "AppTheme:" }
            Text { 
                text: typeof AppTheme !== 'undefined' ? "EXISTS" : "UNDEFINED"
                color: typeof AppTheme !== 'undefined' ? "green" : "red"
            }
            
            Text { text: "testCompactMode:" }
            Text { 
                text: String(testCompactMode)
                color: "green"
            }
        }
        
        // Test buttons
        RowLayout {
            spacing: 10
            
            Button {
                text: "Toggle Test Mode"
                onClicked: {
                    mainWindow.testCompactMode = !mainWindow.testCompactMode
                    console.log("testCompactMode is now:", mainWindow.testCompactMode)
                }
            }
            
            Button {
                text: "Check Context Properties"
                onClicked: {
                    console.log("\n=== Checking Context Properties ===")
                    console.log("compactMode:", typeof compactMode !== 'undefined' ? compactMode : "UNDEFINED")
                    console.log("debugMode:", typeof debugMode !== 'undefined' ? debugMode : "UNDEFINED")
                    console.log("themeController:", typeof themeController !== 'undefined' ? "EXISTS" : "UNDEFINED")
                }
            }
        }
    }
}