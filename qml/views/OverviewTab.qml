import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "../styles"

ScrollView {
    id: overviewTab
    
    property var characterModel
    property bool editMode: false
    
    signal editModeRequested()
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: overviewTab.availableWidth
        spacing: AppTheme.spacingLarge
        
        // Edit mode button
        Button {
            text: qsTr("Enter Edit Mode")
            Layout.alignment: Qt.AlignRight
            visible: !editMode && characterModel && characterModel.hasCharacter
            
            background: Rectangle {
                color: parent.pressed ? AppTheme.button.pressed :
                       parent.hovered ? AppTheme.button.hovered :
                       AppTheme.button.normal
                radius: AppTheme.borderRadius
            }
            
            contentItem: Text {
                text: parent.text
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeBody
                color: AppTheme.textColorLight
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: overviewTab.editModeRequested()
        }
        
        // Character header card
        Rectangle {
            Layout.fillWidth: true
            
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: AppTheme.borderWidth
            radius: AppTheme.card.radius
            
            implicitHeight: headerContent.implicitHeight + 2 * AppTheme.spacingLarge
            
            ColumnLayout {
                id: headerContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacingLarge
                spacing: AppTheme.spacingMedium
                
                // Title
                Text {
                    text: qsTr("Character")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeHeading
                    font.bold: true
                    color: AppTheme.textColor
                }
                
                // Separator
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.borderColor
                }
                
                // Content
                RowLayout {
                    spacing: AppTheme.spacingLarge
                    
                    // Portrait
                    Rectangle {
                        width: 120
                        height: 120
                        radius: AppTheme.borderRadiusLarge
                        color: AppTheme.surfaceColorDark
                        border.color: AppTheme.borderColor
                        border.width: 1
                        
                        Layout.alignment: Qt.AlignTop
                        
                        Text {
                            anchors.centerIn: parent
                            text: qsTr("No Image")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                        }
                    }
                    
                    // Character info
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        spacing: AppTheme.spacing
                        
                        Text {
                            text: characterModel ? characterModel.name : ""
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeDisplay
                            font.bold: true
                            color: AppTheme.textColor
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        
                        Text {
                            text: qsTr("Level") + " " + (characterModel ? characterModel.level : 1)
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeHeading
                            color: AppTheme.textColorSecondary
                        }
                    }
                }
            }
        }
        
        // Stats overview card
        Rectangle {
            Layout.fillWidth: true
            
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: AppTheme.borderWidth
            radius: AppTheme.card.radius
            
            implicitHeight: statsContent.implicitHeight + 2 * AppTheme.spacingLarge
            
            ColumnLayout {
                id: statsContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacingLarge
                spacing: AppTheme.spacingMedium
                
                // Title
                Text {
                    text: qsTr("Ability Scores")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeHeading
                    font.bold: true
                    color: AppTheme.textColor
                }
                
                // Separator
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.borderColor
                }
                
                // Stats grid
                GridLayout {
                    columns: 3
                    columnSpacing: AppTheme.spacingLarge
                    rowSpacing: AppTheme.spacingMedium
                    
                    // Strength
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Strength")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.strength : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.strength.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.strength : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.strength : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    // Agility
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Agility")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.agility : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.agility.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.agility : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.agility : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    // Constitution
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Constitution")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.constitution : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.constitution.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.constitution : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.constitution : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    // Intelligence
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Intelligence")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.intelligence : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.intelligence.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.intelligence : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.intelligence : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    // Wisdom
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Wisdom")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.wisdom : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.wisdom.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.wisdom : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.wisdom : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                    
                    // Charisma
                    ColumnLayout {
                        spacing: AppTheme.spacingSmall
                        
                        Text {
                            text: qsTr("Charisma")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: AppTheme.textColorSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.charisma : 10)
                            Layout.alignment: Qt.AlignHCenter
                            
                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.charisma.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSizeHeading
                                font.bold: true
                                color: AppTheme.textColorLight
                            }
                        }
                        
                        Text {
                            text: {
                                let value = characterModel ? characterModel.charisma : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return modifier >= 0 ? "+" + modifier : modifier.toString()
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSizeBody
                            color: {
                                let value = characterModel ? characterModel.charisma : 10
                                let modifier = Math.floor((value - 10) / 2)
                                return AppTheme.getStatModifierColor(modifier)
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
}