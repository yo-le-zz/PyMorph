"""
Go Obfuscator Module
Advanced obfuscation techniques for Go code
"""

import re
import random
import string
from collections import defaultdict

# Go keywords and protected names
GO_KEYWORDS = {
    'break', 'case', 'chan', 'const', 'continue', 'default', 'defer', 'else', 'fallthrough',
    'for', 'func', 'go', 'goto', 'if', 'import', 'interface', 'map', 'package', 'range',
    'return', 'select', 'struct', 'switch', 'type', 'var', 'nil', 'true', 'false', 'iota',
    'len', 'cap', 'make', 'new', 'append', 'copy', 'delete', 'close', 'panic', 'recover',
    'print', 'println', 'fmt', 'os', 'io', 'strings', 'strconv', 'bytes', 'bufio',
    'time', 'math', 'sort', 'container/list', 'container/heap', 'container/ring',
    'sync', 'sync/atomic', 'net', 'net/http', 'encoding/json', 'encoding/xml'
}

def gen_go_name(length=8):
    """Generate random Go identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length)),
        lambda: random.choice(['x', 'y', 'z', 'w', 'u', 'v']) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length//2)) + ''.join(random.choices(string.ascii_lowercase.upper(), k=length//2)),
        lambda: 'g_' + ''.join(random.choices(string.ascii_lowercase, k=length-2)),
    ]
    return random.choice(patterns)()

def encode_go_string(s):
    """Encode Go strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Backtick string (raw string)
    backtick_string = f'`{s}`'
    
    # Hex encoding with string builder
    hex_encoded = ', '.join([f'0x{ord(c):02x}' for c in s])
    hex_builder = f'string([]byte{{{hex_encoded}}})'
    
    # Unicode escape sequences
    unicode_encoded = ''.join(f'\\u{ord(c):04x}' for c in s)
    unicode_string = f'"{unicode_encoded}"'
    
    # Byte slice conversion
    byte_slice = '[]byte{' + ', '.join([str(ord(c)) for c in s]) + '}'
    byte_string = f'string({byte_slice})'
    
    # Base64-like encoding
    base64_encoded = ''.join([f'\\x{ord(c):02x}' for c in s])
    base64_string = f'"{base64_encoded}"'
    
    # Choose encoding method
    encoding_methods = [
        backtick_string,
        hex_builder,
        unicode_string,
        byte_string,
        base64_string
    ]
    
    return random.choice(encoding_methods)

def decompose_go_number(n):
    """Decompose Go numbers into expressions"""
    if not isinstance(n, int) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x = abs(n): f"{x} ^ 0",
        lambda x = abs(n): f"{x} & 0xFFFFFFFF",
        lambda x = abs(n): f"{x} << 1 >> 1",
        lambda x = abs(n): f"int64({x})",
        lambda x = abs(n): f"uint32({x})",
        lambda x = abs(n): f"float64({x})"
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_go_code(code, options=None):
    """Main obfuscation function for Go code"""
    if options is None:
        options = {
            'rename_variables': True,
            'rename_functions': True,
            'rename_packages': True,
            'encode_strings': True,
            'decompose_numbers': True,
            'add_dummy_code': True
        }
    
    # Store original mappings
    name_map = {}
    string_map = {}
    
    # Remove comments first
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Find package name
    if options.get('rename_packages', True):
        package_pattern = r'package\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        package_match = re.search(package_pattern, code)
        if package_match:
            original_package = package_match.group(1)
            if original_package != 'main' and original_package not in GO_KEYWORDS:
                name_map[original_package] = gen_go_name(6)
    
    # Find function names
    if options.get('rename_functions', True):
        # Function definitions
        func_pattern = r'func\s+(?:\([^)]*\)\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        func_matches = re.finditer(func_pattern, code)
        for match in func_matches:
            name = match.group(1)
            if name not in GO_KEYWORDS and name not in name_map:
                name_map[name] = gen_go_name()
    
    # Find variable names
    if options.get('rename_variables', True):
        # Variable declarations
        var_patterns = [
            r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+',
            r'var\s+\([^)]+\)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+',
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:=\s+',
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s+\w+\s*=',
        ]
        
        for pattern in var_patterns:
            var_matches = re.finditer(pattern, code)
            for match in var_matches:
                name = match.group(1)
                if name not in GO_KEYWORDS and name not in name_map:
                    name_map[name] = gen_go_name()
        
        # Struct names
        struct_pattern = r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+struct'
        struct_matches = re.finditer(struct_pattern, code)
        for match in struct_matches:
            name = match.group(1)
            if name not in GO_KEYWORDS and name not in name_map:
                name_map[name] = gen_go_name()
        
        # Interface names
        interface_pattern = r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+interface'
        interface_matches = re.finditer(interface_pattern, code)
        for match in interface_matches:
            name = match.group(1)
            if name not in GO_KEYWORDS and name not in name_map:
                name_map[name] = gen_go_name()
    
    # Apply obfuscations
    obfuscated_code = code
    
    # Replace names
    if options.get('rename_variables', True) or options.get('rename_functions', True) or options.get('rename_packages', True):
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
                return quote + encode_go_string(content)[1:-1] + quote
            return match.group(0)
        
        # Match both double quoted and backtick strings
        obfuscated_code = re.sub(r'(["`])([^"\'\\]*(\\.[^"\'\\]*)*)\1', replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                return decompose_go_number(num)
            except ValueError:
                return num_str
        
        obfuscated_code = re.sub(r'\b\d+\b', replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_go_code()
        # Insert dummy code after imports
        import_pattern = r'(import\s+\([^)]+\)\s*)+'
        if re.search(import_pattern, obfuscated_code):
            obfuscated_code = re.sub(import_pattern, r'\1\n' + dummy_code + '\n', obfuscated_code, count=1)
        else:
            obfuscated_code = dummy_code + '\n' + obfuscated_code
    
    return obfuscated_code, {
        'variables_renamed': len(name_map),
        'strings_encoded': len(string_map),
        'numbers_decomposed': len(re.findall(r'\b\d+\b', code)),
        'packages_renamed': 1 if options.get('rename_packages') and package_match else 0
    }

def generate_dummy_go_code():
    """Generate dummy Go code to confuse analysis"""
    dummy_functions = [
        '''
func dummyCalc() int {
    x := (15 + 27) / 2
    y := x * 3 - 42
    return y ^ 0x1234
}

func dummyLoop() {
    for i := 0; i < (10 + 5); i++ {
        temp := i * (2 + 1)
        _ = temp / 3
    }
}

func dummyCheck() bool {
    val := (100 >> 2) + 5
    return (val % 7) == 0
}
''',
        '''
type DummyStruct struct {
    field1 int
    field2 string
}

func (d *DummyStruct) dummyMethod() int {
    d.field1 = (42 * 2) / 2
    d.field2 = "dummy"
    return d.field1
}

func dummyProcessor(data []string) []string {
    result := make([]string, 0, len(data))
    for _, item := range data {
        if len(item) > 0 {
            result = append(result, strings.ToUpper(item))
        }
    }
    return result
}
''',
        '''
type DummyInterface interface {
    dummyMethod1()
    dummyMethod2(int) string
}

type DummyImplementation struct{}

func (d DummyImplementation) dummyMethod1() {
    fmt.Println("dummy method 1")
}

func (d DummyImplementation) dummyMethod2(param int) string {
    return fmt.Sprintf("param: %d", param*(2+1)/3)
}

func dummyChannel() {
    ch := make(chan int, (5 + 5))
    go func() {
        for i := 0; i < 10; i++ {
            ch <- i * (2 + 1)
        }
        close(ch)
    }()
    
    for val := range ch {
        _ = val
    }
}
'''
    ]
    
    return random.choice(dummy_functions)

def test_go_obfuscation():
    """Test Go obfuscation"""
    test_code = '''
package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

type DataProcessor struct {
    filename string
    data     []string
}

func NewDataProcessor(filename string) *DataProcessor {
    return &DataProcessor{
        filename: filename,
        data:     make([]string, 0),
    }
}

func (dp *DataProcessor) LoadData() error {
    file, err := os.Open(dp.filename)
    if err != nil {
        fmt.Printf("File %s not found\\n", dp.filename)
        return err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
        if trimmed := strings.TrimSpace(line); trimmed != "" {
            dp.data = append(dp.data, trimmed)
        }
    }

    return scanner.Err()
}

func (dp *DataProcessor) ProcessData() []string {
    processed := make([]string, 0, len(dp.data))
    for _, line := range dp.data {
        upperLine := strings.ToUpper(line)
        if upperLine != "" {
            processed = append(processed, upperLine)
        }
    }
    return processed
}

func (dp *DataProcessor) SaveResults(outputFile string) error {
    processedData := dp.ProcessData()
    file, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer file.Close()

    writer := bufio.NewWriter(file)
    for _, line := range processedData {
        _, err := writer.WriteString(line + "\\n")
        if err != nil {
            return err
        }
    }
    return writer.Flush()
}

func (dp *DataProcessor) GetDataCount() int {
    return len(dp.data)
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run main.go <input_file>")
        return
    }

    processor := NewDataProcessor(os.Args[1])
    if err := processor.LoadData(); err != nil {
        fmt.Printf("Failed to load data: %v\\n", err)
        return
    }

    fmt.Printf("Processed %d lines\\n", processor.GetDataCount())
    if err := processor.SaveResults("output.txt"); err != nil {
        fmt.Printf("Failed to save results: %v\\n", err)
        return
    }

    fmt.Println("Results saved to output.txt")
}
'''
    
    options = {
        'rename_variables': True,
        'rename_functions': True,
        'rename_packages': True,
        'encode_strings': True,
        'decompose_numbers': True,
        'add_dummy_code': True
    }
    
    obfuscated, stats = obfuscate_go_code(test_code, options)
    
    print("=== Go Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_go_obfuscation()
