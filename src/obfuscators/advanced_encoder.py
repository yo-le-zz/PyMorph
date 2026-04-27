"""
Advanced String Encoder Module
Multi-layer encoding for maximum obfuscation
"""

import base64
import random
import string
import hashlib
import zlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

class AdvancedEncoder:
    """Advanced multi-layer string encoder"""
    
    def __init__(self):
        self.encoding_methods = [
            self.base64_double_encode,
            self.base64_hex_encode,
            self.zlib_base64_encode,
            self.xor_encode,
            self.aes_encode,
            self.unicode_mixed_encode,
            self.json_encoded_encode,
            self.hash_based_encode
        ]
    
    def generate_key(self, length=16):
        """Generate random encryption key"""
        return secrets.token_bytes(length)
    
    def base64_double_encode(self, text):
        """Double base64 encoding"""
        encoded = base64.b64encode(text.encode('utf-8'))
        encoded = base64.b64encode(encoded)
        return encoded.decode('utf-8')
    
    def base64_hex_encode(self, text):
        """Base64 + Hex encoding"""
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        hex_encoded = encoded.encode('utf-8').hex()
        return hex_encoded
    
    def zlib_base64_encode(self, text):
        """Zlib compression + Base64"""
        compressed = zlib.compress(text.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        return encoded
    
    def xor_encode(self, text):
        """XOR encoding with random key"""
        key = secrets.randbits(8)
        encoded_bytes = bytearray()
        for char in text.encode('utf-8'):
            encoded_bytes.append(char ^ key)
        encoded = base64.b64encode(encoded_bytes).decode('utf-8')
        return f"{key}:{encoded}"
    
    def aes_encode(self, text):
        """AES encryption encoding"""
        key = self.generate_key()
        cipher = AES.new(key, AES.MODE_CBC)
        padded_text = pad(text.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_text)
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        encrypted_data = base64.b64encode(encrypted).decode('utf-8')
        key_b64 = base64.b64encode(key).decode('utf-8')
        return f"{iv}:{key_b64}:{encrypted_data}"
    
    def unicode_mixed_encode(self, text):
        """Mixed Unicode escape sequences"""
        encoded_chars = []
        for char in text:
            if random.random() < 0.3:
                encoded_chars.append(f'\\u{ord(char):04x}')
            elif random.random() < 0.6:
                encoded_chars.append(f'\\x{ord(char):02x}')
            else:
                encoded_chars.append(char)
        return ''.join(encoded_chars)
    
    def json_encoded_encode(self, text):
        """JSON encoding with obfuscation"""
        # Create complex JSON structure
        data = {
            'data': text,
            'meta': {
                'type': 'string',
                'encoding': 'json',
                'random': random.randint(1000, 9999)
            },
            'nested': {
                'payload': text,
                'checksum': hashlib.md5(text.encode()).hexdigest()[:8]
            }
        }
        json_str = json.dumps(data, separators=(',', ':'))
        return base64.b64encode(json_str.encode()).decode()
    
    def hash_based_encode(self, text):
        """Hash-based encoding with salt"""
        salt = secrets.token_hex(8)
        combined = text + salt
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        return f"{salt}:{hashed}"
    
    def multi_layer_encode(self, text, layers=3):
        """Apply multiple encoding layers"""
        encoded = text
        methods_used = []
        
        for _ in range(layers):
            method = random.choice(self.encoding_methods)
            encoded = method(encoded)
            methods_used.append(method.__name__)
        
        return encoded, methods_used
    
    def create_decoder_function(self, methods_used, language='python'):
        """Generate decoder function based on methods used"""
        if language == 'python':
            return self._create_python_decoder(methods_used)
        elif language == 'javascript':
            return self._create_javascript_decoder(methods_used)
        elif language == 'cpp':
            return self._create_cpp_decoder(methods_used)
        else:
            return ""
    
    def _create_python_decoder(self, methods_used):
        """Create Python decoder function"""
        decoder_code = '''
import base64
import zlib
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def advanced_decoder(encoded_str, method_index):
    """Multi-layer decoder function"""
    try:
        if method_index == 0:  # base64_double_encode
            decoded = base64.b64decode(base64.b64decode(encoded_str)).decode('utf-8')
        elif method_index == 1:  # base64_hex_encode
            hex_decoded = bytes.fromhex(encoded_str)
            decoded = base64.b64decode(hex_decoded).decode('utf-8')
        elif method_index == 2:  # zlib_base64_encode
            compressed = base64.b64decode(encoded_str)
            decoded = zlib.decompress(compressed).decode('utf-8')
        elif method_index == 3:  # xor_encode
            parts = encoded_str.split(':')
            if len(parts) >= 2:
                key = int(parts[0])
                encoded_data = base64.b64decode(parts[1])
                decoded_bytes = bytearray()
                for byte in encoded_data:
                    decoded_bytes.append(byte ^ key)
                decoded = decoded_bytes.decode('utf-8')
            else:
                decoded = encoded_str
        elif method_index == 4:  # aes_encode
            parts = encoded_str.split(':')
            if len(parts) >= 3:
                iv = base64.b64decode(parts[0])
                key = base64.b64decode(parts[1])
                encrypted_data = base64.b64decode(parts[2])
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                decoded = decrypted.decode('utf-8')
            else:
                decoded = encoded_str
        elif method_index == 5:  # unicode_mixed_encode
            decoded = encoded_str.encode().decode('unicode_escape')
        elif method_index == 6:  # json_encoded_encode
            json_str = base64.b64decode(encoded_str).decode('utf-8')
            data = json.loads(json_str)
            decoded = data['data']
        elif method_index == 7:  # hash_based_encode
            parts = encoded_str.split(':')
            if len(parts) >= 2:
                decoded = parts[0]  # Return original salt (simplified)
            else:
                decoded = encoded_str
        else:
            decoded = encoded_str
        return decoded
    except Exception:
        return encoded_str

def decode_string(encoded_str, methods):
    """Decode string using multiple methods"""
    decoded = encoded_str
    for i, method in enumerate(methods):
        method_name = method.replace('encode', 'decode')
        if method_name == 'base64_double_decode':
            decoded = base64.b64decode(base64.b64decode(decoded)).decode('utf-8')
        elif method_name == 'base64_hex_decode':
            hex_decoded = bytes.fromhex(decoded)
            decoded = base64.b64decode(hex_decoded).decode('utf-8')
        elif method_name == 'zlib_base64_decode':
            compressed = base64.b64decode(decoded)
            decoded = zlib.decompress(compressed).decode('utf-8')
        elif method_name == 'xor_decode':
            parts = decoded.split(':')
            if len(parts) >= 2:
                key = int(parts[0])
                encoded_data = base64.b64decode(parts[1])
                decoded_bytes = bytearray()
                for byte in encoded_data:
                    decoded_bytes.append(byte ^ key)
                decoded = decoded_bytes.decode('utf-8')
        elif method_name == 'aes_decode':
            parts = decoded.split(':')
            if len(parts) >= 3:
                iv = base64.b64decode(parts[0])
                key = base64.b64decode(parts[1])
                encrypted_data = base64.b64decode(parts[2])
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
                decoded = decrypted.decode('utf-8')
        elif method_name == 'unicode_mixed_decode':
            decoded = decoded.encode().decode('unicode_escape')
        elif method_name == 'json_encoded_decode':
            json_str = base64.b64decode(decoded).decode('utf-8')
            data = json.loads(json_str)
            decoded = data['data']
        elif method_name == 'hash_based_decode':
            parts = decoded.split(':')
            if len(parts) >= 2:
                decoded = parts[0]
    return decoded
'''
        return decoder_code
    
    def _create_javascript_decoder(self, methods_used):
        """Create JavaScript decoder function"""
        decoder_code = '''
function advancedDecoder(encodedStr, methodIndex) {
    try {
        if (methodIndex === 0) { // base64_double_encode
            return atob(atob(encodedStr));
        } else if (methodIndex === 1) { // base64_hex_encode
            const hexDecoded = hexToBytes(encodedStr);
            return atob(btoa(String.fromCharCode(...hexDecoded)));
        } else if (methodIndex === 2) { // zlib_base64_encode
            // Simplified - would need pako.js for real zlib
            return atob(encodedStr);
        } else if (methodIndex === 3) { // xor_encode
            const parts = encodedStr.split(':');
            if (parts.length >= 2) {
                const key = parseInt(parts[0]);
                const encodedData = atob(parts[1]);
                let decoded = '';
                for (let i = 0; i < encodedData.length; i++) {
                    decoded += String.fromCharCode(encodedData.charCodeAt(i) ^ key);
                }
                return decoded;
            }
        } else if (methodIndex === 5) { // unicode_mixed_encode
            return unescape(encodedStr);
        } else if (methodIndex === 6) { // json_encoded_encode
            const jsonStr = atob(encodedStr);
            const data = JSON.parse(jsonStr);
            return data.data;
        }
        return encodedStr;
    } catch (e) {
        return encodedStr;
    }
}

function hexToBytes(hex) {
    const bytes = [];
    for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
    }
    return bytes;
}
'''
        return decoder_code
    
    def _create_cpp_decoder(self, methods_used):
        """Create C++ decoder function"""
        decoder_code = '''
#include <string>
#include <sstream>
#include <vector>
#include <iomanip>
#include <openssl/evp.h>
#include <openssl/aes.h>

std::string advancedDecoder(const std::string& encodedStr, int methodIndex) {
    try {
        if (methodIndex == 0) { // base64_double_encode
            // Simplified base64 decode
            return decodeBase64(decodeBase64(encodedStr));
        } else if (methodIndex == 1) { // base64_hex_encode
            std::string hexDecoded = hexToString(encodedStr);
            return decodeBase64(hexDecoded);
        } else if (methodIndex == 3) { // xor_encode
            size_t colonPos = encodedStr.find(':');
            if (colonPos != std::string::npos) {
                int key = std::stoi(encodedStr.substr(0, colonPos));
                std::string encodedData = decodeBase64(encodedStr.substr(colonPos + 1));
                std::string decoded;
                for (char c : encodedData) {
                    decoded += c ^ key;
                }
                return decoded;
            }
        }
        return encodedStr;
    } catch (...) {
        return encodedStr;
    }
}

std::string decodeBase64(const std::string& encoded) {
    // Base64 decoding implementation
    static const std::string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    std::string decoded;
    std::vector<int> T(256, -1);
    for (int i = 0; i < 64; i++) T[chars[i]] = i;
    
    int val = 0, valb = -8;
    for (unsigned char c : encoded) {
        if (T[c] == -1) break;
        val = (val << 6) + T[c];
        valb += 6;
        if (valb >= 0) {
            decoded.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }
    }
    return decoded;
}

std::string hexToString(const std::string& hex) {
    std::string result;
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byteString = hex.substr(i, 2);
        char byte = static_cast<char>(strtol(byteString.c_str(), NULL, 16));
        result.push_back(byte);
    }
    return result;
}
'''
        return decoder_code

# Global encoder instance
encoder = AdvancedEncoder()

def encode_string_advanced(text, layers=3):
    """Encode string with advanced multi-layer techniques"""
    return encoder.multi_layer_encode(text, layers)

def create_decoder(methods_used, language='python'):
    """Create decoder function for specified language"""
    return encoder.create_decoder_function(methods_used, language)

def test_advanced_encoding():
    """Test advanced encoding methods"""
    test_strings = [
        "Hello, World!",
        "This is a test string",
        "PyMorph Obfuscator",
        "Advanced Encoding 123!"
    ]
    
    print("=== Advanced Encoding Test ===")
    for test_str in test_strings:
        encoded, methods = encode_string_advanced(test_str, layers=2)
        print(f"\nOriginal: {test_str}")
        print(f"Methods: {methods}")
        print(f"Encoded: {encoded[:100]}...")
        
        # Create decoder
        decoder = create_decoder(methods, 'python')
        print(f"Decoder created: {len(decoder)} characters")

if __name__ == "__main__":
    test_advanced_encoding()
