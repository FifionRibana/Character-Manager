import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    implicitHeight: headerContent.implicitHeight + AppTheme.spacing.huge

    property int eventCount: 0
    property int majorEventCount: 0
    property int uniqueEventCount: 0

    signal addEventRequested

    contentItem: ColumnLayout {
        id: headerContent
        anchors.fill: parent
        anchors.margins: 16
        spacing: 16
        
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: "Character Timeline"
                font.pixelSize: 20
                font.bold: true
                color: "#212121"
                Layout.fillWidth: true
            }
            
            Button {
                text: "Add Event"
                onClicked: iCard.addEventRequested()
                
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
            text: "Chronicle important events, milestones, and story moments in your character's life."
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
                    text: iCard.eventCount
                    font.pixelSize: 24
                    font.bold: true
                    color: "#FF9800"
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Text {
                    text: "Total Events"
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
                    text: iCard.majorEventCount
                    font.pixelSize: 24
                    font.bold: true
                    color: "#3F51B5"
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Text {
                    text: "Major Events"
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
                    text: iCard.uniqueEventCount
                    font.pixelSize: 24
                    font.bold: true
                    color: "#9C27B0"
                    Layout.alignment: Qt.AlignHCenter
                }
                
                Text {
                    text: "Tags Used"
                    font.pixelSize: 10
                    color: "#757575"
                    Layout.alignment: Qt.AlignHCenter
                }
            }
            
            Item { Layout.fillWidth: true }
        }
    }
}