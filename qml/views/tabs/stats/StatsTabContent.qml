import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../../components"
import App.Styles


GridLayout {
    id: iStatsGrid
    columns: 3
    columnSpacing: AppTheme.spacing.large
    rowSpacing: AppTheme.spacing.large

    property int strength: 10
    property int agility: 10
    property int constitution: 10
    property int intelligence: 10
    property int wisdom: 10
    property int charisma: 10
    
    signal strengthChangeRequested(int newValue)
    signal agilityChangeRequested(int newValue)
    signal constitutionChangeRequested(int newValue)
    signal intelligenceChangeRequested(int newValue)
    signal wisdomChangeRequested(int newValue)
    signal charismaChangeRequested(int newValue)


    // Strength
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Strength")
        statAbbreviation: "STR"
        statDescription: qsTr("Physical power and muscle")
        statValue: iStatsGrid.strength
        onValueChanged: function (newValue) { iStatsGrid.strengthChangeRequested(newValue) }
    }
    
    // Agility
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Agility")
        statAbbreviation: "AGI"
        statDescription: qsTr("Speed, reflexes, and dexterity")
        statValue: iStatsGrid.agility
        onValueChanged: function (newValue) { iStatsGrid.agilityChangeRequested(newValue) }
    }
    
    // Constitution
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Constitution")
        statAbbreviation: "CON"
        statDescription: qsTr("Health, stamina, and vitality")
        statValue: iStatsGrid.constitution
        onValueChanged: function (newValue) { iStatsGrid.constitutionChangeRequested(newValue) }
    }
    
    // Intelligence
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Intelligence")
        statAbbreviation: "INT"
        statDescription: qsTr("Reasoning ability and memory")
        statValue: iStatsGrid.intelligence
        onValueChanged: function (newValue) { iStatsGrid.intelligenceChangeRequested(newValue) }
    }
    
    // Wisdom
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Wisdom")
        statAbbreviation: "WIS"
        statDescription: qsTr("Perception and insight")
        statValue: iStatsGrid.wisdom
        onValueChanged: function (newValue) { iStatsGrid.wisdomChangeRequested(newValue) }
    }
    
    // Charisma
    StatWidget {
        Layout.fillWidth: true
        statName: qsTr("Charisma")
        statAbbreviation: "CHA"
        statDescription: qsTr("Force of personality and leadership")
        statValue: iStatsGrid.charisma
        onValueChanged: function (newValue) { iStatsGrid.charismaChangeRequested(newValue) }
    }
}