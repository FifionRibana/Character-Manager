/**
 * StatsTab.qml
 * Interactive character statistics editing tab
 * Features live editing, validation, and D&D-style modifiers
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "./tabs/stats"
import App.Styles

ScrollView {
    id: statsTab
    
    property var characterModel
    
    contentWidth: availableWidth
    clip: true
    
    ColumnLayout {
        width: statsTab.availableWidth
        spacing: AppTheme.spacing.large

        // Header section
        StatsTabHeader {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.topMargin: AppTheme.margin.small

            totalPoints: getTotalPoints()
            totalPointsColor: getTotalPointsColor()
            averageScore: getAverageScore()
            pointBuyCost: getPointBuyCost()
            totalModifiers: getTotalModifiers()

            onReset: statsTab.resetToTens()
            onRollStatsRequested: statsTab.rollStats
        }
            
        // Stats grid
        StatsTabContent {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small

            strength: characterModel && characterModel.strength !== undefined ? characterModel.strength : 10
            agility: characterModel && characterModel.agility !== undefined ? characterModel.agility : 10
            constitution: characterModel && characterModel.constitution !== undefined ? characterModel.constitution : 10
            intelligence: characterModel && characterModel.intelligence !== undefined ? characterModel.intelligence : 10
            wisdom: characterModel && characterModel.wisdom !== undefined ? characterModel.wisdom : 10
            charisma: characterModel && characterModel.charisma !== undefined ? characterModel.charisma : 10
            
            onStrengthChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.strength = newValue
                }
            }
            onAgilityChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.agility = newValue
                }
            }
            onConstitutionChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.constitution = newValue
                }
            }
            onIntelligenceChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.intelligence = newValue
                }
            }
            onWisdomChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.wisdom = newValue
                }
            }
            onCharismaChangeRequested: function(newValue) {
                if (characterModel && newValue !== undefined) {
                    characterModel.charisma = newValue
                }
            }
        }
        
        // Point buy explanation
        StatsTabFooter {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.bottomMargin: AppTheme.margin.small
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