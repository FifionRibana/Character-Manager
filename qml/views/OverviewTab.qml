import QtQuick 6.9
import QtQuick.Controls 6.9
import QtQuick.Layouts 6.9
import QtQuick.Effects 6.9
// import "../styles"
import App.Styles

ScrollView {
    id: overviewTab

    property var characterModel
    property bool editMode: false

    signal editModeRequested

    contentWidth: availableWidth

    ColumnLayout {
        width: overviewTab.availableWidth
        spacing: AppTheme.spacing.large

        // Stats overview card
        Rectangle {
            Layout.fillWidth: true

            color: AppTheme.card.background
            border.color: AppTheme.card.border
            border.width: AppTheme.border.thin
            radius: AppTheme.radius.medium

            implicitHeight: statsContent.implicitHeight + 2 * AppTheme.spacing.large

            ColumnLayout {
                id: statsContent
                anchors.fill: parent
                anchors.margins: AppTheme.spacing.large
                spacing: AppTheme.spacing.medium

                // Title
                Text {
                    text: qsTr("Ability Scores")
                    font.family: AppTheme.fontFamily
                    font.pixelSize: AppTheme.fontSize.large
                    font.bold: true
                    color: AppTheme.colors.text
                }

                // Separator
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: AppTheme.colors.border
                }

                // Stats grid
                GridLayout {
                    columns: 3
                    columnSpacing: AppTheme.spacing.large
                    rowSpacing: AppTheme.spacing.medium

                    // Strength
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Strength")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.strength : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.strength.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.strength : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.strength : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.strength : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }

                    // Agility
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Agility")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.agility : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.agility.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.agility : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.agility : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.agility : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }

                    // Constitution
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Constitution")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.constitution : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.constitution.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.constitution : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.constitution : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.constitution : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }

                    // Intelligence
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Intelligence")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.intelligence : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.intelligence.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.intelligence : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.intelligence : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.intelligence : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }

                    // Wisdom
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Wisdom")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.wisdom : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.wisdom.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.wisdom : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.wisdom : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.wisdom : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }

                    // Charisma
                    ColumnLayout {
                        spacing: AppTheme.spacing.small

                        Text {
                            text: qsTr("Charisma")
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: AppTheme.colors.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            color: AppTheme.getStatColor(characterModel ? characterModel.charisma : 10)
                            Layout.alignment: Qt.AlignHCenter

                            Text {
                                anchors.centerIn: parent
                                text: characterModel ? characterModel.charisma.toString() : "10"
                                font.family: AppTheme.fontFamily
                                font.pixelSize: AppTheme.fontSize.large
                                font.bold: true
                                color: AppTheme.getStatTextColor(characterModel ? characterModel.charisma : 10)
                            }
                        }

                        Text {
                            text: {
                                let value = characterModel ? characterModel.charisma : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return modifier >= 0 ? "+" + modifier : modifier.toString();
                            }
                            font.family: AppTheme.fontFamily
                            font.pixelSize: AppTheme.fontSize.medium
                            color: {
                                let value = characterModel ? characterModel.charisma : 10;
                                let modifier = Math.floor((value - 10) / 2);
                                return AppTheme.getModifierColor(modifier);
                            }
                            horizontalAlignment: Text.AlignHCenter
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}
