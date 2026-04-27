/*
 * C Test File for PyMorph Obfuscation
 * Test file with proper .c extension
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 1024
#define MAX_LINES 1000
#define MAGIC_NUMBER 42
#define PI_VALUE 3.14159

// Structure for statistics
typedef struct {
    int original_lines;
    int processed_lines;
    int total_characters;
    double average_length;
    int max_length;
    int min_length;
} Statistics;

// Structure for data processor
typedef struct {
    char filename[256];
    char* data[MAX_LINES];
    char* processed_data[MAX_LINES];
    int line_count;
    int processed_count;
} DataProcessor;

// Function prototypes
DataProcessor* create_processor(const char* filename);
void free_processor(DataProcessor* processor);
int load_data(DataProcessor* processor);
void process_data(DataProcessor* processor);
int save_results(DataProcessor* processor, const char* output_filename);
Statistics get_statistics(DataProcessor* processor);
double calculate_mean(char* data[], int count);
int find_max_length(char* data[], int count);
int find_min_length(char* data[], int count);
void trim_whitespace(char* str);
void to_uppercase(char* str);

// Create new processor
DataProcessor* create_processor(const char* filename) {
    DataProcessor* processor = (DataProcessor*)malloc(sizeof(DataProcessor));
    if (!processor) return NULL;
    
    strncpy(processor->filename, filename, sizeof(processor->filename) - 1);
    processor->filename[sizeof(processor->filename) - 1] = '\0';
    processor->line_count = 0;
    processor->processed_count = 0;
    
    // Initialize data arrays
    for (int i = 0; i < MAX_LINES; i++) {
        processor->data[i] = NULL;
        processor->processed_data[i] = NULL;
    }
    
    return processor;
}

// Free processor memory
void free_processor(DataProcessor* processor) {
    if (!processor) return;
    
    // Free data lines
    for (int i = 0; i < processor->line_count; i++) {
        if (processor->data[i]) {
            free(processor->data[i]);
        }
    }
    
    // Free processed data lines
    for (int i = 0; i < processor->processed_count; i++) {
        if (processor->processed_data[i]) {
            free(processor->processed_data[i]);
        }
    }
    
    free(processor);
}

// Load data from file
int load_data(DataProcessor* processor) {
    FILE* file = fopen(processor->filename, "r");
    if (!file) {
        fprintf(stderr, "Error: File %s not found\n", processor->filename);
        return 0;
    }
    
    char line[MAX_LINE_LENGTH];
    processor->line_count = 0;
    
    while (fgets(line, sizeof(line), file) && processor->line_count < MAX_LINES) {
        // Remove newline and trim whitespace
        line[strcspn(line, "\n")] = '\0';
        trim_whitespace(line);
        
        // Skip empty lines
        if (strlen(line) > 0) {
            processor->data[processor->line_count] = strdup(line);
            if (!processor->data[processor->line_count]) {
                fprintf(stderr, "Memory allocation error\n");
                fclose(file);
                return 0;
            }
            processor->line_count++;
        }
    }
    
    fclose(file);
    return 1;
}

// Process the loaded data
void process_data(DataProcessor* processor) {
    processor->processed_count = 0;
    
    for (int i = 0; i < processor->line_count; i++) {
        // Create processed line with prefix
        char* original = processor->data[i];
        char* processed = (char*)malloc(strlen(original) + 12); // "PROCESSED: " + null
        
        if (processed) {
            strcpy(processed, "PROCESSED: ");
            strcat(processed, original);
            to_uppercase(processed);
            
            processor->processed_data[processor->processed_count] = processed;
            processor->processed_count++;
        }
    }
}

// Save processed data to file
int save_results(DataProcessor* processor, const char* output_filename) {
    FILE* file = fopen(output_filename, "w");
    if (!file) {
        fprintf(stderr, "Error: Cannot create output file\n");
        return 0;
    }
    
    for (int i = 0; i < processor->processed_count; i++) {
        fprintf(file, "%s\n", processor->processed_data[i]);
    }
    
    fclose(file);
    return 1;
}

// Get processing statistics
Statistics get_statistics(DataProcessor* processor) {
    Statistics stats;
    stats.original_lines = processor->line_count;
    stats.processed_lines = processor->processed_count;
    stats.total_characters = 0;
    stats.average_length = 0.0;
    stats.max_length = 0;
    stats.min_length = 0;
    
    if (processor->line_count > 0) {
        // Calculate total characters
        for (int i = 0; i < processor->line_count; i++) {
            int len = strlen(processor->data[i]);
            stats.total_characters += len;
            
            if (i == 0 || len > stats.max_length) {
                stats.max_length = len;
            }
            
            if (i == 0 || len < stats.min_length) {
                stats.min_length = len;
            }
        }
        
        stats.average_length = (double)stats.total_characters / processor->line_count;
    }
    
    return stats;
}

// Calculate mean length
double calculate_mean(char* data[], int count) {
    if (count == 0) return 0.0;
    
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += strlen(data[i]);
    }
    
    return (double)total / count;
}

// Find maximum length
int find_max_length(char* data[], int count) {
    if (count == 0) return 0;
    
    int max_len = 0;
    for (int i = 0; i < count; i++) {
        int len = strlen(data[i]);
        if (len > max_len) {
            max_len = len;
        }
    }
    
    return max_len;
}

// Find minimum length
int find_min_length(char* data[], int count) {
    if (count == 0) return 0;
    
    int min_len = strlen(data[0]);
    for (int i = 1; i < count; i++) {
        int len = strlen(data[i]);
        if (len < min_len) {
            min_len = len;
        }
    }
    
    return min_len;
}

// Trim whitespace from string
void trim_whitespace(char* str) {
    if (!str) return;
    
    // Trim leading whitespace
    char* start = str;
    while (isspace((unsigned char)*start)) {
        start++;
    }
    
    // Move string to start position
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
    
    // Trim trailing whitespace
    char* end = str + strlen(str) - 1;
    while (end >= str && isspace((unsigned char)*end)) {
        end--;
    }
    *(end + 1) = '\0';
}

// Convert string to uppercase
void to_uppercase(char* str) {
    if (!str) return;
    
    for (int i = 0; str[i]; i++) {
        str[i] = toupper((unsigned char)str[i]);
    }
}

// Main function
int main() {
    const char* test_filename = "input.txt";
    const char* output_filename = "output.txt";
    const char* processing_message = "Processing complete!";
    
    // Create processor instance
    DataProcessor* processor = create_processor(test_filename);
    if (!processor) {
        fprintf(stderr, "Failed to create processor\n");
        return 1;
    }
    
    // Load data
    printf("Loading data...\n");
    if (!load_data(processor)) {
        fprintf(stderr, "Failed to load data\n");
        free_processor(processor);
        return 1;
    }
    
    // Process data
    printf("Processing data...\n");
    process_data(processor);
    
    // Get statistics
    Statistics stats = get_statistics(processor);
    printf("Statistics:\n");
    printf("  Original lines: %d\n", stats.original_lines);
    printf("  Processed lines: %d\n", stats.processed_lines);
    printf("  Total characters: %d\n", stats.total_characters);
    printf("  Average length: %.2f\n", stats.average_length);
    printf("  Max length: %d\n", stats.max_length);
    printf("  Min length: %d\n", stats.min_length);
    
    // Calculate additional metrics
    printf("Additional metrics:\n");
    printf("  Mean length: %.2f\n", calculate_mean(processor->data, processor->line_count));
    printf("  Max length: %d\n", find_max_length(processor->processed_data, processor->processed_count));
    printf("  Min length: %d\n", find_min_length(processor->processed_data, processor->processed_count));
    
    // Save results
    printf("Saving results...\n");
    if (!save_results(processor, output_filename)) {
        fprintf(stderr, "Failed to save results\n");
        free_processor(processor);
        return 1;
    }
    
    printf("Results saved to %s\n", output_filename);
    
    // Display constants
    printf("Constants:\n");
    printf("  Magic number: %d\n", MAGIC_NUMBER);
    printf("  Pi value: %.5f\n", PI_VALUE);
    printf("  Message: %s\n", processing_message);
    
    // Test some calculations
    int test_value = 100;
    double result = (double)test_value * PI_VALUE / MAGIC_NUMBER;
    printf("Test calculation: %.2f\n", result);
    
    // Test array operations
    int numbers[10];
    for (int i = 0; i < 10; i++) {
        numbers[i] = i + 1;
    }
    
    int sum = 0;
    int product = 1;
    for (int i = 0; i < 10; i++) {
        sum += numbers[i];
        product *= numbers[i];
    }
    
    printf("Array operations:\n");
    printf("  Numbers: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    printf("  Sum: %d\n", sum);
    printf("  Product: %d\n", product);
    
    // Test string operations
    char test_string[] = "Hello, C!";
    char reversed[256];
    int len = strlen(test_string);
    
    for (int i = 0; i < len; i++) {
        reversed[i] = test_string[len - 1 - i];
    }
    reversed[len] = '\0';
    
    printf("String operations:\n");
    printf("  Original: %s\n", test_string);
    printf("  Reversed: %s\n", reversed);
    
    to_uppercase(test_string);
    printf("  Uppercased: %s\n", test_string);
    
    printf("Program completed successfully!\n");
    
    // Clean up
    free_processor(processor);
    
    return 0;
}
