/*
 * Rust Test File for PyMorph Obfuscation
 * Test file with proper .rs extension
 */

use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

struct DataProcessor {
    filename: String,
    data: Vec<String>,
    processed_data: Vec<String>,
}

impl DataProcessor {
    // Create new processor
    fn new(filename: &str) -> Self {
        DataProcessor {
            filename: filename.to_string(),
            data: Vec::new(),
            processed_data: Vec::new(),
        }
    }
    
    // Load data from file
    fn load_data(&mut self) -> Result<(), io::Error> {
        let file = File::open(&self.filename)?;
        let reader = BufReader::new(file);
        
        for line in reader.lines() {
            let line = line?;
            if !line.trim().is_empty() {
                self.data.push(line.trim().to_string());
            }
        }
        
        Ok(())
    }
    
    // Process the loaded data
    fn process_data(&mut self) -> &Vec<String> {
        self.processed_data.clear();
        
        for line in &self.data {
            let processed_line = format!("PROCESSED: {}", line.to_uppercase());
            self.processed_data.push(processed_line);
        }
        
        &self.processed_data
    }
    
    // Save processed data to file
    fn save_results(&self, output_filename: &str) -> Result<(), io::Error> {
        let mut file = File::create(output_filename)?;
        
        for line in &self.processed_data {
            writeln!(file, "{}", line)?;
        }
        
        Ok(())
    }
    
    // Get processing statistics
    fn get_statistics(&self) -> Statistics {
        let total_characters: usize = self.data.iter()
            .map(|line| line.len())
            .sum();
        
        let average_length = if self.data.is_empty() {
            0.0
        } else {
            total_characters as f64 / self.data.len() as f64
        };
        
        Statistics {
            original_lines: self.data.len(),
            processed_lines: self.processed_data.len(),
            total_characters,
            average_length,
        }
    }
    
    // Get data size
    fn get_data_size(&self) -> usize {
        self.data.len()
    }
}

// Statistics structure
#[derive(Debug)]
struct Statistics {
    original_lines: usize,
    processed_lines: usize,
    total_characters: usize,
    average_length: f64,
}

// Utility functions
mod utils {
    pub fn calculate_mean(data: &[String]) -> f64 {
        if data.is_empty() {
            return 0.0;
        }
        
        let total: usize = data.iter()
            .map(|line| line.len())
            .sum();
        
        total as f64 / data.len() as f64
    }
    
    pub fn find_max_length(data: &[String]) -> usize {
        if data.is_empty() {
            return 0;
        }
        
        data.iter()
            .map(|line| line.len())
            .max()
            .unwrap_or(0)
    }
    
    pub fn find_min_length(data: &[String]) -> usize {
        if data.is_empty() {
            return 0;
        }
        
        data.iter()
            .map(|line| line.len())
            .min()
            .unwrap_or(0)
    }
}

// Constants
const MAGIC_NUMBER: i32 = 42;
const PI_VALUE: f64 = 3.14159;
const PROCESSING_MESSAGE: &str = "Processing complete!";

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Test parameters
    let test_filename = "input.txt";
    let output_filename = "output.txt";
    
    // Create processor instance
    let mut processor = DataProcessor::new(test_filename);
    
    // Load data
    println!("Loading data...");
    if let Err(e) = processor.load_data() {
        eprintln!("Failed to load data: {}", e);
        return Err(e.into());
    }
    
    // Process data
    println!("Processing data...");
    let processed_data = processor.process_data();
    
    // Get statistics
    let stats = processor.get_statistics();
    println!("Statistics:");
    println!("  Original lines: {}", stats.original_lines);
    println!("  Processed lines: {}", stats.processed_lines);
    println!("  Total characters: {}", stats.total_characters);
    println!("  Average length: {:.2}", stats.average_length);
    
    // Calculate additional metrics
    println!("Additional metrics:");
    println!("  Mean length: {:.2}", utils::calculate_mean(&processor.data));
    println!("  Max length: {}", utils::find_max_length(processed_data));
    println!("  Min length: {}", utils::find_min_length(processed_data));
    
    // Save results
    println!("Saving results...");
    if let Err(e) = processor.save_results(output_filename) {
        eprintln!("Failed to save results: {}", e);
        return Err(e.into());
    }
    
    println!("Results saved to {}", output_filename);
    
    // Display constants
    println!("Constants:");
    println!("  Magic number: {}", MAGIC_NUMBER);
    println!("  Pi value: {}", PI_VALUE);
    println!("  Message: {}", PROCESSING_MESSAGE);
    
    // Test some calculations
    let test_value = 100;
    let result = test_value as f64 * PI_VALUE / MAGIC_NUMBER as f64;
    println!("Test calculation: {:.2}", result);
    
    // Test vector operations
    let numbers: Vec<i32> = (1..=10).collect();
    let sum: i32 = numbers.iter().sum();
    let product: i32 = numbers.iter().product();
    
    println!("Vector operations:");
    println!("  Numbers: {:?}", numbers);
    println!("  Sum: {}", sum);
    println!("  Product: {}", product);
    
    // Test string operations
    let test_string = "Hello, Rust!";
    let reversed: String = test_string.chars().rev().collect();
    let uppercased = test_string.to_uppercase();
    
    println!("String operations:");
    println!("  Original: {}", test_string);
    println!("  Reversed: {}", reversed);
    println!("  Uppercased: {}", uppercased);
    
    println!("Program completed successfully!");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_data_processor_creation() {
        let processor = DataProcessor::new("test.txt");
        assert_eq!(processor.get_data_size(), 0);
    }
    
    #[test]
    fn test_statistics() {
        let processor = DataProcessor::new("test.txt");
        let stats = processor.get_statistics();
        assert_eq!(stats.original_lines, 0);
        assert_eq!(stats.processed_lines, 0);
        assert_eq!(stats.total_characters, 0);
        assert_eq!(stats.average_length, 0.0);
    }
    
    #[test]
    fn test_utils_functions() {
        let data = vec![
            "short".to_string(),
            "medium length".to_string(),
            "very long string here".to_string(),
        ];
        
        assert_eq!(utils::find_max_length(&data), 21);
        assert_eq!(utils::find_min_length(&data), 5);
        assert!((utils::calculate_mean(&data) - 10.67).abs() < 0.1);
    }
}
