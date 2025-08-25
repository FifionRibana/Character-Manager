import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

Card {
    id: iCard
    backgroundColor: AppTheme.colors.backgroundVariant

    implicitHeight: filterContent.implicitHeight + AppTheme.spacing.medium
    padding: AppTheme.padding.small

    property alias relationshipTypes: relationshipTypeFilter.model
    


    signal filterRelationshipsRequested()

    contentItem: RowLayout {
        id: filterContent
        spacing: AppTheme.spacing.medium
        
        Text {
            text: qsTr("Filter by:")
            font.pixelSize: AppTheme.fontSize.tiny
            color: "#495057"
        }
        
        ComboBox {
            id: relationshipTypeFilter
            textRole: "display"
            valueRole: "value"
            currentIndex: 0
            
            Layout.preferredWidth: 120
            
            background: Rectangle {
                color: "#ffffff"
                border.color: "#ced4da"
                border.width: AppTheme.border.thin
                radius: AppTheme.radius.small
            }
            
            contentItem: Text {
                text: parent.displayText
                font.pixelSize: AppTheme.fontSize.tiny
                color: AppTheme.colors.text
                verticalAlignment: Text.AlignVCenter
                leftPadding: 8
            }
            
            onCurrentValueChanged: iCard.filterRelationshipsRequested()
        }
        
        Text {
            text: qsTr("Search:")
            font.pixelSize: AppTheme.fontSize.tiny
            color: "#495057"
        }
        
        TextField {
            id: searchField
            placeholderText: qsTr("Character name...")
            Layout.preferredWidth: 150
            
            background: Rectangle {
                color: "#ffffff"
                border.color: "#ced4da"
                border.width: 1
                radius: 4
            }
            
            onTextChanged: iCard.filterRelationshipsRequested()
        }
        
        Item { Layout.fillWidth: true }
        
        Button {
            text: qsTr("Clear Filters")
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
            
            onClicked: {
                relationshipTypeFilter.currentIndex = 0
                searchField.text = ""
            }
        }
    }
}