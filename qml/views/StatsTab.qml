import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: statsTab
    
    property var characterModel
    
    contentWidth: availableWidth
    
    ColumnLayout {
        width: statsTab.availableWidth
        spacing: 24
        
        // Title
        Text {
            text: "Ability Scores"
            font.pixelSize: 24
            font.bold: true
            color: "#212121"
            Layout.alignment: Qt.AlignTop
        }
        
        // Stats grid
        GridLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            columns: 2
            columnSpacing: 40
            rowSpacing: 24
            
            // Strength
            StatEditor {
                statName: "Strength"
                statValue: characterModel ? characterModel.strength : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.strength = newValue
                    }
                }
            }
            
            // Agility
            StatEditor {
                statName: "Agility"
                statValue: characterModel ? characterModel.agility : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.agility = newValue
                    }
                }
            }
            
            // Constitution
            StatEditor {
                statName: "Constitution"
                statValue: characterModel ? characterModel.constitution : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.constitution = newValue
                    }
                }
            }
            
            // Intelligence
            StatEditor {
                statName: "Intelligence"
                statValue: characterModel ? characterModel.intelligence : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.intelligence = newValue
                    }
                }
            }
            
            // Wisdom
            StatEditor {
                statName: "Wisdom"
                statValue: characterModel ? characterModel.wisdom : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.wisdom = newValue
                    }
                }
            }
            
            // Charisma
            StatEditor {
                statName: "Charisma"
                statValue: characterModel ? characterModel.charisma : 10
                onValueChanged: function(newValue) {
                    if (characterModel) {
                        characterModel.charisma = newValue
                    }
                }
            }
        }
        
        // Stats summary
        Rectangle {
            Layout.fillWidth: true
            Layout.topMargin: 16
            height: summaryContent.implicitHeight + 32
            color: "#ffffff"
            border.color: "#e0e0e0"
            border.width: 1
            radius: 8
            
            ColumnLayout {
                id: summaryContent
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12
                
                Text {
                    text: "Summary"
                    font.pixelSize: 18
                    font.bold: true
                    color: "#212121"
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#e0e0e0"
                }
                
                // Total points
                Text {
                    text: {
                        if (!characterModel) return "Total Points: 60 / 60"
                        
                        let total = characterModel.strength + characterModel.agility + 
                                   characterModel.constitution + characterModel.intelligence + 
                                   characterModel.wisdom + characterModel.charisma
                        return "Total Points: " + total + " / 60"
                    }
                    font.pixelSize: 14
                    color: {
                        if (!characterModel) return "#757575"
                        
                        let total = characterModel.strength + characterModel.agility + 
                                   characterModel.constitution + characterModel.intelligence + 
                                   characterModel.wisdom + characterModel.charisma
                        
                        if (total > 60) return "#f44336"      // Red for over
                        if (total < 60) return "#ff9800"      // Orange for under
                        return "#4caf50"                      // Green for exact
                    }
                    Layout.alignment: Qt.AlignHCenter
                }
                
                // Info text
                Text {
                    text: "Standard array: 15, 14, 13, 12, 10, 8\nHeroic: All stats start at 10\nPoint buy range: 8-15"
                    font.pixelSize: 12
                    color: "#757575"
                    horizontalAlignment: Text.AlignHCenter
                    Layout.alignment: Qt.AlignHCenter
                    wrapMode: Text.WordWrap
                }
                
                // Quick action buttons
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 8
                    
                    Button {
                        text: "Standard Array"
                        onClicked: applyStandardArray()
                    }
                    
                    Button {
                        text: "All 10s"
                        onClicked: resetToTens()
                    }
                    
                    Button {
                        text: "Random"
                        onClicked: randomizeStats()
                    }
                }
            }
        }
        
        Item {
            Layout.fillHeight: true
        }
    }
    
    // Helper functions
    function applyStandardArray() {
        if (!characterModel) return
        
        let standardStats = [15, 14, 13, 12, 10, 8]
        characterModel.strength = standardStats[0]
        characterModel.agility = standardStats[1] 
        characterModel.constitution = standardStats[2]
        characterModel.intelligence = standardStats[3]
        characterModel.wisdom = standardStats[4]
        characterModel.charisma = standardStats[5]
    }
    
    function resetToTens() {
        if (!characterModel) return
        
        characterModel.strength = 10
        characterModel.agility = 10
        characterModel.constitution = 10
        characterModel.intelligence = 10
        characterModel.wisdom = 10
        characterModel.charisma = 10
    }
    
    function randomizeStats() {
        if (!characterModel) return
        
        // 4d6 drop lowest method
        function rollStat() {
            let rolls = []
            for (let i = 0; i < 4; i++) {
                rolls.push(Math.floor(Math.random() * 6) + 1)
            }
            rolls.sort((a, b) => b - a) // Sort descending
            return rolls[0] + rolls[1] + rolls[2] // Sum the highest 3
        }
        
        characterModel.strength = rollStat()
        characterModel.agility = rollStat()
        characterModel.constitution = rollStat()
        characterModel.intelligence = rollStat()
        characterModel.wisdom = rollStat()
        characterModel.charisma = rollStat()
    }
}

// Stat editor component
component StatEditor: Rectangle {
    id: statEditor
    
    property string statName: ""
    property int statValue: 10
    signal valueChanged(int newValue)
    
    width: 280
    height: 120
    color: "#ffffff"
    border.color: "#e0e0e0"
    border.width: 1
    radius: 8
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 8
        
        // Stat name
        Text {
            text: statName
            font.pixelSize: 16
            font.bold: true
            color: "#212121"
            Layout.alignment: Qt.AlignHCenter
        }
        
        // Value controls
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 12
            
            // Decrease button
            Button {
                text: "-"
                width: 32
                height: 32
                enabled: statValue > 1
                onClicked: {
                    if (statValue > 1) {
                        statEditor.valueChanged(statValue - 1)
                    }
                }
            }
            
            // Value display
            Rectangle {
                width: 60
                height: 60
                radius: 30
                color: getStatColor(statValue)
                border.color: "#e0e0e0"
                border.width: 2
                
                Text {
                    anchors.centerIn: parent
                    text: statValue.toString()
                    font.pixelSize: 20
                    font.bold: true
                    color: "#ffffff"
                }
            }
            
            // Increase button
            Button {
                text: "+"
                width: 32
                height: 32
                enabled: statValue < 20
                onClicked: {
                    if (statValue < 20) {
                        statEditor.valueChanged(statValue + 1)
                    }
                }
            }
        }
        
        // Modifier display
        Text {
            text: {
                let modifier = Math.floor((statValue - 10) / 2)
                return modifier >= 0 ? "+" + modifier : modifier.toString()
            }
            font.pixelSize: 14
            color: getModifierColor(Math.floor((statValue - 10) / 2))
            Layout.alignment: Qt.AlignHCenter
        }
        
        // Direct input
        SpinBox {
            from: 1
            to: 20
            value: statValue
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 80
            
            onValueChanged: {
                if (value !== statEditor.statValue) {
                    statEditor.valueChanged(value)
                }
            }
        }
    }
    
    function getStatColor(value) {
        if (value >= 16) return "#4CAF50"      // Green for high stats
        if (value >= 14) return "#8BC34A"      // Light green
        if (value >= 12) return "#CDDC39"      // Yellow-green
        if (value >= 10) return "#FFC107"      // Amber for average
        if (value >= 8) return "#FF9800"       // Orange for low
        return "#F44336"                       // Red for very low
    }
    
    function getModifierColor(modifier) {
        if (modifier > 0) return "#4CAF50"     // Green for positive
        if (modifier < 0) return "#F44336"     // Red for negative
        return "#757575"                       // Gray for zero
    }
}