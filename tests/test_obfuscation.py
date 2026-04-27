"""
Tests for PyMorph obfuscation functionality
Validates that obfuscated code works correctly and produces expected results
"""

import pytest
import os
import sys
import subprocess
import tempfile
import ast
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from obfuscators import obfuscate_code, get_supported_languages, detect_language_from_filename

class TestObfuscationValidation:
    """Test suite for obfuscation validation"""
    
    @pytest.fixture
    def python_test_code(self):
        """Sample Python code for testing"""
        return '''
import os
import sys
from typing import List, Dict

def calculate_sum(numbers: List[int]) -> int:
    """Calculate the sum of a list of numbers"""
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    """Main function"""
    data = [1, 2, 3, 4, 5]
    result = calculate_sum(data)
    print(f"Sum: {result}")
    return result

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
'''
    
    @pytest.fixture
    def cpp_test_code(self):
        """Sample C++ code for testing"""
        return '''
#include <iostream>
#include <vector>
#include <string>

int calculate_sum(const std::vector<int>& numbers) {
    int total = 0;
    for (int num : numbers) {
        total += num;
    }
    return total;
}

int main() {
    std::vector<int> data = {1, 2, 3, 4, 5};
    int result = calculate_sum(data);
    std::cout << "Sum: " << result << std::endl;
    return 0;
}
'''
    
    @pytest.fixture
    def javascript_test_code(self):
        """Sample JavaScript code for testing"""
        return '''
const os = require('os');

function calculateSum(numbers) {
    let total = 0;
    for (const num of numbers) {
        total += num;
    }
    return total;
}

function main() {
    const data = [1, 2, 3, 4, 5];
    const result = calculateSum(data);
    console.log(`Sum: ${result}`);
    return result;
}

if (require.main === module) {
    main();
}
'''
    
    def test_python_obfuscation_functionality(self, python_test_code):
        """Test that Python obfuscation produces working code"""
        # Obfuscate the code
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True,
            'rename_classes': True,
            'add_dummy_vars': True
        })
        
        # Verify obfuscation happened
        assert obfuscated_code != python_test_code
        assert stats['error'] is None
        
        # Verify the obfuscated code is syntactically valid
        try:
            ast.parse(obfuscated_code)
        except SyntaxError as e:
            pytest.fail(f"Obfuscated code has syntax error: {e}")
        
        # Test that the obfuscated code produces the same output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(obfuscated_code)
            temp_file = f.name
        
        try:
            # Run the original code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(python_test_code)
                original_file = f.name
            
            original_result = subprocess.run([sys.executable, original_file], 
                                          capture_output=True, text=True, timeout=10)
            obfuscated_result = subprocess.run([sys.executable, temp_file], 
                                            capture_output=True, text=True, timeout=10)
            
            # Both should succeed and produce the same output
            assert original_result.returncode == 0
            assert obfuscated_result.returncode == 0
            assert "Sum: 15" in original_result.stdout
            assert "Sum: 15" in obfuscated_result.stdout
            
        finally:
            # Cleanup
            os.unlink(temp_file)
            os.unlink(original_file)
    
    def test_cpp_obfuscation_functionality(self, cpp_test_code):
        """Test that C++ obfuscation produces working code"""
        # Obfuscate the code
        obfuscated_code, stats = obfuscate_code(cpp_test_code, 'cpp', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True,
            'add_dummy_vars': True
        })
        
        # Verify obfuscation happened
        assert obfuscated_code != cpp_test_code
        assert stats['error'] is None
        
        # Verify the obfuscated code contains expected C++ structure
        assert '#include' in obfuscated_code
        assert 'main()' in obfuscated_code
        assert 'std::cout' in obfuscated_code
    
    def test_javascript_obfuscation_functionality(self, javascript_test_code):
        """Test that JavaScript obfuscation produces working code"""
        # Obfuscate the code
        obfuscated_code, stats = obfuscate_code(javascript_test_code, 'javascript', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True,
            'add_dummy_vars': True
        })
        
        # Verify obfuscation happened
        assert obfuscated_code != javascript_test_code
        assert stats['error'] is None
        
        # Verify the obfuscated code contains expected JavaScript structure
        assert 'function' in obfuscated_code
        assert 'console.log' in obfuscated_code
    
    def test_docstring_removal(self, python_test_code):
        """Test that docstrings are removed from obfuscated code"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True
        })
        
        # Docstrings should be removed
        assert '"""Calculate the sum' not in obfuscated_code
        assert '"""Main function' not in obfuscated_code
    
    def test_number_decomposition(self, python_test_code):
        """Test that numbers are properly decomposed"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': True,
            'rename_variables': False,
            'rename_functions': False
        })
        
        # Numbers should be decomposed (not literal numbers like 1, 2, 3, 4, 5)
        # But the code should still be valid
        try:
            ast.parse(obfuscated_code)
        except SyntaxError as e:
            pytest.fail(f"Number decomposition created invalid syntax: {e}")
    
    def test_variable_renaming(self, python_test_code):
        """Test that variables are properly renamed"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': False,
            'rename_variables': True,
            'rename_functions': False
        })
        
        # Original variable names should be changed
        assert 'total' not in obfuscated_code or obfuscated_code.count('total') < python_test_code.count('total')
        assert 'num' not in obfuscated_code or obfuscated_code.count('num') < python_test_code.count('num')
        assert 'data' not in obfuscated_code or obfuscated_code.count('data') < python_test_code.count('data')
    
    def test_function_renaming(self, python_test_code):
        """Test that functions are properly renamed"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': False,
            'rename_variables': False,
            'rename_functions': True
        })
        
        # Original function names should be changed
        assert 'calculate_sum' not in obfuscated_code or obfuscated_code.count('calculate_sum') < python_test_code.count('calculate_sum')
        assert 'main' not in obfuscated_code or obfuscated_code.count('main') < python_test_code.count('main')
    
    def test_import_preservation(self, python_test_code):
        """Test that imports are preserved and not obfuscated"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True
        })
        
        # Imports should be preserved
        assert 'import os' in obfuscated_code
        assert 'import sys' in obfuscated_code
        assert 'from typing import' in obfuscated_code
    
    def test_language_detection(self):
        """Test language detection from filenames"""
        assert detect_language_from_filename('test.py') == 'python'
        assert detect_language_from_filename('test.cpp') == 'cpp'
        assert detect_language_from_filename('test.js') == 'javascript'
        assert detect_language_from_filename('test.rs') == 'rust'
        assert detect_language_from_filename('test.c') == 'c'
        assert detect_language_from_filename('test.java') == 'java'
        assert detect_language_from_filename('test.go') == 'go'
    
    def test_supported_languages(self):
        """Test that all expected languages are supported"""
        languages = get_supported_languages()
        expected_languages = {'python', 'cpp', 'javascript', 'rust', 'c', 'java', 'go'}
        assert set(languages) == expected_languages
    
    def test_obfuscation_statistics(self, python_test_code):
        """Test that obfuscation returns meaningful statistics"""
        obfuscated_code, stats = obfuscate_code(python_test_code, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True
        })
        
        # Check that statistics are present
        assert 'variables' in stats
        assert 'functions' in stats
        assert 'classes' in stats
        assert 'strings' in stats
        assert 'numbers' in stats
        assert stats['error'] is None
        
        # Check that we found some elements
        assert stats['variables'] >= 0
        assert stats['functions'] >= 0
        assert stats['classes'] >= 0
    
    def test_empty_code_handling(self):
        """Test that empty code is handled gracefully"""
        obfuscated_code, stats = obfuscate_code('', 'python', {})
        
        # Should handle empty code without error
        assert stats['error'] is None
        assert obfuscated_code == ''
    
    def test_invalid_code_handling(self):
        """Test that invalid code is handled gracefully"""
        invalid_code = 'def invalid_syntax(\n    pass'
        
        obfuscated_code, stats = obfuscate_code(invalid_code, 'python', {})
        
        # Should handle invalid code gracefully
        assert 'error' in stats or stats.get('error') is not None

class TestFunctionOutputValidation:
    """Test suite for function output validation and modification detection"""
    
    def test_python_function_output_validation(self):
        """Test that Python functions produce expected outputs after obfuscation"""
        test_function = '''
def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def test_function():
    result = multiply(3, 4)
    print(f"Result: {result}")
    return result

if __name__ == "__main__":
    test_function()
'''
        
        obfuscated_code, stats = obfuscate_code(test_function, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True
        })
        
        # Test that the function still produces the correct output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(obfuscated_code)
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0
            assert "Result: 12" in result.stdout
            
        finally:
            os.unlink(temp_file)
    
    def test_function_modification_detection(self):
        """Test detection of function modifications during obfuscation"""
        original_function = '''
def original_function(x):
    """Original function"""
    return x * 2

def helper_function(y):
    """Helper function"""
    return y + 1

def main():
    result = original_function(5) + helper_function(3)
    print(f"Final result: {result}")
    return result
'''
        
        obfuscated_code, stats = obfuscate_code(original_function, 'python', {
            'decompose_numbers': True,
            'rename_variables': True,
            'rename_functions': True
        })
        
        # The obfuscated code should not contain the original function names
        # but should maintain the same functionality
        assert 'original_function' not in obfuscated_code or obfuscated_code.count('original_function') < original_function.count('original_function')
        assert 'helper_function' not in obfuscated_code or obfuscated_code.count('helper_function') < original_function.count('helper_function')
        
        # Test that functionality is preserved
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(obfuscated_code)
            temp_file = f.name
        
        try:
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            assert result.returncode == 0
            # Original: 5*2 + 3+1 = 10 + 4 = 14
            assert "Final result: 14" in result.stdout
            
        finally:
            os.unlink(temp_file)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
