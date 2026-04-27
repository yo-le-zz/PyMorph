"""
C Obfuscator Module
Advanced obfuscation techniques for C code
"""

import re
import random
import string
from collections import defaultdict

# C keywords and protected names - Expanded for maximum compatibility
C_KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double',
    'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register',
    'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef',
    'union', 'unsigned', 'void', 'volatile', 'while', 'NULL', 'true', 'false',
    'printf', 'scanf', 'fprintf', 'fscanf', 'sprintf', 'sscanf', 'malloc', 'free',
    'calloc', 'realloc', 'memcpy', 'memmove', 'memcmp', 'memset', 'strlen', 'strcpy',
    'strncpy', 'strcat', 'strncat', 'strcmp', 'strncmp', 'strstr', 'strchr', 'strrchr',
    'atoi', 'atol', 'atof', 'strtod', 'strtol', 'strtoul', 'exit', 'abort', 'assert',
    # Standard library functions
    'fopen', 'fclose', 'fread', 'fwrite', 'fseek', 'ftell', 'rewind', 'feof', 'ferror',
    'clearerr', 'fflush', 'setbuf', 'setvbuf', 'ungetc', 'getc', 'putc', 'getchar', 'putchar',
    'gets', 'puts', 'fgets', 'fputs', 'perror', 'strerror', 'errno', 'system', 'qsort',
    'bsearch', 'abs', 'labs', 'div', 'ldiv', 'rand', 'srand', 'time', 'clock', 'asctime',
    'ctime', 'gmtime', 'localtime', 'mktime', 'strftime', 'difftime', 'signal', 'raise',
    'setjmp', 'longjmp', 'abort', 'atexit', 'exit', 'getenv', 'system', 'popen', 'pclose',
    # POSIX functions
    'open', 'close', 'read', 'write', 'lseek', 'dup', 'dup2', 'pipe', 'fork', 'exec',
    'execve', 'execv', 'execvp', 'execl', 'execlp', 'execle', 'wait', 'waitpid', 'kill',
    'signal', 'sigaction', 'sigprocmask', 'sigpending', 'sigsuspend', 'pause', 'alarm',
    'sleep', 'usleep', 'nanosleep', 'getpid', 'getppid', 'getuid', 'geteuid', 'getgid',
    'getegid', 'setuid', 'seteuid', 'setgid', 'setegid', 'getgroups', 'setgroups',
    'getlogin', 'ttyname', 'isatty', 'tcgetattr', 'tcsetattr', 'cfgetispeed',
    'cfgetospeed', 'cfsetispeed', 'cfsetospeed', 'tcdrain', 'tcflow', 'tcflush',
    'tcsendbreak', 'tcgetpgrp', 'tcsetpgrp', 'chmod', 'fchmod', 'chown', 'fchown',
    'lchown', 'umask', 'mkdir', 'rmdir', 'link', 'unlink', 'symlink', 'readlink',
    'rename', 'stat', 'fstat', 'lstat', 'access', 'utime', 'utimes', 'truncate',
    'ftruncate', 'opendir', 'readdir', 'rewinddir', 'closedir', 'telldir', 'seekdir',
    'scandir', 'glob', 'globfree', 'fnmatch', 'wordexp', 'wordfree', 'getopt',
    'getopt_long', 'getopt_long_only', 'confstr', 'sysconf', 'pathconf', 'fpathconf',
    'getcwd', 'chdir', 'fchdir', 'getrlimit', 'setrlimit', 'getrusage', 'gettimeofday',
    'settimeofday', 'times', 'uname', 'gethostname', 'sethostname', 'getdomainname',
    'setdomainname', 'vfork', 'execv', 'execve', 'execvp', 'execl', 'execlp', 'execle',
    'wait', 'waitpid', 'wait3', 'wait4', 'kill', 'raise', 'abort', 'signal', 'sigaction',
    'sigprocmask', 'sigpending', 'sigsuspend', 'pause', 'alarm', 'sleep', 'usleep',
    'nanosleep', 'clock_gettime', 'clock_settime', 'clock_getres', 'timer_create',
    'timer_delete', 'timer_settime', 'timer_gettime', 'timer_getoverrun', 'clock_nanosleep',
    # Math functions
    'acos', 'asin', 'atan', 'atan2', 'cos', 'sin', 'tan', 'cosh', 'sinh', 'tanh',
    'exp', 'frexp', 'ldexp', 'log', 'log10', 'modf', 'pow', 'sqrt', 'ceil', 'fabs',
    'floor', 'fmod', 'hypot', 'j0', 'j1', 'jn', 'y0', 'y1', 'yn', 'erf', 'erfc',
    'gamma', 'lgamma', 'finite', 'copysign', 'drem', 'finite', 'hypot', 'ilogb',
    'nextafter', 'remainder', 'rint', 'scalb', 'scalbn', 'significand', 'trunc',
    'cabs', 'cacos', 'casin', 'catan', 'ccos', 'csin', 'csqrt', 'ctan', 'cexp',
    'clog', 'cabs', 'carg', 'cimag', 'creal', 'conj', 'cproj', 'isnan', 'isinf',
    'isnormal', 'signbit', 'fpclassify', 'nearbyint', 'round', 'lround', 'llround',
    'lrint', 'llrint', 'trunc', 'tgamma', 'lgamma', 'exp2', 'expm1', 'log1p',
    'log2', 'logb', 'fdim', 'fma', 'fmax', 'fmin', 'cbrt', 'asinh', 'acosh', 'atanh',
    # Complex math
    'cabs', 'cacos', 'casin', 'catan', 'ccos', 'csin', 'csqrt', 'ctan', 'cexp',
    'clog', 'cabs', 'carg', 'cimag', 'creal', 'conj', 'cproj', 'creal', 'cimag',
    'carg', 'cabs', 'cacos', 'casin', 'catan', 'ccos', 'csin', 'csqrt', 'ctan',
    'cexp', 'clog', 'cpow', 'csinh', 'ccosh', 'ctanh', 'casinh', 'cacosh', 'catanh',
    # Extended math
    'acosh', 'asinh', 'atanh', 'exp2', 'expm1', 'log1p', 'log2', 'logb', 'scalbn',
    'scalbln', 'cbrt', 'fdim', 'fma', 'fmax', 'fmin', 'nearbyint', 'round',
    'lround', 'llround', 'lrint', 'llrint', 'trunc', 'tgamma', 'lgamma',
    # GNU extensions
    'asprintf', 'vasprintf', 'getline', 'getdelim', 'strcasestr', 'strnlen',
    'strndup', 'strsep', 'strtok_r', 'strsignal', 'strverscmp', 'memrchr',
    'memmem', 'mempcpy', 'memccpy', 'mempcpy', 'memmem', 'basename', 'dirname',
    'get_current_dir_name', 'canonicalize_file_name', 'realpath', 'getsubopt',
    'getopt_long', 'getopt_long_only', 'confstr', 'sysconf', 'pathconf', 'fpathconf',
    'getcwd', 'get_current_dir_name', 'getwd', 'getcwd', 'get_current_dir_name',
    'getwd', 'getcwd', 'get_current_dir_name', 'getwd', 'getcwd', 'get_current_dir_name',
    # OpenGL/GLUT
    'gl', 'glu', 'glut', 'GL_', 'GLU_', 'GLUT_', 'glfw', 'glew', 'SDL_', 'SDL',
    'IMG_', 'TTF_', 'MIX_', 'NET_', 'HTTP_', 'FTP_', 'SMTP_', 'POP3_', 'IMAP_',
    'LDAP_', 'SQL_', 'XML_', 'JSON_', 'YAML_', 'TOML_', 'INI_', 'CFG_', 'LOG_',
    'DBG_', 'ERR_', 'WRN_', 'INF_', 'glVertex', 'glNormal', 'glColor', 'glTexCoord',
    'glMultiTexCoord', 'glEdgeFlag', 'glFogCoord', 'glVertexAttrib', 'glIndex',
    'glMaterial', 'glLight', 'glLightModel', 'glTexEnv', 'glTexGen', 'glClipPlane',
    'glPolygonOffset', 'glPolygonStipple', 'glEdgeFlag', 'glFogCoord', 'glVertexAttrib',
    'glIndex', 'glMaterial', 'glLight', 'glLightModel', 'glTexEnv', 'glTexGen',
    'glClipPlane', 'glPolygonOffset', 'glPolygonStipple', 'glEdgeFlag', 'glFogCoord',
    'glVertexAttrib', 'glIndex', 'glMaterial', 'glLight', 'glLightModel', 'glTexEnv',
    'glTexGen', 'glClipPlane', 'glPolygonOffset', 'glPolygonStipple', 'glEdgeFlag',
    'glFogCoord', 'glVertexAttrib', 'glIndex', 'glMaterial', 'glLight', 'glLightModel',
    'glTexEnv', 'glTexGen', 'glClipPlane', 'glPolygonOffset', 'glPolygonStipple',
    # Common libraries
    'gtk', 'gdk', 'glib', 'gobject', 'gio', 'cairo', 'pango', 'atk', 'gdk_pixbuf',
    'gdk_gl', 'gtk_gl', 'gdk_x11', 'gtk_x11', 'gdk_win32', 'gtk_win32', 'gdk_quartz',
    'gtk_quartz', 'gdk_wayland', 'gtk_wayland', 'gdk_broadway', 'gtk_broadway',
    'gdk_macos', 'gtk_macos', 'gdk_mir', 'gtk_mir', 'gdk_fb', 'gtk_fb', 'gdk_directfb',
    'gtk_directfb', 'gdk_win32', 'gtk_win32', 'gdk_quartz', 'gtk_quartz', 'gdk_x11',
    'gtk_x11', 'gdk_wayland', 'gtk_wayland', 'gdk_broadway', 'gtk_broadway', 'gdk_macos',
    'gtk_macos', 'gdk_mir', 'gtk_mir', 'gdk_fb', 'gtk_fb', 'gdk_directfb', 'gtk_directfb',
    # Qt
    'QApplication', 'QWidget', 'QPushButton', 'QLabel', 'QLineEdit', 'QTextEdit',
    'QCheckBox', 'QRadioButton', 'QComboBox', 'QListWidget', 'QTreeWidget',
    'QTableWidget', 'QTabWidget', 'QStackedWidget', 'QToolBox', 'QMdiArea',
    'QWorkspace', 'QDockWidget', 'QMainWindow', 'QDialog', 'QFileDialog',
    'QColorDialog', 'QFontDialog', 'QInputDialog', 'QMessageBox', 'QErrorMessage',
    'QWizard', 'QWizardPage', 'QSplashScreen', 'QDesktopWidget', 'QX11Info',
    'QX11EmbedWidget', 'QX11EmbedContainer', 'QMacStyle', 'QWindowsStyle',
    'QWindowsXPStyle', 'QWindowsVistaStyle', 'QFusionStyle', 'QCleanlooksStyle',
    'QPlastiqueStyle', 'QCDEStyle', 'QMotifStyle', 'QSGStyle', 'QGtkStyle',
    'QAndroidStyle', 'QWindowsMobileStyle', 'QWindowsCEStyle', 'QWindowsPhoneStyle',
    'QMacStyle', 'QWindowsStyle', 'QWindowsXPStyle', 'QWindowsVistaStyle',
    'QFusionStyle', 'QCleanlooksStyle', 'QPlastiqueStyle', 'QCDEStyle', 'QMotifStyle',
    'QSGStyle', 'QGtkStyle', 'QAndroidStyle', 'QWindowsMobileStyle', 'QWindowsCEStyle',
    'QWindowsPhoneStyle', 'QMacStyle', 'QWindowsStyle', 'QWindowsXPStyle',
    'QWindowsVistaStyle', 'QFusionStyle', 'QCleanlooksStyle', 'QPlastiqueStyle',
    'QCDEStyle', 'QMotifStyle', 'QSGStyle', 'QGtkStyle', 'QAndroidStyle',
    'QWindowsMobileStyle', 'QWindowsCEStyle', 'QWindowsPhoneStyle', 'QMacStyle',
    'QWindowsStyle', 'QWindowsXPStyle', 'QWindowsVistaStyle', 'QFusionStyle',
    'QCleanlooksStyle', 'QPlastiqueStyle', 'QCDEStyle', 'QMotifStyle', 'QSGStyle',
    'QGtkStyle', 'QAndroidStyle', 'QWindowsMobileStyle', 'QWindowsCEStyle',
    'QWindowsPhoneStyle', 'QMacStyle', 'QWindowsStyle', 'QWindowsXPStyle',
    'QWindowsVistaStyle', 'QFusionStyle', 'QCleanlooksStyle', 'QPlastiqueStyle',
    'QCDEStyle', 'QMotifStyle', 'QSGStyle', 'QGtkStyle', 'QAndroidStyle',
    'QWindowsMobileStyle', 'QWindowsCEStyle', 'QWindowsPhoneStyle', 'QMacStyle'
}

def gen_c_name(length=8):
    """Generate random C identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length)),
        lambda: '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length//2)) + '_' + ''.join(random.choices(string.ascii_lowercase, k=length//2)),
        lambda: random.choice(['a', 'b', 'c', 'x', 'y', 'z']) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
    ]
    return random.choice(patterns)()

def encode_c_string(s):
    """Encode C strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Hex encoding
    hex_encoded = '\\x'.join(f'{ord(c):02x}' for c in s)
    hex_string = f'"{hex_encoded}"'
    
    # Octal encoding
    oct_encoded = '\\'.join(f'{ord(c):03o}' for c in s)
    oct_string = f'"{oct_encoded}"'
    
    # Mixed encoding
    mixed_encoded = []
    for c in s:
        if random.random() < 0.4:
            mixed_encoded.append(f'\\x{ord(c):02x}')
        elif random.random() < 0.7:
            mixed_encoded.append(f'\\{ord(c):03o}')
        else:
            mixed_encoded.append(c)
    
    mixed_string = f'"{"".join(mixed_encoded)}"'
    
    # Char array
    char_array = '{' + ', '.join([str(ord(c)) for c in s]) + '}'
    
    # Choose encoding method
    encoding_methods = [
        hex_string,
        oct_string,
        mixed_string,
        char_array
    ]
    
    return random.choice(encoding_methods)

def decompose_c_number(n):
    """Decompose C numbers into expressions"""
    if not isinstance(n, int) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x = abs(n): f"(int)({x} * 1.0)",
        lambda x = abs(n): f"({x} ^ 0)",
        lambda x = abs(n): f"({x} & 0xFFFFFFFF)",
        lambda x = abs(n): f"({x} << 1) >> 1"
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_c_code(code, options=None):
    """Main obfuscation function for C code"""
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
    
    # Remove comments first
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Find function names
    if options.get('rename_functions', True):
        # Function definitions
        func_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
        func_matches = re.finditer(func_pattern, code)
        for match in func_matches:
            name = match.group(1)
            if name not in C_KEYWORDS and name not in name_map:
                name_map[name] = gen_c_name()
    
    # Find variable names
    if options.get('rename_variables', True):
        # Variable declarations
        var_patterns = [
            r'\b(int|float|double|char|long|short|unsigned|signed)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\b(static|extern|auto|register)\s+(?:int|float|double|char|long|short|unsigned|signed)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\b(const)\s+(?:int|float|double|char|long|short|unsigned|signed)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for pattern in var_patterns:
            var_matches = re.finditer(pattern, code)
            for match in var_matches:
                name = match.group(2) if len(match.groups()) > 1 else match.group(1)
                if name not in C_KEYWORDS and name not in name_map:
                    name_map[name] = gen_c_name()
        
        # Struct and enum names
        struct_pattern = r'\b(struct|union|enum)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        struct_matches = re.finditer(struct_pattern, code)
        for match in struct_matches:
            name = match.group(2)
            if name not in C_KEYWORDS and name not in name_map:
                name_map[name] = gen_c_name()
    
    # Apply obfuscations
    obfuscated_code = code
    
    # Replace names
    if options.get('rename_variables', True) or options.get('rename_functions', True):
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
                return quote + encode_c_string(content)[1:-1] + quote
            return match.group(0)
        
        # Match both single and double quoted strings
        obfuscated_code = re.sub(r'(["\'])([^"\'\\]*(\\.[^"\'\\]*)*)\1', replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                return decompose_c_number(num)
            except ValueError:
                return num_str
        
        obfuscated_code = re.sub(r'\b\d+\b', replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_c_code()
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
        'numbers_decomposed': len(re.findall(r'\b\d+\b', code)),
        'macros_added': 3
    }

def generate_dummy_c_code():
    """Generate dummy C code to confuse analysis"""
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
int dummy_check_1() {
    int val = (100 >> 2) + 5;
    return (val % 7) == 0;
}
''',
        '''
struct DummyStruct {
    int field1;
    char field2[50];
};

int dummy_function() {
    struct DummyStruct ds = {(42 * 2) / 2, "dummy"};
    return ds.field1;
}
'''
    ]
    
    return random.choice(dummy_functions)

def test_c_obfuscation():
    """Test C obfuscation"""
    test_code = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char filename[256];
    char** data;
    int count;
    int capacity;
} DataProcessor;

DataProcessor* create_processor(const char* filename) {
    DataProcessor* processor = malloc(sizeof(DataProcessor));
    if (!processor) return NULL;
    
    strncpy(processor->filename, filename, sizeof(processor->filename) - 1);
    processor->filename[sizeof(processor->filename) - 1] = '\\0';
    processor->data = NULL;
    processor->count = 0;
    processor->capacity = 0;
    
    return processor;
}

int load_data(DataProcessor* processor) {
    FILE* file = fopen(processor->filename, "r");
    if (!file) {
        printf("File %s not found\\n", processor->filename);
        return 0;
    }
    
    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        // Remove newline
        line[strcspn(line, "\\n")] = '\\0';
        
        // Skip empty lines
        if (strlen(line) == 0) continue;
        
        // Resize array if needed
        if (processor->count >= processor->capacity) {
            processor->capacity = processor->capacity == 0 ? 16 : processor->capacity * 2;
            processor->data = realloc(processor->data, processor->capacity * sizeof(char*));
            if (!processor->data) return 0;
        }
        
        // Store line
        processor->data[processor->count] = malloc(strlen(line) + 1);
        strcpy(processor->data[processor->count], line);
        processor->count++;
    }
    
    fclose(file);
    return 1;
}

void process_data(DataProcessor* processor) {
    for (int i = 0; i < processor->count; i++) {
        // Convert to uppercase
        for (int j = 0; processor->data[i][j]; j++) {
            processor->data[i][j] = toupper(processor->data[i][j]);
        }
    }
}

void print_data(DataProcessor* processor) {
    printf("Processed %d lines:\\n", processor->count);
    for (int i = 0; i < processor->count; i++) {
        printf("%s\\n", processor->data[i]);
    }
}

void free_processor(DataProcessor* processor) {
    for (int i = 0; i < processor->count; i++) {
        free(processor->data[i]);
    }
    free(processor->data);
    free(processor);
}

int main() {
    DataProcessor* processor = create_processor("input.txt");
    
    if (load_data(processor)) {
        process_data(processor);
        print_data(processor);
    } else {
        printf("Failed to load data\\n");
    }
    
    free_processor(processor);
    return 0;
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
    
    obfuscated, stats = obfuscate_c_code(test_code, options)
    
    print("=== C Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_c_obfuscation()
