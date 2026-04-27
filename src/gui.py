"""
PyMorph GUI - Interface CustomTkinter
Interface graphique moderne pour l'obfuscateur Python
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess
import shutil

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymorph import obfuscate, compile_with_nuitka

class PyMorphGUI:
    def __init__(self):
        # Configuration du thème
        ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("PyMorph v1.0.0 - Obfuscateur Python")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Désactiver l'icône par défaut pour éviter l'erreur
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # Variables
        self.input_file = ctk.StringVar()
        self.output_name = ctk.StringVar()
        self.log_file = ctk.StringVar(value="obfuscation.log")
        self.encode_strings = ctk.BooleanVar()
        self.multi_file = ctk.BooleanVar()
        self.compile_exe = ctk.BooleanVar()
        
        # Création de l'interface
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Frame principal avec padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Zone de sélection de fichier
        self.create_file_selection(main_frame)
        
        # Options d'obfuscation
        self.create_options(main_frame)
        
        # Options de compilation
        self.create_compilation_options(main_frame)
        
        # Zone de logs
        self.create_log_area(main_frame)
        
        # Boutons d'action
        self.create_action_buttons(main_frame)
        
    def create_header(self, parent):
        """Crée le header avec logo et titre"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titre principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔐 PyMorph v1.0.0",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Obfuscateur Python Multi-File avec Compilation Nuitka",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack()
        
    def create_file_selection(self, parent):
        """Zone de sélection du fichier d'entrée"""
        file_frame = ctk.CTkFrame(parent)
        file_frame.pack(fill="x", pady=10)
        
        # Label
        ctk.CTkLabel(file_frame, text="📁 Fichier Python à obfusquer:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Frame pour la sélection
        select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        select_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Champ de fichier
        self.file_entry = ctk.CTkEntry(
            select_frame,
            textvariable=self.input_file,
            placeholder_text="Sélectionnez un fichier Python...",
            font=ctk.CTkFont(size=12)
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton de sélection
        select_btn = ctk.CTkButton(
            select_frame,
            text="📂 Parcourir",
            command=self.select_file,
            width=120
        )
        select_btn.pack(side="right")
        
    def create_options(self, parent):
        """Options d'obfuscation"""
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", pady=10)
        
        # Label
        ctk.CTkLabel(options_frame, text="⚙️ Options d'obfuscation:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Options
        options_container = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # Encoder les strings
        strings_check = ctk.CTkCheckBox(
            options_container,
            text="🔤 Encoder les chaînes en base64",
            variable=self.encode_strings
        )
        strings_check.pack(anchor="w", pady=5)
        
        # Multi-fichier
        multifile_check = ctk.CTkCheckBox(
            options_container,
            text="📁 Traiter tous les fichiers importés (multi-fichier)",
            variable=self.multi_file
        )
        multifile_check.pack(anchor="w", pady=5)
        
        # Fichier de logs
        log_frame = ctk.CTkFrame(options_container, fg_color="transparent")
        log_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(log_frame, text="📋 Fichier de logs:").pack(side="left")
        log_entry = ctk.CTkEntry(
            log_frame,
            textvariable=self.log_file,
            width=200
        )
        log_entry.pack(side="left", padx=(10, 0))
        
    def create_compilation_options(self, parent):
        """Options de compilation"""
        comp_frame = ctk.CTkFrame(parent)
        comp_frame.pack(fill="x", pady=10)
        
        # Label
        ctk.CTkLabel(comp_frame, text="🚀 Options de compilation:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Options
        comp_container = ctk.CTkFrame(comp_frame, fg_color="transparent")
        comp_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # Compiler en exe
        compile_check = ctk.CTkCheckBox(
            comp_container,
            text="🔥 Compiler en exécutable (.exe) avec Nuitka",
            variable=self.compile_exe,
            command=self.toggle_compilation_options
        )
        compile_check.pack(anchor="w", pady=5)
        
        # Nom de sortie (désactivé par défaut)
        self.output_frame = ctk.CTkFrame(comp_container, fg_color="transparent")
        self.output_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(self.output_frame, text="📦 Nom de sortie:").pack(side="left")
        self.output_entry = ctk.CTkEntry(
            self.output_frame,
            textvariable=self.output_name,
            placeholder_text="nom_du_fichier",
            width=200
        )
        self.output_entry.pack(side="left", padx=(10, 0))
        
        # Désactiver par défaut
        self.output_entry.configure(state="disabled")
        
    def create_log_area(self, parent):
        """Zone d'affichage des logs"""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, pady=10)
        
        # Label
        ctk.CTkLabel(log_frame, text="📜 Journal d'obfuscation:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Zone de texte pour les logs
        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Le scrollbar est automatiquement géré par CustomTkinter
        
    def create_action_buttons(self, parent):
        """Boutons d'action"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Bouton principal
        self.obfuscate_btn = ctk.CTkButton(
            button_frame,
            text="🔐 Lancer l'obfuscation",
            command=self.start_obfuscation,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.obfuscate_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton d'aide
        help_btn = ctk.CTkButton(
            button_frame,
            text="❓ Aide",
            command=self.show_help,
            width=100
        )
        help_btn.pack(side="right")
        
        # Bouton pour effacer les logs
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Effacer",
            command=self.clear_logs,
            width=100
        )
        clear_btn.pack(side="right", padx=(0, 10))
        
    def select_file(self):
        """Ouvre un dialogue pour sélectionner un fichier"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier Python",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.input_file.set(file_path)
            # Définir automatiquement le nom de sortie
            if not self.output_name.get():
                self.output_name.set(Path(file_path).stem)
                
    def toggle_compilation_options(self):
        """Active/désactive les options de compilation"""
        if self.compile_exe.get():
            self.output_entry.configure(state="normal")
        else:
            self.output_entry.configure(state="disabled")
            
    def log_message(self, message):
        """Ajoute un message dans la zone de logs"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def clear_logs(self):
        """Efface la zone de logs"""
        self.log_text.delete("1.0", "end")
        
    def show_help(self):
        """Affiche la fenêtre d'aide"""
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Aide - PyMorph")
        help_window.geometry("600x500")
        
        # Contenu de l'aide
        help_text = """
🔐 PYMORPH - GUIDE D'UTILISATION

📋 DESCRIPTION:
PyMorph est un obfuscateur Python avancé qui transforme votre code en une version quasiment illisible tout en préservant 100% de sa fonctionnalité.

🎯 UTILISATION:

1. Sélectionnez votre fichier Python avec le bouton "Parcourir"
2. Choisissez vos options d'obfuscation:
   • 🔤 Encoder les chaînes: Transforme les strings en base64
   • 📁 Multi-fichier: Traite tous les imports automatiquement
3. Optionnellement, compilez en .exe:
   • Cochez "Compiler en exécutable"
   • Définissez un nom de sortie
4. Cliquez sur "Lancer l'obfuscation"

⚙️ OPTIONS DISPONIBLES:

• Encoder les strings: Les chaînes sont encodées en base64 et décodées dynamiquement
• Multi-fichier: Détecte et obfusque tous les fichiers importés
• Compilation: Crée un fichier .exe autonome avec Nuitka

📁 FICHIERS GÉNÉRÉS:

• obfuscated_nom.py: Script obfusqué
• obfuscated_output/: Répertoire pour les projets multi-fichiers
• nom.exe: Exécutable compilé (si option activée)
• obfuscation.log: Logs détaillés du processus

🛡️ NIVEAU DE PROTECTION:

• Variables renommées aléatoirement
• Fonctions et classes obfusquées
• Nombres décomposés (10 → 7 + 3)
• Variables factices ajoutées
• Strings encodés en base64
• Compilation binaire optionnelle

💡 CONSEILS:

• Testez toujours votre code obfusqué avant distribution
• Sauvegardez votre code original
• Pour les projets complexes, utilisez le mode multi-fichier
• La compilation peut prendre plusieurs minutes

⚠️ AVERTISSEMENT:

PyMorph est conçu pour la protection intellectuelle légale. 
Utilisez-le responsable et conformément aux lois applicables.
"""
        
        help_textbox = ctk.CTkTextbox(help_window, font=ctk.CTkFont(size=12))
        help_textbox.pack(fill="both", expand=True, padx=20, pady=20)
        help_textbox.insert("1.0", help_text)
        help_textbox.configure(state="disabled")
        
    def start_obfuscation(self):
        """Démarre le processus d'obfuscation dans un thread séparé"""
        if not self.input_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier Python.")
            return
            
        if not Path(self.input_file.get()).exists():
            messagebox.showerror("Erreur", "Le fichier sélectionné n'existe pas.")
            return
            
        # Désactiver le bouton pendant le traitement
        self.obfuscate_btn.configure(state="disabled", text="⏳ Traitement en cours...")
        
        # Lancer dans un thread séparé
        thread = threading.Thread(target=self.obfuscate_worker)
        thread.daemon = True
        thread.start()
        
    def obfuscate_worker(self):
        """Worker pour l'obfuscation (thread séparé)"""
        try:
            # Nettoyer les logs
            self.clear_logs()
            
            # Log des informations
            self.log_message("🚀 Démarrage de PyMorph v1.0.0")
            self.log_message("=" * 50)
            self.log_message(f"📁 Fichier: {self.input_file.get()}")
            self.log_message(f"🔧 Options: Strings={self.encode_strings.get()}, Multi-file={self.multi_file.get()}, Compilation={self.compile_exe.get()}")
            self.log_message("=" * 50)
            
            # Obfuscation
            results = obfuscate(
                self.input_file.get(),
                self.log_file.get(),
                self.encode_strings.get(),
                self.multi_file.get()
            )
            
            # Afficher les résultats
            if isinstance(results, list):
                # Mode multi-fichier
                self.log_message(f"📊 Fichiers traités: {len(results)}")
                for result in results:
                    self.log_message(f"   • {Path(result['input']).name} → {Path(result['output']).name}")
                    
                total_vars = sum(r['stats']['variables'] for r in results)
                total_funcs = sum(r['stats']['functions'] for r in results)
                total_classes = sum(r['stats']['classes'] for r in results)
                
                self.log_message(f"\n📈 Statistiques globales:")
                self.log_message(f"   🔢 Variables: {total_vars}")
                self.log_message(f"   ⚙️ Fonctions: {total_funcs}")
                self.log_message(f"   🏗️ Classes: {total_classes}")
                
                # Compilation
                if self.compile_exe.get():
                    self.log_message(f"\n🔥 Lancement de la compilation Nuitka...")
                    main_file = None
                    for result in results:
                        if 'main' in result['input'] or result['input'] == self.input_file.get():
                            main_file = result['output']
                            break
                    
                    if main_file:
                        success = compile_with_nuitka(main_file, self.output_name.get())
                        if success:
                            self.log_message(f"\n🎉 MISSION ACCOMPLIE !")
                            self.log_message(f"   📦 Exécutable: {self.output_name.get()}.exe")
                            self.log_message(f"   🛡️ Protection: Niveau MAXIMUM")
                            self.log_message(f"   ✅ Prêt à distribuer")
                        else:
                            self.log_message(f"\n⚠️ Obfuscation réussie mais compilation échouée")
                    else:
                        self.log_message("❌ Impossible de trouver le fichier principal à compiler")
                        
            else:
                # Mode single fichier
                stats = results[1] if isinstance(results, tuple) else {'variables': 0, 'functions': 0, 'classes': 0}
                output_file = results[0] if isinstance(results, tuple) else results
                
                self.log_message(f"📁 Fichier traité: {Path(self.input_file.get()).name}")
                self.log_message(f"📦 Sortie: {Path(output_file).name}")
                self.log_message(f"📈 Statistiques:")
                self.log_message(f"   🔢 Variables: {stats.get('variables', 0)}")
                self.log_message(f"   ⚙️ Fonctions: {stats.get('functions', 0)}")
                self.log_message(f"   🏗️ Classes: {stats.get('classes', 0)}")
                
                # Compilation
                if self.compile_exe.get():
                    self.log_message(f"\n🔥 Lancement de la compilation Nuitka...")
                    success = compile_with_nuitka(output_file, self.output_name.get())
                    if success:
                        self.log_message(f"\n🎉 MISSION ACCOMPLIE !")
                        self.log_message(f"   📦 Exécutable: {self.output_name.get()}.exe")
                        self.log_message(f"   🛡️ Protection: Niveau MAXIMUM")
                        self.log_message(f"   ✅ Prêt à distribuer")
                    else:
                        self.log_message(f"\n⚠️ Obfuscation réussie mais compilation échouée")
                else:
                    self.log_message(f"\n✅ Obfuscation terminée avec succès")
            
            self.log_message(f"\n💡 Conseil: Testez toujours votre code obfusqué avant distribution !")
            
            # Succès
            self.root.after(0, lambda: messagebox.showinfo("Succès", "Obfuscation terminée avec succès !"))
            
        except Exception as e:
            error_msg = f"❌ Erreur lors de l'obfuscation: {str(e)}"
            self.log_message(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Une erreur est survenue:\n{str(e)}"))
            
        finally:
            # Réactiver le bouton
            self.root.after(0, lambda: self.obfuscate_btn.configure(state="normal", text="🔐 Lancer l'obfuscation"))
            
    def run(self):
        """Démarre l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PyMorphGUI()
    app.run()
