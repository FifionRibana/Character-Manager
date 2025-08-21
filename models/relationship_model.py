#!/usr/bin/env python3
"""
RelationshipModel - PyQt model for character relationships.

This module provides the RelationshipModel class that wraps relationship data
for QML consumption with live updates and validation.
"""

from typing import List, Optional, Dict, Any
from PyQt6.QtCore import (
    QAbstractListModel, QModelIndex, Qt, pyqtSignal, pyqtProperty, 
    QObject, pyqtSlot
)
from dataclasses import asdict

from data.character import Relationship
from data.enums import RelationType


class RelationshipModel(QAbstractListModel):
    """Model for managing character relationships in QML."""
    
    # Define roles for QML access
    IdRole = Qt.ItemDataRole.UserRole + 1
    TargetIdRole = Qt.ItemDataRole.UserRole + 2
    TargetNameRole = Qt.ItemDataRole.UserRole + 3
    TypeRole = Qt.ItemDataRole.UserRole + 4
    TypeDisplayRole = Qt.ItemDataRole.UserRole + 5
    DescriptionRole = Qt.ItemDataRole.UserRole + 6
    StrengthRole = Qt.ItemDataRole.UserRole + 7
    IsPositiveRole = Qt.ItemDataRole.UserRole + 8
    ColorRole = Qt.ItemDataRole.UserRole + 9
    IconRole = Qt.ItemDataRole.UserRole + 10
    
    # Signals for QML
    relationshipAdded = pyqtSignal(str, arguments=["targetId"])
    relationshipRemoved = pyqtSignal(str, arguments=["targetId"]) 
    relationshipUpdated = pyqtSignal(str, arguments=["targetId"])
    countChanged = pyqtSignal()
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._relationships: List[Relationship] = []
        self._role_names = {
            self.IdRole: b"id",
            self.TargetIdRole: b"targetId",
            self.TargetNameRole: b"targetName", 
            self.TypeRole: b"type",
            self.TypeDisplayRole: b"typeDisplay",
            self.DescriptionRole: b"description",
            self.StrengthRole: b"strength",
            self.IsPositiveRole: b"isPositive",
            self.ColorRole: b"color",
            self.IconRole: b"icon"
        }
    
    def roleNames(self) -> Dict[int, bytes]:
        """Return role names for QML."""
        return self._role_names
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of relationships."""
        return len(self._relationships)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Return data for a given index and role."""
        if not self.checkIndex(index):
            return None
        
        relationship = self._relationships[index.row()]
        
        if role == self.IdRole:
            return f"{relationship.target_id}_{relationship.relationship_type.value}"
        elif role == self.TargetIdRole:
            return relationship.target_id
        elif role == self.TargetNameRole:
            return relationship.target_name
        elif role == self.TypeRole:
            return relationship.relationship_type.value
        elif role == self.TypeDisplayRole:
            return self._get_type_display_name(relationship.relationship_type)
        elif role == self.DescriptionRole:
            return relationship.description
        elif role == self.StrengthRole:
            return relationship.strength
        elif role == self.IsPositiveRole:
            return relationship.is_positive
        elif role == self.ColorRole:
            return self._get_relationship_color(relationship.relationship_type)
        elif role == self.IconRole:
            return self._get_relationship_icon(relationship.relationship_type)
        
        return None
    
    @pyqtProperty(int, notify=countChanged)
    def count(self) -> int:
        """Get the number of relationships."""
        return len(self._relationships)
    
    @pyqtSlot(str, str, str, str, int)
    def addRelationship(self, target_id: str, target_name: str, 
                       relationship_type: str, description: str = "", 
                       strength: int = 5) -> None:
        """
        Add a new relationship.
        
        Args:
            target_id: ID of the target character
            target_name: Name of the target character  
            relationship_type: Type of relationship (enum value)
            description: Optional description
            strength: Relationship strength (1-10)
        """
        try:
            rel_type = RelationType(relationship_type)
        except ValueError:
            rel_type = RelationType.NEUTRAL
        
        # Check if relationship already exists
        for i, rel in enumerate(self._relationships):
            if rel.target_id == target_id:
                # Update existing relationship
                self._relationships[i] = Relationship(
                    target_id=target_id,
                    target_name=target_name,
                    relationship_type=rel_type,
                    description=description,
                    strength=strength
                )
                model_index = self.index(i, 0)
                self.dataChanged.emit(model_index, model_index)
                self.relationshipUpdated.emit(target_id)
                return
        
        # Add new relationship
        self.beginInsertRows(QModelIndex(), len(self._relationships), 
                           len(self._relationships))
        
        new_relationship = Relationship(
            target_id=target_id,
            target_name=target_name,
            relationship_type=rel_type,
            description=description,
            strength=strength
        )
        self._relationships.append(new_relationship)
        
        self.endInsertRows()
        self.countChanged.emit()
        self.relationshipAdded.emit(target_id)
    
    @pyqtSlot(str, result=bool)
    def removeRelationship(self, target_id: str) -> bool:
        """
        Remove a relationship by target ID.
        
        Args:
            target_id: ID of the target character
            
        Returns:
            True if relationship was removed, False if not found
        """
        for i, rel in enumerate(self._relationships):
            if rel.target_id == target_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                del self._relationships[i]
                self.endRemoveRows()
                self.countChanged.emit()
                self.relationshipRemoved.emit(target_id)
                return True
        return False
    
    @pyqtSlot(str, str, str, int)
    def updateRelationship(self, target_id: str, relationship_type: str, 
                          description: str, strength: int) -> None:
        """
        Update an existing relationship.
        
        Args:
            target_id: ID of the target character
            relationship_type: New relationship type
            description: New description
            strength: New strength value
        """
        try:
            rel_type = RelationType(relationship_type)
        except ValueError:
            return
        
        for i, rel in enumerate(self._relationships):
            if rel.target_id == target_id:
                self._relationships[i] = Relationship(
                    target_id=target_id,
                    target_name=rel.target_name,
                    relationship_type=rel_type,
                    description=description,
                    strength=strength
                )
                model_index = self.index(i, 0)
                self.dataChanged.emit(model_index, model_index)
                self.relationshipUpdated.emit(target_id)
                break
    
    @pyqtSlot(str, result='QVariant')
    def getRelationship(self, target_id: str) -> Optional[Dict[str, Any]]:
        """
        Get relationship data by target ID.
        
        Args:
            target_id: ID of the target character
            
        Returns:
            Relationship data as dictionary or None
        """
        for rel in self._relationships:
            if rel.target_id == target_id:
                return rel.to_dict()
        return None
    
    def set_relationships(self, relationships: List[Relationship]) -> None:
        """
        Set the complete list of relationships.
        
        Args:
            relationships: List of Relationship objects
        """
        self.beginResetModel()
        self._relationships = relationships.copy()
        self.endResetModel()
        self.countChanged.emit()
    
    def get_relationships(self) -> List[Relationship]:
        """
        Get the current list of relationships.
        
        Returns:
            List of Relationship objects
        """
        return self._relationships.copy()
    
    @pyqtSlot(result='QVariantList')
    def getAllRelationshipTypes(self) -> List[Dict[str, str]]:
        """
        Get all available relationship types for UI.
        
        Returns:
            List of dictionaries with type value and display name
        """
        return [
            {
                "value": rel_type.value,
                "display": self._get_type_display_name(rel_type),
                "color": self._get_relationship_color(rel_type),
                "icon": self._get_relationship_icon(rel_type)
            }
            for rel_type in RelationType
        ]
    
    def _get_type_display_name(self, rel_type: RelationType) -> str:
        """Get human-readable name for relationship type."""
        display_names = {
            RelationType.FAMILY: "Family",
            RelationType.FRIEND: "Friend", 
            RelationType.RIVAL: "Rival",
            RelationType.MENTOR: "Mentor",
            RelationType.STUDENT: "Student",
            RelationType.ALLY: "Ally",
            RelationType.ENEMY: "Enemy",
            RelationType.ROMANTIC: "Romantic",
            RelationType.NEUTRAL: "Neutral"
        }
        return display_names.get(rel_type, rel_type.value.title())
    
    def _get_relationship_color(self, rel_type: RelationType) -> str:
        """Get color for relationship type visualization."""
        colors = {
            RelationType.FAMILY: "#E91E63",      # Pink
            RelationType.FRIEND: "#4CAF50",      # Green
            RelationType.RIVAL: "#FF5722",       # Deep Orange
            RelationType.MENTOR: "#3F51B5",      # Indigo
            RelationType.STUDENT: "#00BCD4",     # Cyan
            RelationType.ALLY: "#8BC34A",        # Light Green
            RelationType.ENEMY: "#F44336",       # Red
            RelationType.ROMANTIC: "#E91E63",    # Pink
            RelationType.NEUTRAL: "#9E9E9E"      # Grey
        }
        return colors.get(rel_type, "#9E9E9E")
    
    def _get_relationship_icon(self, rel_type: RelationType) -> str:
        """Get emoji icon for relationship type."""
        icons = {
            RelationType.FAMILY: "👨‍👩‍👧‍👦",
            RelationType.FRIEND: "😊",
            RelationType.RIVAL: "⚔️",
            RelationType.MENTOR: "👨‍🏫",
            RelationType.STUDENT: "👨‍🎓",
            RelationType.ALLY: "🤝",
            RelationType.ENEMY: "💀",
            RelationType.ROMANTIC: "💕",
            RelationType.NEUTRAL: "😐"
        }
        return icons.get(rel_type, "👤")