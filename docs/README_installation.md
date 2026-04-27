# PyMorph Documentation

## Table des matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Interface Graphique](#interface-graphique)
4. [Ligne de Commande](#ligne-de-commande)
5. [Options](#options)
6. [Exemples](#exemples)
7. [Dépannage](#dépannage)
8. [FAQ](#faq)

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows/Linux/macOS

### Installation automatique
```bash
pip install -r requirements.txt
```

### Installation manuelle
```bash
pip install customtkinter nuitka Pillow
```

## Utilisation

PyMorph offre deux modes d'utilisation :

1. **Interface Graphique** (Recommandé pour débutants)
2. **Ligne de Commande** (Pour automatisation)

## Interface Graphique

### Lancement
```bash
python src/gui.py
```

### Fonctionnalités
- Sélection intuitive de fichiers
- Options d'obfuscation avec cases à cocher
- Logs en temps réel
- Barre de progression
- Aide intégrée

### Capture d'écran
*(Ajouter une capture d'écran ici)*

## Ligne de Commande

### Syntaxe de base
```bash
python src/pymorph.py <fichier> [options]
```

### Options disponibles
- `--encode-strings`: Encoder les chaînes en base64
- `--multi-file`: Traiter tous les fichiers importés
- `--compile`: Compiler en exécutable
- `--output <nom>`: Nom du fichier de sortie
- `--log <fichier>`: Fichier de logs personnalisé

## Options détaillées

### --encode-strings
Transforme toutes les chaînes de caractères en base64 avec décodage dynamique.

**Avant:**
```python
print("Hello World")
```

**Après:**
```python
print(decode_function('SGVsbG8gV29ybGQ='))
```

### --multi-file
Détecte automatiquement tous les fichiers importés et les obfusque ensemble.

**Structure:**
```
main.py
├── module1.py
├── module2.py
└── utils/
    └── helpers.py
```

**Résultat:**
```
obfuscated_main.py
├── obfuscated_module1.py
├── obfuscated_module2.py
└── obfuscated_utils/
    └── obfuscated_helpers.py
```

### --compile
Crée un exécutable autonome avec Nuitka.

**Avantages:**
- Pas besoin de Python pour exécuter
- Protection maximale du code
- Distribution facile

## Exemples

### Exemple 1: Obfuscation simple
```bash
python src/pymorph.py script.py
```

### Exemple 2: Avec strings encodés
```bash
python src/pymorph.py script.py --encode-strings
```

### Exemple 3: Projet multi-fichiers
```bash
python src/pymorph.py main.py --multi-file --encode-strings
```

### Exemple 4: Compilation complète
```bash
python src/pymorph.py app.py --encode-strings --compile --output my_app
```

## Dépannage

### Erreurs communes

#### "ModuleNotFoundError: No module named 'customtkinter'"
**Solution:**
```bash
pip install customtkinter
```

#### "nuitka n'est pas installé"
**Solution:**
```bash
pip install nuitka
```

#### "Le fichier n'existe pas"
**Solution:** Vérifiez le chemin du fichier et qu'il existe bien.

#### Problèmes de compilation
**Solutions:**
- Assurez-vous d'avoir un compilateur C installé
- Sur Windows, installez Visual Studio Build Tools
- Fermez les applications qui utilisent le fichier de sortie

### Logs

Consultez le fichier `obfuscation.log` pour voir les détails du processus.

## FAQ

### Q: PyMorph modifie-t-il mon fichier original ?
**R:** Non, PyMorph crée une copie obfusquée. Votre fichier original reste intact.

### Q: Puis-je décompiler un fichier obfusqué ?
**R:** C'est extrêmement difficile. PyMorph utilise plusieurs couches de protection.

### Q: Le code obfusqué fonctionne-t-il sur tous les systèmes ?
**R:** Oui, tant que Python est installé. Pour les exécutables, aucun runtime n'est nécessaire.

### Q: Puis-je obfuscer des fichiers avec des dépendances externes ?
**R:** Oui, mais les dépendances doivent être installées sur la machine cible.

### Q: La compilation prend beaucoup de temps ?
**R:** Oui, la première compilation peut prendre plusieurs minutes en raison de l'analyse du code.

### Q: Puis-je distribuer l'exécutable compilé ?
**R:** Oui, l'exécutable est autonome et ne nécessite pas d'installation Python.

## Support

Pour obtenir de l'aide :
1. Consultez cette documentation
2. Vérifiez les logs dans `obfuscation.log`
3. Testez avec des fichiers simples d'abord
4. Utilisez l'interface graphique pour plus de facilité

---

*PyMorph v1.0.0 - Protégez votre code Python*
