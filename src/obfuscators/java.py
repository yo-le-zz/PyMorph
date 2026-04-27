"""
Java Obfuscator Module
Advanced obfuscation techniques for Java code
"""

import re
import random
import string
from collections import defaultdict

# Java keywords and protected names
JAVA_KEYWORDS = {
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class',
    'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final',
    'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof',
    'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected',
    'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized',
    'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while',
    'true', 'false', 'null', 'String', 'System', 'out', 'println', 'print', 'Integer',
    'Double', 'Float', 'Long', 'Short', 'Byte', 'Character', 'Boolean', 'Math', 'Random',
    'ArrayList', 'LinkedList', 'HashMap', 'HashSet', 'TreeMap', 'TreeSet', 'Arrays',
    'Collections', 'Objects', 'StringBuilder', 'StringBuffer', 'IOException', 'Exception',
    'RuntimeException', 'NullPointerException', 'IllegalArgumentException'
}

def gen_java_name(length=8):
    """Generate random Java identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length)),
        lambda: random.choice(['x', 'y', 'z', 'w', 'u', 'v']) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length//2)) + ''.join(random.choices(string.ascii_lowercase.upper(), k=length//2)),
        lambda: random.choice(['a', 'b', 'c']) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
    ]
    return random.choice(patterns)()

def encode_java_string(s):
    """Encode Java strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Unicode escape sequences
    unicode_encoded = ''.join(f'\\u{ord(c):04x}' for c in s)
    
    # Hex encoding with StringBuilder
    hex_encoded = ', '.join([f'(char)0x{ord(c):x}' for c in s])
    hex_builder = f'new StringBuilder().append(new String(new char[]{{{hex_encoded}}})).toString()'
    
    # Base64 encoding (simulated)
    base64_chars = []
    for i in range(0, len(s), 3):
        chunk = s[i:i+3]
        # Simple encoding for demonstration
        encoded_chunk = ''.join([f'\\u{ord(c):04x}' for c in chunk])
        base64_chars.append(encoded_chunk)
    
    base64_string = f'"\\u0062\\u0061\\u0073\\u0065\\u0036\\u0034" + "{"".join(base64_chars)}"'
    
    # Character array
    char_array = '{' + ', '.join([f"'{c}'" if c.isprintable() and c != "'" else f"'\\u{ord(c):04x}'" for c in s]) + '}'
    char_string = f'new String({char_array})'
    
    # Choose encoding method
    encoding_methods = [
        f'"{unicode_encoded}"',
        hex_builder,
        base64_string,
        char_string
    ]
    
    return random.choice(encoding_methods)

def decompose_java_number(n):
    """Decompose Java numbers into expressions"""
    if not isinstance(n, int) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x = abs(n): f"(int)({x} * 1.0)",
        lambda x = abs(n): f"({x} ^ 0)",
        lambda x = abs(n): f"Math.abs({-x})",
        lambda x = abs(n): f"Integer.parseInt(\"{x}\")",
        lambda x = abs(n): f"(int)Math.round({x * 1.0})"
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_java_code(code, options=None):
    """Main obfuscation function for Java code"""
    if options is None:
        options = {
            'rename_variables': True,
            'rename_functions': True,
            'rename_classes': True,
            'encode_strings': True,
            'decompose_numbers': True,
            'add_dummy_code': True,
            'obfuscate_packages': True
        }
    
    # Store original mappings
    name_map = {}
    string_map = {}
    
    # Remove comments first
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Find class names
    if options.get('rename_classes', True):
        class_pattern = r'\b(?:public\s+|private\s+|protected\s+)?(?:abstract\s+|final\s+)?class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        class_matches = re.finditer(class_pattern, code)
        for match in class_matches:
            name = match.group(1)
            if name not in JAVA_KEYWORDS and name not in name_map:
                name_map[name] = gen_java_name()
        
        # Interface names
        interface_pattern = r'\binterface\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        interface_matches = re.finditer(interface_pattern, code)
        for match in interface_matches:
            name = match.group(1)
            if name not in JAVA_KEYWORDS and name not in name_map:
                name_map[name] = gen_java_name()
    
    # Find method names
    if options.get('rename_functions', True):
        # Method definitions
        method_pattern = r'\b(?:public\s+|private\s+|protected\s+|static\s+|final\s+|abstract\s+|synchronized\s+)*(?:[a-zA-Z_][a-zA-Z0-9_<>?\[\]]+\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:throws\s+[^{]+)?\s*\{'
        method_matches = re.finditer(method_pattern, code)
        for match in method_matches:
            name = match.group(1)
            if name not in JAVA_KEYWORDS and name not in name_map and not name[0].isupper():  # Skip constructors
                name_map[name] = gen_java_name()
    
    # Find variable names
    if options.get('rename_variables', True):
        # Variable declarations
        var_patterns = [
            r'\b(?:int|double|float|long|short|byte|char|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\b(?:public\s+|private\s+|protected\s+|static\s+|final\s+)*(?:int|double|float|long|short|byte|char|boolean|String)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for pattern in var_patterns:
            var_matches = re.finditer(pattern, code)
            for match in var_matches:
                name = match.group(1)
                if name not in JAVA_KEYWORDS and name not in name_map:
                    name_map[name] = gen_java_name()
    
    # Apply obfuscations
    obfuscated_code = code
    
    # Replace names
    if options.get('rename_variables', True) or options.get('rename_functions', True) or options.get('rename_classes', True):
        for old_name, new_name in sorted(name_map.items(), key=lambda x: len(x[0]), reverse=True):
            # Replace only whole words
            pattern = r'\b' + re.escape(old_name) + r'\b'
            obfuscated_code = re.sub(pattern, new_name, obfuscated_code)
    
    # Encode strings
    if options.get('encode_strings', True):
        def replace_string(match):
            quote = match.group(1)
            content = match.group(2)
            if len(content) > 0 and not content.startswith('\\'):  # Don't re-encode
                return quote + encode_java_string(content)[1:-1] + quote
            return match.group(0)
        
        # Match both single and double quoted strings
        obfuscated_code = re.sub(r'(["\'])([^"\'\\]*(\\.[^"\'\\]*)*)\1', replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                return decompose_java_number(num)
            except ValueError:
                return num_str
        
        obfuscated_code = re.sub(r'\b\d+\b', replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_java_code()
        # Insert dummy code after package and imports
        package_import_pattern = r'(package\s+[^\n]+;\s*)?(?:import\s+[^\n]+;\s*)*'
        if re.search(package_import_pattern, obfuscated_code):
            obfuscated_code = re.sub(package_import_pattern, r'\g<0>\n' + dummy_code + '\n', obfuscated_code, count=1)
        else:
            obfuscated_code = dummy_code + '\n' + obfuscated_code
    
    # Obfuscate package names
    if options.get('obfuscate_packages', True):
        package_pattern = r'package\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)'
        package_match = re.search(package_pattern, obfuscated_code)
        if package_match:
            original_package = package_match.group(1)
            parts = original_package.split('.')
            obfuscated_parts = [gen_java_name(6) for _ in parts]
            obfuscated_package = '.'.join(obfuscated_parts)
            obfuscated_code = re.sub(package_pattern, f'package {obfuscated_package}', obfuscated_code)
    
    return obfuscated_code, {
        'variables_renamed': len(name_map),
        'strings_encoded': len(string_map),
        'numbers_decomposed': len(re.findall(r'\b\d+\b', code)),
        'classes_renamed': len([name for name in name_map.keys() if name[0].isupper()]),
        'methods_renamed': len([name for name in name_map.keys() if name[0].islower()])
    }

def generate_dummy_java_code():
    """Generate dummy Java code to confuse analysis"""
    dummy_classes = [
        '''
class DummyCalculator {
    private int x;
    private int y;
    
    public DummyCalculator() {
        this.x = (15 + 27) / 2;
        this.y = x * 3 - 42;
    }
    
    public int calculate() {
        return x ^ 0x1234;
    }
    
    private void dummyMethod() {
        for(int i = 0; i < (10 + 5); i++) {
            int temp = i * (2 + 1);
            temp = temp / 3;
        }
    }
}
''',
        '''
class DummyProcessor {
    private static final int CONSTANT = (42 * 2) / 2;
    private String dummyField = "dummy";
    
    public boolean dummyCheck() {
        int val = (100 >> 2) + 5;
        return (val % 7) == 0;
    }
    
    protected String dummyOperation(String input) {
        return new StringBuilder(input).reverse().toString();
    }
}
''',
        '''
interface DummyInterface {
    void dummyMethod1();
    int dummyMethod2(int param);
    default String defaultDummy() {
        return "default dummy";
    }
}

class DummyImplementation implements DummyInterface {
    @Override
    public void dummyMethod1() {
        System.out.println("dummy method 1");
    }
    
    @Override
    public int dummyMethod2(int param) {
        return param * (2 + 1) / 3;
    }
}
'''
    ]
    
    return random.choice(dummy_classes)

def test_java_obfuscation():
    """Test Java obfuscation"""
    test_code = '''
package com.example.processor;

import java.io.*;
import java.util.*;

public class DataProcessor {
    private String filename;
    private List<String> data;
    private static final int MAX_SIZE = 1000;
    
    public DataProcessor(String filename) {
        this.filename = filename;
        this.data = new ArrayList<>();
    }
    
    public boolean loadData() throws IOException {
        File file = new File(filename);
        if (!file.exists()) {
            System.err.println("File " + filename + " not found");
            return false;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    data.add(line.trim());
                }
            }
        }
        
        return true;
    }
    
    public List<String> processData() {
        List<String> processed = new ArrayList<>();
        for (String line : data) {
            String upperLine = line.toUpperCase();
            if (!upperLine.isEmpty()) {
                processed.add(upperLine);
            }
        }
        return processed;
    }
    
    public void saveResults(String outputFile) throws IOException {
        List<String> processedData = processData();
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))) {
            for (String line : processedData) {
                writer.write(line);
                writer.newLine();
            }
        }
    }
    
    public int getDataCount() {
        return data.size();
    }
    
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java DataProcessor <input_file>");
            return;
        }
        
        DataProcessor processor = new DataProcessor(args[0]);
        try {
            if (processor.loadData()) {
                System.out.println("Processed " + processor.getDataCount() + " lines");
                processor.saveResults("output.txt");
                System.out.println("Results saved to output.txt");
            } else {
                System.err.println("Failed to load data");
            }
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
'''
    
    options = {
        'rename_variables': True,
        'rename_functions': True,
        'rename_classes': True,
        'encode_strings': True,
        'decompose_numbers': True,
        'add_dummy_code': True,
        'obfuscate_packages': True
    }
    
    obfuscated, stats = obfuscate_java_code(test_code, options)
    
    print("=== Java Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_java_obfuscation()
