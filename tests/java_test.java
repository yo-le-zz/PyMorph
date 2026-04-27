/*
 * Java Test File for PyMorph Obfuscation
 * Test file with proper .java extension
 */

package com.example.pymorph.test;

import java.io.*;
import java.util.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * DataProcessor class for testing Java obfuscation
 * This class demonstrates various Java features for obfuscation testing
 */
public class DataProcessor {
    // Instance variables
    private String filename;
    private List<String> data;
    private List<String> processedData;
    
    // Constants
    private static final int MAX_LINES = 1000;
    private static final String PROCESSING_PREFIX = "PROCESSED: ";
    private static final String ENCODING = StandardCharsets.UTF_8.name();
    
    // Magic numbers for testing
    private static final int MAGIC_NUMBER = 42;
    private static final double PI_VALUE = 3.14159;
    private static final String PROCESSING_MESSAGE = "Processing complete!";
    
    /**
     * Constructor for DataProcessor
     * @param filename the input filename
     */
    public DataProcessor(String filename) {
        this.filename = filename;
        this.data = new ArrayList<>();
        this.processedData = new ArrayList<>();
    }
    
    /**
     * Load data from file
     * @return true if successful, false otherwise
     */
    public boolean loadData() throws IOException {
        data.clear();
        
        try (BufferedReader reader = Files.newBufferedReader(Paths.get(filename))) {
            String line;
            while ((line = reader.readLine()) != null && data.size() < MAX_LINES) {
                String trimmedLine = line.trim();
                if (!trimmedLine.isEmpty()) {
                    data.add(trimmedLine);
                }
            }
        } catch (FileNotFoundException e) {
            System.err.println("Error: File " + filename + " not found");
            return false;
        }
        
        return true;
    }
    
    /**
     * Process the loaded data
     * @return list of processed data
     */
    public List<String> processData() {
        processedData.clear();
        
        for (String line : data) {
            String processedLine = PROCESSING_PREFIX + line.toUpperCase();
            processedData.add(processedLine);
        }
        
        return new ArrayList<>(processedData);
    }
    
    /**
     * Save processed data to file
     * @param outputFilename the output filename
     * @return true if successful, false otherwise
     */
    public boolean saveResults(String outputFilename) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(
                Paths.get(outputFilename), StandardCharsets.UTF_8)) {
            
            for (String line : processedData) {
                writer.write(line);
                writer.newLine();
            }
        }
        
        return true;
    }
    
    /**
     * Get processing statistics
     * @return Statistics object
     */
    public Statistics getStatistics() {
        Statistics stats = new Statistics();
        
        stats.originalLines = data.size();
        stats.processedLines = processedData.size();
        stats.totalCharacters = data.stream()
                .mapToInt(String::length)
                .sum();
        stats.averageLength = stats.originalLines > 0 ? 
                (double) stats.totalCharacters / stats.originalLines : 0.0;
        stats.maxLength = data.stream()
                .mapToInt(String::length)
                .max()
                .orElse(0);
        stats.minLength = data.stream()
                .mapToInt(String::length)
                .min()
                .orElse(0);
        
        return stats;
    }
    
    /**
     * Get the filename
     * @return the filename
     */
    public String getFilename() {
        return filename;
    }
    
    /**
     * Get data size
     * @return number of data lines
     */
    public int getDataSize() {
        return data.size();
    }
    
    /**
     * Get processed data size
     * @return number of processed data lines
     */
    public int getProcessedDataSize() {
        return processedData.size();
    }
    
    // Utility methods
    /**
     * Calculate mean length of strings
     * @param strings list of strings
     * @return mean length
     */
    public static double calculateMean(List<String> strings) {
        if (strings.isEmpty()) {
            return 0.0;
        }
        
        int total = strings.stream()
                .mapToInt(String::length)
                .sum();
        
        return (double) total / strings.size();
    }
    
    /**
     * Find maximum string length
     * @param strings list of strings
     * @return maximum length
     */
    public static int findMaxLength(List<String> strings) {
        return strings.stream()
                .mapToInt(String::length)
                .max()
                .orElse(0);
    }
    
    /**
     * Find minimum string length
     * @param strings list of strings
     * @return minimum length
     */
    public static int findMinLength(List<String> strings) {
        return strings.stream()
                .mapToInt(String::length)
                .min()
                .orElse(0);
    }
    
    /**
     * Test various string operations
     * @param testString the string to test
     */
    public static void testStringOperations(String testString) {
        System.out.println("String operations:");
        System.out.println("  Original: " + testString);
        
        // Reverse string
        String reversed = new StringBuilder(testString).reverse().toString();
        System.out.println("  Reversed: " + reversed);
        
        // Uppercase
        String uppercased = testString.toUpperCase();
        System.out.println("  Uppercased: " + uppercased);
        
        // Lowercase
        String lowercased = testString.toLowerCase();
        System.out.println("  Lowercased: " + lowercased);
        
        // Character count
        long charCount = testString.chars().count();
        System.out.println("  Character count: " + charCount);
    }
    
    /**
     * Test numeric operations
     */
    public static void testNumericOperations() {
        System.out.println("Numeric operations:");
        
        // Test array operations
        Integer[] numbers = new Integer[10];
        for (int i = 0; i < 10; i++) {
            numbers[i] = i + 1;
        }
        
        List<Integer> numberList = Arrays.asList(numbers);
        int sum = numberList.stream().mapToInt(Integer::intValue).sum();
        long product = numberList.stream().mapToLong(Integer::longValue).reduce(1, (a, b) -> a * b);
        double average = numberList.stream().mapToInt(Integer::intValue).average().orElse(0.0);
        
        System.out.println("  Numbers: " + numberList);
        System.out.println("  Sum: " + sum);
        System.out.println("  Product: " + product);
        System.out.println("  Average: " + average);
        
        // Test calculations with constants
        int testValue = 100;
        double result = (double) testValue * PI_VALUE / MAGIC_NUMBER;
        System.out.println("  Test calculation: " + result);
    }
    
    /**
     * Test collection operations
     */
    public static void testCollectionOperations() {
        System.out.println("Collection operations:");
        
        // Create test data
        List<String> testData = Arrays.asList(
            "short",
            "medium length",
            "very long string here",
            "another test string",
            "final string"
        );
        
        // Filter and transform
        List<String> filtered = testData.stream()
                .filter(s -> s.length() > 5)
                .map(String::toUpperCase)
                .sorted()
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
        
        System.out.println("  Original: " + testData);
        System.out.println("  Filtered: " + filtered);
        
        // Group by length
        Map<Integer, List<String>> groupedByLength = testData.stream()
                .collect(Collectors.groupingBy(String::length));
        
        System.out.println("  Grouped by length: " + groupedByLength);
    }
    
    /**
     * Statistics inner class
     */
    public static class Statistics {
        public int originalLines;
        public int processedLines;
        public int totalCharacters;
        public double averageLength;
        public int maxLength;
        public int minLength;
        
        @Override
        public String toString() {
            return String.format(
                "Statistics{originalLines=%d, processedLines=%d, totalCharacters=%d, " +
                "averageLength=%.2f, maxLength=%d, minLength=%d}",
                originalLines, processedLines, totalCharacters, averageLength, maxLength, minLength
            );
        }
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        // Test parameters
        String testFilename = "input.txt";
        String outputFilename = "output.txt";
        
        // Create processor instance
        DataProcessor processor = new DataProcessor(testFilename);
        
        try {
            // Load data
            System.out.println("Loading data...");
            if (!processor.loadData()) {
                System.err.println("Failed to load data");
                System.exit(1);
            }
            
            // Process data
            System.out.println("Processing data...");
            List<String> processedData = processor.processData();
            
            // Get statistics
            Statistics stats = processor.getStatistics();
            System.out.println("Statistics:");
            System.out.println("  " + stats);
            
            // Calculate additional metrics
            System.out.println("Additional metrics:");
            System.out.println("  Mean length: " + calculateMean(processor.data));
            System.out.println("  Max length: " + findMaxLength(processedData));
            System.out.println("  Min length: " + findMinLength(processedData));
            
            // Save results
            System.out.println("Saving results...");
            if (processor.saveResults(outputFilename)) {
                System.out.println("Results saved to " + outputFilename);
            } else {
                System.err.println("Failed to save results");
                System.exit(1);
            }
            
            // Display constants
            System.out.println("Constants:");
            System.out.println("  Magic number: " + MAGIC_NUMBER);
            System.out.println("  Pi value: " + PI_VALUE);
            System.out.println("  Message: " + PROCESSING_MESSAGE);
            
            // Test various operations
            testStringOperations("Hello, Java!");
            testNumericOperations();
            testCollectionOperations();
            
            System.out.println("Program completed successfully!");
            
        } catch (IOException e) {
            System.err.println("IO Error: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
