import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: relationshipWidget
    
    // Properties
    property string targetId: model ? model.targetId : ""
    property string targetName: model ? model.targetName : ""
    property string relationshipType: model ? model.type : ""
    property string typeDisplay: model ? model.typeDisplay : ""
    property string description: model ? model.description : ""
    property int strength: model ? model.strength : 5
    property bool isPositive: model ? model.isPositive : true
    property string relationshipColor: model ? model.color : "#9E9E9E"
    property string relationshipIcon: model ? model.icon : "👤"
    
    // Signals
    signal editRequested(string targetId)
    signal deleteRequested(string targetId)
    signal strengthChangeRequested(string targetId, int newStrength)
    
    // Visual properties
    width: parent.width
    height: expanded ? expandedHeight : collapsedHeight
    color: "#ffffff"
    border.color: isPositive ? relationshipColor : "#F44336"
    border.width: 2
    radius: 8
    
    // Animation states
    property bool expanded: false
    property bool hovered: false
    readonly property int collapsedHeight: 80
    readonly property int expandedHeight: 160
    
    Behavior on height {
        NumberAnimation {
            duration: 200
            easing.type: Easing.OutCubic
        }
    }
    
    Behavior on border.color {
        ColorAnimation {
            duration: 150
        }
    }
    
    // Hover effect
    MouseArea {
        id: hoverArea
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: {
            parent.hovered = true
        }
        
        onExited: {
            parent.hovered = false
        }
        
        onClicked: {
            relationshipWidget.expanded = !relationshipWidget.expanded
        }
    }
    
    // Background highlight for hover
    Rectangle {
        anchors.fill: parent
        color: relationshipColor
        opacity: hovered ? 0.05 : 0
        radius: parent.radius
        
        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8
        
        // Header row (always visible)
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            
            // Relationship icon
            Text {
                text: relationshipIcon
                font.pixelSize: 24
                Layout.alignment: Qt.AlignVCenter
            }
            
            // Name and type
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                
                Text {
                    text: targetName
                    font.pixelSize: 16
                    font.bold: true
                    color: "#212121"
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                }
                
                Text {
                    text: typeDisplay
                    font.pixelSize: 12
                    color: relationshipColor
                    font.bold: true
                    Layout.fillWidth: true
                }
            }
            
            // Strength indicator
            Rectangle {
                width: 40
                height: 20
                color: getStrengthColor(strength)
                radius: 10
                
                Text {
                    anchors.centerIn: parent
                    text: strength
                    color: "#ffffff"
                    font.pixelSize: 10
                    font.bold: true
                }
                
                function getStrengthColor(value) {
                    if (value <= 3) return "#F44336"      // Red
                    if (value <= 5) return "#FF9800"      // Orange  
                    if (value <= 7) return "#FFC107"      // Amber
                    return "#4CAF50"                      // Green
                }
            }
            
            // Expand/collapse indicator
            Text {
                text: expanded ? "🔼" : "🔽"
                font.pixelSize: 12
                color: "#757575"
                Layout.alignment: Qt.AlignVCenter
            }
        }
        
        // Expanded content
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: expanded
            spacing: 8
            
            // Description
            ScrollView {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                Layout.minimumHeight: 40
                
                TextArea {
                    id: descriptionArea
                    text: description
                    placeholderText: "Add a description for this relationship..."
                    wrapMode: TextArea.Wrap
                    selectByMouse: true
                    color: "#212121"
                    font.pixelSize: 12
                    
                    background: Rectangle {
                        color: "#f5f5f5"
                        border.color: "#e0e0e0"
                        border.width: 1
                        radius: 4
                    }
                    
                    onEditingFinished: {
                        // TODO: Update description in model
                        console.log("Description updated:", text)
                    }
                }
            }
            
            // Strength slider and actions
            RowLayout {
                Layout.fillWidth: true
                spacing: 12
                
                Text {
                    text: "Strength:"
                    font.pixelSize: 11
                    color: "#757575"
                }
                
                Slider {
                    id: strengthSlider
                    Layout.fillWidth: true
                    from: 1
                    to: 10
                    stepSize: 1
                    value: strength
                    
                    background: Rectangle {
                        x: strengthSlider.leftPadding
                        y: strengthSlider.topPadding + strengthSlider.availableHeight / 2 - height / 2
                        implicitWidth: 200
                        implicitHeight: 4
                        width: strengthSlider.availableWidth
                        height: implicitHeight
                        radius: 2
                        color: "#e0e0e0"
                        
                        Rectangle {
                            width: strengthSlider.visualPosition * parent.width
                            height: parent.height
                            color: relationshipColor
                            radius: 2
                        }
                    }
                    
                    handle: Rectangle {
                        x: strengthSlider.leftPadding + strengthSlider.visualPosition * (strengthSlider.availableWidth - width)
                        y: strengthSlider.topPadding + strengthSlider.availableHeight / 2 - height / 2
                        implicitWidth: 16
                        implicitHeight: 16
                        radius: 8
                        color: strengthSlider.pressed ? "#bdbdbd" : "#f1f1f1"
                        border.color: relationshipColor
                        border.width: 2
                    }
                    
                    onValueChanged: {
                        relationshipWidget.strengthChangeRequested(targetId, Math.round(value))
                    }
                }
                
                Text {
                    text: Math.round(strengthSlider.value)
                    font.pixelSize: 11
                    color: "#757575"
                    Layout.preferredWidth: 20
                }
            }
            
            // Action buttons
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                
                Button {
                    text: "Edit"
                    Layout.fillWidth: true
                    
                    background: Rectangle {
                        color: parent.pressed ? "#1976D2" : 
                               parent.hovered ? "#42A5F5" : "#2196F3"
                        radius: 4
                        border.color: "#1976D2"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#ffffff"
                        font.pixelSize: 11
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        relationshipWidget.editRequested(targetId)
                    }
                }
                
                Button {
                    text: "Remove"
                    Layout.fillWidth: true
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C62828" : 
                               parent.hovered ? "#EF5350" : "#F44336"
                        radius: 4
                        border.color: "#C62828"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#ffffff"
                        font.pixelSize: 11
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        relationshipWidget.deleteRequested(targetId)
                    }
                }
            }
        }
    }
    
    // Visual enhancement when hovered
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        border.color: relationshipColor
        border.width: hovered ? 3 : 0
        radius: parent.radius
        opacity: 0.5
        
        Behavior on border.width {
            NumberAnimation { duration: 150 }
        }
    }
    
    // Drop shadow effect
    Rectangle {
        anchors.fill: parent
        anchors.topMargin: 2
        anchors.leftMargin: 2
        color: "#40000000"
        radius: parent.radius
        z: -1
        opacity: hovered ? 0.3 : 0.1
        
        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
}