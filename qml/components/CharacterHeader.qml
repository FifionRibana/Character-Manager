import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: characterHeader
    
    property var characterModel
    
    height: 80
    color: AppTheme.surfaceColor
    border.color: AppTheme.borderColor
    border.width: 1
    radius: AppTheme.borderRadius
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: AppTheme.spacingMedium
        spacing: AppTheme.spacingLarge
        
        // Character image placeholder
        Rectangle {
            width: 60
            height: 60
            radius: AppTheme.borderRadiusLarge
            color: AppTheme.surfaceColorDark
            border.color: AppTheme.borderColor
            border.width: 1
            
            Image {
                anchors.fill: parent
                anchors.margins: 2
                source: characterModel && characterModel.imageUrl ? characterModel.imageUrl : ""
                fillMode: Image.PreserveAspectCrop
                visible: characterModel && characterModel.imageUrl.toString() !== ""
            }
            
            Text {
                anchors.centerIn: parent
                text: "📷"
                font.pixelSize: 24
                visible: !characterModel || characterModel.imageUrl.toString() === ""
            }
        }
        
        // Character basic info
        ColumnLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacingSmall
            
            TextField {
                id: nameField
                text: characterModel ? characterModel.name : ""
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeHeading
                font.bold: true
                placeholderText: qsTr("Character Name")
                Layout.fillWidth: true
                
                background: Rectangle {
                    color: parent.activeFocus ? AppTheme.input.backgroundFocused : AppTheme.input.background
                    border.color: parent.activeFocus ? AppTheme.input.borderFocused : AppTheme.input.border
                    border.width: AppTheme.borderWidth
                    radius: AppTheme.borderRadius
                }
                
                onTextChanged: {
                    if (characterModel && characterModel.name !== text) {
                        characterModel.name = text
                    }
                }
            }
            
            RowLayout {
                Text {
                    text: qsTr("Level:")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeBody
                    color: AppTheme.textColorSecondary
                }
                
                SpinBox {
                    id: levelSpinBox
                    from: 1
                    to: 100
                    value: characterModel ? characterModel.level : 1
                    
                    onValueChanged: {
                        if (characterModel && characterModel.level !== value) {
                            characterModel.level = value
                        }
                    }
                }
                
                Item { Layout.fillWidth: true }
            }
        }
    }
}