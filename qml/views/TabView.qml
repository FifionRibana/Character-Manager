import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TabBar {
    id: tabBar
    
    property var characterModel
    currentIndex: tabBar.currentIndex
    
    // Tab selection change signal
    signal tabChanged(int index)
    
    background: Rectangle {
        color: "#f8f9fa"
        border.color: "#dee2e6"
        border.width: 1
    }
    
    // Phase 1 Tabs
    TabButton {
        id: overviewTab
        text: "Overview"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "📋"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    TabButton {
        id: enneagramTab
        text: "Enneagram"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "🧭"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    // Phase 3 Tabs
    TabButton {
        id: statsTab
        text: "Statistics"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "⚔️"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            // Stats indicator dot
            Rectangle {
                width: 8
                height: 8
                radius: 4
                color: getStatsIndicatorColor()
                visible: characterModel && characterModel.totalStatPoints > 0
                
                function getStatsIndicatorColor() {
                    if (!characterModel) return "#9E9E9E"
                    
                    const total = characterModel.totalStatPoints
                    if (total === 72) return "#4CAF50"      // Standard Array
                    if (total >= 65 && total <= 80) return "#FFC107"  // Good range
                    return "#FF5722"  // Outside normal range
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    TabButton {
        id: biographyTab
        text: "Biography"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "📖"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            // Biography completion indicator
            Rectangle {
                width: 8
                height: 8
                radius: 4
                color: getBiographyIndicatorColor()
                visible: characterModel && characterModel.biography.length > 0
                
                function getBiographyIndicatorColor() {
                    if (!characterModel) return "#9E9E9E"
                    
                    const length = characterModel.biography.length
                    if (length >= 500) return "#4CAF50"     // Good detail
                    if (length >= 100) return "#FFC107"     // Some detail
                    return "#FF5722"  // Minimal detail
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    // Phase 4 Tabs - NEW
    TabButton {
        id: relationshipsTab
        text: "Relationships"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "🤝"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            // Relationship count badge
            Rectangle {
                width: Math.max(12, countText.implicitWidth + 4)
                height: 12
                radius: 6
                color: "#4CAF50"
                visible: characterModel && characterModel.relationshipCount > 0
                
                Text {
                    id: countText
                    anchors.centerIn: parent
                    text: characterModel ? characterModel.relationshipCount : "0"
                    font.pixelSize: 8
                    font.bold: true
                    color: "#ffffff"
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    TabButton {
        id: narrativeTab
        text: "Timeline"
        width: implicitWidth
        
        contentItem: RowLayout {
            spacing: 8
            
            Text {
                text: "📅"
                font.pixelSize: 14
            }
            
            Text {
                text: parent.parent.text
                font.pixelSize: 12
                color: parent.parent.checked ? "#007bff" : "#495057"
                
                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
            
            // Event count and importance indicators
            RowLayout {
                spacing: 2
                
                // Event count badge
                Rectangle {
                    width: Math.max(12, eventCountText.implicitWidth + 4)
                    height: 12
                    radius: 6
                    color: "#FF9800"
                    visible: characterModel && characterModel.eventCount > 0
                    
                    Text {
                        id: eventCountText
                        anchors.centerIn: parent
                        text: characterModel ? characterModel.eventCount : "0"
                        font.pixelSize: 8
                        font.bold: true
                        color: "#ffffff"
                    }
                }
                
                // Major event indicator
                Text {
                    text: "⭐"
                    font.pixelSize: 8
                    visible: characterModel && characterModel.majorEventCount > 0
                    opacity: 0.8
                }
            }
        }
        
        background: Rectangle {
            color: parent.checked ? "#ffffff" : "transparent"
            border.color: parent.checked ? "#007bff" : "transparent"
            border.width: parent.checked ? 2 : 0
            radius: 6
            
            Behavior on color {
                ColorAnimation { duration: 150 }
            }
        }
    }
    
    // Tab change handling
    onCurrentIndexChanged: {
        tabChanged(currentIndex)
    }
    
    // Accessibility and keyboard navigation
    Keys.onLeftPressed: {
        if (currentIndex > 0) {
            currentIndex -= 1
        }
    }
    
    Keys.onRightPressed: {
        if (currentIndex < count - 1) {
            currentIndex += 1
        }
    }
    
    // Tab completion indicators
    function getTabCompletionStatus(tabIndex) {
        if (!characterModel) return "incomplete"
        
        switch (tabIndex) {
            case 0: // Overview
                return characterModel.name && characterModel.age > 0 ? "complete" : "incomplete"
            case 1: // Enneagram
                return characterModel.enneagramType !== "unknown" ? "complete" : "incomplete"
            case 2: // Stats
                return characterModel.totalStatPoints > 0 ? "complete" : "incomplete"
            case 3: // Biography
                return characterModel.biography.length >= 100 ? "complete" : "partial"
            case 4: // Relationships
                return characterModel.relationshipCount > 0 ? "complete" : "incomplete"
            case 5: // Timeline
                return characterModel.eventCount > 0 ? "complete" : "incomplete"
            default:
                return "incomplete"
        }
    }
    
    // Tab names for external reference
    readonly property var tabNames: [
        "overview",
        "enneagram", 
        "statistics",
        "biography",
        "relationships",
        "timeline"
    ]
    
    // Current tab name
    readonly property string currentTabName: tabNames[currentIndex] || "overview"
    
    // Navigation helpers
    function goToTab(tabName) {
        const index = tabNames.indexOf(tabName)
        if (index >= 0 && index < count) {
            currentIndex = index
        }
    }
    
    function hasNextTab() {
        return currentIndex < count - 1
    }
    
    function hasPreviousTab() {
        return currentIndex > 0
    }
    
    function nextTab() {
        if (hasNextTab()) {
            currentIndex += 1
        }
    }
    
    function previousTab() {
        if (hasPreviousTab()) {
            currentIndex -= 1
        }
    }
}