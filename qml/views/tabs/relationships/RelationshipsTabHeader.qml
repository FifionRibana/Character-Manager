import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Character Relationships")

    property int relationshipCount: 0
    property int positiveRelationshipCount: 0
    property int negativeRelationshipCount: 0

    signal addRelationshipRequested
    signal filterRelationshipsRequested

    buttons: Button {
        text: qsTr("Add Relationship")
        font.family: AppTheme.fontFamily
        font.pixelSize: AppTheme.fontSize.small
        onClicked: iCard.addRelationshipRequested()
        
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

    content: ColumnLayout {
        spacing: AppTheme.spacing.small
        
        Text {
            text: qsTr("Manage connections between characters. Each relationship includes type, description, and strength.")
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
                value: iCard.relationshipCount
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iPositiveIndicator
                Layout.preferredWidth: 72
                color: "#2196F3"
                label: qsTr("Positive")
                value: iCard.positiveRelationshipCount
            }

            VerticalSeparator { height: 40 }

            StatisticsIndicator {
                id: iNegativeIndicator
                Layout.preferredWidth: 72
                color: "#F44336"
                label: qsTr("Negative")
                value: iCard.negativeRelationshipCount
            }
            
            Item { Layout.fillWidth: true }
        }
    }
}