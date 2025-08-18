import QtQuick
import QtQuick.Controls

Item {
    id: enneagramWheel
    
    property int selectedType: 9
    property real animationDuration: 200
    property real wheelSize: Math.min(width, height) - 40
    property real centerX: width / 2
    property real centerY: height / 2
    property real outerRadius: wheelSize / 2
    property real innerRadius: outerRadius * 0.6
    property real nodeRadius: 25
    
    signal typeSelected(int enneagramType)
    
    // Colors for each type
    property var typeColors: [
        "#E3F2FD", // Type 1 - Light Blue
        "#F3E5F5", // Type 2 - Light Purple
        "#E8F5E8", // Type 3 - Light Green
        "#FFF3E0", // Type 4 - Light Orange
        "#E0F2F1", // Type 5 - Light Teal
        "#FCE4EC", // Type 6 - Light Pink
        "#FFFDE7", // Type 7 - Light Yellow
        "#FFEBEE", // Type 8 - Light Red
        "#F1F8E9"  // Type 9 - Light Light Green
    ]
    
    // Type positions (Type 9 at top, clockwise)
    property var typePositions: calculateTypePositions()
    
    Canvas {
        id: wheelCanvas
        anchors.fill: parent
        
        onPaint: {
            drawWheel()
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: function(mouse) {
                let clickedType = getTypeAtPosition(mouse.x, mouse.y)
                if (clickedType > 0) {
                    selectType(clickedType)
                }
            }
        }
    }
    
    // Type labels
    Repeater {
        model: 9
        
        delegate: Item {
            id: typeLabel
            property int typeNumber: index + 1
            property real angle: -90 + (index * 40) // 360/9 = 40 degrees apart
            property real radian: angle * Math.PI / 180
            property real labelX: centerX + (outerRadius + 35) * Math.cos(radian)
            property real labelY: centerY + (outerRadius + 35) * Math.sin(radian)
            
            x: labelX - 15
            y: labelY - 15
            width: 30
            height: 30
            
            Rectangle {
                anchors.fill: parent
                radius: 15
                color: selectedType === typeNumber ? "#4CAF50" : "transparent"
                border.color: selectedType === typeNumber ? "#4CAF50" : "#757575"
                border.width: 2
                
                Behavior on color {
                    ColorAnimation { duration: animationDuration }
                }
                
                Text {
                    anchors.centerIn: parent
                    text: typeNumber.toString()
                    font.pixelSize: 14
                    font.bold: true
                    color: selectedType === typeNumber ? "#ffffff" : "#212121"
                    
                    Behavior on color {
                        ColorAnimation { duration: animationDuration }
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    onClicked: selectType(typeNumber)
                    cursorShape: Qt.PointingHandCursor
                }
            }
        }
    }
    
    // Center indicator
    Rectangle {
        x: centerX - 6
        y: centerY - 6
        width: 12
        height: 12
        radius: 6
        color: "#4CAF50"
        border.color: "#ffffff"
        border.width: 2
    }
    
    // Integration/Disintegration lines (shown when type is selected)
    Canvas {
        id: connectionsCanvas
        anchors.fill: parent
        visible: selectedType > 0
        
        onPaint: {
            if (selectedType > 0) {
                drawConnections()
            }
        }
    }
    
    // Functions
    function calculateTypePositions() {
        let positions = []
        
        // Type order clockwise from top (Type 9 at 12 o'clock)
        let typeOrder = [9, 1, 2, 3, 4, 5, 6, 7, 8]
        
        for (let i = 0; i < typeOrder.length; i++) {
            let angle = -90 + (i * 40) // Start at top, 40 degrees apart
            let radian = angle * Math.PI / 180
            let x = centerX + outerRadius * Math.cos(radian)
            let y = centerY + outerRadius * Math.sin(radian)
            
            positions[typeOrder[i]] = {x: x, y: y, angle: angle}
        }
        
        return positions
    }
    
    function drawWheel() {
        let ctx = wheelCanvas.getContext("2d")
        if (!ctx) return
        
        ctx.clearRect(0, 0, width, height)
        
        // Draw outer circle
        ctx.strokeStyle = "#e0e0e0"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(centerX, centerY, outerRadius, 0, 2 * Math.PI)
        ctx.stroke()
        
        // Draw inner enneagram figure
        drawEnneagramFigure(ctx)
        
        // Draw type nodes
        drawTypeNodes(ctx)
    }
    
    function drawEnneagramFigure(ctx) {
        ctx.strokeStyle = "#e0e0e0"
        ctx.lineWidth = 1
        
        // Inner triangle (9-3-6-9)
        let triangleConnections = [
            [9, 3], [3, 6], [6, 9]
        ]
        
        // Hexad (1-4-2-8-5-7-1)
        let hexadConnections = [
            [1, 4], [4, 2], [2, 8], [8, 5], [5, 7], [7, 1]
        ]
        
        let allConnections = triangleConnections.concat(hexadConnections)
        
        for (let connection of allConnections) {
            let pos1 = typePositions[connection[0]]
            let pos2 = typePositions[connection[1]]
            
            if (pos1 && pos2) {
                ctx.beginPath()
                ctx.moveTo(pos1.x, pos1.y)
                ctx.lineTo(pos2.x, pos2.y)
                ctx.stroke()
            }
        }
    }
    
    function drawTypeNodes(ctx) {
        for (let type = 1; type <= 9; type++) {
            let pos = typePositions[type]
            if (!pos) continue
            
            let isSelected = (type === selectedType)
            
            // Node circle
            ctx.fillStyle = isSelected ? "#4CAF50" : typeColors[type - 1]
            ctx.strokeStyle = isSelected ? "#388E3C" : "#bdbdbd"
            ctx.lineWidth = isSelected ? 3 : 1
            
            ctx.beginPath()
            ctx.arc(pos.x, pos.y, nodeRadius, 0, 2 * Math.PI)
            ctx.fill()
            ctx.stroke()
            
            // Type number
            ctx.fillStyle = isSelected ? "#ffffff" : "#212121"
            ctx.font = "bold 16px Arial"
            ctx.textAlign = "center"
            ctx.textBaseline = "middle"
            ctx.fillText(type.toString(), pos.x, pos.y)
        }
    }
    
    function drawConnections() {
        let ctx = connectionsCanvas.getContext("2d")
        if (!ctx) return
        
        ctx.clearRect(0, 0, width, height)
        
        if (selectedType === 0) return
        
        // Integration and disintegration points
        let integrationMap = {
            1: 7, 2: 4, 3: 6, 4: 1, 5: 8,
            6: 9, 7: 5, 8: 2, 9: 3
        }
        
        let disintegrationMap = {
            1: 4, 2: 8, 3: 9, 4: 2, 5: 7,
            6: 3, 7: 1, 8: 5, 9: 6
        }
        
        let selectedPos = typePositions[selectedType]
        if (!selectedPos) return
        
        // Draw integration line (green)
        let integrationPoint = integrationMap[selectedType]
        if (integrationPoint) {
            let integrationPos = typePositions[integrationPoint]
            if (integrationPos) {
                drawArrow(ctx, selectedPos, integrationPos, "#4CAF50", "Integration")
            }
        }
        
        // Draw disintegration line (red)
        let disintegrationPoint = disintegrationMap[selectedType]
        if (disintegrationPoint) {
            let disintegrationPos = typePositions[disintegrationPoint]
            if (disintegrationPos) {
                drawArrow(ctx, selectedPos, disintegrationPos, "#F44336", "Stress")
            }
        }
    }
    
    function drawArrow(ctx, from, to, color, label) {
        ctx.strokeStyle = color
        ctx.fillStyle = color
        ctx.lineWidth = 3
        ctx.setLineDash([5, 5])
        
        // Draw line
        ctx.beginPath()
        ctx.moveTo(from.x, from.y)
        ctx.lineTo(to.x, to.y)
        ctx.stroke()
        
        // Draw arrowhead
        let angle = Math.atan2(to.y - from.y, to.x - from.x)
        let arrowLength = 15
        let arrowAngle = Math.PI / 6
        
        ctx.setLineDash([])
        ctx.beginPath()
        ctx.moveTo(to.x, to.y)
        ctx.lineTo(
            to.x - arrowLength * Math.cos(angle - arrowAngle),
            to.y - arrowLength * Math.sin(angle - arrowAngle)
        )
        ctx.lineTo(
            to.x - arrowLength * Math.cos(angle + arrowAngle),
            to.y - arrowLength * Math.sin(angle + arrowAngle)
        )
        ctx.closePath()
        ctx.fill()
        
        // Draw label
        let midX = (from.x + to.x) / 2
        let midY = (from.y + to.y) / 2
        
        ctx.fillStyle = "#ffffff"
        ctx.strokeStyle = color
        ctx.lineWidth = 1
        ctx.font = "bold 10px Arial"
        ctx.textAlign = "center"
        ctx.textBaseline = "middle"
        
        // Background for label
        let textWidth = ctx.measureText(label).width
        ctx.fillRect(midX - textWidth/2 - 4, midY - 8, textWidth + 8, 16)
        ctx.strokeRect(midX - textWidth/2 - 4, midY - 8, textWidth + 8, 16)
        
        ctx.fillStyle = color
        ctx.fillText(label, midX, midY)
    }
    
    function getTypeAtPosition(x, y) {
        for (let type = 1; type <= 9; type++) {
            let pos = typePositions[type]
            if (!pos) continue
            
            let distance = Math.sqrt(Math.pow(x - pos.x, 2) + Math.pow(y - pos.y, 2))
            if (distance <= nodeRadius) {
                return type
            }
        }
        return 0
    }
    
    function selectType(type) {
        if (type !== selectedType) {
            selectedType = type
            
            // Redraw canvases
            wheelCanvas.requestPaint()
            connectionsCanvas.requestPaint()
            
            // Emit signal
            typeSelected(type)
        }
    }
    
    // Public methods
    function setSelectedType(type) {
        selectType(type)
    }
    
    function getSelectedType() {
        return selectedType
    }
    
    // Component initialization
    Component.onCompleted: {
        typePositions = calculateTypePositions()
        wheelCanvas.requestPaint()
    }
    
    // Handle size changes
    onWidthChanged: {
        typePositions = calculateTypePositions()
        wheelCanvas.requestPaint()
        connectionsCanvas.requestPaint()
    }
    
    onHeightChanged: {
        typePositions = calculateTypePositions()
        wheelCanvas.requestPaint()
        connectionsCanvas.requestPaint()
    }
}