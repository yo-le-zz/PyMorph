"""
Rust Obfuscator Module
Advanced obfuscation techniques for Rust code
"""

import re
import random
import string
from collections import defaultdict

# Rust keywords and protected names - Expanded for maximum compatibility
RUST_KEYWORDS = {
    'as', 'break', 'const', 'continue', 'crate', 'else', 'enum', 'extern', 'false', 'fn',
    'for', 'if', 'impl', 'in', 'let', 'loop', 'match', 'mod', 'move', 'mut', 'pub',
    'ref', 'return', 'self', 'Self', 'static', 'struct', 'super', 'trait', 'true', 'type',
    'unsafe', 'use', 'where', 'while', 'async', 'await', 'dyn', 'abstract', 'become',
    'box', 'do', 'final', 'macro', 'override', 'priv', 'try', 'typeof', 'unsized',
    'virtual', 'yield', 'str', 'i8', 'i16', 'i32', 'i64', 'i128', 'u8', 'u16', 'u32',
    'u64', 'u128', 'isize', 'usize', 'f32', 'f64', 'bool', 'char', 'Option', 'Some',
    'None', 'Result', 'Ok', 'Err', 'String', 'Vec', 'HashMap', 'HashSet', 'println',
    'print', 'eprintln', 'eprint', 'format', 'panic', 'unimplemented', 'todo', 'debug_assert',
    'debug_assert_eq', 'debug_assert_ne', 'assert', 'assert_eq', 'assert_ne', 'unreachable',
    'vec', 'vec!', 'format!', 'print!', 'println!', 'eprint!', 'eprintln!', 'panic!',
    'unimplemented!', 'todo!', 'debug_assert!', 'debug_assert_eq!', 'debug_assert_ne!',
    'assert!', 'assert_eq!', 'assert_ne!', 'unreachable!', 'write!', 'writeln!',
    # Standard library types and functions
    'std', 'core', 'alloc', 'collections', 'io', 'fs', 'path', 'env', 'process', 'thread',
    'sync', 'time', 'net', 'os', 'mem', 'ptr', 'num', 'char', 'str', 'slice', 'array',
    'tuple', 'unit', 'clone', 'copy', 'send', 'sync', 'drop', 'sized', 'any', 'borrow',
    'convert', 'default', 'hash', 'cmp', 'partial_eq', 'eq', 'partial_ord', 'ord',
    'as_ref', 'as_mut', 'into', 'from', 'try_from', 'try_into', 'borrow', 'borrow_mut',
    'to_owned', 'clone_into', 'from_str', 'display', 'debug', 'error', 'hasher', 'default_hasher',
    'random_state', 'build_hasher', 'build_hasher_default', 'hash_map', 'hash_set', 'btree_map',
    'btree_set', 'linked_list', 'vec_deque', 'binary_heap', 'option', 'result', 'cell', 'ref_cell',
    'rc', 'arc', 'weak', 'mutex', 'rwlock', 'once', 'once_lock', 'lazy', 'lazy_static',
    'thread_local', 'atomic', 'atomic_bool', 'atomic_i8', 'atomic_i16', 'atomic_i32',
    'atomic_i64', 'atomic_i128', 'atomic_isize', 'atomic_u8', 'atomic_u16', 'atomic_u32',
    'atomic_u64', 'atomic_u128', 'atomic_usize', 'atomic_ptr', 'ordering', 'seq_cst',
    'acquire', 'release', 'acq_rel', 'relaxed', 'fence', 'compiler_fence', 'sync_atomic',
    'parking_lot', 'parking_lot_core', 'parking_lot_mutex', 'parking_lot_rwlock',
    'parking_lot_condvar', 'parking_lot_once', 'parking_lot_once_cell', 'parking_lot_lazy',
    'parking_lot_thread_local', 'parking_lot_deadlock', 'parking_lot_reentrant_mutex',
    'parking_lot_fair_mutex', 'parking_lot_raw_mutex', 'parking_lot_raw_rwlock',
    'parking_lot_fair_rwlock', 'parking_lot_mutex_guard', 'parking_lot_rwlock_guard',
    'parking_lot_mapped_mutex_guard', 'parking_lot_mapped_rwlock_guard',
    'parking_lot_mutex_lock', 'parking_lot_rwlock_lock', 'parking_lot_mutex_unlock',
    'parking_lot_rwlock_unlock', 'parking_lot_mutex_try_lock', 'parking_lot_rwlock_try_lock',
    'parking_lot_mutex_lock_timeout', 'parking_lot_rwlock_lock_timeout',
    'parking_lot_mutex_lock_for', 'parking_lot_rwlock_lock_for',
    'parking_lot_mutex_lock_until', 'parking_lot_rwlock_lock_until',
    'parking_lot_mutex_lock_deadline', 'parking_lot_rwlock_lock_deadline',
    'parking_lot_mutex_lock_blocking', 'parking_lot_rwlock_lock_blocking',
    'parking_lot_mutex_lock_nonblocking', 'parking_lot_rwlock_lock_nonblocking',
    'parking_lot_mutex_lock_interruptible', 'parking_lot_rwlock_lock_interruptible',
    'parking_lot_mutex_lock_interruptible_timeout', 'parking_lot_rwlock_lock_interruptible_timeout',
    'parking_lot_mutex_lock_interruptible_for', 'parking_lot_rwlock_lock_interruptible_for',
    'parking_lot_mutex_lock_interruptible_until', 'parking_lot_rwlock_lock_interruptible_until',
    'parking_lot_mutex_lock_interruptible_deadline', 'parking_lot_rwlock_lock_interruptible_deadline',
    'parking_lot_mutex_lock_interruptible_blocking', 'parking_lot_rwlock_lock_interruptible_blocking',
    'parking_lot_mutex_lock_interruptible_nonblocking', 'parking_lot_rwlock_lock_interruptible_nonblocking',
    'parking_lot_mutex_lock_interruptible_poisoned', 'parking_lot_rwlock_lock_interruptible_poisoned',
    'parking_lot_mutex_lock_interruptible_poisoned_timeout', 'parking_lot_rwlock_lock_interruptible_poisoned_timeout',
    'parking_lot_mutex_lock_interruptible_poisoned_for', 'parking_lot_rwlock_lock_interruptible_poisoned_for',
    'parking_lot_mutex_lock_interruptible_poisoned_until', 'parking_lot_rwlock_lock_interruptible_poisoned_until',
    'parking_lot_mutex_lock_interruptible_poisoned_deadline', 'parking_lot_rwlock_lock_interruptible_poisoned_deadline',
    'parking_lot_mutex_lock_interruptible_poisoned_blocking', 'parking_lot_rwlock_lock_interruptible_poisoned_blocking',
    'parking_lot_mutex_lock_interruptible_poisoned_nonblocking', 'parking_lot_rwlock_lock_interruptible_poisoned_nonblocking',
    'parking_lot_mutex_lock_interruptible_poisoned_timeout', 'parking_lot_rwlock_lock_interruptible_poisoned_timeout',
    'parking_lot_mutex_lock_interruptible_poisoned_for', 'parking_lot_rwlock_lock_interruptible_poisoned_for',
    'parking_lot_mutex_lock_interruptible_poisoned_until', 'parking_lot_rwlock_lock_interruptible_poisoned_until',
    'parking_lot_mutex_lock_interruptible_poisoned_deadline', 'parking_lot_rwlock_lock_interruptible_poisoned_deadline',
    'parking_lot_mutex_lock_interruptible_poisoned_blocking', 'parking_lot_rwlock_lock_interruptible_poisoned_blocking',
    'parking_lot_mutex_lock_interruptible_poisoned_nonblocking', 'parking_lot_rwlock_lock_interruptible_poisoned_nonblocking',
    # External crates
    'serde', 'Serialize', 'Deserialize', 'serde_json', 'serde_yaml', 'serde_cbor', 'serde_pickle',
    'serde_bytes', 'serde_derive', 'serde_with', 'serde_regex', 'serde_repr', 'serde_str',
    'serde_urlencoded', 'serde_qs', 'serde_querystring', 'serde_path_to_error', 'serde_test',
    'tokio', 'tokio_util', 'tokio_stream', 'tokio_test', 'tokio_macros', 'tokio_main',
    'tokio_runtime', 'tokio_executor', 'tokio_timer', 'tokio_sync', 'tokio_net', 'tokio_io',
    'tokio_fs', 'tokio_process', 'tokio_thread', 'tokio_signal', 'tokio_time', 'tokio_util',
    'tokio_codec', 'tokio_tls', 'tokio_native_tls', 'tokio_openssl', 'tokio_rustls',
    'tokio_unix', 'tokio_windows', 'tokio_macos', 'tokio_linux', 'tokio_android', 'tokio_ios',
    'tokio_wasm', 'tokio_web', 'tokio_http', 'tokio_websocket', 'tokio_mpsc', 'tokio_broadcast',
    'tokio_watch', 'tokio_tracing', 'tokio_log', 'tokio_metrics', 'tokio_profiling',
    'tokio_debug', 'tokio_test_util', 'tokio_test', 'tokio_example', 'tokio_bench',
    'tokio_docs', 'tokio_guide', 'tokio_tutorial', 'tokio_book', 'tokio_blog', 'tokio_news',
    'tokio_community', 'tokio_gitter', 'tokio_discord', 'tokio_reddit', 'tokio_twitter',
    'tokio_facebook', 'tokio_linkedin', 'tokio_github', 'tokio_gitlab', 'tokio_bitbucket',
    'tokio_stackoverflow', 'tokio_crates', 'tokio_docs_rs', 'tokio_rust_lang', 'tokio_rustc',
    'tokio_cargo', 'tokio_rustup', 'tokio_rustfmt', 'tokio_clippy', 'tokio_miri', 'tokio_rustdoc',
    'tokio_rust_analyzer', 'tokio_rust_ide', 'tokio_rust_server', 'tokio_rust_client',
    'tokio_rust_toolchain', 'tokio_rust_target', 'tokio_rust_arch', 'tokio_rust_os',
    'tokio_rust_platform', 'tokio_rust_vendor', 'tokio_rust_device', 'tokio_rust_board',
    'tokio_rust_chip', 'tokio_rust_fpga', 'tokio_rust_mcu', 'tokio_rust_embedded',
    'tokio_rust_no_std', 'tokio_rust_std', 'tokio_rust_alloc', 'tokio_rust_core',
    'tokio_rust_std', 'tokio_rust_alloc', 'tokio_rust_core', 'tokio_rust_compiler',
    'tokio_rust_llvm', 'tokio_rust_gcc', 'tokio_rust_clang', 'tokio_rust_msvc',
    'tokio_rust_intel', 'tokio_rust_arm', 'tokio_rust_riscv', 'tokio_rust_powerpc',
    'tokio_rust_mips', 'tokio_rust_sparc', 'tokio_rust_x86', 'tokio_rust_amd64',
    'tokio_rust_i386', 'tokio_rust_arm64', 'tokio_rust_aarch64', 'tokio_rust_riscv64',
    'tokio_rust_powerpc64', 'tokio_rust_mips64', 'tokio_rust_sparc64', 'tokio_rust_x86_64',
    'tokio_rust_windows', 'tokio_rust_linux', 'tokio_rust_macos', 'tokio_rust_android',
    'tokio_rust_ios', 'tokio_rust_wasm', 'tokio_rust_web', 'tokio_rust_embedded',
    'tokio_rust_no_std', 'tokio_rust_std', 'tokio_rust_alloc', 'tokio_rust_core',
    'tokio_rust_std', 'tokio_rust_alloc', 'tokio_rust_core', 'tokio_rust_compiler',
    'tokio_rust_llvm', 'tokio_rust_gcc', 'tokio_rust_clang', 'tokio_rust_msvc',
    'tokio_rust_intel', 'tokio_rust_arm', 'tokio_rust_riscv', 'tokio_rust_powerpc',
    'tokio_rust_mips', 'tokio_rust_sparc', 'tokio_rust_x86', 'tokio_rust_amd64',
    'tokio_rust_i386', 'tokio_rust_arm64', 'tokio_rust_aarch64', 'tokio_rust_riscv64',
    'tokio_rust_powerpc64', 'tokio_rust_mips64', 'tokio_rust_sparc64', 'tokio_rust_x86_64',
    'reqwest', 'hyper', 'actix', 'rocket', 'warp', 'tower', 'axum', 'tonic', 'prost',
    'sqlx', 'diesel', 'sea_orm', 'polars', 'arrow', 'datafusion', 'ballista', 'spark_rust',
    'candle_core', 'candle_nn', 'candle_transformers', 'candle_datasets', 'candle_examples',
    'burn', 'tch', 'ndarray', 'nalgebra', 'cgmath', 'glam', 'vek', 'ultraviolet',
    'mint', 'euclid', 'approx', 'num_traits', 'alga', 'petgraph', 'graph', 'networkx',
    'scipy', 'numpy', 'pandas', 'matplotlib', 'plotly', 'bokeh', 'altair', 'seaborn',
    'ggplot2', 'd3', 'vega', 'vega_lite', 'observable', 'jupyter', 'ipython', 'jupyterlab',
    'vscode', 'sublime', 'atom', 'vim', 'emacs', 'neovim', 'helix', 'kakoune', 'micro',
    'nano', 'gedit', 'kate', 'geany', 'codeblocks', 'qtcreator', 'xcode', 'android_studio',
    'intellij', 'pycharm', 'webstorm', 'phpstorm', 'rubymine', 'clion', 'rider', 'goland',
    'datagrip', 'appcode', 'idea', 'fleet', 'rust_rover', 'rust_analyzer', 'rust_ide',
    'rust_server', 'rust_client', 'rust_toolchain', 'rust_target', 'rust_arch',
    'rust_os', 'rust_platform', 'rust_vendor', 'rust_device', 'rust_board',
    'rust_chip', 'rust_fpga', 'rust_mcu', 'rust_embedded', 'rust_no_std', 'rust_std',
    'rust_alloc', 'rust_core', 'rust_compiler', 'rust_llvm', 'rust_gcc',
    'rust_clang', 'rust_msvc', 'rust_intel', 'rust_arm', 'rust_riscv',
    'rust_powerpc', 'rust_mips', 'rust_sparc', 'rust_x86', 'rust_amd64',
    'rust_i386', 'rust_arm64', 'rust_aarch64', 'rust_riscv64', 'rust_powerpc64',
    'rust_mips64', 'rust_sparc64', 'rust_x86_64', 'rust_windows', 'rust_linux',
    'rust_macos', 'rust_android', 'rust_ios', 'rust_wasm', 'rust_web',
    'rust_embedded', 'rust_no_std', 'rust_std', 'rust_alloc', 'rust_core',
    'rust_compiler', 'rust_llvm', 'rust_gcc', 'rust_clang', 'rust_msvc',
    'rust_intel', 'rust_arm', 'rust_riscv', 'rust_powerpc', 'rust_mips',
    'rust_sparc', 'rust_x86', 'rust_amd64', 'rust_i386', 'rust_arm64',
    'rust_aarch64', 'rust_riscv64', 'rust_powerpc64', 'rust_mips64',
    'rust_sparc64', 'rust_x86_64', 'rust_windows', 'rust_linux',
    'rust_macos', 'rust_android', 'rust_ios', 'rust_wasm', 'rust_web',
    'rust_embedded', 'rust_no_std', 'rust_std', 'rust_alloc', 'rust_core',
    'rust_compiler', 'rust_llvm', 'rust_gcc', 'rust_clang', 'rust_msvc',
    'rust_intel', 'rust_arm', 'rust_riscv', 'rust_powerpc', 'rust_mips',
    'rust_sparc', 'rust_x86', 'rust_amd64', 'rust_i386', 'rust_arm64',
    'rust_aarch64', 'rust_riscv64', 'rust_powerpc64', 'rust_mips64',
    'rust_sparc64', 'rust_x86_64'
}

def gen_rust_name(length=8):
    """Generate random Rust identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length)),
        lambda: random.choice(['x', 'y', 'z', 'w', 'u', 'v']) + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=length//2)) + '_' + ''.join(random.choices(string.ascii_lowercase, k=length//2)),
        lambda: 's_' + ''.join(random.choices(string.ascii_lowercase, k=length-2)),
    ]
    return random.choice(patterns)()

def encode_rust_string(s):
    """Encode Rust strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Byte string encoding
    byte_encoded = ', '.join([str(ord(c)) for c in s])
    byte_encoded_hex = byte_encoded.replace(', ', '\\x')
    byte_string = f"b\"\\x{byte_encoded_hex}\""
    
    # Hex encoding
    hex_encoded = '\\x'.join(f'{ord(c):02x}' for c in s)
    hex_string = f'"\\x{hex_encoded}"'
    
    # Unicode escape sequences
    unicode_encoded = ''.join(f'\\u{{{ord(c):04x}}}' for c in s)
    unicode_string = f'"{unicode_encoded}"'
    
    # Char array
    char_array = '[' + ', '.join([f"'{c}'" if c.isprintable() and c != "'" else f"'\\x{ord(c):02x}'" for c in s]) + ']'
    
    # Choose encoding method
    encoding_methods = [
        byte_string,
        hex_string,
        unicode_string,
        f"&String::from_utf8_lossy(&{char_array}.concat().into_bytes())[..].to_string()"
    ]
    
    return random.choice(encoding_methods)

def decompose_rust_number(n):
    """Decompose Rust numbers into expressions"""
    if not isinstance(n, int) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x: f"({x} as i32) * 1",
        lambda x = abs(n): f"({x} ^ 0)",
        lambda x: f"std::num::Wrapping({x}).0",
        lambda x: f"({x} as u32) as i32"
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_rust_code(code, options=None):
    """Main obfuscation function for Rust code"""
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
        func_pattern = r'\bfn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        func_matches = re.finditer(func_pattern, code)
        for match in func_matches:
            name = match.group(1)
            if name not in RUST_KEYWORDS and name not in name_map:
                name_map[name] = gen_rust_name()
        
        # Method definitions (impl blocks)
        method_pattern = r'\bfn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*(?:->[^{]*)?\{'
        method_matches = re.finditer(method_pattern, code)
        for match in method_matches:
            name = match.group(1)
            if name not in RUST_KEYWORDS and name not in name_map:
                name_map[name] = gen_rust_name()
    
    # Find variable names
    if options.get('rename_variables', True):
        # Variable bindings
        var_patterns = [
            r'\blet\s+(?:mut\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*=',  # let mut/var
            r'\bconst\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:',            # const
            r'\bstatic\s+(?:mut\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*:', # static
        ]
        
        for pattern in var_patterns:
            var_matches = re.finditer(pattern, code)
            for match in var_matches:
                name = match.group(1)
                if name not in RUST_KEYWORDS and name not in name_map:
                    name_map[name] = gen_rust_name()
        
        # Struct and enum names
        struct_pattern = r'\b(struct|enum)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        struct_matches = re.finditer(struct_pattern, code)
        for match in struct_matches:
            name = match.group(2)
            if name not in RUST_KEYWORDS and name not in name_map:
                name_map[name] = gen_rust_name()
    
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
                return quote + encode_rust_string(content)[1:-1] + quote
            return match.group(0)
        
        # Match both double quoted strings
        obfuscated_code = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"', replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                return decompose_rust_number(num)
            except ValueError:
                return num_str
        
        obfuscated_code = re.sub(r'\b\d+\b', replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_rust_code()
        # Insert dummy code after use statements
        use_pattern = r'(use\s+[^;]+;\s*)+'
        if re.search(use_pattern, obfuscated_code):
            obfuscated_code = re.sub(use_pattern, r'\1\n' + dummy_code + '\n', obfuscated_code, count=1)
        else:
            obfuscated_code = dummy_code + '\n' + obfuscated_code
    
    # Obfuscate macros
    if options.get('obfuscate_macros', True):
        # Add dummy macros
        dummy_macros = '''
macro_rules! dummy_macro_1 {
    () => {
        (42 + 7)
    };
}

macro_rules! dummy_macro_2 {
    ($x:expr) => {
        $x * 2 / 2
    };
}
'''
        obfuscated_code = dummy_macros + '\n' + obfuscated_code
    
    return obfuscated_code, {
        'variables_renamed': len(name_map),
        'strings_encoded': len(string_map),
        'numbers_decomposed': len(re.findall(r'\b\d+\b', code)),
        'macros_added': 2
    }

def generate_dummy_rust_code():
    """Generate dummy Rust code to confuse analysis"""
    dummy_functions = [
        '''
fn dummy_calc_1() -> i32 {
    let x = (15 + 27) / 2;
    let y = x * 3 - 42;
    y ^ 0x1234
}
''',
        '''
fn dummy_loop_1() {
    for i in 0..(10 + 5) {
        let temp = i * (2 + 1);
        let _temp = temp / 3;
    }
}
''',
        '''
fn dummy_check_1() -> bool {
    let val = (100 >> 2) + 5;
    (val % 7) == 0
}
''',
        '''
struct DummyStruct {
    field1: i32,
    field2: String,
}

impl DummyStruct {
    fn new() -> Self {
        Self {
            field1: (42 * 2) / 2,
            field2: "dummy".to_string(),
        }
    }
}
'''
    ]
    
    return random.choice(dummy_functions)

def test_rust_obfuscation():
    """Test Rust obfuscation"""
    test_code = '''
use std::collections::HashMap;

struct DataProcessor {
    filename: String,
    data: Vec<String>,
}

impl DataProcessor {
    fn new(filename: &str) -> Self {
        Self {
            filename: filename.to_string(),
            data: Vec::new(),
        }
    }
    
    fn load_data(&mut self) -> Result<(), std::io::Error> {
        use std::fs::File;
        use std::io::{self, BufRead};
        
        let file = File::open(&self.filename)?;
        let reader = io::BufReader::new(file);
        
        for line in reader.lines() {
            let line = line?;
            if !line.trim().is_empty() {
                self.data.push(line);
            }
        }
        
        Ok(())
    }
    
    fn process_data(&self) -> Vec<String> {
        self.data
            .iter()
            .map(|line| line.trim().to_uppercase())
            .filter(|line| !line.is_empty())
            .collect()
    }
    
    fn get_data_count(&self) -> usize {
        self.data.len()
    }
}

fn main() {
    let mut processor = DataProcessor::new("input.txt");
    
    match processor.load_data() {
        Ok(()) => {
            let results = processor.process_data();
            println!("Processed {} lines", results.len());
        }
        Err(e) => {
            eprintln!("Failed to load data: {}", e);
        }
    }
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
    
    obfuscated, stats = obfuscate_rust_code(test_code, options)
    
    print("=== Rust Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_rust_obfuscation()
