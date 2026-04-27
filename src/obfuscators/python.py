"""
Python Obfuscator Module
Advanced obfuscation techniques for Python code
"""

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
from .advanced_encoder import encode_string_advanced, create_decoder

BUILTINS = set(dir(builtins))
PROTECTED = BUILTINS | set(keyword.kwlist) | {
    "True", "False", "None", "__name__", "__file__", "self",
    "__init__", "__str__", "__repr__", "__call__", "__getitem__", "__setitem__",
    "__delitem__", "__contains__", "__iter__", "__next__", "__len__", "__bool__",
    "os", "sys", "typing", "json", "base64", "zlib", "random", "string",
    "collections", "defaultdict", "pathlib", "datetime", "threading", "subprocess",
    "shutil", "tkinter", "customtkinter", "ast", "builtins", "keyword"
}

# Enhanced name generator with more variety
def gen_name(length=8):
    """Generate random names with different patterns"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_letters, k=length)),
        lambda: random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
        lambda: random.choice(['x', 'y', 'z', 'w', 'u', 'v']) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: random.choice(string.ascii_uppercase) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
    ]
    return random.choice(patterns)()

# Advanced string encoding with multiple layers
def encode_string(s):
    """Encode string with advanced multi-layer obfuscation"""
    if not isinstance(s, str):
        return s
    
    # Use advanced encoder with multiple layers
    encoded_data, methods_used = encode_string_advanced(s, layers=random.randint(2, 4))
    
    # Store methods used for decoding
    return {
        'encoded': encoded_data,
        'methods': methods_used,
        'original_length': len(s)
    }

# Mathematical decomposition for numbers
def decompose_number(n):
    """Decompose numbers into mathematical expressions"""
    if not isinstance(n, (int, float)) or abs(n) < 2:
        return n
    
    operations = [
        lambda x: f"({random.randint(1, max(1, x//2))} + {x - random.randint(1, max(1, x//2))})",
        lambda x: f"({x * 2} // 2)",
        lambda x: f"({x + random.randint(1, 5)} - {random.randint(1, 5)})",
        lambda x: f"({x * 3} // 3)",
        lambda x: f"({int(x**0.5)} ** 2)" if x > 0 else str(x),
        lambda x: f"({x} << 1) >> 1",
        lambda x: f"abs({-x})",
        lambda x: f"({x} + ({random.randint(1, 10)} - {random.randint(1, 10)}))",
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

# Analyzer for code structure
class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.var_usage = defaultdict(int)
        self.func_calls = defaultdict(int)
        self.imports = set()
        self.strings = []
        self.numbers = []
        self.variables = set()
        self.functions = set()
        self.classes = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.var_usage[node.id] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.func_calls[node.func.id] += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_Str(self, node):
        self.strings.append(node.s)
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            self.strings.append(node.value)
        elif isinstance(node.value, (int, float)):
            self.numbers.append(node.value)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.classes.add(node.name)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
        self.generic_visit(node)

# Enhanced obfuscation transformer
class Obfuscator(ast.NodeTransformer):
    def __init__(self, encode_strings=True, decompose_numbers=True, add_dummy_vars=True):
        self.encode_strings = encode_strings
        self.decompose_numbers = decompose_numbers
        self.add_dummy_vars = add_dummy_vars
        self.name_map = {}
        self.string_map = {}
        self.dummy_var_count = 0

    def get_new_name(self, old_name):
        """Get new obfuscated name for identifier"""
        if old_name in self.name_map:
            return self.name_map[old_name]
        
        if old_name in PROTECTED:
            return old_name
        
        new_name = gen_name()
        while new_name in PROTECTED or new_name in self.name_map.values():
            new_name = gen_name()
        
        self.name_map[old_name] = new_name
        return new_name

    def add_dummy_variable(self):
        """Add dummy variable to confuse analysis"""
        self.dummy_var_count += 1
        dummy_name = f"dummy_{self.dummy_var_count}_{gen_name(4)}"
        dummy_value = random.choice([
            f"({random.randint(1, 100)} + {random.randint(1, 100)})",
            f"'{gen_name(6)}'",
            f"[{random.randint(1, 10)}]",
            f"{{'dummy_key': {random.randint(1, 100)}}}",
            f"{random.randint(1, 100)}",
            f"'dummy_string_{self.dummy_var_count}'",
        ])
        
        return ast.parse(f"{dummy_name} = {dummy_value}").body[0]

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) and node.id not in PROTECTED:
            node.id = self.get_new_name(node.id)
        elif isinstance(node.ctx, ast.Load) and node.id in self.name_map:
            node.id = self.name_map[node.id]
        return node
    
    def visit_Attribute(self, node):
        """Handle attribute access for method calls"""
        self.generic_visit(node)
        return node
    
    def visit_Call(self, node):
        """Handle function and method calls"""
        # Update method calls to use renamed methods
        if isinstance(node.func, ast.Attribute):
            # This is a method call like obj.method()
            if node.func.attr in self.name_map:
                node.func.attr = self.name_map[node.func.attr]
        elif isinstance(node.func, ast.Name):
            # This is a function call like function()
            if node.func.id in self.name_map:
                node.func.id = self.name_map[node.func.id]
        
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.get_new_name(node.name)
        
        # Add dummy variables at the start of function
        if self.add_dummy_vars and random.random() < 0.7:
            dummy_count = random.randint(1, 3)
            for _ in range(dummy_count):
                dummy_stmt = self.add_dummy_variable()
                node.body.insert(0, dummy_stmt)
        
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = self.get_new_name(node.name)
        self.generic_visit(node)
        return node

    def visit_Constant(self, node):
        # Désactiver complètement l'encodage des chaînes pour éviter les erreurs de syntaxe
        if isinstance(node.value, (int, float)) and self.decompose_numbers:
            try:
                expr = decompose_number(node.value)
                return ast.parse(expr).body[0].value
            except:
                return node
        return node
    
    def visit_Import(self, node):
        """Gérer les imports sans les obfusquer"""
        # Ne pas obfusquer les noms de modules dans les imports
        return node
    
    def visit_ImportFrom(self, node):
        """Gérer les imports from sans les obfusquer"""
        # Ne pas obfusquer les noms de modules dans les imports from
        return node
    
    def visit_JoinedStr(self, node):
        """Gérer les f-strings et mettre à jour les variables renommées"""
        # Traiter chaque valeur dans le f-string pour mettre à jour les noms de variables
        for i, value_node in enumerate(node.values):
            if isinstance(value_node, ast.Name) and value_node.id in self.name_map:
                # Remplacer la variable par son nouveau nom
                node.values[i] = ast.Name(id=self.name_map[value_node.id], ctx=value_node.ctx)
        return node
    
    def visit_Str(self, node):
        # Pour la compatibilité avec Python < 3.8
        return self.visit_Constant(ast.Constant(value=node.s))
    
    def visit_Num(self, node):
        # Pour la compatibilité avec Python < 3.8
        return self.visit_Constant(ast.Constant(value=node.n))
    
    def visit_Expr(self, node):
        """Supprimer les docstrings et les expressions constantes"""
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            # C'est probablement un docstring, le supprimer
            return None
        return node
    
    def remove_docstrings_and_comments(self, tree):
        """Supprimer tous les docstrings et traiter les commentaires"""
        # Parcourir tous les nodes et supprimer les docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    # Supprimer le docstring
                    node.body = node.body[1:]
            elif isinstance(node, ast.Module):
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    # Supprimer le docstring du module
                    node.body = node.body[1:]
        return tree
    
    def update_fstring_variables(self, code):
        """Update variable names in f-strings and global variables after obfuscation"""
        import re
        
        # Find all f-strings and update variable names
        def replace_fstring_vars(match):
            fstring_content = match.group(1)
            
            # Replace variable names in the f-string
            for old_name, new_name in self.name_map.items():
                # Replace {old_name} with {new_name}
                pattern = r'\{' + re.escape(old_name) + r'\}'
                fstring_content = re.sub(pattern, f'{{{new_name}}}', fstring_content)
            
            return f'f{fstring_content}'
        
        # Process f-strings
        fstring_pattern = r"f('([^']*(?:\{[^}]*\}[^']*)*)')"
        code = re.sub(fstring_pattern, replace_fstring_vars, code)
        
        # Process triple-quoted f-strings
        fstring_triple_pattern = r'f"""([^"]*(?:\{[^}]*\}[^"]*)*)"""'
        code = re.sub(fstring_triple_pattern, lambda m: f'f"""{replace_fstring_vars(m)}"""', code)
        
        # Replace global variables that were renamed
        for old_name, new_name in self.name_map.items():
            # Replace variable names in regular code (not in strings)
            pattern = r'\b' + re.escape(old_name) + r'\b'
            code = re.sub(pattern, new_name, code)
        
        return code

# Main obfuscation function
def obfuscate_python_code(code, options=None):
    """Main obfuscation function for Python code"""
    if options is None:
        options = {
            'decompose_numbers': True,
            'add_dummy_vars': True,
            'rename_variables': True,
            'rename_functions': True,
            'rename_classes': True
        }
    
    try:
        # Parse the code
        tree = ast.parse(code)
        
        # Supprimer les docstrings et les commentaires
        obfuscator = Obfuscator(options)
        tree = obfuscator.remove_docstrings_and_comments(tree)
        
        # Analyze the code
        analyzer = Analyzer()
        analyzer.visit(tree)
        
        # Apply obfuscation
        obfuscated_tree = obfuscator.visit(tree)
        
        # Convert back to code
        try:
            obfuscated_code = ast.unparse(obfuscated_tree)
        except:
            # Fallback for older Python versions
            try:
                import astor
                obfuscated_code = astor.to_source(obfuscated_tree)
            except:
                obfuscated_code = code  # Ultimate fallback
        
        # Post-process f-strings to update variable names
        obfuscated_code = obfuscator.update_fstring_variables(obfuscated_code)
        
        return obfuscated_code, {
            'variables': len(analyzer.variables),
            'functions': len(analyzer.functions),
            'classes': len(analyzer.classes),
            'strings': len(analyzer.strings),
            'numbers': len(analyzer.numbers)
        }
        
    except Exception as e:
        logging.error(f"Error during obfuscation: {e}")
        return code, {'error': str(e)}

def generate_decoder_functions(encoding_methods):
    """Generate decoder functions based on encoding methods used"""
    if not encoding_methods:
        return ""
    
    decoder_code = """
# Decoder functions for obfuscated strings
import base64
import zlib
import json

def advanced_decoder(encoded_data):
    \"\"\"Multi-layer decoder for encoded strings\"\"\"
    try:
        if isinstance(encoded_data, str):
            # Handle different encoding formats
            if ':' in encoded_data:
                parts = encoded_data.split(':')
                if len(parts) >= 2:
                    method = parts[0]
                    data = parts[1]
                    
                    if method == 'base64':
                        return base64.b64decode(data).decode('utf-8')
                    elif method == 'hex':
                        return bytes.fromhex(data).decode('utf-8')
                    elif method == 'zlib':
                        return zlib.decompress(base64.b64decode(data)).decode('utf-8')
                    elif method == 'json':
                        return json.loads(base64.b64decode(data).decode('utf-8'))
        return str(encoded_data)
    except:
        return str(encoded_data)

def decoder(encoded_str):
    \"\"\"Simple decoder fallback\"\"\"
    try:
        if isinstance(encoded_str, str) and ':' in encoded_str:
            return advanced_decoder(encoded_str)
        return str(encoded_str)
    except:
        return str(encoded_str)
"""
    return decoder_code

def create_decoder_function():
    """Create a decoder function for encoded strings"""
    decoder_code = '''
def decoder(encoded_str):
    import base64
    parts = encoded_str.split(':')
    if len(parts) >= 2:
        encoded = parts[1]
        decoded = base64.b64decode(base64.b64decode(encoded)).decode('utf-8')
        return decoded
    return encoded_str
'''
    return ast.parse(decoder_code).body[0]

# Test function
def test_python_obfuscation():
    """Test Python obfuscation"""
    test_code = '''
def calculate_sum(a, b):
    result = a + b
    return result

message = "Hello, World!"
number = 42
print(message, number)
'''
    
    options = {
        'encode_strings': True,
        'decompose_numbers': True,
        'add_dummy_vars': True,
        'rename_variables': True,
        'rename_functions': True,
        'rename_classes': True
    }
    
    obfuscated, stats = obfuscate_python_code(test_code, options)
    
    print("=== Python Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_python_obfuscation()
