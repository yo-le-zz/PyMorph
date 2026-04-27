"""
Enhanced PyMorph GUI - Interface CustomTkinter with Advanced Features
Interface graphique moderne avec options personnalisables et thèmes
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import threading
import sys
import os
from pathlib import Path
import subprocess
import shutil
import json
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from obfuscators import obfuscate_code, get_supported_languages, detect_language_from_filename

class EnhancedPyMorphGUI:
    def __init__(self):
        # Configuration initiale
        self.settings_file = "pymorph_settings.json"
        self.load_settings()
        
        # Configuration du thème
        ctk.set_appearance_mode(self.settings.get('theme_mode', 'dark'))
        ctk.set_default_color_theme(self.settings.get('color_theme', 'blue'))
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("🔐 PyMorph v1.0.0 - Multi-Language Code Obfuscator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Icône et configuration visuelle
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Variables
        self.input_file = ctk.StringVar()
        self.output_name = ctk.StringVar()
        self.log_file = ctk.StringVar(value="obfuscation.log")
        self.selected_language = ctk.StringVar(value="python")
        self.output_directory = ctk.StringVar(value="obfuscated_output")
        self.output_filename = ctk.StringVar()
        
        # Language-specific presets
        self.language_presets = {
            'python': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': False,
                'control_flow_obfuscation': False
            },
            'cpp': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': False
            },
            'javascript': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': True
            },
            'rust': {
                'decompose_numbers': True,
                'add_dummy_vars': False,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': False
            },
            'c': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': False
            },
            'java': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': False
            },
            'go': {
                'decompose_numbers': True,
                'add_dummy_vars': True,
                'rename_variables': True,
                'rename_functions': True,
                'rename_classes': True,
                'add_dummy_code': True,
                'control_flow_obfuscation': False
            }
        }
        
        # Variables d'options (toutes désactivables)
        self.options_vars = {
            'encode_strings': ctk.BooleanVar(value=True),
            'decompose_numbers': ctk.BooleanVar(value=True),
            'add_dummy_vars': ctk.BooleanVar(value=True),
            'rename_variables': ctk.BooleanVar(value=True),
            'rename_functions': ctk.BooleanVar(value=True),
            'rename_classes': ctk.BooleanVar(value=True),
            'multi_file': ctk.BooleanVar(value=False),
            'compile_exe': ctk.BooleanVar(value=False),
            'advanced_encoding': ctk.BooleanVar(value=True),
            'control_flow_obfuscation': ctk.BooleanVar(value=False),
            'add_dummy_code': ctk.BooleanVar(value=True),
            'obfuscate_macros': ctk.BooleanVar(value=False)
        }
        
        # Variables de personnalisation UI
        self.custom_colors = {
            'primary': self.settings.get('primary_color', '#1a5fb4'),
            'secondary': self.settings.get('secondary_color', '#3584e4'),
            'accent': self.settings.get('accent_color', '#99c1f1'),
            'background': self.settings.get('background_color', '#242424'),
            'surface': self.settings.get('surface_color', '#2b2b2b')
        }
        
        # Créer l'interface
        self.setup_ui()
        
    def load_settings(self):
        """Charger les paramètres depuis le fichier JSON"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = {
                    'theme_mode': 'dark',
                    'color_theme': 'blue',
                    'primary_color': '#1a5fb4',
                    'secondary_color': '#3584e4',
                    'accent_color': '#99c1f1',
                    'background_color': '#242424',
                    'surface_color': '#2b2b2b',
                    'window_geometry': '1000x800',
                    'last_input_file': '',
                    'last_output_dir': ''
                }
        except:
            self.settings = {}
    
    def save_settings(self):
        """Sauvegarder les paramètres dans le fichier JSON"""
        try:
            self.settings['theme_mode'] = ctk.get_appearance_mode()
            self.settings['window_geometry'] = self.root.geometry()
            self.settings['last_input_file'] = self.input_file.get()
            self.settings['last_output_dir'] = self.output_directory.get()
            
            # Sauvegarder les couleurs personnalisées
            for color_name, color_value in self.custom_colors.items():
                self.settings[f'{color_name}_color'] = color_value
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            self.add_log(f"❌ Erreur sauvegarde settings: {e}", "error")
    
    def setup_ui(self):
        """Configure l'interface utilisateur améliorée"""
        
        # Frame principal avec padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header avec personnalisation
        self.create_enhanced_header(main_frame)
        
        # Sélection de fichiers et langage
        self.create_file_and_language_selection(main_frame)
        
        # Options avancées
        self.create_advanced_options(main_frame)
        
        # Personnalisation
        self.create_customization_options(main_frame)
        
        # Logs
        self.create_log_section(main_frame)
        
        # Boutons d'action
        self.create_enhanced_action_buttons(main_frame)
        
        # Barre de status
        self.create_status_bar(main_frame)
    
    def create_enhanced_header(self, parent):
        """Header amélioré avec personnalisation"""
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Row supérieure avec titre et options
        top_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_row.pack(fill="x")
        
        # Frame pour les boutons à droite
        button_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        button_frame.pack(side="right", padx=5)
        
        # Boutons de personnalisation rapide
        theme_btn = ctk.CTkButton(
            button_frame,
            text="🎨 Thème",
            width=90,
            command=self.open_theme_settings,
            font=ctk.CTkFont(size=14)
        )
        theme_btn.pack(side="right", padx=5)
        
        settings_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ Params",
            width=90,
            command=self.open_settings,
            font=ctk.CTkFont(size=14)
        )
        settings_btn.pack(side="right", padx=5)
        
        # Titre principal (centré)
        title_label = ctk.CTkLabel(
            top_row,
            text="🔐 PyMorph v1.0.0",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title_label.pack(expand=True)
        
        # Sous-titre avec animations
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="🚀 Multi-Language Code Obfuscator • Python • C++ • JavaScript • Rust • C • Java • Go",
            font=ctk.CTkFont(size=18, weight="normal")
        )
        subtitle_label.pack(pady=(8, 0))
    
    def create_file_and_language_selection(self, parent):
        """Zone de sélection de fichier et de langue"""
        selection_frame = ctk.CTkFrame(parent)
        selection_frame.pack(fill="x", pady=10)
        
        # Titre de section
        title_label = ctk.CTkLabel(
            selection_frame,
            text="📁 Sélection Fichier & Langue",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Contenu
        content_frame = ctk.CTkFrame(selection_frame)
        content_frame.pack(fill="x", padx=10, pady=5)
        
        # Sélection de fichier
        file_frame_inner = ctk.CTkFrame(content_frame, fg_color="transparent")
        file_frame_inner.pack(fill="x", pady=5)
        
        file_label = ctk.CTkLabel(file_frame_inner, text="Fichier:", width=80)
        file_label.pack(side="left", padx=5)
        
        self.file_entry = ctk.CTkEntry(
            file_frame_inner,
            textvariable=self.input_file,
            placeholder_text="Sélectionnez un fichier à obfusquer..."
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        browse_btn = ctk.CTkButton(
            file_frame_inner,
            text="📂 Parcourir",
            width=100,
            command=self.browse_file
        )
        browse_btn.pack(side="right", padx=5)
        
        # Langage et preset
        lang_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        lang_frame.pack(fill="x", pady=5)
        
        lang_label = ctk.CTkLabel(lang_frame, text="Langage:", width=80)
        lang_label.pack(side="left", padx=5)
        
        # Sélection du langage
        languages = ['python', 'cpp', 'javascript', 'rust', 'c', 'java', 'go']
        self.language_combo = ctk.CTkComboBox(
            lang_frame,
            values=languages,
            variable=self.selected_language,
            command=lambda x: self.apply_language_preset()
        )
        self.language_combo.pack(side="left", padx=5)
        
        # Bouton preset
        preset_btn = ctk.CTkButton(
            lang_frame,
            text="⚡ Appliquer Preset",
            width=120,
            command=self.apply_language_preset
        )
        preset_btn.pack(side="right", padx=5)
        
        # Dossier de sortie
        output_dir_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        output_dir_frame.pack(fill="x", pady=5)
        
        dir_label = ctk.CTkLabel(output_dir_frame, text="Dossier:", width=80)
        dir_label.pack(side="left", padx=5)
        
        self.dir_entry = ctk.CTkEntry(
            output_dir_frame,
            textvariable=self.output_directory,
            placeholder_text="Dossier de sortie..."
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        dir_btn = ctk.CTkButton(
            output_dir_frame,
            text="📁 Dossier",
            width=100,
            command=self.browse_output_directory
        )
        dir_btn.pack(side="right", padx=5)
        
        # Nom du fichier de sortie
        output_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        output_frame.pack(fill="x", pady=5)
        
        output_label = ctk.CTkLabel(output_frame, text="Nom:", width=80)
        output_label.pack(side="left", padx=5)
        
        self.output_entry = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_filename,
            placeholder_text="Nom du fichier obfusqué (ex: mon_script_obfusqué.py)..."
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Bouton de génération automatique du nom
        auto_btn = ctk.CTkButton(
            output_frame,
            text="🔄 Auto",
            width=60,
            command=self.generate_output_filename
        )
        auto_btn.pack(side="right", padx=5)
        
        return selection_frame
    
    def create_advanced_options(self, parent):
        """Options d'obfuscation avancées avec toggle"""
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", pady=10)
        
        # Titre avec bouton tout/rien
        title_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="⚙️ Options d'Obfuscation Avancées",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left")
        
        # Boutons tout/rien
        all_btn = ctk.CTkButton(
            title_frame,
            text="✅ Tout",
            width=50,
            command=self.enable_all_options
        )
        all_btn.pack(side="right", padx=2)
        
        none_btn = ctk.CTkButton(
            title_frame,
            text="❌ Rien",
            width=50,
            command=self.disable_all_options
        )
        none_btn.pack(side="right", padx=2)
        
        # Options en deux colonnes
        options_content = ctk.CTkFrame(options_frame)
        options_content.pack(fill="x", padx=10, pady=5)
        
        # Colonne gauche
        left_col = ctk.CTkFrame(options_content, fg_color="transparent")
        left_col.pack(side="left", fill="x", expand=True, padx=5)
        
        # Colonne droite
        right_col = ctk.CTkFrame(options_content, fg_color="transparent")
        right_col.pack(side="right", fill="x", expand=True, padx=5)
        
        # Options par colonne
        left_options = [
            ('decompose_numbers', '🔢 Décomposer les nombres'),
            ('rename_variables', '🏷️ Renommer variables'),
            ('rename_functions', '📝 Renommer fonctions')
        ]
        
        right_options = [
            ('rename_classes', '📦 Renommer classes'),
            ('add_dummy_vars', '🎭 Ajouter variables factices')
        ]
        
        for col_frame, column in [(left_col, left_options), (right_col, right_options)]:
            for var_key, label_text in column:
                var = self.options_vars[var_key]
                checkbox = ctk.CTkCheckBox(
                    col_frame,
                    text=label_text,
                    variable=var
                )
                checkbox.pack(anchor="w", pady=2)
    
    def create_customization_options(self, parent):
        """Options de personnalisation de l'UI"""
        custom_frame = ctk.CTkFrame(parent)
        custom_frame.pack(fill="x", pady=10)
        
        # Titre
        title_label = ctk.CTkLabel(
            custom_frame,
            text="🎨 Personnalisation de l'Interface",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Options de personnalisation
        custom_content = ctk.CTkFrame(custom_frame)
        custom_content.pack(fill="x", padx=10, pady=5)
        
        # Première ligne de couleurs
        color_row1 = ctk.CTkFrame(custom_content, fg_color="transparent")
        color_row1.pack(fill="x", pady=2)
        
        # Boutons de couleur
        colors = [
            ('primary', 'Primaire', self.custom_colors['primary']),
            ('secondary', 'Secondaire', self.custom_colors['secondary']),
            ('accent', 'Accent', self.custom_colors['accent']),
            ('background', 'Fond', self.custom_colors['background'])
        ]
        
        for color_key, label, color_value in colors:
            color_frame = ctk.CTkFrame(color_row1, fg_color="transparent")
            color_frame.pack(side="left", padx=5)
            
            label_widget = ctk.CTkLabel(color_frame, text=f"{label}:", width=80)
            label_widget.pack(side="left")
            
            color_btn = ctk.CTkButton(
                color_frame,
                text="    ",
                width=30,
                fg_color=color_value,
                command=lambda k=color_key: self.choose_color(k)
            )
            color_btn.pack(side="left", padx=5)
    
    def create_log_section(self, parent):
        """Section de logs améliorée"""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, pady=10)
        
        # Header avec contrôles
        log_header = ctk.CTkFrame(log_frame)
        log_header.pack(fill="x", padx=10, pady=(10, 5))
        
        log_title = ctk.CTkLabel(
            log_header,
            text="📋 Journal d'Activité",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        log_title.pack(side="left")
        
        # Boutons de contrôle de logs
        clear_log_btn = ctk.CTkButton(
            log_header,
            text="🗑️ Vider",
            width=60,
            command=self.clear_log
        )
        clear_log_btn.pack(side="right", padx=2)
        
        save_log_btn = ctk.CTkButton(
            log_header,
            text="💾 Sauver",
            width=60,
            command=self.save_log
        )
        save_log_btn.pack(side="right", padx=2)
        
        # Zone de texte avec scrollbar
        log_content = ctk.CTkFrame(log_frame)
        log_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = ctk.CTkTextbox(
            log_content,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.log_text.pack(fill="both", expand=True)
        
        # Log initial
        self.add_log("🚀 PyMorph v1.0.0 - Multi-Language Code Obfuscator - Prêt", "info")
    
    def create_enhanced_action_buttons(self, parent):
        """Boutons d'action améliorés"""
        action_frame = ctk.CTkFrame(parent)
        action_frame.pack(fill="x", pady=10)
        
        # Boutons principaux
        button_row = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_row.pack(pady=10)
        
        # Bouton d'obfuscation principal
        self.obfuscate_btn = ctk.CTkButton(
            button_row,
            text="🚀 LANCER L'OBFUSCATION",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=60,
            width=200,
            command=self.start_obfuscation,
            fg_color="#1e8449",
            hover_color="#27ae60"
        )
        self.obfuscate_btn.pack(side="left", expand=True, padx=10)
        
        # Bouton de test
        self.test_btn = ctk.CTkButton(
            button_row,
            text="🧪 TESTER",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            width=150,
            command=self.test_obfuscation,
            fg_color="#d68910",
            hover_color="#f39c12"
        )
        self.test_btn.pack(side="left", expand=True, padx=10)
        
        # Bouton d'aide
        self.help_btn = ctk.CTkButton(
            button_row,
            text="❓ AIDE",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            width=150,
            command=self.show_help,
            fg_color="#2980b9",
            hover_color="#3498db"
        )
        self.help_btn.pack(side="left", expand=True, padx=10)
    
    def create_status_bar(self, parent):
        """Barre de status"""
        status_frame = ctk.CTkFrame(parent, height=30)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Prêt",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Compteur
        self.counter_label = ctk.CTkLabel(
            status_frame,
            text="Fichiers: 0 | Options: 0",
            font=ctk.CTkFont(size=12)
        )
        self.counter_label.pack(side="right", padx=10)
    
    # Méthodes de fonctionnalité
    def browse_file(self):
        """Parcourir et sélectionner un fichier"""
        filetypes = [
            ("Python files", "*.py"),
            ("C++ files", "*.cpp *.cc *.cxx *.h *.hpp"),
            ("JavaScript files", "*.js *.jsx"),
            ("Rust files", "*.rs"),
            ("C files", "*.c *.h"),
            ("Java files", "*.java"),
            ("Go files", "*.go"),
            ("All supported files", "*.py *.cpp *.cc *.cxx *.h *.hpp *.js *.jsx *.rs *.c *.java *.go"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier à obfusquer",
            filetypes=filetypes,
            initialdir=self.settings.get('last_input_dir', '')
        )
        
        if filename:
            self.input_file.set(filename)
            self.settings['last_input_dir'] = os.path.dirname(filename)
            
            # Auto-detect language and apply preset
            detected_language = detect_language_from_filename(filename)
            self.selected_language.set(detected_language)
            self.apply_language_preset()
            
            # Generate output filename automatically
            self.generate_output_filename()
            
            self.add_log(f"📁 Fichier sélectionné: {filename}", "info")
            self.add_log(f"🔍 Langage détecté: {detected_language.upper()}", "info")
            self.update_status(f"Fichier: {os.path.basename(filename)} | Langage: {detected_language.upper()}")
    
    def browse_output_directory(self):
        """Parcourir et sélectionner un dossier de sortie"""
        directory = filedialog.askdirectory(
            title="Sélectionner un dossier de sortie",
            initialdir=self.settings.get('last_output_dir', '')
        )
        
        if directory:
            self.output_directory.set(directory)
            self.settings['last_output_dir'] = directory
            self.add_log(f"📁 Dossier de sortie: {directory}", "info")
    
    def generate_output_filename(self):
        """Génère automatiquement un nom de fichier obfusqué"""
        input_file = self.input_file.get()
        if input_file:
            input_path = Path(input_file)
            language = self.selected_language.get()
            
            # Extensions par langage
            extensions = {
                'python': '.py',
                'cpp': '.cpp',
                'javascript': '.js',
                'rust': '.rs',
                'c': '.c',
                'java': '.java',
                'go': '.go'
            }
            
            # Générer le nom
            base_name = input_path.stem
            obf_name = f"{base_name}_obfuscated{extensions.get(language, '.txt')}"
            self.output_filename.set(obf_name)
            
            self.add_log(f"🔄 Nom généré: {obf_name}", "info")
    
    def apply_language_preset(self):
        """Applique le preset du langage sélectionné"""
        language = self.selected_language.get()
        if language in self.language_presets:
            preset = self.language_presets[language]
            for option, value in preset.items():
                if option in self.options_vars:
                    self.options_vars[option].set(value)
            self.add_log(f"✅ Preset '{language}' appliqué", "success")
    
    def enable_all_options(self):
        """Activer toutes les options"""
        for var in self.options_vars.values():
            var.set(True)
        self.add_log("✅ Toutes les options activées", "success")
    
    def disable_all_options(self):
        """Désactiver toutes les options"""
        for var in self.options_vars.values():
            var.set(False)
        self.add_log("❌ Toutes les options désactivées", "info")
    
    def choose_color(self, color_key):
        """Choisir une couleur personnalisée"""
        color = colorchooser.askcolor(title=f"Choisir la couleur {color_key}")
        if color[1]:
            self.custom_colors[color_key] = color[1]
            self.apply_colors()
            self.add_log(f"🎨 Couleur {color_key} changée", "info")
    
    def reset_colors(self):
        """Réinitialiser les couleurs par défaut"""
        default_colors = {
            'primary': '#1a5fb4',
            'secondary': '#3584e4',
            'accent': '#99c1f1',
            'background': '#242424',
            'surface': '#2b2b2b'
        }
        
        self.custom_colors.update(default_colors)
        self.settings.update({f"{k}_color": v for k, v in default_colors.items()})
        self.add_log("🔄 Couleurs réinitialisées", "info")
        self.apply_colors()
    
    def apply_colors(self):
        """Appliquer les couleurs personnalisées"""
        try:
            # Appliquer le thème
            theme_mode = self.settings.get('theme_mode', 'dark')
            ctk.set_appearance_mode(theme_mode)
            
            # Appliquer les couleurs personnalisées aux widgets principaux
            if hasattr(self, 'root') and self.root:
                # Appliquer la couleur de fond si disponible
                bg_color = self.custom_colors.get('background')
                if bg_color:
                    self.root.configure(fg_color=bg_color)
                
                # Mettre à jour les couleurs des boutons principaux
                if hasattr(self, 'obfuscate_btn'):
                    primary_color = self.custom_colors.get('primary', '#1e8449')
                    self.obfuscate_btn.configure(fg_color=primary_color)
                
                # Mettre à jour les autres boutons si ils existent
                if hasattr(self, 'test_btn'):
                    secondary_color = self.custom_colors.get('secondary', '#d68910')
                    self.test_btn.configure(fg_color=secondary_color)
                
                if hasattr(self, 'help_btn'):
                    accent_color = self.custom_colors.get('accent', '#2980b9')
                    self.help_btn.configure(fg_color=accent_color)
                
                # Mettre à jour le thème de couleur de CustomTkinter
                color_theme = self.settings.get('color_theme', 'blue')
                ctk.set_default_color_theme(color_theme)
                
                # Sauvegarder les settings
                self.save_settings()
                self.add_log("🎨 Couleurs appliquées avec succès", "success")
                
                # Forcer la mise à jour de l'interface
                self.root.update()
        except Exception as e:
            self.add_log(f"❌ Erreur application couleurs: {e}", "error")
    
    def add_log(self, message, level="info"):
        """Ajouter un message au log avec couleur"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Couleurs selon le niveau
        level_colors = {
            'info': '⚪',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        prefix = level_colors.get(level, '⚪')
        formatted_message = f"[{timestamp}] {prefix} {message}\n"
        
        self.log_text.insert("end", formatted_message)
        self.log_text.see("end")
    
    def clear_log(self):
        """Vider la zone de logs"""
        self.log_text.delete("1.0", "end")
        self.add_log("🗑️ Log vidé", "info")
    
    def save_log(self):
        """Sauvegarder le log dans un fichier"""
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder le log",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get("1.0", "end"))
                self.add_log(f"💾 Log sauvegardé: {filename}", "success")
            except Exception as e:
                self.add_log(f"❌ Erreur sauvegarde log: {e}", "error")
    
    def update_status(self, message):
        """Mettre à jour la barre de status"""
        self.status_label.configure(text=message)
        
        # Mettre à jour le compteur
        active_options = sum(1 for var in self.options_vars.values() if var.get())
        self.counter_label.configure(text=f"Fichiers: {1 if self.input_file.get() else 0} | Options: {active_options}")
    
    def clear_all(self):
        """Effacer tous les champs"""
        self.input_file.set("")
        self.output_name.set("")
        self.add_log("🗑️ Tous les champs vidés", "info")
        self.update_status("Prêt")
    
    def quick_obfuscate(self):
        """Obfuscation rapide avec options par défaut"""
        if not self.input_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier d'abord!")
            return
        
        # Activer les options essentielles
        essential_options = ['encode_strings', 'rename_variables', 'rename_functions']
        for key in essential_options:
            self.options_vars[key].set(True)
        
        self.start_obfuscation()
    
    def start_obfuscation(self):
        """Démarrer le processus d'obfuscation"""
        if not self.input_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier!")
            return
        
        # Désactiver le bouton pendant le traitement
        self.obfuscate_btn.configure(state="disabled")
        self.add_log("🔄 Début de l'obfuscation...", "info")
        self.update_status("Obfuscation en cours...")
        
        # Lancer dans un thread séparé
        threading.Thread(target=self._obfuscate_worker, daemon=True).start()
    
    def _obfuscate_worker(self):
        """Worker d'obfuscation en arrière-plan"""
        try:
            # Préparer les options
            options = {key: var.get() for key, var in self.options_vars.items()}
            
            # Obtenir les chemins
            input_file = self.input_file.get()
            output_dir = self.output_directory.get()
            output_filename = self.output_filename.get()
            language = self.selected_language.get()
            
            # Créer le dossier de sortie s'il n'existe pas
            os.makedirs(output_dir, exist_ok=True)
            self.add_log(f"📁 Dossier de sortie: {output_dir}", "info")
            
            # Lire le fichier
            with open(input_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.add_log(f"📖 Fichier lu: {len(code)} caractères", "info")
            
            # Obfusquer le code avec les options
            obfuscated_code, stats = obfuscate_code(code, language, options)
            
            # Déterminer le chemin de sortie
            if output_filename:
                output_path = os.path.join(output_dir, output_filename)
            else:
                # Générer automatiquement si non spécifié
                input_path = Path(input_file)
                extensions = {
                    'python': '.py', 'cpp': '.cpp', 'javascript': '.js',
                    'rust': '.rs', 'c': '.c', 'java': '.java', 'go': '.go'
                }
                ext = extensions.get(language, '.txt')
                output_path = os.path.join(output_dir, f"{input_path.stem}_obfuscated{ext}")
            
            # Écrire le fichier obfusqué
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(obfuscated_code)
            
            # Afficher les statistiques
            self.add_log("✅ Obfuscation terminée avec succès!", "success")
            self.add_log(f"📄 Fichier de sortie: {output_path}", "success")
            
            if stats:
                for key, value in stats.items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            self.add_log(f"📊 {key}.{sub_key}: {sub_value}", "info")
                    else:
                        self.add_log(f"📊 {key}: {value}", "info")
            
            self.update_status("✅ Obfuscation terminée")
            
        except Exception as e:
            error_msg = f"❌ Erreur d'obfuscation: {str(e)}"
            self.add_log(error_msg, "error")
            self.update_status("❌ Erreur")
            messagebox.showerror("Erreur d'obfuscation", str(e))
        
        finally:
            # Réactiver le bouton
            self.obfuscate_btn.configure(state="normal")
    
    def test_obfuscation(self):
        """Tester l'obfuscation avec un fichier test"""
        # Créer un fichier test simple
        test_code = '''def hello_world():
    name = "World"
    message = f"Hello, {name}!"
    print(message)
    return message

result = hello_world()
'''
        
        # Écrire le fichier test
        test_file = "test_sample.py"
        with open(test_file, 'w') as f:
            f.write(test_code)
        
        self.input_file.set(test_file)
        self.selected_language.set("python")
        self.apply_language_preset()
        self.generate_output_filename()
        
        self.add_log("🧪 Fichier test créé", "info")
        self.start_obfuscation()
    
    def show_help(self):
        """Afficher l'aide"""
        help_text = """
🔐 PYMORPH - AIDE

📋 UTILISATION:
1. Sélectionnez un fichier à obfusquer
2. Choisissez le langage (auto-détection disponible)
3. Appliquez un preset ou configurez les options
4. Lancez l'obfuscation

⚙️ OPTIONS DISPONIBLES:
- 🔐 Encoder les chaînes: Encode les chaînes de caractères
- 🔢 Décomposer les nombres: Transforme les nombres en expressions
- 🏷️ Renommer variables: Change les noms de variables
- 📝 Renommer fonctions: Change les noms de fonctions
- 📦 Renommer classes: Change les noms de classes
- 🎭 Ajouter variables factices: Ajoute des variables inutiles
- 🌀 Obfusquer flux contrôle: Modifie la structure du code
- 📜 Ajouter code factice: Ajoute du code inutile

🎨 PERSONNALISATION:
- Cliquez sur les boutons de couleur pour personnaliser l'interface
- Les préférences sont sauvegardées automatiquement

📁 SORTIES:
- Les fichiers obfusqués sont sauvegardés dans le dossier de sortie
- Le nom par défaut est: nom_original_obfuscated.extension
"""
        
        # Créer une fenêtre d'aide
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("🔐 PyMorph - Aide")
        help_window.geometry("600x500")
        
        help_text_widget = ctk.CTkTextbox(help_window)
        help_text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        help_text_widget.insert("1.0", help_text)
        help_text_widget.configure(state="disabled")
    
    def open_theme_settings(self):
        """Ouvrir les paramètres de thème"""
        theme_window = ctk.CTkToplevel(self.root)
        theme_window.title("🎨 Paramètres de Thème")
        theme_window.geometry("400x300")
        
        # Mode de thème
        mode_frame = ctk.CTkFrame(theme_window)
        mode_frame.pack(fill="x", padx=10, pady=10)
        
        mode_label = ctk.CTkLabel(mode_frame, text="Mode:", font=ctk.CTkFont(size=14, weight="bold"))
        mode_label.pack(pady=5)
        
        mode_var = ctk.StringVar(value=self.settings.get('theme_mode', 'dark'))
        dark_radio = ctk.CTkRadioButton(mode_frame, text="Sombre", variable=mode_var, value="dark")
        dark_radio.pack(side="left", padx=10)
        
        light_radio = ctk.CTkRadioButton(mode_frame, text="Clair", variable=mode_var, value="light")
        light_radio.pack(side="left", padx=10)
        
        # Thème de couleur
        color_frame = ctk.CTkFrame(theme_window)
        color_frame.pack(fill="x", padx=10, pady=10)
        
        color_label = ctk.CTkLabel(color_frame, text="Thème de couleur:", font=ctk.CTkFont(size=14, weight="bold"))
        color_label.pack(pady=5)
        
        color_var = ctk.StringVar(value=self.settings.get('color_theme', 'blue'))
        themes = ['blue', 'green', 'dark-blue', 'red']
        
        for theme in themes:
            radio = ctk.CTkRadioButton(color_frame, text=theme.capitalize(), variable=color_var, value=theme)
            radio.pack(side="left", padx=10)
        
        # Boutons
        button_frame = ctk.CTkFrame(theme_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def apply_theme():
            ctk.set_appearance_mode(mode_var.get())
            ctk.set_default_color_theme(color_var.get())
            self.settings['theme_mode'] = mode_var.get()
            self.settings['color_theme'] = color_var.get()
            self.save_settings()
            self.add_log("🎨 Thème appliqué", "success")
            theme_window.destroy()
        
        apply_btn = ctk.CTkButton(button_frame, text="Appliquer", command=apply_theme)
        apply_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Annuler", command=theme_window.destroy)
        cancel_btn.pack(side="right", padx=5)
    
    def open_settings(self):
        """Ouvrir les paramètres généraux"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("⚙️ Paramètres")
        settings_window.geometry("500x400")
        
        # Informations
        info_frame = ctk.CTkFrame(settings_window)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_label = ctk.CTkLabel(info_frame, text="📊 Informations", font=ctk.CTkFont(size=16, weight="bold"))
        info_label.pack(pady=5)
        
        info_text = f"""
Version: PyMorph v1.0.0
Auteur: yo-le-zz
Fichier settings: {self.settings_file}
Dernier fichier: {self.settings.get('last_input_file', 'Aucun')}
Dernier dossier: {self.settings.get('last_output_dir', 'Aucun')}
"""
        info_widget = ctk.CTkTextbox(info_frame, height=100)
        info_widget.pack(fill="x", padx=5, pady=5)
        info_widget.insert("1.0", info_text)
        info_widget.configure(state="disabled")
        
        # Actions
        action_frame = ctk.CTkFrame(settings_window)
        action_frame.pack(fill="x", padx=10, pady=10)
        
        action_label = ctk.CTkLabel(action_frame, text="🔧 Actions", font=ctk.CTkFont(size=16, weight="bold"))
        action_label.pack(pady=5)
        
        reset_colors_btn = ctk.CTkButton(action_frame, text="🔄 Réinitialiser les couleurs", command=self.reset_colors)
        reset_colors_btn.pack(pady=5)
        
        reset_all_btn = ctk.CTkButton(action_frame, text="🗑️ Réinitialiser tout", command=self.reset_all_settings)
        reset_all_btn.pack(pady=5)
        
        close_btn = ctk.CTkButton(action_frame, text="❌ Fermer", command=settings_window.destroy)
        close_btn.pack(pady=10)
    
    def reset_all_settings(self):
        """Réinitialiser tous les paramètres"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir réinitialiser tous les paramètres?"):
            try:
                if os.path.exists(self.settings_file):
                    os.remove(self.settings_file)
                self.settings = {}
                self.load_settings()
                self.add_log("🔄 Paramètres réinitialisés", "success")
            except Exception as e:
                self.add_log(f"❌ Erreur réinitialisation: {e}", "error")
    
    def apply_ui_colors_on_startup(self):
        """Appliquer les couleurs sauvegardées au démarrage"""
        try:
            # Appliquer les couleurs personnalisées après que tous les widgets soient créés
            if hasattr(self, 'root'):
                # Appliquer la couleur de fond
                bg_color = self.custom_colors.get('background')
                if bg_color:
                    self.root.configure(fg_color=bg_color)
            
            if hasattr(self, 'obfuscate_btn'):
                primary_color = self.custom_colors.get('primary', '#1e8449')
                self.obfuscate_btn.configure(fg_color=primary_color)
            
            if hasattr(self, 'test_btn'):
                secondary_color = self.custom_colors.get('secondary', '#d68910')
                self.test_btn.configure(fg_color=secondary_color)
            
            if hasattr(self, 'help_btn'):
                accent_color = self.custom_colors.get('accent', '#2980b9')
                self.help_btn.configure(fg_color=accent_color)
            
            self.add_log("🎨 Couleurs appliquées au démarrage", "success")
        except Exception as e:
            self.add_log(f"❌ Erreur application couleurs démarrage: {e}", "error")
    
    def run(self):
        """Lancer l'interface graphique"""
        # Appliquer les couleurs après la création de tous les widgets
        self.root.after(100, self.apply_ui_colors_on_startup)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Quitter l'application proprement"""
        self.save_settings()
        self.root.destroy()

# Point d'entrée
if __name__ == "__main__":
    app = EnhancedPyMorphGUI()
    app.run()
