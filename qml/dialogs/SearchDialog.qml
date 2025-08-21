import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../styles"

Dialog {
    id: searchDialog
    
    property var controller: null
    property var searchResults: []
    property string currentSearchTerm: ""
    
    title: "Search"
    width: 700
    height: 500
    modal: true
    standardButtons: Dialog.Close
    
    // Search when opened
    onOpened: {
        searchField.text = ""
        searchField.forceActiveFocus()
        searchResults = []
    }
    
    function performSearch() {
        if (searchField.text.length < 2) {
            searchResults = []
            return
        }
        
        currentSearchTerm = searchField.text.toLowerCase()
        var results = []
        
        // Search through all characters
        if (controller && controller.characterList) {
            for (var i = 0; i < controller.characterList.rowCount(); i++) {
                var character = controller.characterList.getCharacterAt(i)
                if (character) {
                    var charResults = searchInCharacter(character)
                    results = results.concat(charResults)
                }
            }
        }
        
        searchResults = results
    }
    
    function searchInCharacter(character) {
        var results = []
        var term = currentSearchTerm
        
        // Search in basic info
        if (character.name && character.name.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Overview",
                field: "Name",
                value: character.name,
                matchText: highlightMatch(character.name)
            })
        }
        
        if (character.occupation && character.occupation.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Overview",
                field: "Occupation",
                value: character.occupation,
                matchText: highlightMatch(character.occupation)
            })
        }
        
        if (character.location && character.location.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Overview",
                field: "Location",
                value: character.location,
                matchText: highlightMatch(character.location)
            })
        }
        
        // Search in biography
        if (character.background && character.background.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Biography",
                field: "Background",
                value: character.background,
                matchText: getContextSnippet(character.background)
            })
        }
        
        if (character.personality && character.personality.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Biography",
                field: "Personality",
                value: character.personality,
                matchText: getContextSnippet(character.personality)
            })
        }
        
        if (character.motivations && character.motivations.toLowerCase().includes(term)) {
            results.push({
                characterId: character.id,
                characterName: character.name,
                category: "Biography",
                field: "Motivations",
                value: character.motivations,
                matchText: getContextSnippet(character.motivations)
            })
        }
        
        // Search in relationships
        if (character.relationshipModel) {
            for (var i = 0; i < character.relationshipModel.rowCount(); i++) {
                var rel = character.relationshipModel.getRelationshipAt(i)
                if (rel) {
                    if (rel.targetName && rel.targetName.toLowerCase().includes(term)) {
                        results.push({
                            characterId: character.id,
                            characterName: character.name,
                            category: "Relationships",
                            field: rel.type,
                            value: rel.targetName,
                            matchText: highlightMatch(rel.targetName)
                        })
                    }
                    
                    if (rel.description && rel.description.toLowerCase().includes(term)) {
                        results.push({
                            characterId: character.id,
                            characterName: character.name,
                            category: "Relationships",
                            field: rel.targetName,
                            value: rel.description,
                            matchText: getContextSnippet(rel.description)
                        })
                    }
                }
            }
        }
        
        // Search in timeline events
        if (character.narrativeModel) {
            for (var j = 0; j < character.narrativeModel.rowCount(); j++) {
                var event = character.narrativeModel.getEventAt(j)
                if (event) {
                    if (event.title && event.title.toLowerCase().includes(term)) {
                        results.push({
                            characterId: character.id,
                            characterName: character.name,
                            category: "Timeline",
                            field: event.date,
                            value: event.title,
                            matchText: highlightMatch(event.title)
                        })
                    }
                    
                    if (event.description && event.description.toLowerCase().includes(term)) {
                        results.push({
                            characterId: character.id,
                            characterName: character.name,
                            category: "Timeline",
                            field: event.title,
                            value: event.description,
                            matchText: getContextSnippet(event.description)
                        })
                    }
                    
                    // Search in tags
                    if (event.tags) {
                        for (var k = 0; k < event.tags.length; k++) {
                            if (event.tags[k].toLowerCase().includes(term)) {
                                results.push({
                                    characterId: character.id,
                                    characterName: character.name,
                                    category: "Timeline",
                                    field: "Tag",
                                    value: event.tags[k],
                                    matchText: highlightMatch(event.tags[k])
                                })
                            }
                        }
                    }
                }
            }
        }
        
        return results
    }
    
    function highlightMatch(text) {
        if (!text) return ""
        
        var index = text.toLowerCase().indexOf(currentSearchTerm)
        if (index === -1) return text
        
        var before = text.substring(0, index)
        var match = text.substring(index, index + currentSearchTerm.length)
        var after = text.substring(index + currentSearchTerm.length)
        
        return before + "<b style='color: " + AppTheme.colors.accent + "'>" + match + "</b>" + after
    }
    
    function getContextSnippet(text) {
        if (!text) return ""
        
        var index = text.toLowerCase().indexOf(currentSearchTerm)
        if (index === -1) return text.substring(0, 100) + "..."
        
        var contextLength = 50
        var start = Math.max(0, index - contextLength)
        var end = Math.min(text.length, index + currentSearchTerm.length + contextLength)
        
        var snippet = (start > 0 ? "..." : "") + 
                     text.substring(start, index) +
                     "<b style='color: " + AppTheme.colors.accent + "'>" +
                     text.substring(index, index + currentSearchTerm.length) +
                     "</b>" +
                     text.substring(index + currentSearchTerm.length, end) +
                     (end < text.length ? "..." : "")
        
        return snippet
    }
    
    function navigateToResult(result) {
        // Select the character
        if (controller) {
            controller.selectCharacter(result.characterId)
            
            // Navigate to appropriate tab based on category
            switch(result.category) {
                case "Overview":
                    mainWindow.tabView.currentIndex = 0
                    break
                case "Biography":
                    mainWindow.tabView.currentIndex = 3
                    break
                case "Relationships":
                    mainWindow.tabView.currentIndex = 4
                    break
                case "Timeline":
                    mainWindow.tabView.currentIndex = 5
                    break
            }
        }
        
        searchDialog.close()
    }
    
    // Main content
    ColumnLayout {
        anchors.fill: parent
        spacing: AppTheme.spacing.medium
        
        // Search input
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.medium
            
            TextField {
                id: searchField
                Layout.fillWidth: true
                placeholderText: "Search across all characters..."
                selectByMouse: true
                
                onTextChanged: {
                    searchTimer.restart()
                }
                
                onAccepted: {
                    performSearch()
                }
                
                // Icon
                leftPadding: 35
                background: Rectangle {
                    color: AppTheme.colors.surface
                    border.color: searchField.activeFocus ? AppTheme.colors.primary : AppTheme.colors.border
                    radius: AppTheme.radius.small
                    
                    Label {
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        text: "🔍"
                        font.pixelSize: 16
                        color: AppTheme.colors.textSecondary
                    }
                }
            }
            
            Button {
                text: "Search"
                enabled: searchField.text.length >= 2
                onClicked: performSearch()
            }
            
            Button {
                text: "Clear"
                enabled: searchField.text.length > 0
                onClicked: {
                    searchField.text = ""
                    searchResults = []
                }
            }
        }
        
        // Search filters
        RowLayout {
            Layout.fillWidth: true
            spacing: AppTheme.spacing.medium
            
            Label {
                text: "Filter by category:"
                color: AppTheme.colors.textSecondary
            }
            
            CheckBox {
                id: filterOverview
                text: "Overview"
                checked: true
            }
            
            CheckBox {
                id: filterBiography
                text: "Biography"
                checked: true
            }
            
            CheckBox {
                id: filterRelationships
                text: "Relationships"
                checked: true
            }
            
            CheckBox {
                id: filterTimeline
                text: "Timeline"
                checked: true
            }
            
            Item { Layout.fillWidth: true }
            
            Label {
                text: searchResults.length + " results"
                color: AppTheme.colors.textSecondary
                visible: searchResults.length > 0
            }
        }
        
        // Separator
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: AppTheme.colors.border
        }
        
        // Results list
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            ListView {
                id: resultsList
                model: searchResults.filter(function(result) {
                    switch(result.category) {
                        case "Overview": return filterOverview.checked
                        case "Biography": return filterBiography.checked
                        case "Relationships": return filterRelationships.checked
                        case "Timeline": return filterTimeline.checked
                        default: return true
                    }
                })
                spacing: AppTheme.spacing.small
                
                delegate: Rectangle {
                    width: ListView.view.width
                    height: resultContent.height + AppTheme.spacing.medium * 2
                    color: mouseArea.containsMouse ? AppTheme.colors.surfaceVariant : AppTheme.colors.surface
                    border.color: AppTheme.colors.border
                    border.width: 1
                    radius: AppTheme.radius.small
                    
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        
                        onClicked: {
                            navigateToResult(modelData)
                        }
                    }
                    
                    ColumnLayout {
                        id: resultContent
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.margins: AppTheme.spacing.medium
                        spacing: AppTheme.spacing.tiny
                        
                        RowLayout {
                            Layout.fillWidth: true
                            
                            Label {
                                text: modelData.characterName
                                font.bold: true
                                font.pixelSize: AppTheme.fontSize.medium
                                color: AppTheme.colors.primary
                            }
                            
                            Label {
                                text: " › "
                                color: AppTheme.colors.textSecondary
                            }
                            
                            Label {
                                text: modelData.category
                                color: AppTheme.colors.textSecondary
                                font.pixelSize: AppTheme.fontSize.small
                            }
                            
                            Label {
                                text: " › "
                                color: AppTheme.colors.textSecondary
                            }
                            
                            Label {
                                text: modelData.field
                                color: AppTheme.colors.textSecondary
                                font.pixelSize: AppTheme.fontSize.small
                            }
                            
                            Item { Layout.fillWidth: true }
                        }
                        
                        Label {
                            Layout.fillWidth: true
                            text: modelData.matchText
                            textFormat: Text.RichText
                            wrapMode: Text.WordWrap
                            color: AppTheme.colors.text
                            font.pixelSize: AppTheme.fontSize.small
                        }
                    }
                }
                
                // Empty state
                Label {
                    anchors.centerIn: parent
                    text: searchField.text.length < 2 ? 
                          "Enter at least 2 characters to search" : 
                          "No results found"
                    color: AppTheme.colors.textDisabled
                    visible: resultsList.count === 0
                }
            }
        }
    }
    
    // Delayed search timer
    Timer {
        id: searchTimer
        interval: 300  // Debounce search
        onTriggered: performSearch()
    }
}