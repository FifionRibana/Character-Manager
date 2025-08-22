
import QtQuick 6.2
import QtQuick.Window 6.2
import QtQuick.Controls 6.2
import App.Styles 1.0

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Test Window"
    
    Component.onCompleted: {
        console.log("=== QML Test Loading ===")
        console.log("compactMode:", typeof compactMode !== 'undefined' ? compactMode : "UNDEFINED")
        console.log("debugMode:", typeof debugMode !== 'undefined' ? debugMode : "UNDEFINED")
        console.log("themeController:", typeof themeController !== 'undefined' ? themeController : "UNDEFINED")
        console.log("AppTheme:", typeof AppTheme !== 'undefined' ? AppTheme : "UNDEFINED")
        
        if (typeof AppTheme !== 'undefined') {
            console.log("AppTheme.colors:", typeof AppTheme.colors !== 'undefined' ? "EXISTS" : "UNDEFINED")
        }
        
        // Test creating an Action with checked property
        var testAction = Qt.createQmlObject('import QtQuick.Controls 6.2; Action { checkable: true; checked: false }', this)
        console.log("Action with checked property:", testAction ? "SUCCESS" : "FAILED")
    }
    
    // Test Action with checked binding
    Action {
        id: testAction
        text: "Test"
        checkable: true
        checked: false  // Direct value
    }
    
    // Test with property binding
    property bool testMode: false
    
    Action {
        id: testAction2
        text: "Test 2"
        checkable: true
        checked: testMode  // Property binding
    }
    
    Text {
        anchors.centerIn: parent
        text: "Check console output for diagnostic information"
        font.pixelSize: 20
    }
}
