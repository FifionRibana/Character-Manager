/**
 * ErrorDialog.qml
 * Reusable error dialog component with different severity levels
 * Features contextual icons, actions, and detailed error information
 */
import QtQuick 6.9
import QtQuick.Controls 6.9
import QtQuick.Layouts 6.9
import "../styles"

// import App.Styles

Dialog {
    id: errorDialog

    // Public properties
    property string errorTitle: qsTr("Error")
    property string errorMessage: ""
    property string errorDetails: ""
    property string errorType: "error"  // "error", "warning", "info"
    property bool showDetails: false
    property bool canRetry: false
    property bool canIgnore: false

    // Visual properties
    readonly property color errorColor: getErrorColor()
    readonly property string errorIcon: getErrorIcon()

    // Signals
    signal retryRequested
    signal ignoreRequested
    signal detailsRequested

    // Dialog configuration
    title: errorTitle
    modal: true
    anchors.centerIn: parent
    width: Math.min(parent.width * 0.8, 600)
    height: Math.min(parent.height * 0.8, showDetails ? 500 : 300)

    background: Rectangle {
        color: AppTheme.card.background
        border.color: errorColor
        border.width: 2
        radius: 12

        // Subtle glow effect
        Rectangle {
            anchors.fill: parent
            anchors.margins: -4
            color: "transparent"
            border.color: errorColor
            border.width: 1
            radius: 16
            opacity: 0.3
            z: -1
        }
    }

    header: Rectangle {
        color: Qt.rgba(errorColor.r, errorColor.g, errorColor.b, 0.1)
        height: 60
        radius: 12

        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: parent.height / 2
            color: parent.color
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.large
            spacing: AppTheme.spacing.medium

            // Error icon
            Rectangle {
                width: 40
                height: 40
                radius: 20
                color: errorColor

                Text {
                    anchors.centerIn: parent
                    text: errorIcon
                    font.pixelSize: 24
                    color: "white"
                }
            }

            // Error title
            Text {
                text: errorTitle
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
                Layout.fillWidth: true
                elide: Text.ElideRight
            }

            // Close button
            Button {
                implicitWidth: 32
                implicitHeight: 32

                background: Rectangle {
                    radius: 16
                    color: parent.hovered ? Qt.rgba(0, 0, 0, 0.1) : "transparent"

                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                contentItem: Text {
                    text: "×"
                    font.pixelSize: 20
                    font.bold: true
                    color: AppTheme.colors.textSecondary
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: errorDialog.reject()
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: AppTheme.spacing.large
        spacing: AppTheme.spacing.medium

        // Main error message
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: showDetails ? 100 : 150
            Layout.minimumHeight: 60

            TextArea {
                text: errorMessage
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                wrapMode: TextArea.Wrap
                readOnly: true
                selectByMouse: true

                background: Rectangle {
                    color: AppTheme.colors.backgroundVariant
                    border.color: AppTheme.colors.borderLight
                    border.width: 1
                    radius: 6
                }
            }
        }

        // Error details section (collapsible)
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: AppTheme.spacing.small
            visible: errorDetails.length > 0

            Button {
                text: showDetails ? qsTr("Hide Details") : qsTr("Show Details")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                Layout.alignment: Qt.AlignLeft

                background: Rectangle {
                    color: parent.hovered ? Qt.rgba(0, 0, 0, 0.05) : "transparent"
                    border.color: AppTheme.colors.border
                    border.width: 1
                    radius: 4
                }

                contentItem: RowLayout {
                    spacing: AppTheme.spacing.small

                    Text {
                        text: parent.parent.text
                        font: parent.parent.font
                        color: AppTheme.colors.text
                    }

                    Text {
                        text: showDetails ? "▼" : "▶"
                        font.pixelSize: AppTheme.fontSize.medium
                        color: AppTheme.colors.textSecondary

                        Behavior on rotation {
                            NumberAnimation {
                                duration: 200
                            }
                        }
                    }
                }

                onClicked: {
                    showDetails = !showDetails;
                    detailsRequested();
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: showDetails

                TextArea {
                    text: errorDetails
                    font.family: "Consolas, Monaco, monospace"
                    font.pixelSize: AppTheme.fontSize.medium
                    color: AppTheme.colors.textSecondary
                    wrapMode: TextArea.Wrap
                    readOnly: true
                    selectByMouse: true

                    background: Rectangle {
                        color: AppTheme.card.background
                        border.color: AppTheme.colors.border
                        border.width: 1
                        radius: 6
                    }
                }
            }
        }

        // Action buttons
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: AppTheme.spacing.medium

            // Copy error button
            Button {
                text: qsTr("Copy Error")
                visible: errorMessage.length > 0 || errorDetails.length > 0

                background: Rectangle {
                    color: parent.hovered ? Qt.lighter(AppTheme.colors.border, 1.1) : AppTheme.colors.border
                    radius: 6

                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: AppTheme.colors.text
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: copyErrorToClipboard()

                ToolTip {
                    text: qsTr("Copy error information to clipboard")
                    visible: parent.hovered
                    delay: 500
                }
            }

            Item {
                Layout.fillWidth: true
            }

            // Ignore button
            Button {
                text: qsTr("Ignore")
                visible: canIgnore

                background: Rectangle {
                    color: parent.hovered ? Qt.lighter("#95a5a6", 1.1) : "#95a5a6"
                    radius: 6

                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    ignoreRequested();
                    errorDialog.reject();
                }
            }

            // Retry button
            Button {
                text: qsTr("Retry")
                visible: canRetry

                background: Rectangle {
                    color: parent.hovered ? Qt.lighter("#f39c12", 1.1) : "#f39c12"
                    radius: 6

                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: {
                    retryRequested();
                    errorDialog.accept();
                }
            }

            // OK/Close button
            Button {
                text: qsTr("OK")

                background: Rectangle {
                    color: parent.hovered ? Qt.lighter(errorColor, 1.1) : errorColor
                    radius: 6

                    Behavior on color {
                        ColorAnimation {
                            duration: 150
                        }
                    }
                }

                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                onClicked: errorDialog.accept()
            }
        }
    }

    // Entrance animation
    enter: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "scale"
                from: 0.8
                to: 1.0
                duration: 200
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                property: "opacity"
                from: 0.0
                to: 1.0
                duration: 200
            }
        }
    }

    // Exit animation
    exit: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "scale"
                from: 1.0
                to: 0.8
                duration: 150
                easing.type: Easing.InCubic
            }
            NumberAnimation {
                property: "opacity"
                from: 1.0
                to: 0.0
                duration: 150
            }
        }
    }

    // Helper functions
    function getErrorColor() {
        switch (errorType) {
        case "warning":
            return "#f39c12";  // Orange
        case "info":
            return "#3498db";  // Blue
        case "success":
            return "#2ecc71";  // Green
        case "error":
        default:
            return "#e74c3c";  // Red
        }
    }

    function getErrorIcon() {
        switch (errorType) {
        case "warning":
            return "⚠️";
        case "info":
            return "ℹ️";
        case "success":
            return "✅";
        case "error":
        default:
            return "❌";
        }
    }

    function copyErrorToClipboard() {
        var errorInfo = "Error: " + errorTitle + "\n\n";
        errorInfo += "Message: " + errorMessage + "\n\n";

        if (errorDetails.length > 0) {
            errorInfo += "Details:\n" + errorDetails + "\n\n";
        }

        errorInfo += "Time: " + new Date().toLocaleString();

        // In a real implementation, you would copy to clipboard
        // For QML, this would typically be handled by the controller
        console.log("Error info copied:", errorInfo);
    }

    // Public methods for easy usage
    function showError(title, message, details) {
        errorType = "error";
        errorTitle = title;
        errorMessage = message;
        errorDetails = details || "";
        showDetails = false;
        canRetry = false;
        canIgnore = false;
        open();
    }

    function showWarning(title, message, details) {
        errorType = "warning";
        errorTitle = title;
        errorMessage = message;
        errorDetails = details || "";
        showDetails = false;
        canRetry = false;
        canIgnore = true;
        open();
    }

    function showInfo(title, message, details) {
        errorType = "info";
        errorTitle = title;
        errorMessage = message;
        errorDetails = details || "";
        showDetails = false;
        canRetry = false;
        canIgnore = false;
        open();
    }

    function showRetryableError(title, message, details) {
        errorType = "error";
        errorTitle = title;
        errorMessage = message;
        errorDetails = details || "";
        showDetails = false;
        canRetry = true;
        canIgnore = true;
        open();
    }
}
