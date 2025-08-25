import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard

    property var relationshipModel

    signal relationshipEditRequested(int relationshipId)
    signal relationshipDeleteRequested(int relationshipId)
    signal relationshipStrengthChangeRequested(int relationshipId, int newStrength)

    contentItem: ScrollView {
        anchors.fill: parent
        anchors.margins: AppTheme.margin.medium
        anchors.leftMargin: 48  // Space for timeline line
        contentWidth: availableWidth
        
        ListView {
            id: relationshipsList
            width: parent.width
            
            model: relationshipModel
            spacing: AppTheme.spacing.medium
            clip: true
            
            delegate: RelationshipWidget {
                width: relationshipsList.width
                
                onEditRequested: function(relationshipId) {
                    iCard.relationshipEditRequested(relationshipId)
                }
                
                onDeleteRequested: function(relationshipId) {
                    iCard.relationshipDeleteRequested(relationshipId)
                }
                
                onStrengthChangeRequested: function(relationshipId, newStrength) {
                    iCard.relationshipStrengthChangeRequested(relationshipId, newStrength)
                }
            }
            
            // Empty state
            Rectangle {
                anchors.centerIn: parent
                width: 200
                height: 120
                color: "transparent"
                visible: relationshipsList.count === 0
                
                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 8
                    
                    Text {
                        text: "🤝"
                        font.pixelSize: 48
                        color: "#e0e0e0"
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "No relationships yet.\nClick 'Add Relationship' to start building your character's social network."
                        font.pixelSize: 12
                        color: "#757575"
                        horizontalAlignment: Text.AlignHCenter
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
        }
    }
}