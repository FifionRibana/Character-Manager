/**
 * EnneagramTab.qml
 * Complete Enneagram personality editing tab
 * Includes enneagramWheelPanel and all psychological aspects
 */
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"
import "./tabs/enneagram"

import App.Styles

ScrollView {
    id: enneagramTab

    property var characterModel

    property int selectedType: characterModel && characterModel.enneagramType !== undefined ? characterModel.enneagramType : 9
    property int wing: characterModel && characterModel.enneagramWing !== undefined ? characterModel.enneagramWing : 0
    property int instinctualVariantIndex: characterModel && characterModel.instinct !== undefined ? getInstinctualVariantIndex(characterModel.instinct) : 0
    property int developmentLevel: characterModel && characterModel.developmentLevel !== undefined ? characterModel.developmentLevel : 5

    contentWidth: availableWidth
    clip: true

    property var instinctualModel: [
        {
            text: qsTr("Self-Preservation (SP)"),
            value: "sp"
        },
        {
            text: qsTr("Social (SO)"),
            value: "so"
        },
        {
            text: qsTr("Sexual/One-to-One (SX)"),
            value: "sx"
        }
    ]

    // Quick help button
    // Button {
    //     text: "?"
    //     anchors.right: parent.right
    //     anchors.top: parent.top
    //     implicitWidth: 32
    //     implicitHeight: 32
    //     font.bold: true

    //     z: 1

    //     background: Rectangle {
    //         radius: 16
    //         color: AppTheme.colors.accent
    //         opacity: parent.hovered ? 0.8 : 0.6

    //         Behavior on opacity {
    //             NumberAnimation {
    //                 duration: 150
    //             }
    //         }
    //     }

    //     contentItem: Text {
    //         text: parent.text
    //         font: parent.font
    //         color: "white"
    //         horizontalAlignment: Text.AlignHCenter
    //         verticalAlignment: Text.AlignVCenter
    //     }

    //     onClicked: helpPopup.open()
    // }

    ColumnLayout {
        width: enneagramTab.availableWidth
        spacing: AppTheme.spacing.small

        // Main content
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.large

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.topMargin: AppTheme.margin.small

            // Left panel - Enneagram Wheel
            EnneagramTabWheelPanel {
                id: enneagramWheelPanel

                selectedType: enneagramTab.selectedType

                Layout.preferredWidth: 480
                Layout.preferredHeight: 480
                Layout.alignment: Qt.AlignTop
                
                onTypeSelected: function (type) {
                    if (characterModel) {
                        characterModel.enneagramType = type;
                        updateWingOptions();
                    }
                }

                onTypeHovered: function (type) {
                    if (type > 0) {
                        enneagramWheelPanel.typeInfo = getTypeDescription(type);
                    } else {
                        enneagramWheelPanel.typeInfo = qsTr("Hover over a type to see its description");
                    }
                }
            }

            // Right panel - Controls and details
            EnneagramTabControlPanel {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                selectedType: enneagramTab.selectedType
                wing: enneagramTab.wing
                instinctualVariantIndex: enneagramTab.instinctualVariantIndex
                developmentLevel: enneagramTab.developmentLevel

                typeName: getTypeName(selectedType)
                typeTitle: getTypeTitle(selectedType)
                developmentLevelName: getDevelopmentLevelName(Math.round(developmentLevel))
                developmentColor: getDevelopmentColor(developmentLevel)
                integrationPoint: getIntegrationPoint(selectedType)
                disintegrationPoint: getDisintegrationPoint(selectedType)

                wingModel: iWingModel
                instinctualModel: enneagramTab.instinctualModel
                
                onWingChangeRequested: function(newWing) {
                    if (characterModel && newWing !== undefined) {
                        characterModel.enneagramWing = newWing;
                    }
                }

                onInstinctualVariantChangeRequested: function (newInstinctualVariant) {
                    if (characterModel && newInstinctualVariant !== undefined) {
                        characterModel.instinct = newInstinctualVariant;
                    }
                }

                onDevelopmentLevelChangeRequested: function(newDevelopmentLevel) {
                    if (characterModel && newDevelopmentLevel !== undefined) {
                        characterModel.developmentLevel = newDevelopmentLevel;
                    }
                }
            }
        }

        EnneagramTabFooter {
            Layout.fillWidth: true

            Layout.leftMargin: AppTheme.margin.small
            Layout.rightMargin: AppTheme.margin.small
            Layout.bottomMargin: AppTheme.margin.small
        }
    }

    // Wing model for ComboBox
    ListModel {
        id: iWingModel

        ListElement {
            text: "No Wing"
            value: 0
        }
        // Will be populated based on selected type
    }

    // Help popup
    Popup {
        id: helpPopup
        anchors.centerIn: parent
        width: Math.min(parent.width * 0.8, 600)
        height: Math.min(parent.height * 0.8, 500)
        modal: true
        focus: true

        background: Rectangle {
            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: 2
            radius: 8
        }

        ScrollView {
            anchors.fill: parent
            anchors.margins: 20

            Text {
                width: helpPopup.width - 40
                text: getEnneagramHelp()
                font.family: AppTheme.fontFamily
                font.pixelSize: AppTheme.fontSize.medium
                color: AppTheme.colors.text
                wrapMode: Text.WordWrap
            }
        }
    }

    // Functions
    function updateWingOptions() {
        iWingModel.clear();
        iWingModel.append({
            text: qsTr("No Wing"),
            value: 0
        });

        var type = enneagramTab.selectedType;
        var leftWing = type === 1 ? 9 : type - 1;
        var rightWing = type === 9 ? 1 : type + 1;

        iWingModel.append({
            text: qsTr("Wing") + " " + leftWing,
            value: leftWing
        });
        iWingModel.append({
            text: qsTr("Wing") + " " + rightWing,
            value: rightWing
        });
    }

    function getInstinctualVariantIndex(value) {
        var instinctualVariant = {
            "sp": 0,
            "so": 1,
            "sx": 2
        }
        return instinctualVariant[value] || 0
    }

    function getTypeName(type) {
        var names = {
            1: qsTr("Type 1"),
            2: qsTr("Type 2"),
            3: qsTr("Type 3"),
            4: qsTr("Type 4"),
            5: qsTr("Type 5"),
            6: qsTr("Type 6"),
            7: qsTr("Type 7"),
            8: qsTr("Type 8"),
            9: qsTr("Type 9")
        };
        return names[type] || qsTr("Unknown");
    }

    function getTypeTitle(type) {
        var titles = {
            1: qsTr("The Reformer"),
            2: qsTr("The Helper"),
            3: qsTr("The Achiever"),
            4: qsTr("The Individualist"),
            5: qsTr("The Investigator"),
            6: qsTr("The Loyalist"),
            7: qsTr("The Enthusiast"),
            8: qsTr("The Challenger"),
            9: qsTr("The Peacemaker")
        };
        return titles[type] || "";
    }

    function getTypeDescription(type) {
        var descriptions = {
            1: qsTr("Rational, idealistic, principled, purposeful, self-controlled, and perfectionistic."),
            2: qsTr("Caring, interpersonal, demonstrative, generous, people-pleasing, and possessive."),
            3: qsTr("Success-oriented, pragmatic, adaptive, driven, image-conscious, and hostility."),
            4: qsTr("Sensitive, introspective, expressive, dramatic, self-absorbed, and temperamental."),
            5: qsTr("Intense, cerebral, perceptive, innovative, secretive, and isolated."),
            6: qsTr("Committed, security-oriented, engaging, responsible, anxious, and suspicious."),
            7: qsTr("Spontaneous, versatile, acquisitive, scattered, enthusiastic, and escapist."),
            8: qsTr("Self-confident, decisive, willful, confrontational, controlling, and intense."),
            9: qsTr("Receptive, reassuring, complacent, resigned, passive-aggressive, and stubborn.")
        };
        return descriptions[type] || "";
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


    function getDevelopmentLevelName(level) {
        var names = {
            1: qsTr("Liberation"),
            2: qsTr("Psychological Capacity"),
            3: qsTr("Social Value"),
            4: qsTr("Imbalance"),
            5: qsTr("Interpersonal Control"),
            6: qsTr("Overcompensation"),
            7: qsTr("Violation"),
            8: qsTr("Obsession"),
            9: qsTr("Pathological")
        };
        return names[level] || "";
    }

    function getEnneagramHelp() {
        return qsTr("The Enneagram is a powerful personality system that describes nine distinct patterns of thinking, feeling, and acting.\n\n") + qsTr("• Click on numbers around the wheel to select your core type\n") + qsTr("• Choose a wing (adjacent type that influences your core type)\n") + qsTr("• Select your instinctual variant (primary life focus)\n") + qsTr("• Set your development level (psychological health)\n\n") + qsTr("The colored lines show integration (growth) and disintegration (stress) patterns between types.");
    }

    // Initialize when character changes
    onCharacterModelChanged: {
        if (characterModel) {
            enneagramWheelPanel.selectedType = characterModel.enneagramType || 9;
            updateWingOptions();
        }
    }

    Component.onCompleted: {
        updateWingOptions();
    }
}
