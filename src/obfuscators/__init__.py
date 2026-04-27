"""
Obfuscators Package
Multi-language obfuscation modules
"""

from pathlib import Path

from .python import obfuscate_python_code, test_python_obfuscation
from .cpp import obfuscate_cpp_code, test_cpp_obfuscation
from .javascript import obfuscate_javascript_code, test_javascript_obfuscation
from .rust import obfuscate_rust_code, test_rust_obfuscation
from .c import obfuscate_c_code, test_c_obfuscation
from .java import obfuscate_java_code, test_java_obfuscation
from .go import obfuscate_go_code, test_go_obfuscation

# Language detection and routing
def obfuscate_code(code, language='python', options=None):
    """
    Route obfuscation to appropriate language module
    
    Args:
        code: Source code to obfuscate
        language: Target language ('python', 'cpp', 'javascript', 'rust', 'c', 'java', 'go')
        options: Obfuscation options dictionary
    
    Returns:
        tuple: (obfuscated_code, statistics)
    """
    language = language.lower()
    
    if language == 'python' or language == 'py':
        return obfuscate_python_code(code, options)
    elif language == 'cpp' or language == 'c++':
        return obfuscate_cpp_code(code, options)
    elif language == 'javascript' or language == 'js':
        return obfuscate_javascript_code(code, options)
    elif language == 'rust' or language == 'rs':
        return obfuscate_rust_code(code, options)
    elif language == 'c':
        return obfuscate_c_code(code, options)
    elif language == 'java':
        return obfuscate_java_code(code, options)
    elif language == 'go':
        return obfuscate_go_code(code, options)
    else:
        raise ValueError(f"Unsupported language: {language}")

def get_supported_languages():
    """Get list of supported languages"""
    return ['python', 'cpp', 'javascript', 'rust', 'c', 'java', 'go']

def get_language_extensions():
    """Get mapping of languages to file extensions"""
    return {
        'python': ['.py'],
        'cpp': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
        'javascript': ['.js', '.jsx', '.mjs'],
        'rust': ['.rs'],
        'c': ['.c', '.h'],
        'java': ['.java'],
        'go': ['.go']
    }

def detect_language_from_filename(filename):
    """Detect language from file extension"""
    ext = Path(filename).suffix.lower()
    
    for lang, extensions in get_language_extensions().items():
        if ext in extensions:
            return lang
    
    return 'python'  # Default fallback

def run_all_tests():
    """Run obfuscation tests for all languages"""
    print("=== Running All Obfuscation Tests ===")
    
    print("\n1. Python Obfuscation Test:")
    test_python_obfuscation()
    
    print("\n2. C++ Obfuscation Test:")
    test_cpp_obfuscation()
    
    print("\n3. JavaScript Obfuscation Test:")
    test_javascript_obfuscation()
    
    print("\n4. Rust Obfuscation Test:")
    test_rust_obfuscation()
    
    print("\n5. C Obfuscation Test:")
    test_c_obfuscation()
    
    print("\n6. Java Obfuscation Test:")
    test_java_obfuscation()
    
    print("\n7. Go Obfuscation Test:")
    test_go_obfuscation()
    
    print("\n=== All Tests Complete ===")

if __name__ == "__main__":
    run_all_tests()
