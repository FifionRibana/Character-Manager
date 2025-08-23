import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

Rectangle {
    color: AppTheme.colors.backgroundVariant
    border.color: AppTheme.colors.borderLight
    border.width: AppTheme.border.thin
    radius: AppTheme.radius.small
    
    implicitHeight: explanationContent.implicitHeight + 2 * AppTheme.spacing.medium
    
    ColumnLayout {
        id: explanationContent
        anchors.fill: parent
        anchors.margins: AppTheme.spacing.medium
        spacing: AppTheme.spacing.small
        
        Text {
            text: qsTr("Stat Generation Methods")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.large
            font.bold: true
            color: AppTheme.colors.text
        }
        
        Text {
            text: qsTr("• 4d6 Roll: Rolls four 6-sided dice and drops the lowest for each stat\n" +
                        "• Point Buy: Start with 8 in each stat, spend 27 points to increase (costs vary)\n" +
                        "• Manual: Click +/- buttons or use spinboxes to set exact values")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.medium
            color: AppTheme.colors.textSecondary
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
    }
}