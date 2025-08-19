#!/usr/bin/env python3
"""
Diagnostic complet pour identifier tous les problèmes restants.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_enum_consistency():
    """Vérifier la cohérence des enums."""
    print("🔍 Vérification de la cohérence des enums")
    print("-" * 40)
    
    try:
        from data.enums import (
            RelationType, StatType, StorageKeys, 
            ValidationLimits, UIConstants, EnneagramType,
            InstinctualVariant, DevelopmentLevel
        )
        
        print("✅ Tous les enums importés avec succès")
        
        # Vérifier RelationType
        print(f"\n📋 RelationType disponibles:")
        for rel_type in RelationType:
            print(f"  - {rel_type.name}: {rel_type.value}")
        
        # Vérifier StatType
        print(f"\n📋 StatType disponibles:")
        for stat_type in StatType:
            print(f"  - {stat_type.name}: {stat_type.value}")
        
        # Vérifier les constantes importantes
        print(f"\n🎯 Constantes importantes:")
        print(f"  - UIConstants.MAX_RECENT_FILES: {UIConstants.MAX_RECENT_FILES}")
        print(f"  - ValidationLimits.DEFAULT_CHARACTER_LEVEL: {ValidationLimits.DEFAULT_CHARACTER_LEVEL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur enum: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_character_model():
    """Vérifier les propriétés de CharacterModel."""
    print("\n🔍 Vérification de CharacterModel")
    print("-" * 40)
    
    try:
        from models.character_model import CharacterModel
        from data.character import Character
        
        # Créer un modèle de test
        character = Character.create_default("Test")
        model = CharacterModel()
        model.set_character(character)
        
        # Lister toutes les propriétés disponibles
        print("📋 Propriétés CharacterModel disponibles:")
        
        # Test des propriétés de base
        basic_props = [
            "name", "level", "hasCharacter",
            "strength", "agility", "constitution", 
            "intelligence", "wisdom", "charisma",
            "totalStats", "biography"
        ]
        
        for prop in basic_props:
            if hasattr(model, prop):
                try:
                    value = getattr(model, prop)
                    print(f"  ✅ {prop}: {value}")
                except Exception as e:
                    print(f"  ⚠️  {prop}: erreur lors de l'accès ({e})")
            else:
                print(f"  ❌ {prop}: propriété manquante")
        
        # Test des propriétés avancées (qui pourraient ne pas exister)
        advanced_props = [
            "healthCategory", "enneagramTitle", "enneagramNotation", 
            "averageStat", "developmentLevel"
        ]
        
        print(f"\n📋 Propriétés avancées (optionnelles):")
        for prop in advanced_props:
            if hasattr(model, prop):
                try:
                    value = getattr(model, prop)
                    print(f"  ✅ {prop}: {value}")
                except Exception as e:
                    print(f"  ⚠️  {prop}: disponible mais erreur ({e})")
            else:
                print(f"  ❌ {prop}: non implémentée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur CharacterModel: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_storage_controller():
    """Vérifier StorageController."""
    print("\n🔍 Vérification de StorageController")
    print("-" * 40)
    
    try:
        from controllers.storage_controller import StorageController
        from data.character import Character
        
        storage = StorageController()
        character = Character.create_default("Test Storage")
        character_dict = character.to_dict()
        
        # Test de validation
        print("🧪 Test de validation:")
        is_valid, error_msg = storage._validate_character_data(character_dict)
        if is_valid:
            print(f"  ✅ Validation réussie")
        else:
            print(f"  ❌ Validation échouée: {error_msg}")
            
            # Essayer de corriger les erreurs communes
            if "character_id" in error_msg.lower():
                character_dict["id"] = character.id
                print(f"  🔧 Correction: ajout de l'ID")
                is_valid, error_msg = storage._validate_character_data(character_dict)
                if is_valid:
                    print(f"    ✅ Validation réussie après correction")
                else:
                    print(f"    ❌ Validation encore échouée: {error_msg}")
        
        # Test des méthodes principales
        print(f"\n🧪 Test des méthodes:")
        
        # file_exists
        try:
            result = storage.file_exists("test.json")
            print(f"  ✅ file_exists: fonctionne (résultat: {result})")
        except Exception as e:
            print(f"  ❌ file_exists: erreur ({e})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur StorageController: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_relationship_types():
    """Vérifier les types de relations utilisés dans les tests."""
    print("\n🔍 Vérification des types de relations")
    print("-" * 40)
    
    try:
        from data.enums import RelationType
        
        # Types utilisés dans les tests
        test_types = ["FRIEND", "MENTOR", "STUDENT", "FAMILY", "ENEMY"]
        
        print("📋 Types de relations dans les tests:")
        for test_type in test_types:
            if hasattr(RelationType, test_type):
                rel_type = getattr(RelationType, test_type)
                print(f"  ✅ {test_type}: {rel_type.value}")
            else:
                print(f"  ❌ {test_type}: manquant")
                # Suggérer des alternatives
                alternatives = [r.name for r in RelationType if test_type.lower() in r.name.lower()]
                if alternatives:
                    print(f"      Alternatives possibles: {alternatives}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur types de relations: {e}")
        return False

def main():
    """Exécuter tous les diagnostics."""
    print("🚨 DIAGNOSTIC COMPLET - Phase 3")
    print("=" * 50)
    
    checks = [
        ("Cohérence des enums", check_enum_consistency),
        ("CharacterModel", check_character_model),
        ("StorageController", check_storage_controller),
        ("Types de relations", check_relationship_types),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n{'=' * 50}")
        if check_func():
            passed += 1
            print(f"✅ {check_name}: OK")
        else:
            print(f"❌ {check_name}: PROBLÈMES DÉTECTÉS")
    
    print(f"\n{'=' * 50}")
    print(f"📊 Résultat du diagnostic: {passed}/{total} vérifications passées")
    
    if passed == total:
        print("🎉 Aucun problème détecté! Votre système semble fonctionnel.")
    else:
        print("⚠️  Quelques problèmes détectés. Consultez les détails ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)