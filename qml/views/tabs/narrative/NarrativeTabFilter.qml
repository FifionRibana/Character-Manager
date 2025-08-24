import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    implicitHeight: controlsContent.implicitHeight + AppTheme.spacing.huge

    property var availableTags: []
    property bool timelineMode: timelineViewBtn.checked

    signal sortModeChangeRequested(string sortMode)
    signal filterEventsByTagRequested(string tag)
    signal exportTimelineRequested()

    contentItem: RowLayout {
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
                iCard.sortModeChangeRequested("timeline")
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
                iCard.sortModeChangeRequested("importance")
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
                iCard.sortModeChangeRequested("chapter")
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
            model: availableTags
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
                iCard.filterEventsByTagRequested(tagFilter.currentText)
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
                exportTimelineRequested()
            }
        }
    }
}