import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    implicitHeight: headerContent.implicitHeight + AppTheme.spacing.huge

    property alias relationshipCount: iRelationshipIndicator.value
    property alias positiveRelationshipCount: iPositiveIndicator.value
    property alias negativeRelationshipCount: iNegativeIndicator.value

    signal addRelationshipRequested

    contentItem: ColumnLayout {
        id: headerContent
        anchors.fill: parent
        anchors.margins: AppTheme.margin.medium
        spacing: AppTheme.spacing.small
        
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: qsTr("Character Relationships")
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                Layout.fillWidth: true
            }
            
            Button {
                text: qsTr("Add Relationship")
                onClicked: iCard.addRelationshipRequested()
                
                background: Rectangle {
                    color: parent.pressed ? "#388E3C" : 
                            parent.hovered ? "#45A049" : "#4CAF50"
                    radius: AppTheme.radius.small
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "#ffffff"
                    font.pixelSize: AppTheme.fontSize.small
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: AppTheme.border.thin
            color: AppTheme.card.border
        }
        
        Text {
            text: "Manage connections between characters. Each relationship includes type, description, and strength."
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
                id: iRelationshipIndicator
                Layout.preferredWidth: 72
                color: AppTheme.colors.success
                label: qsTr("Total Relations")
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iPositiveIndicator
                Layout.preferredWidth: 72
                color: "#2196F3"
                label: qsTr("Positive")
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iNegativeIndicator
                Layout.preferredWidth: 72
                color: "#F44336"
                label: qsTr("Negative")
            }
            
            Item { Layout.fillWidth: true }
        }
    }
}