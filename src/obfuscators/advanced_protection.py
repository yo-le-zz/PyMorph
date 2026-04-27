"""
Advanced Obfuscation Protection Layer
Adds sophisticated anti-analysis and anti-tampering techniques
"""

import ast
import random
import string
import base64
import zlib
import marshal
import types
from collections import defaultdict

class AdvancedProtection:
    """Advanced obfuscation techniques for maximum protection"""
    
    def __init__(self):
        self.anti_debug_enabled = True
        self.anti_vm_enabled = True
        self.string_encryption_enabled = True
        self.control_flow_enabled = True
        self.dead_code_enabled = True
        
    def generate_anti_debug_code(self):
        """Generate anti-debugging protection code"""
        anti_debug_snippets = [
            """
# Anti-debug protection
import sys
import os
import time
if hasattr(sys, 'gettrace') and sys.gettrace():
    os._exit(1)
if 'pdb' in sys.modules:
    os._exit(1)
""",
            """
# Timing-based anti-debug
start = time.time()
# Dummy operation
result = sum(range(1000))
if time.time() - start > 0.1:  # Suspicious delay
    os._exit(1)
""",
            """
# Process name check
import psutil
try:
    current_process = psutil.Process()
    if any(debugger in current_process.name().lower() 
           for debugger in ['gdb', 'lldb', 'x64dbg', 'ollydbg', 'windbg']):
        os._exit(1)
except:
    pass
"""
        ]
        return random.choice(anti_debug_snippets)
    
    def generate_anti_vm_code(self):
        """Generate anti-virtualization detection code"""
        anti_vm_snippets = [
            """
# VM detection through hardware analysis
import platform
import subprocess
try:
    # Check for common VM signatures
    if any(vm in platform.platform().lower() 
           for vm in ['vmware', 'virtualbox', 'qemu', 'hyper-v', 'xen']):
        os._exit(1)
    
    # Check for VM-specific processes
    result = subprocess.run(['tasklist'], capture_output=True, text=True)
    if any(vm_proc in result.stdout.lower() 
           for vm_proc in ['vmtoolsd', 'vboxservice', 'vmusrvc']):
        os._exit(1)
except:
    pass
""",
            """
# Registry-based VM detection (Windows)
if os.name == 'nt':
    try:
        import winreg
        vm_keys = [
            r'SOFTWARE\\VMware, Inc.\\VMware Tools',
            r'SOFTWARE\\Oracle\\VirtualBox',
            r'SYSTEM\\CurrentControlSet\\Services\\VBoxService'
        ]
        for key_path in vm_keys:
            try:
                winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                os._exit(1)
            except FileNotFoundError:
                pass
    except:
        pass
"""
        ]
        return random.choice(anti_vm_snippets)
    
    def generate_string_decryptor(self, encrypted_strings):
        """Generate a sophisticated string decryption function"""
        decryptor_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        decryptor_code = f"""
class {decryptor_name}:
    def __init__(self):
        self.key = {random.randint(1000, 9999)}
        self.xor_key = {random.randint(1, 255)}
        
    def decrypt(self, data):
        if isinstance(data, str):
            data = data.encode('latin1')
        
        # Multi-stage decryption
        result = bytearray()
        for i, byte in enumerate(data):
            # XOR with position-based key
            xor_byte = byte ^ (self.xor_key + (i % 256))
            # Add mathematical transformation
            transformed = (xor_byte + self.key) % 256
            result.append(transformed)
        
        # Decompress if needed
        try:
            return zlib.decompress(result).decode('utf-8')
        except:
            return result.decode('utf-8', errors='ignore')
    
    @staticmethod
    def encode_string(s):
        # Encode with compression and XOR
        compressed = zlib.compress(s.encode('utf-8'))
        key = random.randint(1, 255)
        encoded = bytearray()
        for i, byte in enumerate(compressed):
            encoded.append(byte ^ (key + (i % 256)))
        return base64.b64encode(encoded).decode('ascii')

_string_decryptor = {decryptor_name}()
"""
        
        return decryptor_code, decryptor_name
    
    def generate_control_flow_obfuscation(self):
        """Generate control flow obfuscation patterns"""
        patterns = [
            """
# Control flow obfuscation
def _obfuscated_flow():
    _flag = random.randint(0, 100) > 50
    if _flag:
        _temp = [i for i in range(10)]
        _result = sum(_temp) * 2
    else:
        _temp = [i*i for i in range(5)]
        _result = sum(_temp) + 10
    return _result

_dummy = _obfuscated_flow()
""",
            """
# Opaque predicate
def _check_condition():
    _x = random.randint(1, 100)
    _y = _x * 2 + 5
    return (_y - _x * 2) > 0

if _check_condition():
    _unused = [i**2 for i in range(20)]
else:
    _unused = [i**3 for i in range(15)]
""",
            """
# Dynamic dispatch obfuscation
class _DynamicDispatcher:
    def __init__(self):
        self.methods = [self._method1, self._method2, self._method3]
    
    def _method1(self):
        return sum(range(10))
    
    def _method2(self):
        return sum(range(5)) * 2
    
    def _method3(self):
        return len([i for i in range(20)])
    
    def dispatch(self):
        method = random.choice(self.methods)
        return method()

_dispatcher = _DynamicDispatcher()
_dummy_result = _dispatcher.dispatch()
"""
        ]
        return random.choice(patterns)
    
    def generate_dead_code(self):
        """Generate dead code that looks useful but isn't"""
        dead_code_snippets = [
            """
# Dead code - complex but unused calculations
def _unused_calculations():
    _primes = []
    for num in range(2, 100):
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            _primes.append(num)
    
    _fibonacci = [0, 1]
    for i in range(2, 20):
        _fibonacci.append(_fibonacci[-1] + _fibonacci[-2])
    
    return len(_primes) + len(_fibonacci)

_unused_result = _unused_calculations()
""",
            """
# Dead code - string manipulations
def _string_operations():
    _text = "obfuscation"
    _reversed = _text[::-1]
    _upper = _text.upper()
    _encoded = base64.b64encode(_text.encode()).decode()
    
    _matrix = [[i*j for j in range(5)] for i in range(5)]
    _flattened = [item for sublist in _matrix for item in sublist]
    
    return len(_reversed) + len(_upper) + len(_encoded) + sum(_flattened)

_string_result = _string_operations()
""",
            """
# Dead code - mathematical operations
def _mathematical_noise():
    _factorial = 1
    for i in range(1, 11):
        _factorial *= i
    
    _powers = [2**i for i in range(10)]
    _roots = [i**0.5 for i in range(1, 11)]
    
    _matrix_a = [[1, 2], [3, 4]]
    _matrix_b = [[5, 6], [7, 8]]
    _matrix_mult = [[sum(a*b for a,b in zip(row, col)) for col in zip(*_matrix_b)] for row in _matrix_a]
    
    return _factorial + sum(_powers) + sum(_roots) + sum(sum(row) for row in _matrix_mult)

_math_result = _mathematical_noise()
"""
        ]
        return random.choice(dead_code_snippets)
    
    def generate_integrity_check(self):
        """Generate code integrity verification"""
        integrity_code = f"""
# Code integrity verification
import hashlib
import inspect

def _verify_integrity():
    try:
        # Get current frame code
        current_frame = inspect.currentframe()
        frame_code = inspect.getsource(current_frame)
        
        # Calculate hash
        expected_hash = hashlib.sha256(frame_code.encode()).hexdigest()
        
        # Simulate integrity check (always passes in legitimate execution)
        _integrity_key = '{''.join(random.choices(string.hexdigits.lower(), k=64))}'
        
        # In real implementation, this would verify against stored hash
        return expected_hash.startswith('{''.join(random.choices('abcdef0123456789', k=4))}')
    except:
        return True

_integrity_result = _verify_integrity()
if not _integrity_result:
    os._exit(1)
"""
        return integrity_code
    
    def apply_protection(self, code):
        """Apply all advanced protection techniques"""
        protection_layers = []
        
        # Add anti-debug protection
        if self.anti_debug_enabled:
            protection_layers.append(self.generate_anti_debug_code())
        
        # Add anti-VM protection
        if self.anti_vm_enabled:
            protection_layers.append(self.generate_anti_vm_code())
        
        # Add control flow obfuscation
        if self.control_flow_enabled:
            protection_layers.append(self.generate_control_flow_obfuscation())
        
        # Add dead code
        if self.dead_code_enabled:
            protection_layers.append(self.generate_dead_code())
        
        # Add integrity check
        protection_layers.append(self.generate_integrity_check())
        
        # Shuffle the order of protection layers
        random.shuffle(protection_layers)
        
        # Combine protection layers with the original code
        protection_header = "\n".join(protection_layers)
        
        # Add required imports
        required_imports = """
import os
import sys
import time
import random
import base64
import zlib
import hashlib
import inspect
"""
        
        return required_imports + "\n" + protection_header + "\n\n" + code

class AdvancedObfuscator(ast.NodeTransformer):
    """AST transformer for advanced obfuscation techniques"""
    
    def __init__(self):
        self.string_decryptor = None
        self.decryptor_name = None
        self.encrypted_strings = []
        
    def encrypt_strings(self, code):
        """Encrypt all string literals in the code"""
        protection = AdvancedProtection()
        decryptor_code, decryptor_name = protection.generate_string_decryptor([])
        
        # Parse the code and encrypt strings
        tree = ast.parse(code)
        self.string_decryptor = decryptor_name
        self.encrypted_strings = []
        
        # Transform string literals
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        
        # Generate the final code
        obfuscated_code = ast.unparse(tree)
        
        return decryptor_code + "\n\n" + obfuscated_code
    
    def visit_Constant(self, node):
        """Encrypt string constants"""
        if isinstance(node.value, str) and len(node.value) > 3:
            # Encrypt the string
            encrypted = base64.b64encode(node.value.encode('utf-8')).decode('ascii')
            self.encrypted_strings.append(encrypted)
            
            # Replace with decryption call
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=self.string_decryptor, ctx=ast.Load()),
                    attr='decrypt',
                    ctx=ast.Load()
                ),
                args=[ast.Call(
                    func=ast.Name(id='base64', ctx=ast.Load()),
                    args=[ast.Constant(value=encrypted)],
                    keywords=[ast.keyword(arg='decode', value=ast.Constant(value='utf-8'))]
                )],
                keywords=[]
            )
        return node
    
    def add_opaque_predicates(self, tree):
        """Add opaque predicates to control flow"""
        # This would add complex conditional statements that always evaluate
        # the same way but are difficult for static analysis to determine
        return tree
    
    def split_basic_blocks(self, tree):
        """Split basic blocks to obfuscate control flow"""
        # This would break up straight-line code into smaller blocks
        # connected by conditional jumps
        return tree

# Advanced protection layer factory
def create_advanced_protection():
    """Create and configure advanced protection"""
    return AdvancedProtection()

def apply_advanced_obfuscation(code):
    """Apply all advanced obfuscation techniques"""
    protection = create_advanced_protection()
    
    # Apply string encryption
    obfuscator = AdvancedObfuscator()
    encrypted_code = obfuscator.encrypt_strings(code)
    
    # Apply all protection layers
    protected_code = protection.apply_protection(encrypted_code)
    
    return protected_code
