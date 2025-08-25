import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard
    backgroundColor: AppTheme.colors.backgroundVariant

    implicitHeight: controlsContent.implicitHeight + AppTheme.spacing.medium
    padding: AppTheme.padding.small

    property var availableTags: []
    property bool timelineMode: timelineViewBtn.checked

    signal sortModeChangeRequested(string sortMode)
    signal filterEventsByTagRequested(string tag)
    signal exportTimelineRequested()

    contentItem: RowLayout {
        id: controlsContent
        spacing: AppTheme.spacing.medium
        
        Text {
            text: qsTr("View:")
            font.pixelSize: AppTheme.fontSize.tiny
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
                border.width: AppTheme.border.thin
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: AppTheme.fontSize.tiny
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
                border.width: AppTheme.border.thin
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: AppTheme.fontSize.tiny
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
                border.width: AppTheme.border.thin
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: AppTheme.fontSize.tiny
                color: parent.checked ? "#ffffff" : "#007bff"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: {
                iCard.sortModeChangeRequested("chapter")
            }
        }
        
        VerticalSeparator { height: 20 }
        
        Text {
            text: qsTr("Filter:")
            font.pixelSize: AppTheme.fontSize.tiny
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
                font.pixelSize: AppTheme.fontSize.tiny
                color: AppTheme.colors.text
                verticalAlignment: Text.AlignVCenter
                leftPadding: 8
            }
            
            onCurrentTextChanged: iCard.filterEventsByTagRequested(tagFilter.currentText)
        }
        
        Item { Layout.fillWidth: true }
        
        Button {
            text: qsTr("Export Timeline")
            implicitHeight: 28
            
            background: Rectangle {
                color: parent.pressed ? "#e9ecef" : 
                        parent.hovered ? "#f8f9fa" : "transparent"
                border.color: "#6c757d"
                border.width: AppTheme.border.thin
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: AppTheme.fontSize.tiny
                color: "#6c757d"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: exportTimelineRequested()
        }
    }
}