/**
 * EnneagramWheel.qml
 * Interactive Enneagram wheel component with Canvas rendering
 * Complete implementation with visual feedback and animations
 */
import QtQuick 6.9
import QtQuick.Controls 6.9
// import "../styles"
import App.Styles

Item {
    id: enneagramWheel

    // Public properties
    property int selectedType: 9
    property real animationDuration: 200
    property bool showConnections: true
    property bool interactiveMode: true

    // Computed properties
    readonly property real wheelSize: Math.min(width, height) - 60
    readonly property real centerX: width / 2
    readonly property real centerY: height / 2
    readonly property real outerRadius: wheelSize / 2
    readonly property real innerRadius: outerRadius * 0.6
    readonly property real nodeRadius: 22

    // Signals
    signal typeSelected(int enneagramType)
    signal typeHovered(int enneagramType)

    // Colors for each type (following Enneagram tradition)
    readonly property var typeColors: [""           // Index 0 (unused)
        , "#e74c3c"    // Type 1 - Red (Reformer)
        , "#3498db"    // Type 2 - Blue (Helper)
        , "#f39c12"    // Type 3 - Orange (Achiever)
        , "#9b59b6"    // Type 4 - Purple (Individualist)
        , "#2ecc71"    // Type 5 - Green (Investigator)
        , "#e67e22"    // Type 6 - Dark Orange (Loyalist)
        , "#f1c40f"    // Type 7 - Yellow (Enthusiast)
        , "#34495e"    // Type 8 - Dark Blue (Challenger)
        , "#95a5a6"     // Type 9 - Gray (Peacemaker)
    ]

    // Type positions calculated dynamically
    property var typePositions: ({})

    // Background wheel
    Canvas {
        id: wheelCanvas
        anchors.fill: parent

        onPaint: {
            drawWheel();
        }

        function drawWheel() {
            var ctx = getContext("2d");
            if (!ctx)
                return;
            ctx.clearRect(0, 0, width, height);

            // Anti-aliasing
            ctx.imageSmoothingEnabled = true;

            // Draw outer circle
            ctx.strokeStyle = AppTheme.colors.border;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(centerX, centerY, outerRadius, 0, 2 * Math.PI);
            ctx.stroke();

            // Draw inner triangle and hexagon (traditional Enneagram symbol)
            drawEnneagramSymbol(ctx);
        }

        function drawEnneagramSymbol(ctx) {
            // Draw the inner triangle (3-6-9)
            ctx.strokeStyle = AppTheme.colors.border;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([5, 3]);

            var trianglePoints = [3, 6, 9];
            ctx.beginPath();
            for (var i = 0; i < trianglePoints.length; i++) {
                var currentType = trianglePoints[i];
                var nextType = trianglePoints[(i + 1) % trianglePoints.length];

                var pos1 = getTypePosition(currentType);
                var pos2 = getTypePosition(nextType);

                if (i === 0) {
                    ctx.moveTo(pos1.x, pos1.y);
                }
                ctx.lineTo(pos2.x, pos2.y);
            }
            ctx.closePath();
            ctx.stroke();

            // Draw the hexagon (1-4-2-8-5-7)
            ctx.strokeStyle = AppTheme.colors.borderLight;
            ctx.lineWidth = 1;
            ctx.setLineDash([3, 2]);

            var hexagonSequence = [1, 4, 2, 8, 5, 7];
            ctx.beginPath();
            for (var j = 0; j < hexagonSequence.length; j++) {
                var currentHexType = hexagonSequence[j];
                var nextHexType = hexagonSequence[(j + 1) % hexagonSequence.length];

                var hexPos1 = getTypePosition(currentHexType);
                var hexPos2 = getTypePosition(nextHexType);

                if (j === 0) {
                    ctx.moveTo(hexPos1.x, hexPos1.y);
                }
                ctx.lineTo(hexPos2.x, hexPos2.y);
            }
            ctx.closePath();
            ctx.stroke();

            // Reset line dash
            ctx.setLineDash([]);
        }
    }

    // Connection lines (integration/disintegration)
    Canvas {
        id: connectionsCanvas
        anchors.fill: parent
        visible: showConnections && selectedType > 0

        onPaint: {
            if (selectedType > 0) {
                drawConnections();
            }
        }

        function drawConnections() {
            var ctx = getContext("2d");
            if (!ctx)
                return;
            ctx.clearRect(0, 0, width, height);

            // Draw integration line (growth direction)
            var integrationPoint = getIntegrationPoint(selectedType);
            if (integrationPoint > 0) {
                drawConnectionLine(ctx, selectedType, integrationPoint, "#2ecc71", 3);
            }

            // Draw disintegration line (stress direction)
            var disintegrationPoint = getDisintegrationPoint(selectedType);
            if (disintegrationPoint > 0) {
                drawConnectionLine(ctx, selectedType, disintegrationPoint, "#e74c3c", 3);
            }
        }

        function drawConnectionLine(ctx, fromType, toType, color, lineWidth) {
            var fromPos = getTypePosition(fromType);
            var toPos = getTypePosition(toType);

            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.setLineDash([8, 4]);

            ctx.beginPath();
            ctx.moveTo(fromPos.x, fromPos.y);
            ctx.lineTo(toPos.x, toPos.y);
            ctx.stroke();

            // Draw arrow head
            var angle = Math.atan2(toPos.y - fromPos.y, toPos.x - fromPos.x);
            var arrowLength = 12;
            var arrowAngle = Math.PI / 6;

            ctx.setLineDash([]);
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.moveTo(toPos.x, toPos.y);
            ctx.lineTo(toPos.x - arrowLength * Math.cos(angle - arrowAngle), toPos.y - arrowLength * Math.sin(angle - arrowAngle));
            ctx.lineTo(toPos.x - arrowLength * Math.cos(angle + arrowAngle), toPos.y - arrowLength * Math.sin(angle + arrowAngle));
            ctx.closePath();
            ctx.fill();
        }
    }

    // Type nodes
    Repeater {
        model: 9

        delegate: Item {
            id: typeNode
            property int typeNumber: index + 1
            property var position: getTypePosition(typeNumber)
            property bool isSelected: selectedType === typeNumber
            property bool isHovered: false

            x: position.x - nodeRadius
            y: position.y - nodeRadius
            width: nodeRadius * 2
            height: nodeRadius * 2

            Rectangle {
                id: nodeBackground
                anchors.fill: parent
                radius: nodeRadius
                color: isSelected ? typeColors[typeNumber] : isHovered ? Qt.lighter(typeColors[typeNumber], 1.3) : Qt.lighter(typeColors[typeNumber], 1.6)
                border.color: isSelected ? Qt.darker(typeColors[typeNumber], 1.2) : typeColors[typeNumber]
                border.width: isSelected ? 3 : 2

                Behavior on color {
                    ColorAnimation {
                        duration: animationDuration
                    }
                }

                Behavior on border.width {
                    NumberAnimation {
                        duration: animationDuration
                    }
                }

                // Subtle shadow effect
                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 2
                    radius: parent.radius - 2
                    color: "transparent"
                    border.color: "white"
                    border.width: isSelected ? 2 : 1
                    opacity: isSelected ? 0.7 : 0.3

                    Behavior on opacity {
                        NumberAnimation {
                            duration: animationDuration
                        }
                    }
                }
            }

            Text {
                id: nodeText
                anchors.centerIn: parent
                text: typeNumber.toString()
                font.family: AppTheme.fontFamily
                font.pixelSize: isSelected ? 16 : 14
                font.bold: true
                color: isSelected ? "white" : AppTheme.colors.text

                Behavior on font.pixelSize {
                    NumberAnimation {
                        duration: animationDuration
                    }
                }

                Behavior on color {
                    ColorAnimation {
                        duration: animationDuration
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                enabled: interactiveMode
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    selectType(typeNumber);
                }

                onEntered: {
                    parent.isHovered = true;
                    typeHovered(typeNumber);
                }

                onExited: {
                    parent.isHovered = false;
                    typeHovered(0);
                }
            }

            // Scale animation for selection
            scale: isSelected ? 1.1 : (isHovered ? 1.05 : 1.0)

            Behavior on scale {
                NumberAnimation {
                    duration: animationDuration
                    easing.type: Easing.OutCubic
                }
            }
        }
    }

    // Center dot
    Rectangle {
        x: centerX - 4
        y: centerY - 4
        width: 8
        height: 8
        radius: 4
        color: AppTheme.colors.accent
        border.color: "white"
        border.width: 1
    }

    // Public functions
    function getTypePosition(type) {
        if (typePositions[type]) {
            return typePositions[type];
        }

        // Calculate position for type (Type 9 at top, clockwise)
        var typeOrder = [9, 1, 2, 3, 4, 5, 6, 7, 8];
        var index = typeOrder.indexOf(type);
        if (index === -1)
            return {
                x: centerX,
                y: centerY
            };

        var angle = -90 + (index * 40); // 360/9 = 40 degrees
        var radian = angle * Math.PI / 180;
        var x = centerX + outerRadius * Math.cos(radian);
        var y = centerY + outerRadius * Math.sin(radian);

        return {
            x: x,
            y: y
        };
    }

    function selectType(type) {
        if (type !== selectedType && type >= 1 && type <= 9) {
            selectedType = type;
            wheelCanvas.requestPaint();
            connectionsCanvas.requestPaint();
            typeSelected(type);
        }
    }

    function getIntegrationPoint(type) {
        var integrations = {
            1: 7,
            2: 4,
            3: 6,
            4: 1,
            5: 8,
            6: 9,
            7: 5,
            8: 2,
            9: 3
        };
        return integrations[type] || 0;
    }

    function getDisintegrationPoint(type) {
        var disintegrations = {
            1: 4,
            2: 8,
            3: 9,
            4: 2,
            5: 7,
            6: 3,
            7: 1,
            8: 5,
            9: 6
        };
        return disintegrations[type] || 0;
    }

    // Component initialization
    Component.onCompleted: {
        // Pre-calculate all positions
        for (var i = 1; i <= 9; i++) {
            typePositions[i] = getTypePosition(i);
        }
        wheelCanvas.requestPaint();
    }

    // Handle resize
    onWidthChanged: Qt.callLater(recalculatePositions)
    onHeightChanged: Qt.callLater(recalculatePositions)

    function recalculatePositions() {
        for (var i = 1; i <= 9; i++) {
            typePositions[i] = getTypePosition(i);
        }
        wheelCanvas.requestPaint();
        connectionsCanvas.requestPaint();
    }
}
