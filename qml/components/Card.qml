import QtQuick
import QtQuick.Controls

import App.Styles

Control {
    id: iCard
    
    padding: AppTheme.padding.medium
    property color backgroundColor: AppTheme.card.background

    background: Rectangle {
        color: iCard.backgroundColor
        border.color: AppTheme.card.border
        border.width: AppTheme.border.thin
        radius: AppTheme.radius.medium
    }

}
    