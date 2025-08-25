import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Ability Scores")

    property int totalPoints
    property color totalPointsColor
    property int averageScore
    property int pointBuyCost
    property int totalModifiers

    signal reset
    signal rollStatsRequested

    buttons: RowLayout {
        spacing: AppTheme.spacing.small
        
        Button {
            text: qsTr("4d6 Roll")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.small
            onClicked: rollStatsRequested()
            
            background: Rectangle {
                color: parent.hovered ? Qt.lighter("#2ecc71", 1.1) : "#2ecc71"
                radius: AppTheme.radius.small
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            contentItem: Text {
            text: parent.text
            font: parent.font
            color: "#ffffff"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            }
            
            // ToolTip {
            //     text: qsTr("Roll 4d6 drop lowest for each stat")
            //     visible: parent.hovered
            //     delay: 500
            // }
        }
        
        Button {
            text: qsTr("Reset to 10")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.small
            onClicked: reset()
            
            background: Rectangle {
                color: parent.hovered ? Qt.lighter("#95a5a6", 1.1) : "#95a5a6"
                radius: AppTheme.radius.small
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            contentItem: Text {
                text: parent.text
                font: parent.font
                color: "#ffffff"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            // ToolTip {
            //     text: qsTr("Reset all stats to 10 (standard baseline)")
            //     visible: parent.hovered
            //     delay: 500
            // }
        }
    }
        
    // Stats summary
    content: RowLayout {
        id: summaryContent
        Layout.fillWidth: true
        spacing: AppTheme.spacing.large
        
        // Total points
        StatisticsIndicator {
            Layout.preferredWidth: 72
            color: iCard.totalPointsColor
            label: qsTr("Total Points")
            value: iCard.totalPoints
        }

        VerticalSeparator { height: 40 }
        
        // Average stat
        StatisticsIndicator {
            Layout.preferredWidth: 72
            color: AppTheme.colors.text
            label: qsTr("Average")
            value: iCard.averageScore
        }
        
        VerticalSeparator { height: 40 }
        
        // Point buy cost (if applicable)
        StatisticsIndicator {
            Layout.preferredWidth: 72
            color: iCard.pointBuyCost <= 27 ? "#2ecc71" : "#e74c3c"
            label: qsTr("Point Buy Cost")
            value: iCard.pointBuyCost.toString() + "/27"
        }
        
        Item { Layout.fillWidth: true }
        
        // Modifier bonus indicator
        StatisticsIndicator {
            Layout.preferredWidth: 72
            color: iCard.totalModifiers >= 0 ? "#2ecc71" : "#e74c3c"
            label: qsTr("Modifier Bonus")
            value: iCard.totalModifiers >= 0 ? "+" + iCard.totalModifiers : iCard.totalModifiers.toString()
        }
    }
}