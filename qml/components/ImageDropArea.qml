/**
 * ImageDropArea.qml
 * Drag & drop area for character images with validation and preview
 * Supports multiple image formats and provides visual feedback
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../styles"

Rectangle {
    id: imageDropArea
    
    // Public properties
    property string imageData: ""                   // Base64 image data
    property bool imageLoaded: imageData.length > 0
    property real imageSize: 120
    property bool allowDrop: true
    property bool showBrowseButton: true
    
    // Visual properties
    property real animationDuration: 200
    property color dropZoneColor: AppTheme.accentColor
    property color dragActiveColor: Qt.lighter(dropZoneColor, 1.2)
    
    // Supported image formats
    readonly property var supportedFormats: ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
    readonly property int maxFileSize: 5 * 1024 * 1024 // 5MB
    
    // Signals
    signal imageChanged(string imageData)
    signal imageCleared()
    signal dropRejected(string reason)
    signal fileSelected(url fileUrl)
    
    // Styling
    width: imageSize
    height: imageSize
    radius: 8
    color: getBackgroundColor()
    border.color: getBorderColor()
    border.width: getBorderWidth()
    
    Behavior on color {
        ColorAnimation { duration: animationDuration }
    }
    
    Behavior on border.color {
        ColorAnimation { duration: animationDuration }
    }
    
    Behavior on border.width {
        NumberAnimation { duration: animationDuration }
    }
    
    // Drop zone
    DropArea {
        id: dropArea
        anchors.fill: parent
        enabled: allowDrop
        
        onEntered: function(drag) {
            if (validateDragData(drag)) {
                drag.accept()
                parent.state = "dragActive"
            } else {
                drag.reject()
                parent.state = "dragRejected"
            }
        }
        
        onExited: {
            parent.state = ""
        }
        
        onDropped: function(drop) {
            parent.state = ""
            
            if (drop.hasUrls) {
                var url = drop.urls[0]
                if (validateImageFile(url)) {
                    handleImageDrop(url)
                    drop.accept()
                } else {
                    var reason = qsTr("Invalid image file. Supported formats: ") + supportedFormats.join(", ")
                    dropRejected(reason)
                    drop.reject()
                }
            } else {
                dropRejected(qsTr("No valid file detected"))
                drop.reject()
            }
        }
    }
    
    // Content based on state
    StackLayout {
        anchors.fill: parent
        anchors.margins: 8
        currentIndex: imageLoaded ? 1 : 0
        
        // Empty state - drop zone
        Item {
            ColumnLayout {
                anchors.centerIn: parent
                spacing: AppTheme.spacingSmall
                
                // Drop icon
                Text {
                    text: getDropIcon()
                    font.pixelSize: Math.max(24, imageSize * 0.2)
                    color: getDropIconColor()
                    Layout.alignment: Qt.AlignHCenter
                    
                    Behavior on color {
                        ColorAnimation { duration: animationDuration }
                    }
                }
                
                // Drop text
                Text {
                    text: getDropText()
                    font.family: AppTheme.fontFamily
                    font.pixelSize: Math.max(10, imageSize * 0.08)
                    color: getDropTextColor()
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    Layout.maximumWidth: parent.width - 16
                    Layout.alignment: Qt.AlignHCenter
                    
                    Behavior on color {
                        ColorAnimation { duration: animationDuration }
                    }
                }
                
                // Browse button
                Button {
                    visible: showBrowseButton
                    text: qsTr("Browse")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: Math.max(8, imageSize * 0.06)
                    Layout.alignment: Qt.AlignHCenter
                    
                    background: Rectangle {
                        color: parent.hovered ? Qt.lighter(dropZoneColor, 1.1) : dropZoneColor
                        radius: 4
                        
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
                    
                    onClicked: fileDialog.open()
                }
            }
        }
        
        // Image loaded state
        Item {
            // Actual image
            Image {
                id: displayImage
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
                source: imageData ? "data:image/png;base64," + imageData : ""
                asynchronous: true
                cache: false
                
                // Loading indicator
                BusyIndicator {
                    anchors.centerIn: parent
                    running: displayImage.status === Image.Loading
                    visible: running
                }
                
                // Error state
                Rectangle {
                    anchors.fill: parent
                    visible: displayImage.status === Image.Error
                    color: AppTheme.backgroundColorSecondary
                    
                    Text {
                        anchors.centerIn: parent
                        text: "❌\n" + qsTr("Load Error")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSizeCaption
                        color: AppTheme.textColorSecondary
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }
            
            // Image overlay with actions
            Rectangle {
                anchors.fill: parent
                color: "black"
                opacity: imageMouseArea.containsMouse ? 0.5 : 0
                radius: parent.parent.radius
                
                Behavior on opacity {
                    NumberAnimation { duration: animationDuration }
                }
                
                RowLayout {
                    anchors.centerIn: parent
                    visible: parent.opacity > 0
                    spacing: AppTheme.spacingSmall
                    
                    // Change image button
                    Button {
                        implicitWidth: 40
                        implicitHeight: 40
                        
                        background: Rectangle {
                            radius: 20
                            color: parent.hovered ? Qt.lighter("#3498db", 1.2) : "#3498db"
                            
                            Behavior on color {
                                ColorAnimation { duration: 150 }
                            }
                        }
                        
                        contentItem: Text {
                            text: "📁"
                            font.pixelSize: 20
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: fileDialog.open()
                        
                        ToolTip {
                            text: qsTr("Change Image")
                            visible: parent.hovered
                            delay: 500
                        }
                    }
                    
                    // Remove image button
                    Button {
                        implicitWidth: 40
                        implicitHeight: 40
                        
                        background: Rectangle {
                            radius: 20
                            color: parent.hovered ? Qt.lighter("#e74c3c", 1.2) : "#e74c3c"
                            
                            Behavior on color {
                                ColorAnimation { duration: 150 }
                            }
                        }
                        
                        contentItem: Text {
                            text: "🗑️"
                            font.pixelSize: 20
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: clearImage()
                        
                        ToolTip {
                            text: qsTr("Remove Image")
                            visible: parent.hovered
                            delay: 500
                        }
                    }
                }
            }
            
            // Mouse area for hover detection
            MouseArea {
                id: imageMouseArea
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton
            }
        }
    }
    
    // File dialog
    FileDialog {
        id: fileDialog
        title: qsTr("Select Character Image")
        nameFilters: [
            qsTr("Image files") + " (*.png *.jpg *.jpeg *.gif *.bmp *.webp)",
            qsTr("All files") + " (*)"
        ]
        
        onAccepted: {
            if (selectedFile) {
                fileSelected(selectedFile)
                handleImageFile(selectedFile)
            }
        }
    }
    
    // States for visual feedback
    states: [
        State {
            name: "dragActive"
            PropertyChanges {
                target: imageDropArea
                border.color: dragActiveColor
                border.width: 3
                color: Qt.rgba(dragActiveColor.r, dragActiveColor.g, dragActiveColor.b, 0.1)
            }
        },
        State {
            name: "dragRejected"
            PropertyChanges {
                target: imageDropArea
                border.color: "#e74c3c"
                border.width: 3
                color: Qt.rgba(0.9, 0.3, 0.2, 0.1)
            }
        }
    ]
    
    // Pulse animation for drag active state
    SequentialAnimation {
        id: pulseAnimation
        running: imageDropArea.state === "dragActive"
        loops: Animation.Infinite
        
        PropertyAnimation {
            target: imageDropArea
            property: "scale"
            to: 1.02
            duration: 500
            easing.type: Easing.InOutCubic
        }
        
        PropertyAnimation {
            target: imageDropArea
            property: "scale"
            to: 1.0
            duration: 500
            easing.type: Easing.InOutCubic
        }
    }
    
    // Helper functions
    function getBackgroundColor() {
        if (imageLoaded) {
            return "transparent"
        }
        
        switch (state) {
            case "dragActive":
                return Qt.rgba(dragActiveColor.r, dragActiveColor.g, dragActiveColor.b, 0.1)
            case "dragRejected":
                return Qt.rgba(0.9, 0.3, 0.2, 0.1)
            default:
                return AppTheme.backgroundColorSecondary
        }
    }
    
    function getBorderColor() {
        if (imageLoaded) {
            return AppTheme.borderColor
        }
        
        switch (state) {
            case "dragActive":
                return dragActiveColor
            case "dragRejected":
                return "#e74c3c"
            default:
                return AppTheme.borderColor
        }
    }
    
    function getBorderWidth() {
        switch (state) {
            case "dragActive":
            case "dragRejected":
                return 3
            default:
                return imageLoaded ? 1 : 2
        }
    }
    
    function getDropIcon() {
        switch (state) {
            case "dragActive":
                return "📥"
            case "dragRejected":
                return "❌"
            default:
                return "🖼️"
        }
    }
    
    function getDropText() {
        switch (state) {
            case "dragActive":
                return qsTr("Drop image here")
            case "dragRejected":
                return qsTr("Invalid file type")
            default:
                return qsTr("Drop image\nor click to browse")
        }
    }
    
    function getDropIconColor() {
        switch (state) {
            case "dragActive":
                return dragActiveColor
            case "dragRejected":
                return "#e74c3c"
            default:
                return AppTheme.textColorSecondary
        }
    }
    
    function getDropTextColor() {
        switch (state) {
            case "dragActive":
                return dragActiveColor
            case "dragRejected":
                return "#e74c3c"
            default:
                return AppTheme.textColorSecondary
        }
    }
    
    function validateDragData(drag) {
        return drag.hasUrls && drag.urls.length > 0
    }
    
    function validateImageFile(url) {
        var urlString = url.toString()
        var extension = urlString.split('.').pop().toLowerCase()
        return supportedFormats.includes(extension)
    }
    
    function handleImageDrop(url) {
        // In a real implementation, you would:
        // 1. Read the file from the URL
        // 2. Validate the file size
        // 3. Convert to base64
        // 4. Emit the imageChanged signal
        
        // For now, we'll simulate this
        console.log("Image dropped:", url)
        // TODO: Implement actual file reading and base64 conversion
    }
    
    function handleImageFile(url) {
        // Similar to handleImageDrop but from file dialog
        console.log("Image selected:", url)
        // TODO: Implement actual file reading and base64 conversion
    }
    
    function clearImage() {
        imageData = ""
        imageCleared()
    }
    
    function setImageData(base64Data) {
        imageData = base64Data
        imageChanged(base64Data)
    }
    
    // Property change handler
    onImageDataChanged: {
        // Emit signal when image data changes externally
        if (imageData !== "") {
            imageChanged(imageData)
        }
    }
}