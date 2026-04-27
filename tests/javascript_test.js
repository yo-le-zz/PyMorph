/*
 * JavaScript Test File for PyMorph Obfuscation
 * Test file with proper .js extension
 */

// Constants for testing
const MAGIC_NUMBER = 42;
const PI_VALUE = 3.14159;
const PROCESSING_MESSAGE = "Processing complete!";
const MAX_LINES = 1000;
const PROCESSING_PREFIX = "PROCESSED: ";

/**
 * DataProcessor class for testing JavaScript obfuscation
 */
class DataProcessor {
    /**
     * Constructor
     * @param {string} filename - Input filename
     */
    constructor(filename) {
        this.filename = filename;
        this.data = [];
        this.processedData = [];
    }

    /**
     * Load data from file
     * @returns {Promise<boolean>} - Success status
     */
    async loadData() {
        try {
            const fs = require('fs').promises;
            const content = await fs.readFile(this.filename, 'utf8');
            const lines = content.split('\n');
            
            this.data = lines
                .map(line => line.trim())
                .filter(line => line.length > 0)
                .slice(0, MAX_LINES);
            
            return true;
        } catch (error) {
            console.error(`Error loading file ${this.filename}:`, error.message);
            return false;
        }
    }

    /**
     * Process the loaded data
     * @returns {Array<string>} - Processed data
     */
    processData() {
        this.processedData = this.data.map(line => 
            PROCESSING_PREFIX + line.toUpperCase()
        );
        return this.processedData;
    }

    /**
     * Save processed data to file
     * @param {string} outputFilename - Output filename
     * @returns {Promise<boolean>} - Success status
     */
    async saveResults(outputFilename) {
        try {
            const fs = require('fs').promises;
            const content = this.processedData.join('\n');
            await fs.writeFile(outputFilename, content, 'utf8');
            return true;
        } catch (error) {
            console.error(`Error saving file ${outputFilename}:`, error.message);
            return false;
        }
    }

    /**
     * Get processing statistics
     * @returns {Object} - Statistics object
     */
    getStatistics() {
        const totalCharacters = this.data.reduce((sum, line) => sum + line.length, 0);
        const averageLength = this.data.length > 0 ? totalCharacters / this.data.length : 0;
        const lengths = this.data.map(line => line.length);
        const maxLength = Math.max(...lengths, 0);
        const minLength = Math.min(...lengths, 0);

        return {
            originalLines: this.data.length,
            processedLines: this.processedData.length,
            totalCharacters,
            averageLength,
            maxLength,
            minLength
        };
    }

    /**
     * Get data size
     * @returns {number} - Number of data lines
     */
    getDataSize() {
        return this.data.length;
    }

    /**
     * Get processed data size
     * @returns {number} - Number of processed data lines
     */
    getProcessedDataSize() {
        return this.processedData.length;
    }

    /**
     * Get filename
     * @returns {string} - Filename
     */
    getFilename() {
        return this.filename;
    }
}

// Utility functions

/**
 * Calculate mean length of strings
 * @param {Array<string>} strings - Array of strings
 * @returns {number} - Mean length
 */
function calculateMean(strings) {
    if (strings.length === 0) return 0;
    
    const total = strings.reduce((sum, str) => sum + str.length, 0);
    return total / strings.length;
}

/**
 * Find maximum string length
 * @param {Array<string>} strings - Array of strings
 * @returns {number} - Maximum length
 */
function findMaxLength(strings) {
    return Math.max(...strings.map(str => str.length), 0);
}

/**
 * Find minimum string length
 * @param {Array<string>} strings - Array of strings
 * @returns {number} - Minimum length
 */
function findMinLength(strings) {
    return Math.min(...strings.map(str => str.length), 0);
}

/**
 * Test various string operations
 * @param {string} testString - String to test
 */
function testStringOperations(testString) {
    console.log("String operations:");
    console.log(`  Original: ${testString}`);
    
    // Reverse string
    const reversed = testString.split('').reverse().join('');
    console.log(`  Reversed: ${reversed}`);
    
    // Uppercase
    const uppercased = testString.toUpperCase();
    console.log(`  Uppercased: ${uppercased}`);
    
    // Lowercase
    const lowercased = testString.toLowerCase();
    console.log(`  Lowercased: ${lowercased}`);
    
    // Character count
    const charCount = testString.length;
    console.log(`  Character count: ${charCount}`);
    
    // Word count
    const wordCount = testString.trim().split(/\s+/).length;
    console.log(`  Word count: ${wordCount}`);
}

/**
 * Test numeric operations
 */
function testNumericOperations() {
    console.log("Numeric operations:");
    
    // Test array operations
    const numbers = Array.from({length: 10}, (_, i) => i + 1);
    const sum = numbers.reduce((acc, num) => acc + num, 0);
    const product = numbers.reduce((acc, num) => acc * num, 1);
    const average = sum / numbers.length;
    
    console.log(`  Numbers: [${numbers.join(', ')}]`);
    console.log(`  Sum: ${sum}`);
    console.log(`  Product: ${product}`);
    console.log(`  Average: ${average}`);
    
    // Test calculations with constants
    const testValue = 100;
    const result = (testValue * PI_VALUE) / MAGIC_NUMBER;
    console.log(`  Test calculation: ${result}`);
    
    // Test Math functions
    console.log(`  Math.sqrt(16): ${Math.sqrt(16)}`);
    console.log(`  Math.pow(2, 3): ${Math.pow(2, 3)}`);
    console.log(`  Math.abs(-42): ${Math.abs(-42)}`);
    console.log(`  Math.round(3.7): ${Math.round(3.7)}`);
    console.log(`  Math.floor(3.7): ${Math.floor(3.7)}`);
    console.log(`  Math.ceil(3.2): ${Math.ceil(3.2)}`);
}

/**
 * Test collection operations
 */
function testCollectionOperations() {
    console.log("Collection operations:");
    
    // Create test data
    const testData = [
        "short",
        "medium length",
        "very long string here",
        "another test string",
        "final string"
    ];
    
    // Filter and transform
    const filtered = testData
        .filter(str => str.length > 5)
        .map(str => str.toUpperCase())
        .sort();
    
    console.log(`  Original: [${testData.join(', ')}]`);
    console.log(`  Filtered: [${filtered.join(', ')}]`);
    
    // Group by length
    const groupedByLength = testData.reduce((acc, str) => {
        const length = str.length;
        if (!acc[length]) {
            acc[length] = [];
        }
        acc[length].push(str);
        return acc;
    }, {});
    
    console.log(`  Grouped by length:`, groupedByLength);
    
    // Test Set operations
    const uniqueChars = new Set(testData.join('').split(''));
    console.log(`  Unique characters: [${Array.from(uniqueChars).join(', ')}]`);
    
    // Test Map operations
    const charCount = new Map();
    for (const str of testData) {
        for (const char of str) {
            charCount.set(char, (charCount.get(char) || 0) + 1);
        }
    }
    console.log(`  Character counts:`, Object.fromEntries(charCount));
}

/**
 * Test object operations
 */
function testObjectOperations() {
    console.log("Object operations:");
    
    // Create test object
    const testObject = {
        name: "Test Object",
        value: MAGIC_NUMBER,
        active: true,
        items: ["item1", "item2", "item3"],
        nested: {
            prop1: "value1",
            prop2: 42
        }
    };
    
    // Object operations
    const keys = Object.keys(testObject);
    const values = Object.values(testObject);
    const entries = Object.entries(testObject);
    
    console.log(`  Keys: [${keys.join(', ')}]`);
    console.log(`  Values: [${values.join(', ')}]`);
    console.log(`  Entries:`, entries);
    
    // Object destructuring
    const {name, value, nested: {prop1}} = testObject;
    console.log(`  Destructured: name=${name}, value=${value}, prop1=${prop1}`);
    
    // Object spread
    const newObject = {...testObject, newProp: "new value"};
    console.log(`  Spread object:`, newObject);
}

/**
 * Test function operations
 */
function testFunctionOperations() {
    console.log("Function operations:");
    
    // Higher order functions
    const multiply = (a) => (b) => a * b;
    const multiplyBy2 = multiply(2);
    const multiplyBy5 = multiply(5);
    
    console.log(`  multiplyBy2(10): ${multiplyBy2(10)}`);
    console.log(`  multiplyBy5(10): ${multiplyBy5(10)}`);
    
    // Function composition
    const compose = (f, g) => (x) => f(g(x));
    const addOne = x => x + 1;
    const double = x => x * 2;
    const addOneThenDouble = compose(double, addOne);
    
    console.log(`  addOneThenDouble(5): ${addOneThenDouble(5)}`);
    
    // Recursive function
    const factorial = n => n <= 1 ? 1 : n * factorial(n - 1);
    console.log(`  factorial(5): ${factorial(5)}`);
    
    // Memoization
    const memoize = (fn) => {
        const cache = new Map();
        return (...args) => {
            const key = JSON.stringify(args);
            if (cache.has(key)) {
                return cache.get(key);
            }
            const result = fn(...args);
            cache.set(key, result);
            return result;
        };
    };
    
    const memoizedFactorial = memoize(factorial);
    console.log(`  memoizedFactorial(6): ${memoizedFactorial(6)}`);
}

/**
 * Test async operations
 */
async function testAsyncOperations() {
    console.log("Async operations:");
    
    // Promise creation
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    
    // Sequential async operations
    const result1 = await delay(100).then(() => "First result");
    const result2 = await delay(50).then(() => "Second result");
    
    console.log(`  Sequential: ${result1}, ${result2}`);
    
    // Parallel async operations
    const [parallel1, parallel2] = await Promise.all([
        delay(100).then(() => "Parallel 1"),
        delay(100).then(() => "Parallel 2")
    ]);
    
    console.log(`  Parallel: ${parallel1}, ${parallel2}`);
    
    // Async/await with error handling
    try {
        const result = await delay(50).then(() => {
            throw new Error("Test error");
        });
    } catch (error) {
        console.log(`  Caught error: ${error.message}`);
    }
    
    // Fetch simulation (if in browser environment)
    if (typeof fetch !== 'undefined') {
        try {
            const response = await fetch('https://api.github.com/users/github');
            const data = await response.json();
            console.log(`  GitHub user: ${data.login}`);
        } catch (error) {
            console.log(`  Fetch error: ${error.message}`);
        }
    } else {
        console.log(`  Fetch not available in this environment`);
    }
}

/**
 * Test error handling
 */
function testErrorHandling() {
    console.log("Error handling:");
    
    // Try-catch with different error types
    try {
        // Type error
        const obj = null;
        obj.property = "value";
    } catch (error) {
        console.log(`  TypeError caught: ${error.message}`);
    }
    
    try {
        // Reference error
        undefinedVariable.property = "value";
    } catch (error) {
        console.log(`  ReferenceError caught: ${error.message}`);
    }
    
    try {
        // Custom error
        throw new Error(`Custom error with value: ${MAGIC_NUMBER}`);
    } catch (error) {
        console.log(`  Custom error caught: ${error.message}`);
    }
    
    // Error handling with finally
    let resourceAcquired = false;
    try {
        resourceAcquired = true;
        console.log(`  Resource acquired`);
        // Simulate some work
        throw new Error("Simulated error");
    } catch (error) {
        console.log(`  Error in resource usage: ${error.message}`);
    } finally {
        if (resourceAcquired) {
            console.log(`  Resource released`);
        }
    }
}

/**
 * Main function
 */
async function main() {
    // Test parameters
    const testFilename = "input.txt";
    const outputFilename = "output.txt";
    
    // Create processor instance
    const processor = new DataProcessor(testFilename);
    
    try {
        // Load data
        console.log("Loading data...");
        const loadSuccess = await processor.loadData();
        if (!loadSuccess) {
            console.error("Failed to load data");
            process.exit(1);
        }
        
        // Process data
        console.log("Processing data...");
        const processedData = processor.processData();
        
        // Get statistics
        const stats = processor.getStatistics();
        console.log("Statistics:");
        console.log(`  Original lines: ${stats.originalLines}`);
        console.log(`  Processed lines: ${stats.processedLines}`);
        console.log(`  Total characters: ${stats.totalCharacters}`);
        console.log(`  Average length: ${stats.averageLength.toFixed(2)}`);
        console.log(`  Max length: ${stats.maxLength}`);
        console.log(`  Min length: ${stats.minLength}`);
        
        // Calculate additional metrics
        console.log("Additional metrics:");
        console.log(`  Mean length: ${calculateMean(processor.data).toFixed(2)}`);
        console.log(`  Max length: ${findMaxLength(processedData)}`);
        console.log(`  Min length: ${findMinLength(processedData)}`);
        
        // Save results
        console.log("Saving results...");
        const saveSuccess = await processor.saveResults(outputFilename);
        if (!saveSuccess) {
            console.error("Failed to save results");
            process.exit(1);
        }
        
        console.log(`Results saved to ${outputFilename}`);
        
        // Display constants
        console.log("Constants:");
        console.log(`  Magic number: ${MAGIC_NUMBER}`);
        console.log(`  Pi value: ${PI_VALUE}`);
        console.log(`  Message: ${PROCESSING_MESSAGE}`);
        
        // Test various operations
        testStringOperations("Hello, JavaScript!");
        testNumericOperations();
        testCollectionOperations();
        testObjectOperations();
        testFunctionOperations();
        await testAsyncOperations();
        testErrorHandling();
        
        console.log("Program completed successfully!");
        
    } catch (error) {
        console.error("Unexpected error:", error.message);
        process.exit(1);
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DataProcessor,
        calculateMean,
        findMaxLength,
        findMinLength,
        testStringOperations,
        testNumericOperations,
        testCollectionOperations,
        testObjectOperations,
        testFunctionOperations,
        testAsyncOperations,
        testErrorHandling,
        main
    };
}

// Run main function if called directly
if (require.main === module) {
    main().catch(error => {
        console.error("Main function error:", error);
        process.exit(1);
    });
}
