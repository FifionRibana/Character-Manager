import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

TabHeaderCard {
    id: iCard

    title: qsTr("Affiliations & Organizations")

    property var affiliations

    signal addAffiliationRequested

    buttons: Button {
        text: qsTr("Add Affiliation")
        font.family: AppTheme.fontFamily
        font.pixelSize: AppTheme.fontSize.medium
        onClicked: iCard.addAffiliationRequested()
        
        background: Rectangle {
            color: parent.pressed ? "#388E3C" : 
                    parent.hovered ? "#45A049" : "#4CAF50"
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
        
    }

    // Affiliations list
    content: ColumnLayout {
        spacing: AppTheme.spacing.small
        
        ColumnLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.small
            
            Repeater {
                model: iCard.affiliations
                
                delegate: Rectangle {
                    Layout.fillWidth: true
                    implicitHeight: affiliationRow.implicitHeight + AppTheme.spacing.medium
                    color: AppTheme.colors.backgroundVariant
                    border.color: AppTheme.colors.borderLight
                    border.width: AppTheme.border.thin
                    radius: AppTheme.radius.small
                    
                    RowLayout {
                        id: affiliationRow
                        anchors.fill: parent
                        anchors.margins: AppTheme.spacing.small
                        spacing: AppTheme.spacing.medium
                        
                        // Organization icon
                        Rectangle {
                            width: 40
                            height: 40
                            radius: 20
                            color: AppTheme.colors.accent
                            
                            Text {
                                anchors.centerIn: parent
                                text: AppTheme.getAffiliationIcon(modelData || "")
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                color: "white"
                            }
                        }
                        
                        // Affiliation name
                        Text {
                            text: modelData
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.text
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                        
                        // Remove button
                        Button {
                            text: "×"
                            implicitWidth: 32
                            implicitHeight: 32
                            
                            background: Rectangle {
                                radius: 16
                                color: parent.hovered ? "#e74c3c" : "transparent"
                                border.color: "#e74c3c"
                                border.width: 1
                                
                                Behavior on color {
                                    ColorAnimation { duration: 150 }
                                }
                            }
                            
                            contentItem: Text {
                                text: parent.text
                                font.family: AppTheme.fontFamily
                                font.pixelSize: 16
                                font.bold: true
                                color: parent.hovered ? "white" : "#e74c3c"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                            
                            onClicked: removeAffiliation(modelData)
                            
                            ToolTip {
                                text: qsTr("Remove ") + (modelData || "")
                                visible: parent.hovered
                                delay: 500
                            }
                        }
                    }
                }
            }
            
            // Empty state
            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 100
                visible: !iCard.affiliations || iCard.affiliations.length === 0
                color: "transparent"
                border.color: AppTheme.colors.borderLight
                border.width: AppTheme.border.medium
                radius: AppTheme.radius.medium
                
                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: AppTheme.spacing.small
                    
                    Text {
                        text: "🏛️"
                        font.pixelSize: 32
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: qsTr("No affiliations yet")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.medium
                        color: AppTheme.colors.textSecondary
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: qsTr("Add organizations, guilds, or groups your character belongs to")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.small
                        color: AppTheme.colors.textSecondary
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
        }
        
        // Affiliation examples
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.colors.backgroundVariant
            border.color: AppTheme.colors.borderLight
            border.width: 1
            radius: 6
            
            implicitHeight: examplesContent.implicitHeight + AppTheme.spacing.medium
            
            RowLayout {
                id: examplesContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.small
                spacing: AppTheme.spacing.small
                
                Text {
                    text: "💡"
                    font.pixelSize: AppTheme.fontSize.medium
                }
                
                Text {
                    text: qsTr("Examples: Royal Guard, Thieves' Guild, Mages' College, Noble House Stark, Rangers of the North, Church of Light")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
            }
        }
    }
}