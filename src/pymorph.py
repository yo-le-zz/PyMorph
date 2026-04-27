import ast
import sys
import random
import string
import keyword
import builtins
import logging
import base64
import os
import importlib.util
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Import advanced protection
try:
    from .obfuscators.advanced_protection import apply_advanced_obfuscation
    ADVANCED_PROTECTION_AVAILABLE = True
except ImportError:
    ADVANCED_PROTECTION_AVAILABLE = False

BUILTINS = set(dir(builtins))
PROTECTED = BUILTINS | set(keyword.kwlist) | {
    "True", "False", "None", "__name__", "__file__", "self",
    "__init__", "__str__", "__repr__", "__call__", "__getitem__", "__setitem__",
    "__delitem__", "__contains__", "__iter__", "__next__", "__len__", "__bool__"
}


# =========================
# NAME GENERATOR
# =========================
def gen_name():
    return ''.join(random.choices(string.ascii_letters, k=8))


# =========================
# ANALYSER
# =========================
class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.var_usage = defaultdict(int)
        self.func_calls = defaultdict(int)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.var_usage[node.id] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.func_calls[node.func.id] += 1
        self.generic_visit(node)


# =========================
# MULTI-FILE MANAGER
# =========================
class MultiFileManager:
    def __init__(self):
        self.all_files = set()
        self.import_graph = defaultdict(set)
        self.processed_files = set()
        self.function_mappings = {}  # Pour stocker les mappings de fonctions entre fichiers
        
    def find_all_dependencies(self, file_path):
        """Trouve tous les fichiers dépendants récursivement"""
        if file_path in self.processed_files:
            return
            
        self.processed_files.add(file_path)
        self.all_files.add(file_path)
        
        # Ajouter tous les fichiers Python du même répertoire et sous-répertoires
        current_dir = Path(file_path).parent
        self._scan_directory_for_python_files(current_dir, current_dir)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Analyser les imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._handle_import(alias.name, file_path)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._handle_import(node.module, file_path)
                        
        except Exception as e:
            print(f"Erreur analysant {file_path}: {e}")
    
    def _scan_directory_for_python_files(self, directory, root_dir):
        """Scanne récursivement un répertoire pour trouver tous les fichiers Python"""
        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix == '.py':
                    # Ajouter tous les fichiers Python trouvés
                    self.all_files.add(str(item))
                elif item.is_dir() and not item.name.startswith('.'):
                    # Scanner les sous-répertoires récursivement
                    self._scan_directory_for_python_files(item, root_dir)
        except PermissionError:
            pass  # Ignorer les répertoires sans permission
            
    def _handle_import(self, module_name, current_file):
        """Gère un import pour trouver les fichiers locaux"""
        # Convertir le nom de module en chemin de fichier potentiel
        module_path = module_name.replace('.', os.sep)
        current_dir = Path(current_file).parent
        
        # Chercher les fichiers locaux correspondants avec gestion des sous-dossiers
        possible_paths = [
            current_dir / f"{module_path}.py",
            current_dir / module_path / "__init__.py"
        ]
        
        # Ajouter les chemins relatifs plus profonds
        if '.' in module_name:
            # Gérer les imports comme 'package.subpackage.module'
            parts = module_path.split(os.sep)
            for i in range(len(parts)):
                test_path = current_dir
                for j in range(i + 1):
                    test_path = test_path / parts[j]
                
                # Tester .py et __init__.py
                py_file = test_path.with_suffix('.py')
                init_file = test_path / '__init__.py'
                
                if py_file.exists() and py_file.is_file():
                    possible_paths.append(py_file)
                if init_file.exists() and init_file.is_file():
                    possible_paths.append(init_file)
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                self.import_graph[current_file].add(str(path))
                self.find_all_dependencies(str(path))
                break
                
    def get_all_files(self):
        """Retourne tous les fichiers à traiter"""
        return list(self.all_files)
        
    def add_function_mapping(self, file_path, func_map):
        """Ajoute les mappings de fonctions pour un fichier"""
        self.function_mappings[file_path] = func_map
        
    def get_function_mapping(self, module_name):
        """Retourne les mappings de fonctions pour un module"""
        # Chercher le fichier correspondant au module
        for file_path in self.all_files:
            if Path(file_path).stem == module_name:
                return self.function_mappings.get(file_path, {})
        return {}


# =========================
# OBFUSCATOR
# =========================
class Obfuscator(ast.NodeTransformer):
    def __init__(self, encode_strings=False):
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.import_map = {}
        self.used = set()
        self.encode_strings = encode_strings
        self.string_decoder_name = None

    def safe(self, name):
        return name not in PROTECTED

    def new(self):
        while True:
            n = gen_name()
            if n not in self.used:
                self.used.add(n)
                return n
                
    def encode_string(self, s):
        """Encode une chaîne en base64 avec une clé"""
        if not isinstance(s, str):
            return s
            
        # Créer une clé simple basée sur la chaîne
        key = sum(ord(c) for c in s) % 256
        encoded_bytes = base64.b64encode(s.encode('utf-8'))
        
        # Ajouter la clé au début
        return f"{key}:{encoded_bytes.decode('utf-8')}"
        
    def create_string_decoder(self):
        """Crée une fonction pour décoder les strings"""
        if self.string_decoder_name:
            return self.string_decoder_name
            
        self.string_decoder_name = self.new()
        
        # Créer la fonction de décodage
        decoder_code = f'''
def {self.string_decoder_name}(encoded_str):
    if ':' not in encoded_str:
        return encoded_str
    
    key, encoded = encoded_str.split(':', 1)
    try:
        import base64
        decoded = base64.b64decode(encoded).decode('utf-8')
        return decoded
    except:
        return encoded_str
'''
        
        return decoder_code
                
    def decompose_number(self, n):
        """Décompose un nombre en opérations plus complexes"""
        if not isinstance(n, (int, float)):
            return n
            
        # Pour les petits nombres, créer des opérations complexes
        if isinstance(n, int) and abs(n) < 100:
            if n == 0:
                return ast.BinOp(
                    left=ast.Constant(value=1),
                    op=ast.Sub(),
                    right=ast.Constant(value=1)
                )
            elif n == 1:
                return ast.BinOp(
                    left=ast.Constant(value=2),
                    op=ast.Sub(),
                    right=ast.Constant(value=1)
                )
            elif n > 0:
                # Décomposer en somme de deux nombres
                part1 = random.randint(1, max(1, n-1))
                part2 = n - part1
                return ast.BinOp(
                    left=ast.Constant(value=part1),
                    op=ast.Add(),
                    right=ast.Constant(value=part2)
                )
            else:
                # Pour les nombres négatifs
                part1 = random.randint(-10, -1)
                part2 = n - part1
                return ast.BinOp(
                    left=ast.Constant(value=part1),
                    op=ast.Add(),
                    right=ast.Constant(value=part2)
                )
        return ast.Constant(value=n)
        
    def create_dummy_operation(self):
        """Crée une opération mathématique inutile"""
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        ops = [ast.Add, ast.Sub, ast.Mult, ast.Div]
        op = random.choice(ops)
        
        if op == ast.Div and b == 0:
            b = 1
            
        return ast.BinOp(
            left=ast.Constant(value=a),
            op=op(),
            right=ast.Constant(value=b)
        )

    # =========================
    # CONSTANTS
    # =========================
    def visit_Constant(self, node):
        # Obfusquer les nombres
        if isinstance(node.value, (int, float)):
            return self.decompose_number(node.value)
        # Encoder les strings si demandé
        elif self.encode_strings and isinstance(node.value, str):
            encoded = self.encode_string(node.value)
            return ast.Call(
                func=ast.Name(id=self.string_decoder_name, ctx=ast.Load()),
                args=[ast.Constant(value=encoded)],
                keywords=[]
            )
        return node

    # =========================
    # IMPORTS
    # =========================
    def visit_Import(self, node):
        # Pour le mode multi-fichier, ne pas obfusquer les imports locaux
        if hasattr(self, 'file_manager'):
            # Vérifier si c'est un import local
            for alias in node.names:
                original_name = alias.name
                # Si c'est un module local, ne pas l'obfusquer
                if any(Path(f).stem == original_name for f in self.file_manager.all_files):
                    continue
                # Sinon, l'obfusquer normalement
                if original_name not in self.import_map:
                    self.import_map[original_name] = self.new()
                alias.asname = self.import_map[original_name]
        else:
            # Mode single fichier, obfusquer normalement
            for alias in node.names:
                original_name = alias.name
                if original_name not in self.import_map:
                    self.import_map[original_name] = self.new()
                alias.asname = self.import_map[original_name]
        
        self.generic_visit(node)
        return node
        
    def visit_ImportFrom(self, node):
        if node.module and node.module not in self.import_map:
            self.import_map[node.module] = self.new()
        self.generic_visit(node)
        return node

    # =========================
    # VARIABLES / NAMES
    # =========================
    def visit_Name(self, node):
        if self.safe(node.id):

            # Pour le mode multi-fichier, ne pas obfusquer les noms de modules locaux
            if hasattr(self, 'file_manager'):
                if any(Path(f).stem == node.id for f in self.file_manager.all_files):
                    return node

            # imports priority
            if node.id in self.import_map:
                node.id = self.import_map[node.id]
                return node

            # classes priority (for instantiation)
            if node.id in self.class_map:
                node.id = self.class_map[node.id]
                return node

            # functions priority
            if node.id in self.func_map:
                node.id = self.func_map[node.id]
                return node

            if node.id not in self.var_map:
                self.var_map[node.id] = self.new()

            node.id = self.var_map[node.id]

        return node

    # =========================
    # GLOBAL DECLARATIONS
    # =========================
    def visit_Global(self, node):
        for i, name in enumerate(node.names):
            if name in self.var_map:
                node.names[i] = self.var_map[name]
        self.generic_visit(node)
        return node

    
    # =========================
    # FUNCTIONS
    # =========================
    def visit_FunctionDef(self, node):
        if self.safe(node.name):
            if node.name not in self.func_map:
                self.func_map[node.name] = self.new()

            node.name = self.func_map[node.name]

        # args (sauf 'self' pour les méthodes)
        for arg in node.args.args:
            if self.safe(arg.arg) and arg.arg != 'self':
                if arg.arg not in self.var_map:
                    self.var_map[arg.arg] = self.new()
                arg.arg = self.var_map[arg.arg]

        # Ajouter des variables factices au début de chaque fonction
        dummy_statements = []
        for _ in range(random.randint(1, 3)):
            dummy_var = self.new()
            dummy_op = self.create_dummy_operation()
            dummy_assign = ast.Assign(
                targets=[ast.Name(id=dummy_var, ctx=ast.Store())],
                value=dummy_op
            )
            dummy_statements.append(dummy_assign)
        
        # Insérer les statements factices au début
        node.body = dummy_statements + node.body

        self.generic_visit(node)
        return node

    # =========================
    # CALLS (FIX FINAL IMPORTANT)
    # =========================
    def visit_Call(self, node):
        self.generic_visit(node)

        if isinstance(node.func, ast.Name):
            name = node.func.id

            # FIX CRITICAL: function mapping always applied
            if name in self.func_map:
                node.func.id = self.func_map[name]

            # safety: entry point main() fix
            if name == "main" and "main" in self.func_map:
                node.func.id = self.func_map["main"]
                
        elif isinstance(node.func, ast.Attribute):
            # Handle method calls like obj.method()
            if node.func.attr in self.func_map:
                node.func.attr = self.func_map[node.func.attr]
            # Handle module function calls like module.function()
            elif isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
                
                # Pour le mode multi-fichier, remplacer les noms de modules locaux
                if hasattr(self, 'file_manager'):
                    if any(Path(f).stem == module_name for f in self.file_manager.all_files):
                        # Remplacer par le nom du module obfusqué
                        node.func.value.id = f"obfuscated_{module_name}"
                        
                        # Obtenir le mapping des fonctions du module
                        func_mapping = self.file_manager.get_function_mapping(module_name)
                        if node.func.attr in func_mapping:
                            node.func.attr = func_mapping[node.func.attr]

        return node

    # =========================
    # CLASSES
    # =========================
    def visit_ClassDef(self, node):
        if self.safe(node.name):
            if node.name not in self.class_map:
                self.class_map[node.name] = self.new()

            node.name = self.class_map[node.name]

        self.generic_visit(node)
        return node


# =========================
# LOGGER SETUP
# =========================
def setup_logging(log_file="obfuscation.log"):
    """Configure le système de logging dans un fichier"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("=== Démarrage de l'obfuscateur Python ===")
    return logger


# =========================
# MAIN FUNCTION
# =========================
def _adjust_local_imports(code, current_file, obfuscator):
    """Ajuste les imports locaux pour le mode multi-fichier"""
    lines = code.split('\n')
    adjusted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') and 'base64' not in stripped:
            # Vérifier si c'est un import local
            import_part = stripped[7:]  # Enlever 'import '
            if '.' not in import_part:  # Import local simple
                # Remplacer par l'import du fichier obfusqué
                adjusted_lines.append(f'import obfuscated_{import_part}')
            else:
                adjusted_lines.append(line)
        elif stripped.startswith('obfuscated_module_test.') or stripped.startswith('module_test.'):
            # Remplacer les appels de fonctions de modules
            parts = stripped.split('.')
            if len(parts) >= 2:
                module_name = parts[0]
                func_name = parts[1].split('(')[0].strip()  # Extraire le nom de la fonction
                
                # Obtenir le mapping des fonctions du module
                func_mapping = obfuscator.file_manager.get_function_mapping(module_name.replace('obfuscated_', ''))
                if func_name in func_mapping:
                    new_func_name = func_mapping[func_name]
                    # Remplacer dans la ligne
                    new_line = stripped.replace(f'{module_name}.{func_name}', f'obfuscated_{module_name.replace("obfuscated_", "")}.{new_func_name}')
                    adjusted_lines.append(new_line)
                else:
                    adjusted_lines.append(line)
            else:
                adjusted_lines.append(line)
        else:
            adjusted_lines.append(line)
    
    return '\n'.join(adjusted_lines)

def obfuscate(file_path, log_file="obfuscation.log", encode_strings=False, multi_file=False, advanced_protection=False):
    logger = setup_logging(log_file)
    
    try:
        files_to_process = []
        
        if multi_file:
            # Mode multi-fichiers
            logger.info("Mode multi-fichiers activé")
            file_manager = MultiFileManager()
            file_manager.find_all_dependencies(file_path)
            files_to_process = file_manager.get_all_files()
            logger.info(f"Fichiers découverts: {len(files_to_process)}")
        else:
            # Mode single fichier
            files_to_process = [file_path]
        
        all_results = []
        
        for current_file in files_to_process:
            logger.info(f"Traitement du fichier: {current_file}")
            
            code = Path(current_file).read_text(encoding="utf-8")
            tree = ast.parse(code)

            # ANALYSIS
            logger.info("Analyse du code source...")
            analyzer = Analyzer()
            analyzer.visit(tree)

            # OBFUSCATION
            logger.info("Obfuscation en cours...")
            obf = Obfuscator(encode_strings=encode_strings)
            
            # Ajouter le file manager si mode multi-fichier
            if multi_file:
                obf.file_manager = file_manager
            
            # Créer le décodeur de strings si nécessaire
            decoder_code = ""
            if encode_strings:
                decoder_code = obf.create_string_decoder()
            
            tree = obf.visit(tree)
            ast.fix_missing_locations(tree)
            
            # Sauvegarder les mappings de fonctions pour le mode multi-fichier
            if multi_file:
                file_manager.add_function_mapping(current_file, obf.func_map)

            # OUTPUT
            if multi_file:
                # Créer un répertoire de sortie qui préserve la structure
                output_dir = Path("obfuscated_output")
                output_dir.mkdir(exist_ok=True)
                
                # Trouver le répertoire racine commun à tous les fichiers
                root_dir = Path(files_to_process[0]).parent
                for f in files_to_process[1:]:
                    root_dir = Path(root_dir).commonpath([Path(f).parent])
                
                # Calculer le chemin relatif depuis la racine
                current_path = Path(current_file)
                try:
                    rel_path = current_path.relative_to(root_dir)
                except ValueError:
                    # Fallback si le calcul de chemin relatif échoue
                    rel_path = current_path.name
                
                # Créer le chemin de sortie en préservant la structure
                output_file = output_dir / rel_path.parent / f"obfuscated_{rel_path.name}"
            else:
                output_file = "obfuscated_" + Path(current_file).name
                
            new_code = ast.unparse(tree)
            
            # Ajouter le décodeur de strings au début si nécessaire
            if encode_strings and decoder_code:
                new_code = decoder_code + "\n\n" + new_code
            
            # Pour le mode multi-fichier, ajuster les imports locaux
            if multi_file:
                new_code = _adjust_local_imports(new_code, current_file, obf)
            
            # Appliquer la protection avancée si activée
            if advanced_protection and ADVANCED_PROTECTION_AVAILABLE:
                logger.info("Application de la protection avancée...")
                try:
                    new_code = apply_advanced_obfuscation(new_code)
                    logger.info("Protection avancée appliquée avec succès")
                except Exception as e:
                    logger.warning(f"Erreur lors de l'application de la protection avancée: {e}")
            
            # Ajouter un header avec les informations d'obfuscation
            header = f'''# ╔══════════════════════════════════════════════════════════════╗
# ║                    ShadowPy v1.0.0 - Code Obfusqué           ║
# ╠══════════════════════════════════════════════════════════════╣
# ║  Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}           ║
# ║  Fichier original: {current_file}                              ║
# ║  Protection: Niveau {'MAXIMUM+' if advanced_protection else 'MAXIMUM'}      ║
# ║  Variables: {len(obf.var_map)} obfusquées                        ║
# ║  Fonctions: {len(obf.func_map)} obfusquées                       ║
# ║  Classes: {len(obf.class_map)} obfusquées                         ║
# ║  Strings encodés: {encode_strings}                              ║
# ║  Protection avancée: {advanced_protection}                      ║
# ╚══════════════════════════════════════════════════════════════╝

'''
            
            final_code = header + new_code
            
            # Créer les répertoires nécessaires
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(final_code, encoding="utf-8")
            
            logger.info(f"Script obfusqué sauvegardé dans: {output_file}")
            
            # REPORT pour ce fichier
            print(f"\n--- Fichier: {current_file} ---")
            print(f"📁 OUTPUT: {output_file}")
            print(f"🔢 Variables: {len(obf.var_map)}")
            print(f"⚙️ Fonctions: {len(obf.func_map)}")
            print(f"🏗️ Classes: {len(obf.class_map)}")
            
            all_results.append({
                'input': current_file,
                'output': str(output_file),
                'stats': {
                    'variables': len(obf.var_map),
                    'functions': len(obf.func_map),
                    'classes': len(obf.class_map)
                }
            })

        print("\n==============================")
        print("🚀 OBFUSCATOR MULTI-FILE v8")
        print("==============================\n")
        
        if multi_file:
            print(f"📁 Fichiers traités: {len(all_results)}")
            print(f"📋 LOG: {log_file}")
            print(f"🔐 Strings encodées: {encode_strings}")
        
        print("\n✅ OBFUSCATION TERMINÉE AVEC SUCCÈS")
        logger.info("Obfuscation terminée avec succès")
        
        return all_results

    except Exception as e:
        logger.error(f"Erreur lors de l'obfuscation: {str(e)}")
        raise


# =========================
# ENTRY POINT
# =========================
def compile_with_nuitka(input_file, output_name=None):
    """Compile un fichier Python avec Nuitka en mode --onefile"""
    try:
        # Vérifier si Nuitka est installé
        subprocess.run([sys.executable, '-m', 'nuitka', '--version'], capture_output=True, check=True)
        
        # Déterminer le nom de sortie
        if output_name is None:
            output_name = Path(input_file).stem
        
        print(f"\n🔥 Compilation Nuitka en cours...")
        print(f"📁 Input: {input_file}")
        print(f"🎯 Output: {output_name}.exe")
        
        # Commande Nuitka
        cmd = [
            sys.executable, '-m', 'nuitka',
            '--onefile',
            '--assume-yes-for-downloads',
            '--remove-output',
            '--no-pyi-file',
            f'--output-filename={output_name}.exe',
            input_file
        ]
        
        # Exécuter la compilation
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Compilation réussie: {output_name}.exe")
            
            # Nettoyer les fichiers temporaires
            build_dir = Path(f"{output_name}.build")
            if build_dir.exists():
                shutil.rmtree(build_dir)
                
            return True
        else:
            print(f"❌ Erreur de compilation:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Nuitka n'est pas installé. Installation en cours...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'nuitka'], check=True)
            print("✅ Nuitka installé. Nouvelle tentative de compilation...")
            return compile_with_nuitka(input_file, output_name)
        except:
            print("❌ Impossible d'installer Nuitka.")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la compilation: {str(e)}")
        return False

def print_banner():
    """Affiche la bannière PyMorph"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                     PyMorph v1.0.0 🚀                       ║
║              Multi-Language Code Obfuscator                  ║
║                                                              ║
║  🔐 7 Langages  📁 Multi-fichiers  🚀 Compilation  🎨 GUI    ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_usage():
    """Affiche les exemples d'utilisation"""
    examples = """
🎯 UTILISATION:
  
  Mode GUI (Recommandé):
    python pymorph.py
    
  Mode simple:
    python pymorph.py script.py
    
  Mode avancé:
    python pymorph.py script.py --encode-strings
    python pymorph.py main.py --multi-file --encode-strings
    python pymorph.py script.py --advanced-protection --encode-strings
    python pymorph.py script.py --multi-file --advanced-protection --encode-strings --compile --output mon_app
    
⚙️ OPTIONS:
  --encode-strings        Encoder les chaînes en base64
  --multi-file             Traiter tous les fichiers importés
  --advanced-protection    Appliquer une protection avancée anti-analyse
  --compile                Compiler avec Nuitka (--onefile)
  --output NOM             Nom du fichier de sortie (compilation)
  --log FICHIER            Fichier de logs personnalisé
  
📁 SORTIES:
  obfuscated_script.py     # Script obfusqué
  obfuscated_output/       # Répertoire multi-fichiers
  mon_app.exe             # Exe compilé
  obfuscation.log          # Logs détaillés

💻 COMMANDES TERMINAL:
  python src/enhanced_gui.py    # Interface graphique améliorée
  python build.py               # Compilation en exécutable
"""
    print(examples)

def main():
    print_banner()
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PyMorph v1.0.0 - Multi-Language Code Obfuscator with Compilation Nuitka',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python pymorph.py                    # Lance l'interface graphique
  python pymorph.py script.py          # Mode ligne de commande
  python pymorph.py script.py --encode-strings
  python pymorph.py main.py --multi-file --encode-strings
  python pymorph.py script.py --encode-strings --compile --output mon_app
        """
    )
    
    parser.add_argument('input_file', nargs='?', help='Fichier Python à obfusquer')
    parser.add_argument('-l', '--log', default='obfuscation.log', help='Fichier de logs (défaut: obfuscation.log)')
    parser.add_argument('--encode-strings', action='store_true', help='Encoder les chaînes de caractères en base64')
    parser.add_argument('--multi-file', action='store_true', help='Traiter les imports et obfusquer tous les fichiers')
    parser.add_argument('--advanced-protection', action='store_true', help='Appliquer une protection avancée anti-analyse')
    parser.add_argument('--compile', action='store_true', help='Compiler avec Nuitka en mode --onefile')
    parser.add_argument('--output', help='Nom du fichier de sortie pour la compilation')
    parser.add_argument('--examples', action='store_true', help='Afficher des exemples d\'utilisation')
    
    args = parser.parse_args()
    
    if args.examples:
        print_usage()
        return
    
    # Si aucun fichier n'est spécifié, lancer l'interface graphique
    if not args.input_file:
        print("🎨 Lancement de l'interface graphique PyMorph...")
        
        # Vérifier et installer les dépendances manquantes
        missing_deps = []
        try:
            import customtkinter
        except ImportError:
            missing_deps.append("customtkinter")
        
        try:
            from Crypto.Cipher import AES
        except ImportError:
            missing_deps.append("pycryptodome")
        
        try:
            import cryptography
        except ImportError:
            missing_deps.append("cryptography")
        
        if missing_deps:
            print(f"❌ Dépendances manquantes: {', '.join(missing_deps)}")
            print("💡 Installation automatique des dépendances...")
            try:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_deps)
                print("✅ Dépendances installées avec succès!")
            except subprocess.CalledProcessError:
                print("❌ Échec de l'installation automatique")
                print("💡 Installation manuelle requise:")
                print(f"   pip install {' '.join(missing_deps)}")
                return
        
        # Lancer l'interface graphique
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from enhanced_gui import EnhancedPyMorphGUI
            app = EnhancedPyMorphGUI()
            app.run()
        except ImportError as e:
            print(f"❌ Interface graphique non disponible: {e}")
            print("💡 Utilisez --examples pour voir l'aide.")
            print("💡 Ou lancez directement: python src/enhanced_gui.py")
        except Exception as e:
            print(f"❌ Erreur lors du lancement de l'interface graphique: {e}")
        return
    
    # Validation des arguments
    if not Path(args.input_file).exists():
        print(f"❌ Erreur: Le fichier '{args.input_file}' n'existe pas.")
        sys.exit(1)
    
    if args.compile and not args.output:
        args.output = Path(args.input_file).stem
    
    print(f"🎯 Fichier cible: {args.input_file}")
    print(f"🔧 Configuration: Strings={args.encode_strings}, Multi-file={args.multi_file}, Compilation={args.compile}")
    
    try:
        results = obfuscate(
            args.input_file, 
            args.log, 
            args.encode_strings, 
            args.multi_file,
            args.advanced_protection
        )
        
        # Afficher le résumé détaillé
        print("\n" + "="*60)
        print("📊 RAPPORT D'OBFUSCATION")
        print("="*60)
        
        if args.multi_file and len(results) > 1:
            total_vars = sum(r['stats']['variables'] for r in results)
            total_funcs = sum(r['stats']['functions'] for r in results)
            total_classes = sum(r['stats']['classes'] for r in results)
            
            print(f"📁 Fichiers traités: {len(results)}")
            for result in results:
                print(f"   • {Path(result['input']).name} → {Path(result['output']).name}")
            
            print(f"\n📈 Statistiques globales:")
            print(f"   🔢 Variables obfusquées: {total_vars}")
            print(f"   ⚙️ Fonctions obfusquées: {total_funcs}")
            print(f"   🏗️ Classes obfusquées: {total_classes}")
            
            # Compiler avec Nuitka si demandé
            if args.compile:
                print(f"\n🔥 Lancement de la compilation Nuitka...")
                main_file = None
                for result in results:
                    if 'main' in result['input'] or result['input'] == args.input_file:
                        main_file = result['output']
                        break
                
                if main_file:
                    success = compile_with_nuitka(main_file, args.output)
                    if success:
                        print(f"\n🎉 ShadowPy v1.0.0 - MISSION ACCOMPLIE !")
                        print(f"   📦 Fichier compilé: {args.output}.exe")
                        print(f"   🛡️ Protection: Niveau MAXIMUM")
                        print(f"   ✅ Prêt à distribuer")
                    else:
                        print(f"\n⚠️ OBFUSCATION RÉUSSIE mais compilation échouée")
                else:
                    print("❌ Impossible de trouver le fichier principal à compiler")
        else:
            # Mode single fichier
            output_file = results if isinstance(results, str) else results[0]['output']
            stats = results if isinstance(results, dict) else results[0]['stats']
            
            print(f"📁 Fichier traité: {Path(args.input_file).name}")
            print(f"📦 Sortie: {Path(output_file).name}")
            print(f"📈 Statistiques:")
            print(f"   🔢 Variables obfusquées: {stats['variables']}")
            print(f"   ⚙️ Fonctions obfusquées: {stats['functions']}")
            print(f"   🏗️ Classes obfusquées: {stats['classes']}")
            
            if args.compile:
                print(f"\n🔥 Lancement de la compilation Nuitka...")
                success = compile_with_nuitka(output_file, args.output)
                if success:
                    print(f"\n🎉 ShadowPy v1.0.0 - MISSION ACCOMPLIE !")
                    print(f"   📦 Fichier compilé: {args.output}.exe")
                    print(f"   🛡️ Protection: Niveau MAXIMUM")
                    print(f"   ✅ Prêt à distribuer")
                else:
                    print(f"\n⚠️ OBFUSCATION RÉUSSIE mais compilation échouée")
            else:
                print(f"\n✅ ShadowPy v1.0.0 - OBFUSCATION TERMINÉE")
                print(f"   🛡️ Protection active")
                print(f"   📋 Logs: {args.log}")
        
        print(f"\n💡 Conseil: Testez toujours votre code obfusqué avant distribution !")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Opération annulée par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique: {str(e)}")
        print(f"📋 Consultez les logs dans: {args.log}")
        sys.exit(1)

if __name__ == "__main__":
    main()
