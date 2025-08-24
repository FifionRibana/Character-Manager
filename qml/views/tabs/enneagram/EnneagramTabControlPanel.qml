import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import App.Styles

import "../../../components"

ColumnLayout {
    id: iControlPanel
    spacing: AppTheme.spacing.medium

    // Properties
    property int selectedType
    property string typeName
    property string typeTitle
    property string developmentColor: getDevelopmentColor(developmentLevel)
    property string developmentLevelName
    property int integrationPoint
    property int disintegrationPoint

    // Models
    property var wingModel
    property var instinctualModel

    // Character's data
    property int wing: 9
    property int instinctualVariantIndex: 0
    property int developmentLevel: 5
    onDevelopmentLevelChanged: console.log("Forom internale", developmentLevel)

    // Signals
    signal wingChangeRequested(int newWing)
    signal instinctualVariantChangeRequested(string newInstinctualVariant)
    signal developmentLevelChangeRequested(int newDevelopmentLevel)

    // Core Type Information
    Card {
        Layout.fillWidth: true

        implicitHeight: coreTypeContent.implicitHeight + 2 * AppTheme.spacing.medium

        contentItem: ColumnLayout {
            id: coreTypeContent
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.medium
            spacing: AppTheme.spacing.small

            Text {
                text: qsTr("Core Type")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
            }

            Rectangle {
                Layout.fillWidth: true
                height: AppTheme.border.thin
                color: AppTheme.colors.border
            }

            Text {
                text: qsTr("Selected Type") + ": " + iControlPanel.typeName
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                font.bold: true
            }

            Text {
                text: iControlPanel.typeTitle
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.textSecondary
                font.italic: true
            }
        }
    }

    // Wing Selection
    Card {
        Layout.fillWidth: true

        implicitHeight: wingContent.implicitHeight + 2 * AppTheme.spacing.medium

        contentItem: ColumnLayout {
            id: wingContent
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.medium
            spacing: AppTheme.spacing.small

            Text {
                text: qsTr("Wing")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
            }

            ComboBox {
                id: wingComboBox
                Layout.fillWidth: true

                model: iControlPanel.wingModel
                textRole: "text"
                valueRole: "value"

                currentIndex: iControlPanel.wing

                background: Rectangle {
                    color: AppTheme.input.background
                    border.color: AppTheme.colors.border
                    border.width: AppTheme.border.thin
                    radius: AppTheme.radius.small
                }

                onCurrentValueChanged: iControlPanel.wingChangeRequested(currentValue)
            }

            Text {
                id: wingNotationText
                text: getWingNotation()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                font.bold: true
                color: AppTheme.colors.accent
                visible: wingComboBox.currentValue > 0
            }
        }
    }

    // Instinctual Variant
    Rectangle {
        Layout.fillWidth: true
        color: AppTheme.card.background
        border.color: AppTheme.card.border
        border.width: AppTheme.border.thin
        radius: AppTheme.radius.medium

        implicitHeight: instinctContent.implicitHeight + 2 * AppTheme.spacing.medium

        ColumnLayout {
            id: instinctContent
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.medium
            spacing: AppTheme.spacing.small

            Text {
                text: qsTr("Instinctual Variant")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
            }

            Text {
                text: qsTr("Primary instinct (most developed)")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
            }

            ComboBox {
                id: instinctComboBox
                Layout.fillWidth: true

                currentIndex: iControlPanel.instinctualVariantIndex

                model: iControlPanel.instinctualModel

                textRole: "text"
                valueRole: "value"

                background: Rectangle {
                    color: AppTheme.input.background
                    border.color: AppTheme.colors.border
                    border.width: AppTheme.border.thin
                    radius: AppTheme.radius.small
                }

                onCurrentValueChanged: iControlPanel.instinctualVariantChangeRequested(currentValue)
            }
        }
    }

    // Development Level
    Rectangle {
        Layout.fillWidth: true
        color: AppTheme.card.background
        border.color: AppTheme.card.border
        border.width: AppTheme.border.thin
        radius: AppTheme.radius.medium

        implicitHeight: developmentContent.implicitHeight + 2 * AppTheme.spacing.medium

        ColumnLayout {
            id: developmentContent
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.medium
            spacing: AppTheme.spacing.small

            Text {
                text: qsTr("Development Level")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
            }

            RowLayout {
                Layout.fillWidth: true

                Text {
                    text: qsTr("Healthy")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: "#2ecc71"
                }

                Slider {
                    id: developmentSlider
                    Layout.fillWidth: true
                    from: 1
                    to: 9
                    value: iControlPanel.developmentLevel
                    stepSize: 1
                    snapMode: Slider.SnapAlways

                    onValueChanged: iControlPanel.developmentLevelChangeRequested(value)

                    background: Rectangle {
                        x: developmentSlider.leftPadding
                        y: developmentSlider.topPadding + developmentSlider.availableHeight / 2 - height / 2
                        implicitWidth: 200
                        implicitHeight: 4
                        width: developmentSlider.availableWidth
                        height: implicitHeight
                        radius: AppTheme.radius.tiny
                        color: AppTheme.colors.border

                        Rectangle {
                            width: developmentSlider.visualPosition * parent.width
                            height: parent.height
                            color: iControlPanel.developmentColor
                            radius: AppTheme.radius.tiny
                        }
                    }

                    handle: Rectangle {
                        x: developmentSlider.leftPadding + developmentSlider.visualPosition * (developmentSlider.availableWidth - width)
                        y: developmentSlider.topPadding + developmentSlider.availableHeight / 2 - height / 2
                        implicitWidth: 20
                        implicitHeight: 20
                        radius: width / 2.
                        color: iControlPanel.developmentColor
                        border.color: AppTheme.colors.border
                        border.width: AppTheme.border.medium
                    }
                }

                Text {
                    text: qsTr("Unhealthy")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.small
                    color: "#e74c3c"
                }
            }

            Text {
                text: qsTr("Level") + " " + Math.round(developmentSlider.value) + " - " + iControlPanel.developmentLevelName
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                font.bold: true
            }
        }
    }

    // Integration/Disintegration info
    Rectangle {
        Layout.fillWidth: true
        color: AppTheme.card.background
        border.color: AppTheme.card.border
        border.width: AppTheme.border.thin
        radius: AppTheme.radius.medium

        implicitHeight: connectionContent.implicitHeight + 2 * AppTheme.spacing.medium

        ColumnLayout {
            id: connectionContent
            anchors.fill: parent
            anchors.margins: AppTheme.spacing.medium
            spacing: AppTheme.spacing.small

            Text {
                text: qsTr("Connections")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.large
                font.bold: true
                color: AppTheme.colors.text
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 2
                columnSpacing: AppTheme.spacing.medium
                rowSpacing: AppTheme.spacing.small

                Text {
                    text: qsTr("Integration (Growth):")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: AppTheme.colors.textSecondary
                }

                Text {
                    text: qsTr("Type") + " " + iControlPanel.integrationPoint
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: "#2ecc71"
                    font.bold: true
                }

                Text {
                    text: qsTr("Disintegration (Stress):")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: AppTheme.colors.textSecondary
                }

                Text {
                    text: qsTr("Type") + " " + iControlPanel.disintegrationPoint
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.medium
                    color: "#e74c3c"
                    font.bold: true
                }
            }

            Text {
                text: qsTr("Green arrows show growth direction, red arrows show stress direction")
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.small
                color: AppTheme.colors.textSecondary
                font.italic: true
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
        }
    }
    
    // Functions
    function getWingNotation() {
        if (wingComboBox.currentValue <= 0)
            return "";
        return iControlPanel.selectedType + "w" + wingComboBox.currentValue;
    }
    
    function getDevelopmentColor(level) {
        if (level <= 3)
            return "#2ecc71";      // Healthy - Green
        if (level <= 6)
            return "#f39c12";     // Average - Orange
        return "#e74c3c";                     // Unhealthy - Red
    }
}