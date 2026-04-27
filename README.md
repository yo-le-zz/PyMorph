# 🔐 PyMorph v1.0.0

**Advanced Multi-Language Code Obfuscator with Maximum Protection**

*Auteur: yo-le-zz*

PyMorph est un outil d'obfuscation de pointe qui transforme votre code source en une version pratiquement illisible tout en préservant 100% de sa fonctionnalité. Supporte **7 langages de programmation** avec des techniques d'obfuscation multi-couches et une protection anti-analyse avancée.

---

## 🌟 Fonctionnalités Principales

### 🚀 **Multi-Language Support**
- **Python** (.py) - AST-based obfuscation
- **C++** (.cpp, .cc, .cxx) - Templates et STL
- **JavaScript** (.js, .jsx) - ES6+ et async/await
- **Rust** (.rs) - Structs, traits, lifetimes
- **C** (.c, .h) - Pointeurs et macros
- **Java** (.java) - Classes et interfaces
- **Go** (.go) - Goroutines et interfaces

### 🔐 **Techniques d'Obfuscation Avancées**

- **Encodage multi-couches** (8 méthodes différentes)
- **Renommage intelligent** des variables, fonctions, classes
- **Décomposition mathématique** des nombres
- **Variables factices** pour brouiller l'analyse
- **Encodage de chaînes** pré-stockées
- **Code factice** automatique
- **Obfuscation du flux de contrôle** (JavaScript)
- **Protection anti-analyse** avancée (anti-debug, anti-VM)
- **Support multi-fichiers** avec gestion des sous-dossiers
- **Encodage avancé des strings** avec décodage dynamique
- **Vérification d'intégrité** du code
- **Dead code injection** et contrôle flux opaque

### 🎨 **Interface Graphique Moderne**

- **Détection automatique** du langage depuis l'extension
- **Options entièrement configurables** et désactivables
- **Personnalisation des couleurs** et thèmes
- **Logs détaillés** avec timestamps
- **Sauvegarde automatique** des paramètres
- **Support multi-fichiers** glisser-déposer
- **Aperçu en temps réel** des transformations
- **Statistiques détaillées** d'obfuscation

---

## 📦 Installation

### Installation Automatique

```bash
# Cloner le projet
git clone <repository-url>
cd PyMorph

# Créer l'environnement virtuel
python -m venv env

# Activer l'environnement virtuel
# Windows:
env\Scripts\activate
# Linux/macOS:
source env/bin/activate

# Installer les dépendances
pip install -r assets/requirements.txt

# Compiler l'exécutable (optionnel)
python build.py
```

### Dépendances

```
customtkinter>=5.2.0  # Interface graphique
nuitka>=4.0.0         # Compilation en exécutable
cryptography>=3.4.0   # Cryptographie avancée
psutil>=5.8.0        # Détection anti-debug/VM
pycryptodome>=3.15.0 # Support AES
```

---

## 🎯 Utilisation

### Interface Graphique (Recommandé)

#### Lancement Direct (Recommandé)
```bash
# Lancement avec installation automatique des dépendances
python src/pymorph.py
```

#### Lancement Manuel
```bash
# Activer l'environnement virtuel d'abord
env\Scripts\activate

# Puis lancer l'interface
python src/enhanced_gui.py
```

**Fonctionnalités:**
- Sélectionnez un fichier → Détection automatique du langage
- Configurez les options d'obfuscation
- Lancez le processus avec un clic
- Visualisez les résultats et statistiques

### Ligne de Commande

```python
from src.obfuscators import obfuscate_code, detect_language_from_filename

# Obfusquer un fichier
language = detect_language_from_filename("script.py")  # "python"
with open("script.py", "r") as f:
    code = f.read()

obfuscated, stats = obfuscate_code(code, language, {
    'encode_strings': True,
    'rename_variables': True,
    'rename_functions': True,
    'decompose_numbers': True,
    'advanced_protection': True
})

# Sauvegarder le résultat
with open("obfuscated_script.py", "w") as f:
    f.write(obfuscated)
```

### Mode Multi-Fichiers Avancé

```bash
# Obfusquer un projet complet avec sous-dossiers
python src/pymorph.py main.py --multi-file --advanced-protection

# Obfusquer avec encodage de strings et protection maximale
python src/pymorph.py app.py --multi-file --encode-strings --advanced-protection

# Compiler en exécutable avec protection maximale
python src/pymorph.py main.py --multi-file --advanced-protection --compile --output secure_app
```

---

## ⚙️ Options d'Obfuscation

| Option | Description | Langages |
|--------|-------------|----------|
| `encode_strings` | Encoder les chaînes avec multi-couches | Tous |
| `rename_variables` | Renommer les variables locales | Tous |
| `rename_functions` | Renommer les fonctions/méthodes | Tous |
| `rename_classes` | Renommer les classes/structs | Python, Java, Rust, C++ |
| `decompose_numbers` | Décomposer les nombres mathématiquement | Tous |
| `add_dummy_vars` | Ajouter variables factices | Python, C++, C |
| `add_dummy_code` | Ajouter code factice | C++, C, Rust, Java, Go |
| `control_flow_obfuscation` | Brouiller le flux de contrôle | JavaScript |
| `obfuscate_macros` | Obfusquer les macros/directives | C++, C, Rust |
| `advanced_protection` | Protection anti-analyse complète | Python |
| `multi_file_support` | Support multi-fichiers avec sous-dossiers | Python |
| `integrity_check` | Vérification d'intégrité du code | Python |

---

## 📁 Structure du Projet

```
PyMorph/
├── src/                          # Code source
│   ├── obfuscators/              # Modules d'obfuscation
│   │   ├── python.py             # Obfuscateur Python
│   │   ├── cpp.py                # Obfuscateur C++
│   │   ├── javascript.py         # Obfuscateur JavaScript
│   │   ├── rust.py               # Obfuscateur Rust
│   │   ├── c.py                  # Obfuscateur C
│   │   ├── java.py               # Obfuscateur Java
│   │   ├── go.go                 # Obfuscateur Go
│   │   ├── advanced_encoder.py   # Encodage multi-couches
│   │   ├── advanced_protection.py # Protection anti-analyse
│   │   └── __init__.py           # Interface unifiée
│   ├── enhanced_gui.py           # Interface graphique
│   └── pymorph.py                # Moteur principal amélioré
├── tests/                        # Fichiers de test
│   ├── python_test.py            # Test Python
│   ├── cpp_test.cpp              # Test C++
│   ├── javascript_test.js        # Test JavaScript
│   ├── rust_test.rs              # Test Rust
│   ├── c_test.c                  # Test C
│   ├── java_test.java            # Test Java
│   ├── go_test.go                # Test Go
│   └── README.md                 # Documentation des tests
├── docs/                         # Documentation
│   └── old_readme_v2.md          # Ancienne documentation
├── assets/                       # Ressources
│   ├── requirements.txt          # Dépendances
│   └── icon.ico                  # Icône (si présente)
├── dist/                         # Fichiers compilés
├── build.py                      # Script de compilation
├── README.md                     # Ce fichier
├── CHANGELOG.md                  # Historique des versions
├── LICENSE                       # Licence restrictive
└── .gitignore                    # Fichiers ignorés par Git
```

---

## 🔥 Niveau de Protection

PyMorph offre une protection "maximum" :

### 🛡️ **Multi-Layer Encoding**

- **Double Base64** → Encodage hexadécimal → Compression zlib
- **XOR encryption** → AES encryption → Encodage Unicode
- **JSON encoding** → Hash-based encoding → Encodage mixte
- **Advanced string encryption** with dynamic decryption
- **Multi-stage decryption** with position-based keys

### 🎭 **Code Brouillé**

- **Noms aléatoires** pour tous les identifiants
- **Chaînes masquées** avec décodage dynamique
- **Nombres transformés** en opérations complexes
- **Code factice** pour confondre l'analyse
- **Dead code injection** et opaque predicates
- **Control flow obfuscation** avancée

### 🚀 **Anti-Analysis Protection**

- **Anti-debug detection** (traceurs, débogueurs)
- **Anti-virtualization** (VM detection)
- **Timing analysis** protection
- **Process name checks**
- **Registry-based detection** (Windows)
- **Code integrity verification**

### 🚀 **Compilation Binaire**

- **Code source complètement invisible**
- **Exécutable autonome** sans dépendances
- **Protection maximale** contre la rétro-ingénierie
- **Multi-file projects** supportés

---

## 📊 Exemples de Transformation

### Python
```python
# Avant
def calculate_sum(a, b):
    result = a + b
    return result

message = "Hello, World!"
print(message)

# Après (simplifié)
def xKjzMvP(aBcDeF, xYzWqR):
    pLmNoPq = (4 + 2) / (1 + 1)
    return aBcDeF + xYzWqR + (6 + 4)

rEsTuVw = xKjzMvP(2 + 3, 1 + 2)
print(advanced_decoder(encoded_string))
```

### JavaScript
```javascript
// Avant
function calculateSum(a, b) {
    return a + b;
}
const result = calculateSum(10, 20);

// Après (simplifié)
function aBcDeF(xYzWqR, pLmNoPq) {
    return xYzWqR + pLmNoPq;
}
const rEsTuVw = aBcDeF((5 + 5), (10 + 10));
```

---

## 🎨 Personnalisation

### Thèmes et Couleurs
- **Modes**: Dark, Light, System
- **Thèmes**: Blue, Green, Dark-Blue
- **Couleurs personnalisées**: Primaire, Secondaire, Accent, Fond, Surface

### Paramètres Persistants
- **Sauvegarde automatique** dans `pymorph_settings.json`
- **Historique des fichiers** récents
- **Préférences utilisateur** mémorisées

---

## 🛠️ Compilation

### Créer l'Exécutable
```bash
python build.py
```

**Résultat:**
- `dist/PyMorph.exe` - Exécutable principal
- `dist/PyMorph_Portable/` - Package portable complet

### Options de Compilation
- **One-file**: Exécutable autonome
- **Icon**: Icône personnalisée
- **Version**: Informations de version
- **Company**: Métadonnées de l'entreprise

---

## 📈 Performance

### Benchmarks
- **Python**: ~1000 lignes/sec
- **JavaScript**: ~1500 lignes/sec  
- **C++**: ~800 lignes/sec
- **Rust**: ~600 lignes/sec
- **Java**: ~700 lignes/sec
- **Go**: ~900 lignes/sec
- **C**: ~1200 lignes/sec

### Taille des Fichiers
- **Augmentation typique**: 200-400%
- **Compression avec Nuitka**: -60%
- **Ratio obfuscation/performance**: Optimal

---

## 🔧 Dépannage

### Problèmes Communs
```bash
# Erreur: customtkinter non trouvé
pip install customtkinter

# Erreur: nuitka non trouvé  
pip install nuitka

# Erreur: Permission refusée (Linux/macOS)
chmod +x build.py
sudo python build.py
```

### Support des Langages
- **Python**: 3.7+ requis
- **JavaScript**: ES6+ supporté
- **C/C++**: C11/C++17
- **Rust**: 2018 edition
- **Java**: 8+ (11+ recommandé)
- **Go**: 1.16+

---

## ⚠️ Avertissement

**PyMorph est conçu pour la protection intellectuelle et l'obfuscation légale.**

### Usage Autorisé ✅
- **Protection** de votre code propriétaire
- **Sécurisation** d'algorithmes sensibles
- **Licence** de logiciel obfusqué
- **Distribution** d'applications protégées

### Usage Interdit ❌
- **Activités illégales** ou malveillantes
- **Reverse engineering** non autorisé
- **Contournement** de protections
- **Usage commercial** non licencié

---

## 📝 Logs et Monitoring

PyMorph génère des logs détaillés pour chaque opération:
- **Fichiers traités** et leur statut
- **Éléments obfusqués** avec comptage
- **Erreurs éventuelles** et solutions
- **Statistiques complètes** de performance
- **Timestamps** pour traçabilité

---

## 🤝 Contribuer

**Ce projet est sous licence restrictive - voir `LICENSE` pour les détails.**

### Rapports de Bugs
- **Issues GitHub** pour les bugs
- **Logs complets** requis
- **Exemples reproductibles** appréciés

### Suggestions
- **Nouvelles fonctionnalités** via discussions
- **Améliorations** de performance
- **Nouveaux langages** envisagés

---

## 📄 Licence

**PyMorph v1.0.0 - Licence Restrictive**

Voir le fichier `LICENSE` pour les termes complets.

**Points clés:**
- ✅ **Utilisation autorisée** du programme
- ✅ **Obfuscation de votre code** permise
- ❌ **Réutilisation du code source** interdite
- ❌ **Redistribution** non autorisée
- ❌ **Vente** du programme interdite
- ❌ **Modification** du code source interdite

---

## 🚀 Version

**Version actuelle:** `v1.0.0`
**Auteur:** `yo-le-zz`
**Date:** `2026-04-27`
**Statut:** `Production Ready`

---

## 📞 Contact

**Pour le support et questions:**
- **GitHub Issues** (problèmes techniques)
- **Documentation** dans `/docs/`
- **README des tests** dans `/tests/`

---

**🔐 PyMorph v1.0.0 - Protégez votre code, multi-langages.**

*Avec une obfuscation si avancée que même vous ne le reconnaîtrez plus !* 😄
