# PyMorph Tests

Ce dossier contient les fichiers de test pour PyMorph.

## Fichiers de test

### test_multi.py
Script de test pour le mode multi-fichiers.

**Contenu:**
- Import de module local
- Fonctions simples
- Variables globales
- Classe avec méthodes
- Point d'entrée main()

### module_test.py
Module de test importé par `test_multi.py`.

**Contenu:**
- Fonctions d'aide
- Calculs simples
- Pas de point d'entrée principal

## Utilisation des tests

### Test en ligne de commande
```bash
# Test simple
python src/pymorph.py tests/test_multi.py

# Test avec options
python src/pymorph.py tests/test_multi.py --multi-file --encode-strings

# Test avec compilation
python src/pymorph.py tests/test_multi.py --encode-strings --compile --output test_app
```

### Test avec l'interface graphique
1. Lancez `python src/gui.py`
2. Sélectionnez `tests/test_multi.py`
3. Choisissez vos options
4. Lancez l'obfuscation

### Vérification des résultats
Après obfuscation, vérifiez que :

1. **Fichiers générés:**
   - `obfuscated_test_multi.py`
   - `obfuscated_module_test.py` (mode multi-fichier)

2. **Fonctionnalité:**
   ```bash
   # Original
   python tests/test_multi.py
   
   # Obfusqué
   python obfuscated_test_multi.py
   
   # Les deux devraient donner le même résultat
   ```

3. **Compilation (si activée):**
   - `test_app.exe` devrait fonctionner
   - Même output que les scripts Python

## Résultats attendus

### Output des tests
```
Result: 30
Hello World
```

### Statistiques d'obfuscation
- Variables: ~5-10
- Fonctions: ~3-5
- Classes: 1
- Strings: Encodés si option activée

## Ajout de nouveaux tests

Pour ajouter de nouveaux tests :

1. **Créer le fichier de test:**
   ```python
   # tests/new_test.py
   def test_function():
       return "test"
   
   if __name__ == "__main__":
       print(test_function())
   ```

2. **Tester avec PyMorph:**
   ```bash
   python src/pymorph.py tests/new_test.py --encode-strings
   ```

3. **Vérifier le résultat:**
   - Le fichier obfusqué devrait fonctionner
   - Les logs devraient montrer les statistiques

## Tests automatiques

Pour créer des tests automatisés, utilisez le framework `unittest`:

```python
# tests/test_pymorph.py
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pymorph import obfuscate

class TestPyMorph(unittest.TestCase):
    def test_basic_obfuscation(self):
        result = obfuscate("tests/test_multi.py")
        self.assertIsNotNone(result)
    
    def test_string_encoding(self):
        result = obfuscate("tests/test_multi.py", encode_strings=True)
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
```

## Dépannage des tests

### Problèmes communs

1. **Import non trouvé:**
   - Vérifiez que les fichiers sont dans le bon dossier
   - Assurez-vous que les chemins d'import sont corrects

2. **Compilation échouée:**
   - Vérifiez que Nuitka est installé
   - Testez avec des fichiers plus simples

3. **Output différent:**
   - Comparez les logs d'obfuscation
   - Vérifiez que toutes les options sont correctes

## Rapport de bugs

Si vous trouvez un bug avec les tests :

1. Documentez le fichier de test utilisé
2. Incluez les options d'obfuscation
3. Fournissez les logs générés
4. Décrivez le résultat attendu vs obtenu

---

*Utilisez ces tests pour valider chaque nouvelle version de PyMorph*
