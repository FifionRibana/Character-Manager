import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../../components"

Card {
    id: iCard
    Layout.fillWidth: true

    Layout.leftMargin: AppTheme.margin.small
    Layout.rightMargin: AppTheme.margin.small
    Layout.topMargin: AppTheme.margin.small

    implicitHeight: headerContent.implicitHeight + AppTheme.spacing.huge

    property int totalPoints
    property color totalPointsColor
    property int averageScore
    property int pointBuyCost
    property int totalModifiers

    signal reset()
    signal rollStatsRequested()

    contentItem: ColumnLayout {
        id: headerContent
        spacing: AppTheme.spacing.medium
        anchors.fill: parent
        anchors.margins: AppTheme.margin.medium

        RowLayout {
            Layout.fillWidth: true
                    
            Text {
                text: qsTr("Ability Scores")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                Layout.fillWidth: true
            }
        

            Item { Layout.fillWidth: true }
            
            // Quick action buttons
            RowLayout {
                spacing: AppTheme.spacing.medium
                
                Button {
                    text: qsTr("4d6 Roll")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    
                    background: Rectangle {
                        color: parent.hovered ? Qt.lighter("#2ecc71", 1.1) : "#2ecc71"
                        radius: 6
                        
                        Behavior on color {
                            ColorAnimation { duration: 150 }
                        }
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: rollStatsRequested()
                    
                    ToolTip {
                        text: qsTr("Roll 4d6 drop lowest for each stat")
                        visible: parent.hovered
                        delay: 500
                    }
                }
                
                Button {
                    text: qsTr("Reset to 10")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    
                    background: Rectangle {
                        color: parent.hovered ? Qt.lighter("#95a5a6", 1.1) : "#95a5a6"
                        radius: 6
                        
                        Behavior on color {
                            ColorAnimation { duration: 150 }
                        }
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: reset()
                    
                    ToolTip {
                        text: qsTr("Reset all stats to 10 (standard baseline)")
                        visible: parent.hovered
                        delay: 500
                    }
                }
            }
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: AppTheme.border.thin
            color: AppTheme.card.border
        }
        
        // Stats summary
        RowLayout {
            id: summaryContent
            Layout.fillWidth: true
            spacing: AppTheme.spacing.large
            
            // Total points
            ColumnLayout {
                spacing: AppTheme.spacing.small
                
                Text {
                    text: qsTr("Total Points")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                }
                
                Text {
                    text: totalPoints.toString()
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    font.bold: true
                    color: totalPointsColor
                }
            }
            
            Rectangle {
                width: AppTheme.border.thin
                Layout.fillHeight: true
                color: AppTheme.colors.border
            }
            
            // Average stat
            ColumnLayout {
                spacing: AppTheme.spacing.small
                
                Text {
                    text: qsTr("Average")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                }
                
                Text {
                    text: averageScore.toFixed(1)
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    font.bold: true
                    color: AppTheme.colors.text
                }
            }
            
            Rectangle {
                width: AppTheme.border.thin
                Layout.fillHeight: true
                color: AppTheme.colors.border
            }
            
            // Point buy cost (if applicable)
            ColumnLayout {
                spacing: AppTheme.spacing.small
                
                Text {
                    text: qsTr("Point Buy Cost")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                }
                
                Text {
                    text: pointBuyCost.toString() + "/27"
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    font.bold: true
                    color: pointBuyCost <= 27 ? "#2ecc71" : "#e74c3c"
                }
            }
            
            Item { Layout.fillWidth: true }
            
            // Modifier bonus indicator
            ColumnLayout {
                spacing: AppTheme.spacing.small
                
                Text {
                    text: qsTr("Modifier Bonus")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                }
                
                Text {
                    text: totalModifiers >= 0 ? "+" + totalModifiers : totalModifiers.toString()
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    font.bold: true
                    color: totalModifiers >= 0 ? "#2ecc71" : "#e74c3c"
                }
            }
        }
    }
}