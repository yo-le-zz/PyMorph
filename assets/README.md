# PyMorph Assets

Ce dossier contient les ressources utilisées par PyMorph.

## Fichiers

### icon.ico
Icône de l'application PyMorph.

**Spécifications:**
- Taille: 256x256 pixels
- Format: ICO avec plusieurs tailles (16x16, 32x32, 48x48, 128x128, 256x256)
- Style: Moderne avec cadenas stylisé

### Création de l'icône

Si vous souhaitez personnaliser l'icône :

1. **Design:**
   - Theme: Sombre/bleu
   - Éléments: Cadenas + texte "Py"
   - Dimensions carrées

2. **Outils recommandés:**
   - Adobe Illustrator
   - Inkscape (gratuit)
   - GIMP (gratuit)
   - IcoFX (spécialisé ICO)

3. **Format requis:**
   - Format ICO avec multiples tailles
   - Transparence supportée
   - Compatible Windows

### Génération automatique

Le script `build.py` peut générer une icône par défaut si aucune n'est présente.

```python
# Dans build.py
create_icon()  # Génère icon.ico si inexistant
```

## Ajout de ressources

Pour ajouter de nouvelles ressources :

1. Placer les fichiers dans ce dossier
2. Mettre à jour `build.py` pour les inclure
3. Documenter les nouveaux fichiers ici

## Formats supportés

- **ICO**: Icônes Windows
- **PNG**: Images avec transparence
- **SVG**: Vectoriels (pour documentation)

## Licence

Les assets sont distribués sous la même licence que PyMorph.
