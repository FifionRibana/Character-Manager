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
            text: qsTr("Enneagram info.")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.large
            font.bold: true
            color: AppTheme.colors.text
        }
        
        Text {

            text: qsTr("The Enneagram is a powerful personality system that describes nine distinct patterns of thinking, feeling, and acting.\n" +
                        "• Click on numbers around the wheel to select your core type\n" + 
                        "• Choose a wing (adjacent type that influences your core type)\n" +
                        "• Select your instinctual variant (primary life focus)\n" +
                        "• Set your development level (psychological health)\n" +
                        "The colored lines show integration (growth) and disintegration (stress) patterns between types.")
            font.family: AppTheme.fontFamily
            font.pixelSize: AppTheme.fontSize.medium
            color: AppTheme.colors.textSecondary
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
    }
}