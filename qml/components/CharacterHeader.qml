/**
 * CharacterHeader.qml
 * Header component showing character's basic information
 * Includes image, name, level, and quick actions
 */
import QtQuick 6.9
import QtQuick.Controls 6.9
import QtQuick.Layouts 6.9
import QtQuick.Dialogs 6.9
import "../styles"

// import App.Styles

Rectangle {
    id: characterHeader

    // Public properties
    property var characterModel
    property bool editMode: false
    property bool imageUploadEnabled: true

    // Visual properties
    property real imageSize: 120

    // Signals
    signal imageChangeRequested
    signal nameChanged(string newName)
    signal levelChanged(int newLevel)
    signal editModeToggled

    // Styling
    color: AppTheme.card.background
    border.color: AppTheme.card.border
    border.width: AppTheme.borderWidth
    radius: AppTheme.radius.medium

    implicitHeight: contentLayout.implicitHeight + 2 * AppTheme.spacing.large

    RowLayout {
        id: contentLayout
        anchors.fill: parent
        anchors.margins: AppTheme.spacing.large
        spacing: AppTheme.spacing.large

        // Character image section
        Item {
            Layout.preferredWidth: imageSize
            Layout.preferredHeight: imageSize
            Layout.alignment: Qt.AlignTop

            // Image container with drop shadow effect
            Rectangle {
                id: imageContainer
                anchors.fill: parent
                radius: 8
                color: "transparent"

                // Drop shadow
                Rectangle {
                    anchors.fill: parent
                    anchors.margins: -2
                    radius: parent.radius + 2
                    color: "transparent"
                    border.color: AppTheme.colors.shadow
                    border.width: 1
                    opacity: 0.2
                    z: -1
                }

                // Actual image
                Rectangle {
                    id: imageBackground
                    anchors.fill: parent
                    radius: 8
                    color: AppTheme.colors.backgroundVariant
                    border.color: AppTheme.colors.border
                    border.width: 2

                    Image {
                        id: characterImage
                        anchors.fill: parent
                        anchors.margins: 2
                        fillMode: Image.PreserveAspectCrop
                        source: getImageSource()

                        // Placeholder when no image
                        Rectangle {
                            anchors.fill: parent
                            visible: characterImage.status !== Image.Ready
                            color: AppTheme.colors.backgroundVariant
                            radius: 6

                            Text {
                                anchors.centerIn: parent
                                text: getInitials()
                                font.family: AppTheme.fontFamily
                                font.pixelSize: imageSize * 0.3
                                font.bold: true
                                color: AppTheme.colors.textSecondary
                            }
                        }

                        // Loading indicator
                        BusyIndicator {
                            anchors.centerIn: parent
                            running: characterImage.status === Image.Loading
                            visible: running
                        }
                    }

                    // Edit overlay
                    Rectangle {
                        anchors.fill: parent
                        radius: parent.radius
                        color: "black"
                        opacity: editMode && imageMouseArea.containsMouse ? 0.5 : 0
                        visible: opacity > 0

                        Behavior on opacity {
                            NumberAnimation {
                                duration: 150
                            }
                        }

                        Text {
                            anchors.centerIn: parent
                            text: qsTr("Change Image")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            font.bold: true
                            color: "white"
                            visible: parent.opacity > 0
                        }
                    }

                    // Mouse area for image interaction
                    MouseArea {
                        id: imageMouseArea
                        anchors.fill: parent
                        hoverEnabled: editMode && imageUploadEnabled
                        cursorShape: editMode && imageUploadEnabled ? Qt.PointingHandCursor : Qt.ArrowCursor

                        onClicked: {
                            if (editMode && imageUploadEnabled) {
                                imageDialog.open();
                            }
                        }
                    }
                }
            }

            // Level badge
            Rectangle {
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: -8
                width: 40
                height: 24
                radius: 12
                color: AppTheme.colors.accent
                border.color: "white"
                border.width: 2

                Text {
                    anchors.centerIn: parent
                    text: characterModel ? characterModel.level.toString() : "1"
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    font.bold: true
                    color: "white"
                }
            }
        }

        // Character information section
        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter
            spacing: AppTheme.spacing.small

            // Name section
            RowLayout {
                Layout.fillWidth: true
                spacing: AppTheme.spacing.medium

                // Name display/edit
                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: editMode ? nameEdit.implicitHeight : nameDisplay.implicitHeight

                    // Display mode
                    Text {
                        id: nameDisplay
                        anchors.fill: parent
                        text: characterModel ? characterModel.name : qsTr("Unnamed Character")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.medium
                        font.bold: true
                        color: AppTheme.colors.text
                        elide: Text.ElideRight
                        verticalAlignment: Text.AlignVCenter
                        visible: !editMode
                    }

                    // Edit mode
                    TextField {
                        id: nameEdit
                        anchors.fill: parent
                        text: characterModel ? characterModel.name : ""
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.medium
                        font.bold: true
                        visible: editMode

                        background: Rectangle {
                            color: AppTheme.input.background
                            border.color: AppTheme.colors.border
                            border.width: 1
                            radius: 4
                        }

                        onEditingFinished: {
                            if (characterModel && text !== characterModel.name) {
                                nameChanged(text);
                            }
                        }

                        Keys.onReturnPressed: focus = false
                        Keys.onEnterPressed: focus = false
                        Keys.onEscapePressed: {
                            text = characterModel ? characterModel.name : "";
                            focus = false;
                        }
                    }
                }

                // Edit button
                Button {
                    text: editMode ? qsTr("Done") : qsTr("Edit")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium

                    background: Rectangle {
                        color: editMode ? AppTheme.colors.accent : "transparent"
                        border.color: AppTheme.colors.accent
                        border.width: 2
                        radius: 6
                        opacity: parent.hovered ? 0.8 : 1.0

                        Behavior on opacity {
                            NumberAnimation {
                                duration: 150
                            }
                        }
                    }

                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: editMode ? "white" : AppTheme.colors.accent
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    onClicked: {
                        console.log("Edit clicked");
                        editModeToggled();
                    }
                }
            }

            // Level section
            RowLayout {
                Layout.fillWidth: true
                spacing: AppTheme.spacing.medium

                Text {
                    text: qsTr("Level:")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    color: AppTheme.colors.textSecondary
                }

                // Level display/edit
                Item {
                    Layout.preferredWidth: editMode ? levelSpinBox.implicitWidth : levelDisplay.implicitWidth
                    Layout.preferredHeight: editMode ? levelSpinBox.implicitHeight : levelDisplay.implicitHeight

                    // Display mode
                    Text {
                        id: levelDisplay
                        anchors.fill: parent
                        text: characterModel ? characterModel.level.toString() : "1"
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.large
                        font.bold: true
                        color: AppTheme.colors.accent
                        verticalAlignment: Text.AlignVCenter
                        visible: !editMode
                    }

                    // Edit mode
                    SpinBox {
                        id: levelSpinBox
                        anchors.fill: parent
                        from: 1
                        to: 100
                        value: characterModel ? characterModel.level : 1
                        visible: editMode

                        background: Rectangle {
                            color: AppTheme.colors.background
                            border.color: AppTheme.colors.border
                            border.width: 1
                            radius: 4
                        }

                        onValueChanged: {
                            if (characterModel && value !== characterModel.level) {
                                levelChanged(value);
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                }
            }

            // Additional info row
            RowLayout {
                Layout.fillWidth: true
                spacing: AppTheme.spacing.large

                // Enneagram type display
                RowLayout {
                    spacing: AppTheme.spacing.small

                    Text {
                        text: qsTr("Type:")
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.medium
                        color: AppTheme.colors.textSecondary
                    }

                    Text {
                        text: getEnneagramDisplay()
                        font.family: AppTheme.fontFamily
                        font.pixelSize: AppTheme.fontSize.medium
                        font.bold: true
                        color: AppTheme.colors.text
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

                // Last modified
                Text {
                    text: qsTr("Modified: ") + getLastModified()
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: AppTheme.colors.textSecondary
                    font.italic: true
                }
            }
        }
    }

    // File dialog for image selection
    FileDialog {
        id: imageDialog
        title: qsTr("Select Character Image")
        nameFilters: ["Image files (*.png *.jpg *.jpeg *.gif *.bmp)", "All files (*)"]

        onAccepted: {
            // TODO: Handle image file selection
            // This would typically involve:
            // 1. Loading the image file
            // 2. Converting to base64
            // 3. Updating the character model
            imageChangeRequested();
        }
    }

    // Helper functions
    function getImageSource() {
        if (characterModel && characterModel.imageData) {
            return "data:image/png;base64," + characterModel.imageData;
        }
        return "";
    }

    function getInitials() {
        if (!characterModel || !characterModel.name) {
            return "?";
        }

        var words = characterModel.name.trim().split(/\\s+/);
        if (words.length === 1) {
            return words[0].charAt(0).toUpperCase();
        } else {
            return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
        }
    }

    function getEnneagramDisplay() {
        if (!characterModel) {
            return qsTr("Not set");
        }

        var type = characterModel.enneagramType || 9;
        var wing = characterModel.enneagramWing || 0;

        if (wing > 0) {
            return type + "w" + wing;
        } else {
            return qsTr("Type ") + type;
        }
    }

    function getLastModified() {
        if (characterModel && characterModel.updatedAt) {
            // Format the date nicely
            var date = new Date(characterModel.updatedAt);
            return date.toLocaleDateString() + " " + date.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        return qsTr("Unknown");
    }

    // Focus handling for edit mode
    onEditModeChanged: {
        if (editMode) {
            nameEdit.focus = true;
            nameEdit.selectAll();
        }
    }
}
