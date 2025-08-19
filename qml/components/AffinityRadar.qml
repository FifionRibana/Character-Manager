/**
 * AffinityRadar.qml
 * Radar chart visualization for Enneagram type affinities
 * Shows compatibility scores between character and other types
 */
import QtQuick
import QtQuick.Controls
import "../styles"

Item {
    id: affinityRadar
    
    // Public properties
    property var characterModel
    property real animationDuration: 300
    property bool showGrid: true
    property bool showLabels: true
    property bool interactive: false
    property color gridColor: AppTheme.borderColor
    property color lineColor: AppTheme.accentColor
    property color fillColor: Qt.rgba(AppTheme.accentColor.r, AppTheme.accentColor.g, AppTheme.accentColor.b, 0.3)
    
    // Computed properties
    readonly property real centerX: width / 2
    readonly property real centerY: height / 2
    readonly property real radius: Math.min(width, height) / 2 - 40
    readonly property real labelRadius: radius + 25
    
    // Type affinity data (0.0 to 1.0)
    property var affinityData: getAffinityData()
    
    // Signals
    signal typeClicked(int enneagramType)
    signal affinityChanged(int enneagramType, real affinity)
    
    // Background grid
    Canvas {
        id: gridCanvas
        anchors.fill: parent
        visible: showGrid
        
        onPaint: {
            drawGrid()
        }
        
        function drawGrid() {
            var ctx = getContext("2d")
            if (!ctx) return
            
            ctx.clearRect(0, 0, width, height)
            
            // Configure grid style
            ctx.strokeStyle = gridColor
            ctx.lineWidth = 1
            ctx.setLineDash([2, 2])
            
            // Draw concentric circles
            var steps = 5
            for (var i = 1; i <= steps; i++) {
                var circleRadius = (radius * i) / steps
                ctx.beginPath()
                ctx.arc(centerX, centerY, circleRadius, 0, 2 * Math.PI)
                ctx.stroke()
            }
            
            // Draw radial lines to each type
            ctx.setLineDash([])
            ctx.lineWidth = 0.5
            
            for (var type = 1; type <= 9; type++) {
                var angle = getTypeAngle(type)
                var x = centerX + radius * Math.cos(angle)
                var y = centerY + radius * Math.sin(angle)
                
                ctx.beginPath()
                ctx.moveTo(centerX, centerY)
                ctx.lineTo(x, y)
                ctx.stroke()
            }
        }
    }
    
    // Affinity visualization
    Canvas {
        id: affinityCanvas
        anchors.fill: parent
        
        onPaint: {
            drawAffinities()
        }
        
        function drawAffinities() {
            var ctx = getContext("2d")
            if (!ctx) return
            
            ctx.clearRect(0, 0, width, height)
            
            // Draw filled polygon
            ctx.fillStyle = fillColor
            ctx.strokeStyle = lineColor
            ctx.lineWidth = 3
            
            ctx.beginPath()
            
            var firstPoint = true
            for (var type = 1; type <= 9; type++) {
                var affinity = affinityData[type] || 0.5
                var angle = getTypeAngle(type)
                var distance = radius * affinity
                var x = centerX + distance * Math.cos(angle)
                var y = centerY + distance * Math.sin(angle)
                
                if (firstPoint) {
                    ctx.moveTo(x, y)
                    firstPoint = false
                } else {
                    ctx.lineTo(x, y)
                }
            }
            
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            
            // Draw affinity points
            drawAffinityPoints(ctx)
        }
        
        function drawAffinityPoints(ctx) {
            for (var type = 1; type <= 9; type++) {
                var affinity = affinityData[type] || 0.5
                var angle = getTypeAngle(type)
                var distance = radius * affinity
                var x = centerX + distance * Math.cos(angle)
                var y = centerY + distance * Math.sin(angle)
                
                // Point background
                ctx.fillStyle = "white"
                ctx.beginPath()
                ctx.arc(x, y, 8, 0, 2 * Math.PI)
                ctx.fill()
                
                // Point color based on affinity
                ctx.fillStyle = getAffinityColor(affinity)
                ctx.beginPath()
                ctx.arc(x, y, 6, 0, 2 * Math.PI)
                ctx.fill()
                
                // Point border
                ctx.strokeStyle = lineColor
                ctx.lineWidth = 2
                ctx.beginPath()
                ctx.arc(x, y, 6, 0, 2 * Math.PI)
                ctx.stroke()
            }
        }
    }
    
    // Type labels
    Repeater {
        model: 9
        visible: showLabels
        
        delegate: Item {
            property int typeNumber: index + 1
            property real angle: getTypeAngle(typeNumber)
            property real labelX: centerX + labelRadius * Math.cos(angle)
            property real labelY: centerY + labelRadius * Math.sin(angle)
            
            x: labelX - width / 2
            y: labelY - height / 2
            width: typeLabel.implicitWidth + 16
            height: typeLabel.implicitHeight + 8
            
            Rectangle {
                anchors.fill: parent
                radius: height / 2
                color: AppTheme.card.background
                border.color: AppTheme.card.border
                border.width: 1
                
                // Highlight if this is the character's type
                Rectangle {
                    anchors.fill: parent
                    radius: parent.radius
                    color: isCharacterType() ? AppTheme.accentColor : "transparent"
                    opacity: 0.2
                }
            }
            
            Text {
                id: typeLabel
                anchors.centerIn: parent
                text: typeNumber.toString()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeBody
                font.bold: isCharacterType()
                color: isCharacterType() ? AppTheme.accentColor : AppTheme.textColor
            }
            
            MouseArea {
                anchors.fill: parent
                enabled: interactive
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                
                onClicked: {
                    typeClicked(typeNumber)
                }
                
                onPressed: {
                    parent.scale = 0.95
                }
                
                onReleased: {
                    parent.scale = 1.0
                }
            }
            
            ToolTip {
                text: getTypeInfo(typeNumber)
                visible: parent.children[2].containsMouse
                delay: 500
            }
            
            function isCharacterType() {
                return characterModel && characterModel.enneagramType === typeNumber
            }
            
            Behavior on scale {
                NumberAnimation { duration: 150 }
            }
        }
    }
    
    // Center point
    Rectangle {
        x: centerX - 4
        y: centerY - 4
        width: 8
        height: 8
        radius: 4
        color: AppTheme.accentColor
        border.color: "white"
        border.width: 2
    }
    
    // Interactive affinity editing (if enabled)
    MouseArea {
        anchors.fill: parent
        enabled: interactive
        
        onClicked: function(mouse) {
            var clickedType = getTypeAtPosition(mouse.x, mouse.y)
            if (clickedType > 0) {
                // Calculate new affinity based on distance from center
                var dx = mouse.x - centerX
                var dy = mouse.y - centerY
                var distance = Math.sqrt(dx * dx + dy * dy)
                var newAffinity = Math.min(1.0, Math.max(0.0, distance / radius))
                
                setAffinity(clickedType, newAffinity)
            }
        }
    }
    
    // Legend
    Rectangle {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10
        width: 120
        height: legendContent.implicitHeight + 16
        color: AppTheme.card.background
        border.color: AppTheme.card.border
        border.width: 1
        radius: 6
        opacity: 0.9
        
        ColumnLayout {
            id: legendContent
            anchors.fill: parent
            anchors.margins: 8
            spacing: 4
            
            Text {
                text: qsTr("Affinity")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSizeCaption
                font.bold: true
                color: AppTheme.textColor
            }
            
            RowLayout {
                spacing: 4
                
                Rectangle {
                    width: 12
                    height: 12
                    radius: 6
                    color: "#e74c3c"
                }
                
                Text {
                    text: qsTr("Low")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeCaption
                    color: AppTheme.textColorSecondary
                }
            }
            
            RowLayout {
                spacing: 4
                
                Rectangle {
                    width: 12
                    height: 12
                    radius: 6
                    color: "#f39c12"
                }
                
                Text {
                    text: qsTr("Medium")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeCaption
                    color: AppTheme.textColorSecondary
                }
            }
            
            RowLayout {
                spacing: 4
                
                Rectangle {
                    width: 12
                    height: 12
                    radius: 6
                    color: "#2ecc71"
                }
                
                Text {
                    text: qsTr("High")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSizeCaption
                    color: AppTheme.textColorSecondary
                }
            }
        }
    }
    
    // Functions
    function getTypeAngle(type) {
        // Types arranged clockwise starting from top (Type 9)
        var typeOrder = [9, 1, 2, 3, 4, 5, 6, 7, 8]
        var index = typeOrder.indexOf(type)
        if (index === -1) return 0
        
        // Start at top (-90 degrees) and go clockwise
        return (-Math.PI / 2) + (index * 2 * Math.PI / 9)
    }
    
    function getAffinityData() {
        var data = {}
        
        if (characterModel && characterModel.enneagramType) {
            // Get affinities from character model if available
            // For now, use default values
            for (var i = 1; i <= 9; i++) {
                data[i] = getDefaultAffinity(characterModel.enneagramType, i)
            }
        } else {
            // Default neutral affinities
            for (var j = 1; j <= 9; j++) {
                data[j] = 0.5
            }
        }
        
        return data
    }
    
    function getDefaultAffinity(mainType, otherType) {
        if (mainType === otherType) return 1.0
        
        // Simplified affinity calculation based on Enneagram theory
        var wing1 = mainType === 1 ? 9 : mainType - 1
        var wing2 = mainType === 9 ? 1 : mainType + 1
        
        if (otherType === wing1 || otherType === wing2) {
            return 0.8 // High affinity with wings
        }
        
        // Integration/disintegration points
        var integrations = {1: 7, 2: 4, 3: 6, 4: 1, 5: 8, 6: 9, 7: 5, 8: 2, 9: 3}
        var disintegrations = {1: 4, 2: 8, 3: 9, 4: 2, 5: 7, 6: 3, 7: 1, 8: 5, 9: 6}
        
        if (otherType === integrations[mainType]) {
            return 0.7 // Good affinity with integration point
        }
        
        if (otherType === disintegrations[mainType]) {
            return 0.4 // Lower affinity with stress point
        }
        
        // Same triad
        var triads = {
            body: [8, 9, 1],
            heart: [2, 3, 4],
            head: [5, 6, 7]
        }
        
        for (var triad in triads) {
            if (triads[triad].includes(mainType) && triads[triad].includes(otherType)) {
                return 0.6 // Moderate affinity within triad
            }
        }
        
        return 0.5 // Neutral affinity
    }
    
    function getAffinityColor(affinity) {
        if (affinity >= 0.7) return "#2ecc71"      // Green for high
        if (affinity >= 0.4) return "#f39c12"      // Orange for medium
        return "#e74c3c"                           // Red for low
    }
    
    function getTypeAtPosition(x, y) {
        var minDistance = Infinity
        var closestType = 0
        
        for (var type = 1; type <= 9; type++) {
            var angle = getTypeAngle(type)
            var affinity = affinityData[type] || 0.5
            var distance = radius * affinity
            var typeX = centerX + distance * Math.cos(angle)
            var typeY = centerY + distance * Math.sin(angle)
            
            var distanceToClick = Math.sqrt(Math.pow(x - typeX, 2) + Math.pow(y - typeY, 2))
            
            if (distanceToClick < 15 && distanceToClick < minDistance) {
                minDistance = distanceToClick
                closestType = type
            }
        }
        
        return closestType
    }
    
    function setAffinity(type, affinity) {
        affinityData[type] = Math.min(1.0, Math.max(0.0, affinity))
        affinityCanvas.requestPaint()
        affinityChanged(type, affinityData[type])
    }
    
    function getTypeInfo(type) {
        var titles = {
            1: qsTr("Type 1 - The Reformer"),
            2: qsTr("Type 2 - The Helper"),
            3: qsTr("Type 3 - The Achiever"),
            4: qsTr("Type 4 - The Individualist"),
            5: qsTr("Type 5 - The Investigator"),
            6: qsTr("Type 6 - The Loyalist"),
            7: qsTr("Type 7 - The Enthusiast"),
            8: qsTr("Type 8 - The Challenger"),
            9: qsTr("Type 9 - The Peacemaker")
        }
        
        var title = titles[type] || ""
        var affinity = affinityData[type] || 0.5
        var percentage = Math.round(affinity * 100)
        
        return title + "\n" + qsTr("Affinity: ") + percentage + "%"
    }
    
    // Update when character changes
    onCharacterModelChanged: {
        affinityData = getAffinityData()
        gridCanvas.requestPaint()
        affinityCanvas.requestPaint()
    }
    
    // Component initialization
    Component.onCompleted: {
        gridCanvas.requestPaint()
        affinityCanvas.requestPaint()
    }
    
    // Handle resize
    onWidthChanged: Qt.callLater(function() {
        gridCanvas.requestPaint()
        affinityCanvas.requestPaint()
    })
    
    onHeightChanged: Qt.callLater(function() {
        gridCanvas.requestPaint()
        affinityCanvas.requestPaint()
    })
}