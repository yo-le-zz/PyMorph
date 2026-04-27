/*
 * Go Test File for PyMorph Obfuscation
 * Test file with proper .go extension
 */

package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

// Constants for testing
const (
	MAGIC_NUMBER     = 42
	PI_VALUE        = 3.14159
	PROCESSING_MSG  = "Processing complete!"
	MAX_LINES       = 1000
	PROCESSING_PREF = "PROCESSED: "
)

// DataProcessor structure
type DataProcessor struct {
	filename      string
	data          []string
	processedData []string
}

// Statistics structure
type Statistics struct {
	OriginalLines   int
	ProcessedLines  int
	TotalCharacters int
	AverageLength   float64
	MaxLength       int
	MinLength       int
}

// NewDataProcessor creates a new DataProcessor instance
func NewDataProcessor(filename string) *DataProcessor {
	return &DataProcessor{
		filename:      filename,
		data:          make([]string, 0),
		processedData: make([]string, 0),
	}
}

// LoadData loads data from file
func (dp *DataProcessor) LoadData() error {
	file, err := os.Open(dp.filename)
	if err != nil {
		return fmt.Errorf("file not found: %s", dp.filename)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	dp.data = dp.data[:0] // Clear existing data

	for scanner.Scan() && len(dp.data) < MAX_LINES {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			dp.data = append(dp.data, line)
		}
	}

	return scanner.Err()
}

// ProcessData processes the loaded data
func (dp *DataProcessor) ProcessData() []string {
	dp.processedData = dp.processedData[:0] // Clear existing data

	for _, line := range dp.data {
		processedLine := PROCESSING_PREF + strings.ToUpper(line)
		dp.processedData = append(dp.processedData, processedLine)
	}

	return dp.processedData
}

// SaveResults saves processed data to file
func (dp *DataProcessor) SaveResults(outputFilename string) error {
	file, err := os.Create(outputFilename)
	if err != nil {
		return fmt.Errorf("cannot create output file: %s", outputFilename)
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	for _, line := range dp.processedData {
		_, err := writer.WriteString(line + "\n")
		if err != nil {
			return err
		}
	}

	return writer.Flush()
}

// GetStatistics calculates processing statistics
func (dp *DataProcessor) GetStatistics() Statistics {
	stats := Statistics{
		OriginalLines:   len(dp.data),
		ProcessedLines:  len(dp.processedData),
		TotalCharacters: 0,
		AverageLength:   0.0,
		MaxLength:       0,
		MinLength:       0,
	}

	if len(dp.data) > 0 {
		for _, line := range dp.data {
			length := len(line)
			stats.TotalCharacters += length

			if length > stats.MaxLength {
				stats.MaxLength = length
			}

			if stats.MinLength == 0 || length < stats.MinLength {
				stats.MinLength = length
			}
		}

		stats.AverageLength = float64(stats.TotalCharacters) / float64(stats.OriginalLines)
	}

	return stats
}

// GetDataSize returns the number of data lines
func (dp *DataProcessor) GetDataSize() int {
	return len(dp.data)
}

// GetProcessedDataSize returns the number of processed data lines
func (dp *DataProcessor) GetProcessedDataSize() int {
	return len(dp.processedData)
}

// GetFilename returns the filename
func (dp *DataProcessor) GetFilename() string {
	return dp.filename
}

// Utility functions

// CalculateMean calculates the mean length of strings
func CalculateMean(data []string) float64 {
	if len(data) == 0 {
		return 0.0
	}

	total := 0
	for _, line := range data {
		total += len(line)
	}

	return float64(total) / float64(len(data))
}

// FindMaxLength finds the maximum string length
func FindMaxLength(data []string) int {
	maxLen := 0
	for _, line := range data {
		if len(line) > maxLen {
			maxLen = len(line)
		}
	}
	return maxLen
}

// FindMinLength finds the minimum string length
func FindMinLength(data []string) int {
	if len(data) == 0 {
		return 0
	}

	minLen := len(data[0])
	for _, line := range data {
		if len(line) < minLen {
			minLen = len(line)
		}
	}
	return minLen
}

// TestStringOperations tests various string operations
func TestStringOperations(testString string) {
	fmt.Println("String operations:")
	fmt.Printf("  Original: %s\n", testString)

	// Reverse string
	reversed := ReverseString(testString)
	fmt.Printf("  Reversed: %s\n", reversed)

	// Uppercase
	uppercased := strings.ToUpper(testString)
	fmt.Printf("  Uppercased: %s\n", uppercased)

	// Lowercase
	lowercased := strings.ToLower(testString)
	fmt.Printf("  Lowercased: %s\n", lowercased)

	// Character count
	charCount := len([]rune(testString))
	fmt.Printf("  Character count: %d\n", charCount)

	// Word count
	wordCount := len(strings.Fields(testString))
	fmt.Printf("  Word count: %d\n", wordCount)
}

// ReverseString reverses a string
func ReverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// TestNumericOperations tests various numeric operations
func TestNumericOperations() {
	fmt.Println("Numeric operations:")

	// Test slice operations
	numbers := make([]int, 10)
	for i := 0; i < 10; i++ {
		numbers[i] = i + 1
	}

	sum := 0
	product := 1
	for _, num := range numbers {
		sum += num
		product *= num
	}

	average := float64(sum) / float64(len(numbers))

	fmt.Printf("  Numbers: %v\n", numbers)
	fmt.Printf("  Sum: %d\n", sum)
	fmt.Printf("  Product: %d\n", product)
	fmt.Printf("  Average: %.2f\n", average)

	// Test calculations with constants
	testValue := 100
	result := float64(testValue) * PI_VALUE / float64(MAGIC_NUMBER)
	fmt.Printf("  Test calculation: %.2f\n", result)

	// Test math functions
	fmt.Printf("  Math.Sqrt(16): %.2f\n", math.Sqrt(16))
	fmt.Printf("  Math.Pow(2, 3): %.2f\n", math.Pow(2, 3))
	fmt.Printf("  Math.Abs(-42): %.2f\n", math.Abs(-42))
}

// TestCollectionOperations tests various collection operations
func TestCollectionOperations() {
	fmt.Println("Collection operations:")

	// Create test data
	testData := []string{
		"short",
		"medium length",
		"very long string here",
		"another test string",
		"final string",
	}

	// Filter and transform
	var filtered []string
	for _, s := range testData {
		if len(s) > 5 {
			filtered = append(filtered, strings.ToUpper(s))
		}
	}

	sort.Strings(filtered)

	fmt.Printf("  Original: %v\n", testData)
	fmt.Printf("  Filtered: %v\n", filtered)

	// Group by length
	groupedByLength := make(map[int][]string)
	for _, s := range testData {
		length := len(s)
		groupedByLength[length] = append(groupedByLength[length], s)
	}

	fmt.Printf("  Grouped by length: %v\n", groupedLength)
}

// TestMapOperations tests map operations
func TestMapOperations() {
	fmt.Println("Map operations:")

	// Create test map
	testMap := make(map[string]int)
	testMap["apple"] = 5
	testMap["banana"] = 3
	testMap["cherry"] = 8
	testMap["date"] = 2

	// Calculate total
	total := 0
	for _, value := range testMap {
		total += value
	}

	fmt.Printf("  Test map: %v\n", testMap)
	fmt.Printf("  Total value: %d\n", total)
	fmt.Printf("  Map size: %d\n", len(testMap))

	// Find max value
	maxValue := 0
	maxKey := ""
	for key, value := range testMap {
		if value > maxValue {
			maxValue = value
			maxKey = key
		}
	}

	fmt.Printf("  Max value: %d (key: %s)\n", maxValue, maxKey)
}

// TestInterfaceOperations tests interface operations
func TestInterfaceOperations() {
	fmt.Println("Interface operations:")

	// Define interface
	type Processor interface {
		Process(input string) string
		GetName() string
	}

	// Implement interface
	type StringProcessor struct {
		name string
	}

	func (sp *StringProcessor) Process(input string) string {
		return strings.ToUpper(input)
	}

	func (sp *StringProcessor) GetName() string {
		return sp.name
	}

	// Use interface
	processors := []Processor{
		&StringProcessor{name: "Upper"},
		&StringProcessor{name: "Lower"},
	}

	testInput := "hello world"
	for _, processor := range processors {
		result := processor.Process(testInput)
		fmt.Printf("  %s processor: %s -> %s\n", processor.GetName(), testInput, result)
	}
}

// TestErrorHandling tests error handling
func TestErrorHandling() {
	fmt.Println("Error handling:")

	// Test file operations
	_, err := os.Open("nonexistent_file.txt")
	if err != nil {
		fmt.Printf("  Expected error: %v\n", err)
	}

	// Test string to int conversion
	_, err = strconv.Atoi("not_a_number")
	if err != nil {
		fmt.Printf("  Conversion error: %v\n", err)
	}

	// Test custom error
	customError := fmt.Errorf("custom error with value: %d", MAGIC_NUMBER)
	fmt.Printf("  Custom error: %v\n", customError)
}

// Main function
func main() {
	// Test parameters
	testFilename := "input.txt"
	outputFilename := "output.txt"

	// Create processor instance
	processor := NewDataProcessor(testFilename)

	// Load data
	fmt.Println("Loading data...")
	if err := processor.LoadData(); err != nil {
		fmt.Printf("Failed to load data: %v\n", err)
		os.Exit(1)
	}

	// Process data
	fmt.Println("Processing data...")
	processedData := processor.ProcessData()

	// Get statistics
	stats := processor.GetStatistics()
	fmt.Println("Statistics:")
	fmt.Printf("  Original lines: %d\n", stats.OriginalLines)
	fmt.Printf("  Processed lines: %d\n", stats.ProcessedLines)
	fmt.Printf("  Total characters: %d\n", stats.TotalCharacters)
	fmt.Printf("  Average length: %.2f\n", stats.AverageLength)
	fmt.Printf("  Max length: %d\n", stats.MaxLength)
	fmt.Printf("  Min length: %d\n", stats.MinLength)

	// Calculate additional metrics
	fmt.Println("Additional metrics:")
	fmt.Printf("  Mean length: %.2f\n", CalculateMean(processor.data))
	fmt.Printf("  Max length: %d\n", FindMaxLength(processedData))
	fmt.Printf("  Min length: %d\n", FindMinLength(processedData))

	// Save results
	fmt.Println("Saving results...")
	if err := processor.SaveResults(outputFilename); err != nil {
		fmt.Printf("Failed to save results: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Results saved to %s\n", outputFilename)

	// Display constants
	fmt.Println("Constants:")
	fmt.Printf("  Magic number: %d\n", MAGIC_NUMBER)
	fmt.Printf("  Pi value: %.5f\n", PI_VALUE)
	fmt.Printf("  Message: %s\n", PROCESSING_MSG)

	// Test various operations
	TestStringOperations("Hello, Go!")
	TestNumericOperations()
	TestCollectionOperations()
	TestMapOperations()
	TestInterfaceOperations()
	TestErrorHandling()

	// Test goroutine (simple example)
	fmt.Println("Goroutine test:")
	done := make(chan bool)
	go func() {
		for i := 0; i < 5; i++ {
			fmt.Printf("  Goroutine iteration: %d\n", i+1)
		}
		done <- true
	}()
	<-done // Wait for goroutine to finish

	fmt.Println("Program completed successfully!")
}
