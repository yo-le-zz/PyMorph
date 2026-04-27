"""
JavaScript Obfuscator Module
Advanced obfuscation techniques for JavaScript code
"""

import re
import random
import string
import json

# JavaScript keywords and protected names - Expanded for maximum compatibility
JS_KEYWORDS = {
    'var', 'let', 'const', 'function', 'return', 'if', 'else', 'while', 'for', 'do',
    'switch', 'case', 'break', 'continue', 'goto', 'typeof', 'instanceof', 'new', 'delete',
    'this', 'try', 'catch', 'finally', 'throw', 'class', 'extends', 'super', 'static',
    'import', 'export', 'default', 'async', 'await', 'yield', 'of', 'in', 'void', 'debugger',
    'true', 'false', 'null', 'undefined', 'NaN', 'Infinity', 'Object', 'Array', 'String',
    'Number', 'Boolean', 'Date', 'RegExp', 'Math', 'JSON', 'console', 'document', 'window',
    'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'alert', 'confirm', 'prompt',
    'require', 'os', 'fs', 'path', 'process', 'Buffer', 'module', 'exports', '__dirname', '__filename',
    # Node.js built-ins
    'events', 'EventEmitter', 'Stream', 'Readable', 'Writable', 'Duplex', 'Transform', 'PassThrough',
    'util', 'inherits', 'inspect', 'format', 'deprecate', 'callbackify', 'promisify', 'debuglog',
    'child_process', 'spawn', 'exec', 'execFile', 'fork', 'cluster', 'worker', 'isMaster', 'isWorker',
    'net', 'Server', 'Socket', 'createConnection', 'connect', 'createServer', 'isIP', 'isIPv4', 'isIPv6',
    'dns', 'lookup', 'resolve', 'reverse', 'resolveMx', 'resolveTxt', 'resolveSrv', 'resolveNs', 'resolveCname',
    'resolveAny', 'setServers', 'getServers', 'http', 'createServer', 'request', 'get', 'Agent', 'ClientRequest',
    'ServerResponse', 'IncomingMessage', 'https', 'createServer', 'request', 'get', 'Agent', 'ClientRequest',
    'url', 'parse', 'resolve', 'format', 'resolveObject', 'URL', 'URLSearchParams', 'domain', 'punycode',
    'querystring', 'escape', 'unescape', 'stringify', 'parse', 'readline', 'createInterface', 'cursorTo',
    'moveCursor', 'clearLine', 'clearScreenDown', 'createInterface', 'tty', 'isatty', 'setRawMode', 'ReadStream',
    'WriteStream', 'zlib', 'createGzip', 'createGunzip', 'createDeflate', 'createInflate', 'createDeflateRaw',
    'createInflateRaw', 'gzip', 'gunzip', 'deflate', 'inflate', 'deflateRaw', 'inflateRaw', 'unzip', 'constants',
    'fs', 'access', 'appendFile', 'chmod', 'chown', 'close', 'copyFile', 'createReadStream', 'createWriteStream',
    'exists', 'fchmod', 'fchown', 'fdatasync', 'fstat', 'fsync', 'ftruncate', 'futimes', 'lchmod', 'lchown',
    'link', 'lstat', 'mkdir', 'mkdtemp', 'open', 'read', 'readFile', 'readdir', 'readlink', 'realpath',
    'rename', 'rmdir', 'stat', 'symlink', 'truncate', 'unlink', 'utimes', 'write', 'writeFile',
    'path', 'normalize', 'join', 'resolve', 'isAbsolute', 'relative', 'dirname', 'basename', 'extname',
    'parse', 'format', 'sep', 'delimiter', 'win32', 'posix', 'crypto', 'createHash', 'createHmac',
    'createCipher', 'createDecipher', 'createCipheriv', 'createDecipheriv', 'createSign', 'createVerify',
    'createDiffieHellman', 'pbkdf2', 'randomBytes', 'pseudoRandomBytes', 'scrypt', 'timingSafeEqual',
    'getHashes', 'getCiphers', 'getCiphers', 'getCurves', 'getDiffieHellman', 'constants', 'DEFAULT_ENCODING',
    # Browser APIs
    'localStorage', 'sessionStorage', 'indexedDB', 'IDBDatabase', 'IDBObjectStore', 'IDBIndex',
    'IDBTransaction', 'IDBRequest', 'IDBCursor', 'fetch', 'Response', 'Request', 'Headers',
    'FormData', 'URL', 'URLSearchParams', 'Blob', 'File', 'FileReader', 'ArrayBuffer', 'DataView',
    'TypedArray', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray', 'Int16Array', 'Uint16Array',
    'Int32Array', 'Uint32Array', 'Float32Array', 'Float64Array', 'BigInt64Array', 'BigUint64Array',
    'Map', 'Set', 'WeakMap', 'WeakSet', 'Proxy', 'Reflect', 'Symbol', 'Promise', 'Generator',
    'GeneratorFunction', 'AsyncFunction', 'AsyncGenerator', 'AsyncGeneratorFunction', 'WebAssembly',
    'WebAssembly', 'Instance', 'Module', 'Memory', 'Table', 'CompileError', 'LinkError', 'RuntimeError',
    'Worker', 'SharedWorker', 'ServiceWorker', 'MessagePort', 'MessageChannel', 'MessageEvent',
    'BroadcastChannel', 'Performance', 'PerformanceEntry', 'PerformanceMark', 'PerformanceMeasure',
    'PerformanceNavigation', 'PerformanceResourceTiming', 'PerformanceObserver', 'PerformanceObserverEntryList',
    'Geolocation', 'Position', 'Coordinates', 'Navigator', 'MediaDevices', 'MediaStream', 'MediaStreamTrack',
    'getUserMedia', 'RTCPeerConnection', 'RTCDataChannel', 'RTCIceCandidate', 'RTCSessionDescription',
    'WebSocket', 'EventSource', 'Notification', 'PaymentRequest', 'PaymentResponse', 'PaymentMethodChangeEvent',
    'PaymentAddress', 'PaymentCompletion', 'Credential', 'CredentialsContainer', 'FederatedCredential',
    'PasswordCredential', 'PublicKeyCredential', 'AuthenticatorResponse', 'AuthenticatorAttestationResponse',
    'AuthenticatorAssertionResponse', 'PublicKeyCredentialWithAttestation', 'PublicKeyCredentialWithAssertion',
    'WebGL', 'WebGLRenderingContext', 'WebGL2RenderingContext', 'WebGLBuffer', 'WebGLFramebuffer',
    'WebGLProgram', 'WebGLRenderbuffer', 'WebGLShader', 'WebGLShaderPrecisionFormat', 'WebGLTexture',
    'WebGLUniformLocation', 'WebGLActiveInfo', 'WebGLContextEvent', 'CanvasRenderingContext2D',
    'CanvasGradient', 'CanvasPattern', 'ImageBitmap', 'ImageData', 'Path2D', 'TextMetrics',
    'Transform', 'DOMMatrix', 'DOMMatrixReadOnly', 'DOMPoint', 'DOMPointReadOnly', 'DOMRect',
    'DOMRectReadOnly', 'DOMQuad', 'SVG', 'SVGElement', 'SVGSVGElement', 'SVGGraphicsElement',
    'SVGGeometryElement', 'SVGPathElement', 'SVGTextElement', 'SVGTSpanElement', 'SVGImageElement',
    'SVGSwitchElement', 'SVGUseElement', 'SVGSymbolElement', 'SVGDefsElement', 'SVGDescElement',
    'SVGMetadataElement', 'SVGTitleElement', 'SVGScriptElement', 'SVGStyleElement', 'SVGAnchorElement',
    'SVGViewElement', 'SVGMPathElement', 'SVGAnimateElement', 'SVGAnimateMotionElement', 'SVGAnimateTransformElement',
    'SVGSetElement', 'SVGAnimateColorElement', 'SVGFilterElement', 'SVGFEBlendElement', 'SVGFEColorMatrixElement',
    'SVGFEComponentTransferElement', 'SVGFECompositeElement', 'SVGFEConvolveMatrixElement',
    'SVGFEDiffuseLightingElement', 'SVGFEDisplacementMapElement', 'SVGFEDistantLightElement',
    'SVGFEDropShadowElement', 'SVGFEFloodElement', 'SVGFEGaussianBlurElement', 'SVGFEImageElement',
    'SVGFEMergeElement', 'SVGFEMergeNodeElement', 'SVGFEMorphologyElement', 'SVGFEOffsetElement',
    'SVGFEPointLightElement', 'SVGFESpecularLightingElement', 'SVGFESpotLightElement', 'SVGFETileElement',
    'SVGFETurbulenceElement', 'SVGClipPathElement', 'SVGMaskElement', 'SVGPatternElement',
    'SVGMarkerElement', 'SVGLinearGradientElement', 'SVGRadialGradientElement', 'SVGStopElement',
    'SVGForeignObjectElement', 'SVGCursorElement', 'SVGAElement', 'SVGTextPathElement', 'SVGFontElement',
    'SVGGlyphElement', 'SVGHKernElement', 'SVGVKernElement', 'SVGFontFaceElement', 'SVGFontFaceSrcElement',
    'SVGFontFaceUriElement', 'SVGFontFaceFormatElement', 'SVGFontFaceNameElement', 'SVGMissingGlyphElement',
    'SVGTRefElement', 'SVGAltGlyphDefElement', 'SVGAltGlyphItemElement', 'SVGAltGlyphElement',
    'SVGTextContentElement', 'SVGTextPositioningElement', 'SVGTextElement', 'SVGTSpanElement',
    'SVGTextPathElement', 'SVGAltGlyphDefElement', 'SVGAltGlyphItemElement', 'SVGAltGlyphElement',
    'SVGTextContentElement', 'SVGTextPositioningElement', 'SVGTextElement', 'SVGTSpanElement',
    # React
    'React', 'Component', 'PureComponent', 'Fragment', 'StrictMode', 'Suspense', 'SuspenseList',
    'useState', 'useEffect', 'useContext', 'useReducer', 'useCallback', 'useMemo', 'useRef',
    'useImperativeHandle', 'useLayoutEffect', 'useDebugValue', 'useTransition', 'useDeferredValue',
    'useId', 'forwardRef', 'memo', 'createContext', 'createRef', 'createElement', 'cloneElement',
    'isValidElement', 'Children', 'render', 'hydrate', 'unmountComponentAtNode', 'findDOMNode',
    'createPortal', 'flushSync', 'batchedUpdates', 'unstable_batchedUpdates', 'unstable_renderSubtreeIntoContainer',
    'unstable_createPortal', 'unstable_getCurrentPriorityLevel', 'unstable_runWithPriority',
    'unstable_scheduleCallback', 'unstable_cancelCallback', 'unstable_wrapCallback',
    'unstable_getCurrentFiber', 'unstable_getFiberCurrentOwner', 'unstable_isFiberScheduled',
    'unstable_flushDiscreteUpdates', 'unstable_flushControl', 'unstable_startTransition',
    'unstable_getCacheForType', 'unstable_getCacheForType', 'unstable_getCacheForType',
    # Vue
    'Vue', 'createApp', 'createSSRApp', 'defineComponent', 'defineAsyncComponent', 'defineCustomElement',
    'ref', 'reactive', 'computed', 'watch', 'watchEffect', 'onMounted', 'onUnmounted', 'onUpdated',
    'onBeforeMount', 'onBeforeUnmount', 'onBeforeUpdate', 'onErrorCaptured', 'onRenderTracked',
    'onRenderTriggered', 'onActivated', 'onDeactivated', 'onServerPrefetch', 'provide', 'inject',
    'nextTick', 'useCssModule', 'useCssVars', 'useSlots', 'useAttrs', 'useSSRContext', 'useTransitionState',
    'useHydrationStore', 'useRoute', 'useRouter', 'useLink', 'useStore', 'usePinia', 'createPinia',
    'defineStore', 'storeToRefs', 'acceptHMRUpdate', 'createNamespacedHelpers', 'mapState',
    'mapGetters', 'mapActions', 'mapMutations', 'createNamespacedHelpers', 'createLogger',
    'createPersistedState', 'createSharedMutations', 'createUndoState', 'createSync',
    # Angular
    'angular', 'Component', 'Directive', 'Injectable', 'NgModule', 'Input', 'Output', 'HostListener',
    'HostBinding', 'ContentChild', 'ContentChildren', 'ViewChild', 'ViewChildren', 'ElementRef',
    'Renderer2', 'ChangeDetectorRef', 'ApplicationRef', 'NgZone', 'Injector', 'TemplateRef',
    'ViewContainerRef', 'EmbeddedViewRef', 'ComponentRef', 'NgModuleRef', 'ComponentFactoryResolver',
    'ComponentFactory', 'ComponentRef', 'NgModuleFactory', 'NgModuleRef', 'ModuleWithComponentFactories',
    'SystemJsNgModuleLoader', 'Compiler', 'CompilerFactory', 'ModuleWithProviders', 'ModuleWithProviders',
    'Type', 'InjectionToken', 'OpaqueToken', 'forwardRef', 'Inject', 'Optional', 'Self', 'SkipSelf',
    'Host', 'Attribute', 'ContentChild', 'ContentChildren', 'ViewChild', 'ViewChildren', 'Query',
    'QueryList', 'IterableDiffer', 'IterableDiffers', 'KeyValueDiffer', 'KeyValueDiffers',
    'DefaultIterableDiffer', 'CollectionChangeRecord', 'KeyValueChangeRecord', 'IterableChanges',
    'KeyValueChanges', 'PipeTransform', 'Pipe', 'OnInit', 'OnDestroy', 'OnChanges', 'DoCheck',
    'AfterContentInit', 'AfterContentChecked', 'AfterViewInit', 'AfterViewChecked',
    'CanActivate', 'CanActivateChild', 'CanDeactivate', 'CanLoad', 'Resolve', 'CanActivate',
    'CanActivateChild', 'CanDeactivate', 'CanLoad', 'Resolve', 'Route', 'Router', 'ActivatedRoute',
    'RouterState', 'RouterEvent', 'NavigationStart', 'NavigationEnd', 'NavigationCancel',
    'NavigationError', 'RoutesRecognized', 'GuardsCheckStart', 'GuardsCheckEnd', 'ResolveStart',
    'ResolveEnd', 'RouteConfigLoadStart', 'RouteConfigLoadEnd', 'ChildActivationStart',
    'ChildActivationEnd', 'ActivationStart', 'ActivationEnd', 'Scroll', 'Navigation',
    'NavigationExtras', 'NavigationBehaviorOptions', 'DefaultUrlSerializer', 'UrlSerializer',
    'UrlTree', 'UrlSegment', 'UrlSegmentGroup', 'UrlHandlingStrategy', 'PreloadingStrategy',
    'PreloadAllModules', 'NoPreloading', 'PreloadSelectedModules', 'RouterPreloader',
    'RouterLink', 'RouterLinkWithHref', 'RouterOutlet', 'ActivatedRoute', 'ActivatedRouteSnapshot',
    'RouterStateSnapshot', 'ParamMap', 'Data', 'RouteConfigLoadEnd', 'RouteConfigLoadStart',
    'Router', 'RouterLink', 'RouterLinkWithHref', 'RouterOutlet', 'Routes', 'RouterState',
    'RouterStateSnapshot', 'UrlTree', 'UrlSegmentGroup', 'UrlSegment', 'ParamMap', 'Data',
    'Route', 'ActivatedRoute', 'ActivatedRouteSnapshot', 'RouterStateSnapshot', 'ParamMap',
    'Data', 'RouteConfigLoadEnd', 'RouteConfigLoadStart', 'Router', 'RouterLink',
    'RouterLinkWithHref', 'RouterOutlet', 'Routes', 'RouterState', 'RouterStateSnapshot',
    'UrlTree', 'UrlSegmentGroup', 'UrlSegment', 'ParamMap', 'Data', 'Route', 'ActivatedRoute',
    'ActivatedRouteSnapshot', 'RouterStateSnapshot', 'ParamMap', 'Data', 'RouteConfigLoadEnd',
    'RouteConfigLoadStart', 'Router', 'RouterLink', 'RouterLinkWithHref', 'RouterOutlet',
    'Routes', 'RouterState', 'RouterStateSnapshot', 'UrlTree', 'UrlSegmentGroup', 'UrlSegment',
    'ParamMap', 'Data', 'Route', 'ActivatedRoute', 'ActivatedRouteSnapshot', 'RouterStateSnapshot',
    'ParamMap', 'Data', 'RouteConfigLoadEnd', 'RouteConfigLoadStart', 'Router', 'RouterLink',
    'RouterLinkWithHref', 'RouterOutlet', 'Routes', 'RouterState', 'RouterStateSnapshot',
    'UrlTree', 'UrlSegmentGroup', 'UrlSegment', 'ParamMap', 'Data', 'Route', 'ActivatedRoute',
    'ActivatedRouteSnapshot', 'RouterStateSnapshot', 'ParamMap', 'Data', 'RouteConfigLoadEnd',
    'RouteConfigLoadStart', 'Router', 'RouterLink', 'RouterLinkWithHref', 'RouterOutlet',
    'Routes', 'RouterState', 'RouterStateSnapshot', 'UrlTree', 'UrlSegmentGroup', 'UrlSegment',
    'ParamMap', 'Data', 'Route', 'ActivatedRoute', 'ActivatedRouteSnapshot', 'RouterStateSnapshot'
}

def gen_js_name(length=8):
    """Generate random JavaScript identifier names"""
    patterns = [
        lambda: ''.join(random.choices(string.ascii_letters, k=length)),
        lambda: '_' + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: '$' + ''.join(random.choices(string.ascii_lowercase, k=length-1)),
        lambda: random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length-1)),
    ]
    return random.choice(patterns)()

def encode_js_string(s):
    """Encode JavaScript strings with multiple techniques"""
    if not isinstance(s, str):
        return s
    
    # Unicode escape sequences
    unicode_encoded = ''.join(f'\\u{ord(c):04x}' for c in s)
    
    # Hex escape sequences
    hex_encoded = ''.join(f'\\x{ord(c):02x}' for c in s)
    
    # Mixed encoding
    mixed_encoded = []
    for c in s:
        if random.random() < 0.4:
            mixed_encoded.append(f'\\u{ord(c):04x}')
        elif random.random() < 0.7:
            mixed_encoded.append(f'\\x{ord(c):02x}')
        else:
            mixed_encoded.append(c)
    
    # String.fromCharCode array
    char_codes = [str(ord(c)) for c in s]
    fromCharCode = f'String.fromCharCode({", ".join(char_codes)})'
    
    # Choose encoding method
    encoding_methods = [
        f'"{unicode_encoded}"',
        f'"{hex_encoded}"',
        f'"{"".join(mixed_encoded)}"',
        fromCharCode,
    ]
    
    return random.choice(encoding_methods)

def decompose_js_number(n):
    """Decompose JavaScript numbers into expressions"""
    if not isinstance(n, (int, float)) or abs(n) < 2:
        return str(n)
    
    operations = [
        lambda x: f"({random.randint(1, x//2)} + {x - random.randint(1, x//2)})",
        lambda x: f"({x} * 2) / 2",
        lambda x: f"({x} + {random.randint(1, 5)}) - {random.randint(1, 5)}",
        lambda x: f"({x} * 3) / 3",
        lambda x: f"~~({x} * 1.0)",
        lambda x: f"({x} ^ 0)" if x >= 0 else str(x),
        lambda x: f"Math.abs({-abs(x)})",
        lambda x: f"parseInt('{x}')",
    ]
    
    try:
        return random.choice(operations)(abs(n))
    except:
        return str(n)

def obfuscate_javascript_code(code, options=None):
    """Main obfuscation function for JavaScript code"""
    if options is None:
        options = {
            'rename_variables': True,
            'rename_functions': True,
            'encode_strings': True,
            'decompose_numbers': True,
            'add_dummy_code': True,
            'control_flow_obfuscation': True
        }
    
    # Store mappings
    name_map = {}
    string_map = {}
    
    # Remove comments and docstrings
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove JSDoc comments
    code = re.sub(r'/\*\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove inline documentation strings
    code = re.sub(r'"""[^"]*"""', '', code)
    code = re.sub(r"'[^']*'", '', code)  # Simple strings (be careful with this)
    
    # Find function names
    if options.get('rename_functions', True):
        func_pattern = r'\bfunction\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
        func_matches = re.finditer(func_pattern, code)
        for match in func_matches:
            name = match.group(1)
            if name not in JS_KEYWORDS and name not in name_map:
                name_map[name] = gen_js_name()
        
        # Arrow functions and method names
        method_pattern = r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*function'
        method_matches = re.finditer(method_pattern, code)
        for match in method_matches:
            name = match.group(1)
            if name not in JS_KEYWORDS and name not in name_map:
                name_map[name] = gen_js_name()
    
    # Find variable names
    if options.get('rename_variables', True):
        var_patterns = [
            r'\bvar\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
            r'\blet\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
            r'\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
        ]
        
        for pattern in var_patterns:
            var_matches = re.finditer(pattern, code)
            for match in var_matches:
                name = match.group(1)
                if name not in JS_KEYWORDS and name not in name_map:
                    name_map[name] = gen_js_name()
    
    # Apply obfuscations
    obfuscated_code = code
    
    # Replace names
    if options.get('rename_variables', True) or options.get('rename_functions', True):
        for old_name, new_name in sorted(name_map.items(), key=lambda x: len(x[0]), reverse=True):
            # Replace only whole words, not inside strings
            pattern = r'\b' + re.escape(old_name) + r'\b(?=(?:"[^"]*"|\'[^\']*\'|[^\'"])*$)'
            obfuscated_code = re.sub(pattern, new_name, obfuscated_code)
    
    # Encode strings
    if options.get('encode_strings', True):
        def replace_string(match):
            quote = match.group(1)
            content = match.group(2)
            if len(content) > 0 and not content.startswith('\\'):  # Don't re-encode
                return quote + encode_js_string(content)[1:-1] + quote
            return match.group(0)
        
        # Match both single and double quoted strings
        obfuscated_code = re.sub(r'(["\'])([^"\'\\]*(\\.[^"\'\\]*)*)\1', replace_string, obfuscated_code)
    
    # Decompose numbers
    if options.get('decompose_numbers', True):
        def replace_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                return decompose_js_number(num)
            except ValueError:
                try:
                    num = float(num_str)
                    return decompose_js_number(num)
                except:
                    return num_str
        
        obfuscated_code = re.sub(r'\b\d+(?:\.\d+)?\b', replace_number, obfuscated_code)
    
    # Add dummy code
    if options.get('add_dummy_code', True):
        dummy_code = generate_dummy_js_code()
        obfuscated_code = dummy_code + '\n' + obfuscated_code
    
    # Control flow obfuscation
    if options.get('control_flow_obfuscation', True):
        obfuscated_code = obfuscate_control_flow(obfuscated_code)
    
    return obfuscated_code, {
        'variables_renamed': len(name_map),
        'strings_encoded': len(string_map),
        'numbers_decomposed': len(re.findall(r'\b\d+\b', code)),
        'dummy_functions_added': 1
    }

def generate_dummy_js_code():
    """Generate dummy JavaScript code"""
    dummy_functions = [
        '''
(function dummy_1() {
    var x = (15 + 27) >> 1;
    var y = x * 3 - 42;
    return y ^ 0x1234;
})();
''',
        '''
(function dummy_2() {
    for(var i = 0; i < (10 + 5); i++) {
        var temp = i * (2 + 1);
        temp = temp / 3;
    }
})();
''',
        '''
(function dummy_3() {
    var arr = [1,2,3,4,5];
    var sum = arr.reduce(function(a,b) { return a + b; }, 0);
    return sum * 2;
})();
'''
    ]
    
    return random.choice(dummy_functions)

def obfuscate_control_flow(code):
    """Add control flow obfuscation"""
    # Split code into lines
    lines = code.split('\n')
    obfuscated_lines = []
    
    for line in lines:
        if line.strip():
            # Add random dummy conditions
            if random.random() < 0.1:
                dummy_condition = random.choice([
                    'if (true) {',
                    'if (false) { /* dummy */ } else {',
                    'while (false) { /* dummy */ }',
                ])
                obfuscated_lines.append(dummy_condition)
            obfuscated_lines.append(line)
            
            # Close dummy blocks
            if random.random() < 0.05:
                if 'if' in line or 'while' in line:
                    obfuscated_lines.append('}')
        else:
            obfuscated_lines.append(line)
    
    return '\n'.join(obfuscated_lines)

def test_javascript_obfuscation():
    """Test JavaScript obfuscation"""
    test_code = '''
function calculateSum(a, b) {
    let result = a + b;
    return result;
}

const message = "Hello, World!";
const number = 42;
console.log(message, number);

let total = calculateSum(10, 20);
console.log("Total:", total);
'''
    
    options = {
        'rename_variables': True,
        'rename_functions': True,
        'encode_strings': True,
        'decompose_numbers': True,
        'add_dummy_code': True,
        'control_flow_obfuscation': True
    }
    
    obfuscated, stats = obfuscate_javascript_code(test_code, options)
    
    print("=== JavaScript Obfuscation Test ===")
    print("Original code:")
    print(test_code)
    print("\nObfuscated code:")
    print(obfuscated)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_javascript_obfuscation()
