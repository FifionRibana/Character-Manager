import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Character Timeline")

    property int eventCount: 0
    property int majorEventCount: 0
    property int uniqueEventCount: 0

    signal addEventRequested

    buttons: RowLayout {
        spacing: AppTheme.spacing.small
        Button {
            text: qsTr("Add Event")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.small
            onClicked: iCard.addEventRequested()
            
            background: Rectangle {
                color: parent.pressed ? "#388E3C" : 
                        parent.hovered ? "#45A049" : "#4CAF50"
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.text
                font: parent.font
                color: "#ffffff"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
        
    content: ColumnLayout {
        spacing: AppTheme.spacing.small
        
        Text {
            text: qsTr("Chronicle important events, milestones, and story moments in your character's life.")
            font.pixelSize: AppTheme.fontSize.small
            color: AppTheme.colors.textSecondary
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
        
        // Statistics row
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.large
            
            StatisticsIndicator {
                id: iEventsIndicator
                Layout.preferredWidth: 72
                color: "#FF9800"
                label: qsTr("Total Events")
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iMajorIndicator
                Layout.preferredWidth: 72
                color: "#3F51B5"
                label: qsTr("Major Events")
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iTagIndicator
                Layout.preferredWidth: 72
                color: "#9C27B0"
                label: qsTr("Tags Used")
            }
            
            Item { Layout.fillWidth: true }
        }
    }
}