import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles


ColumnLayout {
    spacing: AppTheme.spacing.tiny

    property alias value: iTextValue.text
    property alias color: iTextValue.color
    property alias label: iTextLabel.text

    Text {
        id: iTextValue
        text: "0"
        font.pixelSize: AppTheme.fontSize.huge
        font.bold: true
        color: "#FF9800"
        Layout.alignment: Qt.AlignHCenter
    }
    
    Text {
        id: iTextLabel
        text: "Total Events"
        font.pixelSize: AppTheme.fontSize.tiny
        color: AppTheme.colors.textSecondary
        Layout.alignment: Qt.AlignHCenter
    }
}