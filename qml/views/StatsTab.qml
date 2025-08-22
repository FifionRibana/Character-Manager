/**
 * StatsTab.qml
 * Interactive character statistics editing tab
 * Features live editing, validation, and D&D-style modifiers
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
// import "../styles"
import App.Styles

ScrollView {
    id: statsTab
    
    property var characterModel
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: statsTab.availableWidth
        spacing: AppTheme.spacing.large || 24
        
        // Title and quick actions
        RowLayout {
            Layout.fillWidth: true
            
            Text {
                text: qsTr("Ability Scores")
                font.family: AppTheme.fontFamily || "Inter"
                font.pixelSize: AppTheme.fontSizeDisplay || 32
                font.bold: true
                color: AppTheme.colors.text || "#212121"
            }
            
            Item { Layout.fillWidth: true }
            
            // Quick action buttons
            RowLayout {
                spacing: AppTheme.spacing.medium || 16
                
                Button {
                    text: qsTr("Standard Array")
                    font.family: AppTheme.fontFamily || "Inter"
                    font.pixelSize: AppTheme.fontSize.medium || 14
                    
                    background: Rectangle {
                        color: parent.hovered ? Qt.lighter(AppTheme.colors.accent || "#FF5722", 1.1) : (AppTheme.colors.accent || "#FF5722")
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
                    
                    onClicked: applyStandardArray()
                    
                    ToolTip {
                        text: qsTr("Apply D&D 5e standard array: 15, 14, 13, 12, 10, 8")
                        visible: parent.hovered
                        delay: 500
                    }
                }
                
                Button {
                    text: qsTr("4d6 Roll")
                    font.family: AppTheme.fontFamily || "Inter"
                    font.pixelSize: AppTheme.fontSize.medium || 14
                    
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
                    
                    onClicked: rollStats()
                    
                    ToolTip {
                        text: qsTr("Roll 4d6 drop lowest for each stat")
                        visible: parent.hovered
                        delay: 500
                    }
                }
                
                Button {
                    text: qsTr("Reset to 10")
                    font.family: AppTheme.fontFamily || "Inter"
                    font.pixelSize: AppTheme.fontSize.medium || 14
                    
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
                    
                    onClicked: resetToTens()
                    
                    ToolTip {
                        text: qsTr("Reset all stats to 10 (standard baseline)")
                        visible: parent.hovered
                        delay: 500
                    }
                }
            }
        }
        
        // Stats summary card
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.card.background || "#FFFFFF"
            border.color: AppTheme.card.border || "#E0E0E0"
            border.width: AppTheme.borderWidth || 1
            radius: AppTheme.radius.medium || 8
            
            implicitHeight: summaryContent.implicitHeight + 2 * (AppTheme.spacing.medium || 16)
            
            RowLayout {
                id: summaryContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.medium || 16
                spacing: AppTheme.spacing.large || 24
                
                // Total points
                ColumnLayout {
                    spacing: AppTheme.spacing.small || 8
                    
                    Text {
                        text: qsTr("Total Points")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.small || 12
                        color: AppTheme.colors.textSecondary || "#757575"
                    }
                    
                    Text {
                        text: getTotalPoints().toString()
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: getTotalPointsColor()
                    }
                }
                
                Rectangle {
                    width: 1
                    Layout.fillHeight: true
                    color: AppTheme.colors.border || "#E0E0E0"
                }
                
                // Average stat
                ColumnLayout {
                    spacing: AppTheme.spacing.small || 8
                    
                    Text {
                        text: qsTr("Average")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.small || 12
                        color: AppTheme.colors.textSecondary || "#757575"
                    }
                    
                    Text {
                        text: getAverageScore().toFixed(1)
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: AppTheme.colors.text || "#212121"
                    }
                }
                
                Rectangle {
                    width: 1
                    Layout.fillHeight: true
                    color: AppTheme.colors.border || "#E0E0E0"
                }
                
                // Point buy cost (if applicable)
                ColumnLayout {
                    spacing: AppTheme.spacing.small || 8
                    
                    Text {
                        text: qsTr("Point Buy Cost")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.small || 12
                        color: AppTheme.colors.textSecondary || "#757575"
                    }
                    
                    Text {
                        text: getPointBuyCost().toString() + "/27"
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: getPointBuyCost() <= 27 ? "#2ecc71" : "#e74c3c"
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                // Modifier bonus indicator
                ColumnLayout {
                    spacing: AppTheme.spacing.small || 8
                    
                    Text {
                        text: qsTr("Modifier Bonus")
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.small || 12
                        color: AppTheme.colors.textSecondary || "#757575"
                    }
                    
                    Text {
                        text: getTotalModifiers() >= 0 ? "+" + getTotalModifiers() : getTotalModifiers().toString()
                        font.family: AppTheme.fontFamily || "Inter"
                        font.pixelSize: AppTheme.fontSize.large || 20
                        font.bold: true
                        color: getTotalModifiers() >= 0 ? "#2ecc71" : "#e74c3c"
                    }
                }
            }
        }
        
        // Stats grid
        GridLayout {
            Layout.fillWidth: true
            columns: 3
            columnSpacing: AppTheme.spacing.large || 24
            rowSpacing: AppTheme.spacing.large || 24
            
            // Strength
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Strength")
                statAbbreviation: "STR"
                statDescription: qsTr("Physical power and muscle")
                statValue: characterModel && characterModel.strength !== undefined ? characterModel.strength : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.strength = newValue
                    }
                }
            }
            
            // Agility
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Agility")
                statAbbreviation: "AGI"
                statDescription: qsTr("Speed, reflexes, and dexterity")
                statValue: characterModel && characterModel.agility !== undefined ? characterModel.agility : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.agility = newValue
                    }
                }
            }
            
            // Constitution
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Constitution")
                statAbbreviation: "CON"
                statDescription: qsTr("Health, stamina, and vitality")
                statValue: characterModel && characterModel.constitution !== undefined ? characterModel.constitution : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.constitution = newValue
                    }
                }
            }
            
            // Intelligence
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Intelligence")
                statAbbreviation: "INT"
                statDescription: qsTr("Reasoning ability and memory")
                statValue: characterModel && characterModel.intelligence !== undefined ? characterModel.intelligence : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.intelligence = newValue
                    }
                }
            }
            
            // Wisdom
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Wisdom")
                statAbbreviation: "WIS"
                statDescription: qsTr("Perception and insight")
                statValue: characterModel && characterModel.wisdom !== undefined ? characterModel.wisdom : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.wisdom = newValue
                    }
                }
            }
            
            // Charisma
            StatWidget {
                Layout.fillWidth: true
                statName: qsTr("Charisma")
                statAbbreviation: "CHA"
                statDescription: qsTr("Force of personality and leadership")
                statValue: characterModel && characterModel.charisma !== undefined ? characterModel.charisma : 10
                onValueChanged: function(newValue) {
                    if (characterModel && newValue !== undefined) {
                        characterModel.charisma = newValue
                    }
                }
            }
        }
        
        // Point buy explanation
        Rectangle {
            Layout.fillWidth: true
            color: AppTheme.colors.backgroundVariant || "#F8F9FA"
            border.color: AppTheme.colors.borderLight || "#DEE2E6"
            border.width: 1
            radius: 6
            
            implicitHeight: explanationContent.implicitHeight + 2 * (AppTheme.spacing.medium || 16)
            
            ColumnLayout {
                id: explanationContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.medium || 16
                spacing: AppTheme.spacing.small || 8
                
                Text {
                    text: qsTr("Stat Generation Methods")
                    font.family: AppTheme.fontFamily || "Inter"
                    font.pixelSize: AppTheme.fontSize.large || 20
                    font.bold: true
                    color: AppTheme.colors.text || "#212121"
                }
                
                Text {
                    text: qsTr("• Standard Array: Uses the balanced D&D 5e array (15, 14, 13, 12, 10, 8)\n" +
                              "• 4d6 Roll: Rolls four 6-sided dice and drops the lowest for each stat\n" +
                              "• Point Buy: Start with 8 in each stat, spend 27 points to increase (costs vary)\n" +
                              "• Manual: Click +/- buttons or use spinboxes to set exact values")
                    font.family: AppTheme.fontFamily || "Inter"
                    font.pixelSize: AppTheme.fontSize.medium || 14
                    color: AppTheme.colors.textSecondary || "#757575"
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
            }
        }
    }
    
    // Helper functions
    function getTotalPoints() {
        if (!characterModel) return 60
        
        return (characterModel.strength || 10) + (characterModel.agility || 10) + (characterModel.constitution || 10) +
               (characterModel.intelligence || 10) + (characterModel.wisdom || 10) + (characterModel.charisma || 10)
    }
    
    function getTotalPointsColor() {
        var total = getTotalPoints()
        var baseline = 60 // 6 stats * 10 each
        
        if (total > baseline + 6) return "#3498db"  // Blue for high
        if (total > baseline) return "#2ecc71"      // Green for above average
        if (total < baseline - 6) return "#e74c3c" // Red for low
        return AppTheme.colors.text || "#212121"      // Normal for average
    }
    
    function getAverageScore() {
        return getTotalPoints() / 6
    }
    
    function getTotalModifiers() {
        if (!characterModel) return 0
        
        var getModifier = function(stat) {
            return Math.floor((stat - 10) / 2)
        }
        
        return getModifier(characterModel.strength || 10) + getModifier(characterModel.agility || 10) +
               getModifier(characterModel.constitution || 10) + getModifier(characterModel.intelligence || 10) +
               getModifier(characterModel.wisdom || 10) + getModifier(characterModel.charisma || 10)
    }
    
    function getPointBuyCost() {
        if (!characterModel) return 0
        
        var calculateCost = function(stat) {
            if (stat <= 8) return 0
            if (stat <= 13) return stat - 8
            if (stat <= 15) return (stat - 8) + (stat - 13)
            return (stat - 8) + 2 + ((stat - 15) * 2)
        }
        
        return calculateCost(characterModel.strength || 10) + calculateCost(characterModel.agility || 10) +
               calculateCost(characterModel.constitution || 10) + calculateCost(characterModel.intelligence || 10) +
               calculateCost(characterModel.wisdom || 10) + calculateCost(characterModel.charisma || 10)
    }
    
    function applyStandardArray() {
        if (!characterModel) return
        
        // D&D 5e standard array
        characterModel.strength = 15
        characterModel.agility = 14
        characterModel.constitution = 13
        characterModel.intelligence = 12
        characterModel.wisdom = 10
        characterModel.charisma = 8
    }
    
    function rollStats() {
        if (!characterModel) return
        
        // 4d6 drop lowest method
        var rollStat = function() {
            var rolls = []
            for (var i = 0; i < 4; i++) {
                rolls.push(Math.floor(Math.random() * 6) + 1)
            }
            rolls.sort(function(a, b) { return b - a }) // Sort descending
            return rolls[0] + rolls[1] + rolls[2] // Sum the highest 3
        }
        
        characterModel.strength = rollStat()
        characterModel.agility = rollStat()
        characterModel.constitution = rollStat()
        characterModel.intelligence = rollStat()
        characterModel.wisdom = rollStat()
        characterModel.charisma = rollStat()
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
}