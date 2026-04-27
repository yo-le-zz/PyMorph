"""
C++ Obfuscator Module
Advanced obfuscation techniques for C++ code
"""

import re
import random
import string
from collections import defaultdict

# C++ keywords and protected names - Expanded for maximum compatibility
CPP_KEYWORDS = {
    'int', 'float', 'double', 'char', 'bool', 'void', 'return', 'if', 'else', 'while', 'for',
    'do', 'switch', 'case', 'break', 'continue', 'goto', 'sizeof', 'typedef', 'struct', 'class',
    'public', 'private', 'protected', 'virtual', 'static', 'const', 'extern', 'inline', 'namespace',
    'using', 'template', 'typename', 'new', 'delete', 'this', 'friend', 'operator', 'overload',
    'enum', 'union', 'volatile', 'register', 'auto', 'mutable', 'explicit', 'export', 'asm',
    'catch', 'throw', 'try', 'catch', 'finally', 'noexcept', 'constexpr', 'nullptr', 'decltype',
    'override', 'final', 'co_await', 'co_return', 'co_yield', 'concept', 'requires', 'import',
    'module', 'true', 'false', 'null', 'NULL', 'std', 'cout', 'cin', 'endl', 'string', 'vector',
    'map', 'set', 'list', 'array', 'queue', 'stack', 'deque', 'pair', 'tuple', 'unique_ptr',
    'shared_ptr', 'weak_ptr', 'make_shared', 'make_unique',
    # Standard library types and functions
    'iostream', 'fstream', 'sstream', 'algorithm', 'memory', 'functional', 'chrono', 'thread',
    'mutex', 'condition_variable', 'future', 'promise', 'atomic', 'numeric', 'complex',
    'valarray', 'bitset', 'regex', 'iterator', 'exception', 'stdexcept', 'typeinfo',
    'type_traits', 'utility', 'limits', 'numeric_limits', 'cmath', 'cctype', 'cstdlib',
    'cstdio', 'cstring', 'ctime', 'cstdarg', 'cstddef', 'climits', 'cfloat', 'cinttypes',
    'cstdint', 'cerr', 'clog', 'setw', 'setprecision', 'fixed', 'scientific', 'boolalpha',
    'noboolalpha', 'showbase', 'noshowbase', 'showpoint', 'noshowpoint', 'showpos', 'noshowpos',
    'skipws', 'noskipws', 'left', 'right', 'internal', 'dec', 'hex', 'oct', 'uppercase',
    'nouppercase', 'fixed', 'scientific', 'hexfloat', 'defaultfloat', 'unitbuf', 'nounitbuf',
    # OpenGL/GLUT
    'gl', 'glu', 'glut', 'GL_', 'GLU_', 'GLUT_', 'glfw', 'glew', 'SDL_', 'SDL', 'IMG_', 'TTF_',
    'MIX_', 'NET_', 'HTTP_', 'FTP_', 'SMTP_', 'POP3_', 'IMAP_', 'LDAP_', 'SQL_', 'XML_',
    'JSON_', 'YAML_', 'TOML_', 'INI_', 'CFG_', 'LOG_', 'DBG_', 'ERR_', 'WRN_', 'INF_',
    # Common frameworks
    'Qt', 'QWidget', 'QApplication', 'QObject', 'QString', 'QList', 'QVector', 'QMap',
    'QSet', 'QHash', 'QQueue', 'QStack', 'QPair', 'QTuple', 'QSharedPointer', 'QWeakPointer',
    'QScopedPointer', 'QPointer', 'QUniquePointer', 'QMakeShared', 'QMakeUnique',
    'wx', 'wxWidget', 'wxApp', 'wxFrame', 'wxPanel', 'wxDialog', 'wxButton', 'wxTextCtrl',
    'wxListBox', 'wxComboBox', 'wxCheckBox', 'wxRadioButton', 'wxMenu', 'wxMenuBar',
    'wxStatusBar', 'wxToolBar', 'wxNotebook', 'wxGrid', 'wxTreeCtrl', 'wxListCtrl',
    'wxSplitterWindow', 'wxScrolledWindow', 'wxStaticText', 'wxStaticBitmap',
    'wxStaticLine', 'wxStaticBox', 'wxGauge', 'wxSlider', 'wxSpinCtrl', 'wxDatePickerCtrl',
    'wxCalendarCtrl', 'wxTimer', 'wxSocket', 'wxHTTP', 'wxFTP', 'wxEmail', 'wxProtocol',
    'wxURL', 'wxFileSystem', 'wxFile', 'wxDir', 'wxFileName', 'wxPath', 'wxTextFile',
    'wxBinaryFile', 'wxTempFile', 'wxZip', 'wxGzip', 'wxBzip2', 'wxLzma', 'wxTar',
    # Boost libraries
    'boost', 'asio', 'system', 'regex', 'filesystem', 'thread', 'chrono', 'date_time',
    'signals2', 'bind', 'function', 'shared_ptr', 'weak_ptr', 'scoped_ptr', 'intrusive_ptr',
    'make_shared', 'make_unique', 'static_pointer_cast', 'dynamic_pointer_cast',
    'const_pointer_cast', 'reinterpret_pointer_cast', 'enable_shared_from_this',
    'weak_ptr', 'owner_less', 'owner_hash', 'owner_equal', 'get_deleter',
    # SFML
    'sf', 'RenderWindow', 'Texture', 'Sprite', 'Font', 'Text', 'Shape', 'CircleShape',
    'RectangleShape', 'ConvexShape', 'VertexArray', 'VertexBuffer', 'IndexBuffer',
    'Shader', 'Glsl', 'Clock', 'Time', 'Sound', 'Music', 'SoundBuffer', 'SoundRecorder',
    'Listener', 'Input', 'Keyboard', 'Mouse', 'Joystick', 'Touch', 'Sensor', 'Event',
    'VideoMode', 'ContextSettings', 'Style', 'Window', 'View', 'Transform', 'RenderStates',
    'BlendMode', 'Shader', 'Texture', 'Image', 'Font', 'Text', 'Sprite', 'Drawable',
    'Transformable', 'Shape', 'CircleShape', 'RectangleShape', 'ConvexShape', 'Polygon',
    'Line', 'Vertex', 'VertexArray', 'VertexBuffer', 'IndexBuffer', 'RenderTexture',
    'RenderWindow', 'Window', 'Context', 'Glsl', 'Shader', 'Clock', 'Time', 'Sound',
    'Music', 'SoundBuffer', 'SoundRecorder', 'Listener', 'Input', 'Keyboard', 'Mouse',
    'Joystick', 'Touch', 'Sensor', 'Event', 'VideoMode', 'ContextSettings', 'Style'
}

def gen_cpp_name(length=8):
    """Generate random C++ identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_letters, k=length)),
        lambda: '_' + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: random.choice(string.ascii_uppercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
        lambda: random.choice(['a', 'b', 'c', 'd', 'e']) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
    ]
    return random.choice(patterns)()

def encode_cpp_string(s):
    """Encode C++ strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Hex encoding
    hex_encoded = ''.join(f'\\x{ord(c):02x}' for c in s)
    
    # Octal encoding
    oct_encoded = ''.join(f'\\{ord(c):03o}' for c in s)
    
    # Mixed encoding
    mixed_encoded = []
    for c in s:
        if random.random() < 0.5:
            mixed_encoded.append(f'\\x{ord(c):02x}')
        else:
            mixed_encoded.append(f'\\{ord(c):03o}')
    
    # Choose encoding method
    encoding_methods = [
        f'"{hex_encoded}"',
        f'"{oct_encoded}"',
        f'"{"".join(mixed_encoded)}"',
        # Char array
        '{' + ','.join([str(ord(c)) for c in s]) + '}',
    ]
    
    return random.choice(encoding_methods)

def decompose_cpp_number(n):
    """Decompose C++ numbers into expressions"""
    if not isinstance(n, int) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x: f"(int)({x} * 1.0)",
        lambda x: f"({x} ^ 0)" if x >= 0 else str(x),
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_cpp_code(code, options=None):
    """Main obfuscation function for C++ code"""
    if options is None:
        options = {
            'rename_variables': True,
            'rename_functions': True,
            'encode_strings': True,
            'decompose_numbers': True,
            'add_dummy_code': True,
            'obfuscate_macros': True
        }
    
    # Store original mappings
    name_map = {}
    string_map = {}
    
    # Find all identifiers and strings
    # Variable/function patterns
    var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
    string_pattern = r'"([^"]*)"'
    char_pattern = r"'([^'])'"
    number_pattern = r'\b(\d+)\b'
    
    # Find and map variable/function names
    if options.get('rename_variables', True):
        # Find function definitions
        func_matches = re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{', code)
        for match in func_matches:
            name = match.group(1)
            if name not in CPP_KEYWORDS and name not in name_map:
                name_map[name] = gen_cpp_name()
        
        # Find variable declarations
        var_matches = re.finditer(r'\b(int|float|double|char|bool|string|auto)\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        for match in var_matches:
            name = match.group(2)
            if name not in CPP_KEYWORDS and name not in name_map:
                name_map[name] = gen_cpp_name()
    
    # Apply obfuscations
    obfuscated_code = code
    
    # Replace variable/function names
    if options.get('rename_variables', True):
        for old_name, new_name in sorted(name_map.items(), key=lambda x: len(x[0]), reverse=True):
            # Replace only whole words
            pattern = r'\b' + re.escape(old_name) + r'\b'
            obfuscated_code = re.sub(pattern, new_name, obfuscated_code)
    
    # Encode strings
    if options.get('encode_strings', True):
        def replace_string(match):
            original = match.group(0)
            content = match.group(1)
            if len(content) > 0:  # Don't encode empty strings
                return encode_cpp_string(content)
            return original
        
        obfuscated_code = re.sub(string_pattern, replace_string, obfuscated_code)
        obfuscated_code = re.sub(char_pattern, replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num = int(match.group(1))
            return decompose_cpp_number(num)
        
        obfuscated_code = re.sub(number_pattern, replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_cpp_code()
        # Insert dummy code after includes
        include_pattern = r'(#include\s+[^\n]+\n)+'
        if re.search(include_pattern, obfuscated_code):
            obfuscated_code = re.sub(include_pattern, r'\1\n' + dummy_code + '\n', obfuscated_code, count=1)
        else:
            obfuscated_code = dummy_code + '\n' + obfuscated_code
    
    # Obfuscate macros
    if options.get('obfuscate_macros', True):
        # Add dummy defines
        dummy_defines = '''
#define DUMMY_MACRO_1 0x1234
#define DUMMY_MACRO_2 ((42) + (7))
#define UNUSED_VAR __attribute__((unused))
'''
        obfuscated_code = dummy_defines + '\n' + obfuscated_code
    
    return obfuscated_code, {
        'variables_renamed': len(name_map),
        'strings_encoded': len(string_map),
        'numbers_decomposed': len(re.findall(number_pattern, code)),
        'macros_added': 3
    }

def generate_dummy_cpp_code():
    """Generate dummy C++ code to confuse analysis"""
    dummy_functions = [
        '''
int dummy_calc_1() {
    int x = (15 + 27) / 2;
    int y = x * 3 - 42;
    return y ^ 0x1234;
}
''',
        '''
void dummy_loop_1() {
    for(int i = 0; i < (10 + 5); i++) {
        int temp = i * (2 + 1);
        temp = temp / 3;
    }
}
''',
        '''
bool dummy_check_1() {
    int val = (100 >> 2) + 5;
    return (val % 7) == 0;
}
'''
    ]
    
    return random.choice(dummy_functions)

def test_cpp_obfuscation():
    """Test C++ obfuscation"""
    test_code = '''
#include <iostream>
#include <string>
using namespace std;

int calculate(int a, int b) {
    int result = a + b;
    return result;
}

int main() {
    string message = "Hello, World!";
    int number = 42;
    cout << message << " " << number << endl;
    return calculate(10, 20);
}
'''
    
    options = {
        'rename_variables': True,
        'rename_functions': True,
        'encode_strings': True,
        'decompose_numbers': True,
        'add_dummy_code': True,
        'obfuscate_macros': True
    }
    
    obfuscated, stats = obfuscate_cpp_code(test_code, options)
    
    print("=== C++ Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_cpp_obfuscation()
