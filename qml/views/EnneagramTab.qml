import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: enneagramTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: enneagramTab.availableWidth
        spacing: 24
        
        // Main Type Selection
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: mainTypeContent.implicitHeight + 32
            
            ColumnLayout {
                id: mainTypeContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Text {
                    text: "Enneagram Type"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                // Type selector grid
                GridLayout {
                    Layout.fillWidth: true
                    columns: 3
                    columnSpacing: 12
                    rowSpacing: 12
                    
                    Repeater {
                        model: [
                            {type: 1, name: "The Reformer", color: "#E3F2FD", desc: "Principled, purposeful, self-controlled, and perfectionistic."},
                            {type: 2, name: "The Helper", color: "#F3E5F5", desc: "Generous, demonstrative, people-pleasing, and possessive."},
                            {type: 3, name: "The Achiever", color: "#E8F5E8", desc: "Adaptable, excelling, driven, and image-conscious."},
                            {type: 4, name: "The Individualist", color: "#FFF3E0", desc: "Expressive, dramatic, self-absorbed, and temperamental."},
                            {type: 5, name: "The Investigator", color: "#E0F2F1", desc: "Perceptive, innovative, secretive, and isolated."},
                            {type: 6, name: "The Loyalist", color: "#FCE4EC", desc: "Engaging, responsible, anxious, and suspicious."},
                            {type: 7, name: "The Enthusiast", color: "#FFFDE7", desc: "Spontaneous, versatile, acquisitive, and scattered."},
                            {type: 8, name: "The Challenger", color: "#FFEBEE", desc: "Self-confident, decisive, willful, and confrontational."},
                            {type: 9, name: "The Peacemaker", color: "#F1F8E9", desc: "Receptive, reassuring, complacent, and resigned."}
                        ]
                        
                        delegate: Rectangle {
                            width: 120
                            height: 100
                            radius: 8
                            color: modelData.color
                            border.color: currentType === modelData.type ? "#4CAF50" : "#e0e0e0"
                            border.width: currentType === modelData.type ? 3 : 1
                            
                            property int currentType: characterModel ? characterModel.enneagramType : 9
                            
                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 8
                                spacing: 4
                                
                                Text {
                                    text: modelData.type.toString()
                                    font.pixelSize: 24
                                    font.bold: true
                                    color: "#212121"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                
                                Text {
                                    text: modelData.name
                                    font.pixelSize: 10
                                    font.bold: true
                                    color: "#212121"
                                    horizontalAlignment: Text.AlignHCenter
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                            
                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    if (characterModel) {
                                        // Update character model enneagram type
                                        console.log("Selected type:", modelData.type)
                                        // TODO: Update characterModel.enneagramType = modelData.type
                                    }
                                    typeDescription.text = modelData.desc
                                }
                            }
                        }
                    }
                }
                
                // Type description
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 60
                    color: "#f5f5f5"
                    border.color: "#e0e0e0"
                    border.width: 1
                    radius: 4
                    
                    Text {
                        id: typeDescription
                        anchors.fill: parent
                        anchors.margins: 12
                        text: "Receptive, reassuring, complacent, and resigned." // Default Type 9
                        font.pixelSize: 12
                        color: "#212121"
                        wrapMode: Text.WordWrap
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
        
        // Wing and Development
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: wingDevContent.implicitHeight + 32
            
            ColumnLayout {
                id: wingDevContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Text {
                    text: "Wing & Development"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 24
                    rowSpacing: 16
                    
                    // Wing selection
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        
                        Text {
                            text: "Wing"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#212121"
                        }
                        
                        ComboBox {
                            id: wingCombo
                            Layout.fillWidth: true
                            
                            model: [
                                {text: "No Wing", value: 0},
                                {text: "Wing 8", value: 8},
                                {text: "Wing 1", value: 1}
                            ]
                            
                            textRole: "text"
                            valueRole: "value"
                            
                            background: Rectangle {
                                color: "#ffffff"
                                border.color: "#e0e0e0"
                                border.width: 1
                                radius: 4
                            }
                            
                            onCurrentValueChanged: {
                                // TODO: Update character model wing
                                console.log("Wing selected:", currentValue)
                            }
                        }
                        
                        Text {
                            text: getWingNotation()
                            font.pixelSize: 14
                            font.bold: true
                            color: "#4CAF50"
                            visible: wingCombo.currentValue > 0
                        }
                    }
                    
                    // Development level
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        
                        Text {
                            text: "Development Level"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#212121"
                        }
                        
                        RowLayout {
                            Layout.fillWidth: true
                            
                            Text {
                                text: "1"
                                font.pixelSize: 10
                                color: "#757575"
                            }
                            
                            Slider {
                                id: developmentSlider
                                Layout.fillWidth: true
                                from: 1
                                to: 9
                                value: 5
                                stepSize: 1
                                
                                background: Rectangle {
                                    height: 4
                                    radius: 2
                                    color: "#e0e0e0"
                                    
                                    Rectangle {
                                        width: developmentSlider.visualPosition * parent.width
                                        height: parent.height
                                        color: getDevelopmentColor(developmentSlider.value)
                                        radius: 2
                                    }
                                }
                                
                                handle: Rectangle {
                                    x: developmentSlider.leftPadding + developmentSlider.visualPosition * (developmentSlider.availableWidth - width)
                                    y: developmentSlider.topPadding + developmentSlider.availableHeight / 2 - height / 2
                                    width: 20
                                    height: 20
                                    radius: 10
                                    color: getDevelopmentColor(developmentSlider.value)
                                    border.color: "#ffffff"
                                    border.width: 2
                                }
                                
                                onValueChanged: {
                                    // TODO: Update character model development level
                                    console.log("Development level:", value)
                                }
                            }
                            
                            Text {
                                text: "9"
                                font.pixelSize: 10
                                color: "#757575"
                            }
                        }
                        
                        Text {
                            text: "Level " + Math.round(developmentSlider.value) + " - " + getDevelopmentDescription(developmentSlider.value)
                            font.pixelSize: 12
                            color: getDevelopmentColor(developmentSlider.value)
                        }
                    }
                }
            }
        }
        
        // Instinctual Variants
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: instinctContent.implicitHeight + 32
            
            ColumnLayout {
                id: instinctContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Text {
                    text: "Instinctual Variants"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                Text {
                    text: "Order from strongest (primary) to weakest (tertiary) instinct."
                    font.pixelSize: 12
                    color: "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    
                    Repeater {
                        model: ["Primary", "Secondary", "Tertiary"]
                        
                        delegate: RowLayout {
                            Layout.fillWidth: true
                            
                            Text {
                                text: modelData + ":"
                                font.pixelSize: 14
                                font.bold: true
                                color: "#212121"
                                Layout.minimumWidth: 80
                            }
                            
                            ComboBox {
                                Layout.fillWidth: true
                                
                                model: [
                                    {text: "Self-Preservation (SP) - Focus on safety, comfort, and material security", value: "sp"},
                                    {text: "Social (SO) - Focus on social standing, groups, and community", value: "so"},
                                    {text: "Sexual/One-on-One (SX) - Focus on intensity, chemistry, and connections", value: "sx"}
                                ]
                                
                                textRole: "text"
                                valueRole: "value"
                                
                                currentIndex: index
                                
                                background: Rectangle {
                                    color: "#ffffff"
                                    border.color: "#e0e0e0"
                                    border.width: 1
                                    radius: 4
                                }
                                
                                onCurrentValueChanged: {
                                    // TODO: Update character model instinctual stack
                                    console.log("Instinct", index, ":", currentValue)
                                }
                            }
                        }
                    }
                }
                
                // Stack notation
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    color: "#f5f5f5"
                    border.color: "#e0e0e0"
                    border.width: 1
                    radius: 4
                    
                    Text {
                        anchors.centerIn: parent
                        text: "Stack: SP/SO/SX" // TODO: Generate from selections
                        font.pixelSize: 14
                        font.bold: true
                        color: "#212121"
                    }
                }
            }
        }
        
        // Integration & Disintegration
        Rectangle {
            Layout.fillWidth: true
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            implicitHeight: dynamicsContent.implicitHeight + 32
            
            ColumnLayout {
                id: dynamicsContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                
                Text {
                    text: "Type Dynamics"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 24
                    rowSpacing: 16
                    
                    // Integration
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        
                        Text {
                            text: "Integration (Growth)"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#4CAF50"
                        }
                        
                        Rectangle {
                            Layout.fillWidth: true
                            height: 60
                            radius: 4
                            color: "#E8F5E8"
                            border.color: "#4CAF50"
                            border.width: 1
                            
                            ColumnLayout {
                                anchors.centerIn: parent
                                
                                Text {
                                    text: "Type 3"
                                    font.pixelSize: 18
                                    font.bold: true
                                    color: "#4CAF50"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                
                                Text {
                                    text: "The Achiever"
                                    font.pixelSize: 10
                                    color: "#4CAF50"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                        }
                        
                        Text {
                            text: "When healthy, Type 9 becomes more focused, energetic, and goal-oriented like Type 3."
                            font.pixelSize: 10
                            color: "#757575"
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                    
                    // Disintegration
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        
                        Text {
                            text: "Disintegration (Stress)"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#F44336"
                        }
                        
                        Rectangle {
                            Layout.fillWidth: true
                            height: 60
                            radius: 4
                            color: "#FFEBEE"
                            border.color: "#F44336"
                            border.width: 1
                            
                            ColumnLayout {
                                anchors.centerIn: parent
                                
                                Text {
                                    text: "Type 6"
                                    font.pixelSize: 18
                                    font.bold: true
                                    color: "#F44336"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                
                                Text {
                                    text: "The Loyalist"
                                    font.pixelSize: 10
                                    color: "#F44336"
                                    Layout.alignment: Qt.AlignHCenter
                                }
                            }
                        }
                        
                        Text {
                            text: "Under stress, Type 9 becomes anxious, reactive, and suspicious like Type 6."
                            font.pixelSize: 10
                            color: "#757575"
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // Helper functions
    function getWingNotation() {
        let mainType = characterModel ? characterModel.enneagramType : 9
        let wing = wingCombo.currentValue
        
        if (wing > 0) {
            return mainType + "w" + wing
        }
        return mainType.toString()
    }
    
    function getDevelopmentColor(level) {
        if (level <= 3) return "#4CAF50"      // Healthy - Green
        if (level <= 6) return "#FF9800"      // Average - Orange
        return "#F44336"                      // Unhealthy - Red
    }
    
    function getDevelopmentDescription(level) {
        if (level <= 3) return "Healthy"
        if (level <= 6) return "Average"
        return "Unhealthy"
    }
}