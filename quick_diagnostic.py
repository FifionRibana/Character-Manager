#!/usr/bin/env python3
"""
Diagnostic rapide pour identifier le problème exact avec StatType.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def diagnostic_enum_access():
    """Test direct de l'accès aux enums."""
    print("🔍 Diagnostic StatType Access")
    print("-" * 30)
    
    try:
        from data.enums import StatType
        print("✅ StatType importé avec succès")
        
        # Lister tous les membres de StatType
        print("\n📋 Membres de StatType:")
        for stat in StatType:
            print(f"  - {stat.name} = '{stat.value}'")
        
        # Tester l'accès spécifique à AGILITY
        print(f"\n🎯 Test d'accès spécifique:")
        print(f"  - StatType.AGILITY: {StatType.AGILITY}")
        print(f"  - StatType.AGILITY.value: {StatType.AGILITY.value}")
        
        # Tester tous les stats attendus
        expected_stats = ["STRENGTH", "AGILITY", "CONSTITUTION", "INTELLIGENCE", "WISDOM", "CHARISMA"]
        print(f"\n🧪 Test de tous les stats attendus:")
        for stat_name in expected_stats:
            try:
                stat_enum = getattr(StatType, stat_name)
                print(f"  ✅ {stat_name}: {stat_enum.value}")
            except AttributeError:
                print(f"  ❌ {stat_name}: MANQUANT!")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur d'import StatType: {e}")
        import traceback
        traceback.print_exc()
        return False

def diagnostic_character_stats():
    """Test direct de CharacterStats."""
    print("\n🔍 Diagnostic CharacterStats")
    print("-" * 30)
    
    try:
        from data.character import CharacterStats
        print("✅ CharacterStats importé avec succès")
        
        # Créer une instance
        stats = CharacterStats()
        print(f"✅ CharacterStats créé")
        
        # Lister tous les champs
        print(f"\n📋 Champs de CharacterStats:")
        fields = ["strength", "agility", "constitution", "intelligence", "wisdom", "charisma"]
        for field in fields:
            value = getattr(stats, field)
            print(f"  - {field}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur CharacterStats: {e}")
        import traceback
        traceback.print_exc()
        return False

def diagnostic_serialization():
    """Test direct de la sérialisation."""
    print("\n🔍 Diagnostic Sérialisation")
    print("-" * 30)
    
    try:
        from data.character import CharacterStats
        from data.enums import StatType
        
        stats = CharacterStats(strength=15, agility=12)
        print(f"✅ CharacterStats créé avec des valeurs personnalisées")
        print(f"  - strength: {stats.strength}")
        print(f"  - agility: {stats.agility}")
        
        # Test de sérialisation ligne par ligne
        print(f"\n🧪 Test de sérialisation ligne par ligne:")
        
        try:
            strength_value = StatType.STRENGTH.value
            print(f"  ✅ StatType.STRENGTH.value: '{strength_value}'")
        except Exception as e:
            print(f"  ❌ StatType.STRENGTH: {e}")
            return False
        
        try:
            agility_value = StatType.AGILITY.value
            print(f"  ✅ StatType.AGILITY.value: '{agility_value}'")
        except Exception as e:
            print(f"  ❌ StatType.AGILITY: {e}")
            return False
        
        # Test de la méthode to_dict complète
        print(f"\n🎯 Test to_dict() complet:")
        stats_dict = stats.to_dict()
        print(f"  ✅ to_dict() réussi: {stats_dict}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de sérialisation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Exécuter tous les diagnostics."""
    print("🚨 DIAGNOSTIC RAPIDE - StatType & CharacterStats")
    print("=" * 50)
    
    tests = [
        diagnostic_enum_access,
        diagnostic_character_stats,
        diagnostic_serialization
    ]
    
    for test in tests:
        success = test()
        if not success:
            print(f"\n🛑 Test échoué - arrêt du diagnostic")
            return False
    
    print(f"\n🎉 Tous les diagnostics sont passés!")
    print(f"Le problème StatType/AGILITY semble résolu.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)