"""
PyMorph Build Script
Script de compilation pour créer l'exécutable PyMorph
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Installe les dépendances nécessaires"""
    print("🔧 Installation des dépendances...")
    
    dependencies = [
        "customtkinter",
        "nuitka"
    ]
    
    for dep in dependencies:
        try:
            print(f"   📦 Installation de {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"   ✅ {dep} installé")
        except subprocess.CalledProcessError:
            print(f"   ❌ Erreur lors de l'installation de {dep}")
            return False
    
    return True

def check_icon():
    """Vérifie si une icône existe"""
    icon_path = Path("assets/icon.ico")
    if icon_path.exists():
        print("   ✅ Icône trouvée")
        return True
    else:
        print("   ⚠️ Aucune icône trouvée, utilisation de l'icône par défaut")
        return False

def build_executable():
    """Compile l'exécutable PyMorph avec Nuitka"""
    print("🔥 Compilation de PyMorph...")
    
    # S'assurer que le répertoire dist existe
    Path("dist").mkdir(exist_ok=True)
    
    # Commande Nuitka
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--assume-yes-for-downloads",
        "--remove-output",
        "--no-pyi-file",
        "--enable-plugin=pyqt6",
        "--enable-plugin=numpy",
        "--enable-plugin=tk-inter",
        "--noupx",
        "--noupx-dir",
        "--noupx-onefile",
        f"--output-dir=dist",
        f"--output-filename=PyMorph.exe",
        "--windows-icon-from-ico=assets/icon.ico" if Path("assets/icon.ico").exists() else "",
        "--company-name=yo-le-zz",
        "--product-name=PyMorph",
        "--product-version=1.0.0",
        "--file-version=1.0.0",
        "--file-description=PyMorph Multi-Language Obfuscator",
        "--copyright=Copyright (c) 2026 yo-le-zz",
        "src/enhanced_gui.py"
    ]
    
    # Filtrer les arguments vides
    cmd = [arg for arg in cmd if arg]
    
    try:
        print(f"   📦 Commande: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Compilation réussie!")
        
        # Nettoyer les fichiers temporaires
        build_dir = Path("dist/PyMorph.build")
        if build_dir.exists():
            shutil.rmtree(build_dir)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erreur de compilation: {e}")
        print(f"   📋 Sortie d'erreur: {e.stderr}")
        return False

def create_portable_package():
    """Crée un package portable"""
    print("📦 Création du package portable...")
    
    package_dir = Path("dist/PyMorph_Portable")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir(parents=True)
    
    # Copier l'exécutable
    exe_path = Path("dist/PyMorph.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir / "PyMorph.exe")
        print("   ✅ Exécutable copié")
    
    # Copier les assets
    assets_dir = Path("assets")
    if assets_dir.exists():
        shutil.copytree(assets_dir, package_dir / "assets")
        print("   ✅ Assets copiés")
    
    # Créer un README pour le package
    readme_content = """# PyMorph v1.0.0 - Package Portable

## Utilisation

1. Double-cliquez sur `PyMorph.exe` pour lancer l'interface graphique
2. Sélectionnez votre fichier Python à obfusquer
3. Choisissez vos options d'obfuscation
4. Lancez le processus

## Fonctionnalités

- 🔐 Obfuscation complète du code Python
- 📁 Support multi-fichiers
- 🔤 Encodage des chaînes en base64
- 🚀 Compilation en exécutable
- 🎨 Interface graphique moderne

## Fichiers générés

Les fichiers obfusqués seront créés dans le même répertoire que vos fichiers sources:
- `obfuscated_nom.py` - Script obfusqué
- `obfuscated_output/` - Répertoire multi-fichiers
- `nom.exe` - Exécutable compilé

## Support

Pour plus d'informations, consultez la documentation dans le dossier `docs/`.

---
PyMorph v1.0.0 - Protégez votre code Python 🛡️
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("   ✅ Package portable créé dans dist/PyMorph_Portable")

def main():
    """Fonction principale de build"""
    print("🚀 PyMorph Build Script v1.0.0")
    print("=" * 50)
    
    # Étape 1: Installer les dépendances
    if not install_dependencies():
        print("❌ Échec de l'installation des dépendances")
        return False
    
    # Étape 2: Vérifier l'icône
    check_icon()
    
    # Étape 3: Compiler l'exécutable
    if not build_executable():
        print("❌ Échec de la compilation")
        return False
    
    # Étape 4: Créer le package portable
    create_portable_package()
    
    print("\n🎉 Build terminé avec succès !")
    print("📦 Fichiers créés:")
    print("   • dist/PyMorph.exe - Exécutable principal")
    print("   • dist/PyMorph_Portable/ - Package portable")
    print("\n✅ PyMorph est prêt à être distribué !")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\nAppuyez sur Entrée pour quitter...")
        else:
            input("\nAppuyez sur Entrée pour quitter...")
    except KeyboardInterrupt:
        print("\n⏹️ Build annulé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        input("\nAppuyez sur Entrée pour quitter...")
