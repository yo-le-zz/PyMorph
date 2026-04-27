"""
Python Test File for PyMorph Obfuscation
Test file with proper .py extension
"""

import os
import sys
from typing import List, Dict, Optional

class DataProcessor:
    """Example class for testing Python obfuscation"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.data: List[str] = []
        self.processed_data: List[str] = []
    
    def load_data(self) -> bool:
        """Load data from file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = [line.strip() for line in file if line.strip()]
            return True
        except FileNotFoundError:
            print(f"Error: File {self.filename} not found")
            return False
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def process_data(self) -> List[str]:
        """Process the loaded data"""
        self.processed_data = []
        for line in self.data:
            # Convert to uppercase and add prefix
            processed_line = f"PROCESSED: {line.upper()}"
            self.processed_data.append(processed_line)
        return self.processed_data
    
    def save_results(self, output_filename: str) -> bool:
        """Save processed data to file"""
        try:
            with open(output_filename, 'w', encoding='utf-8') as file:
                for line in self.processed_data:
                    file.write(line + '\n')
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, int]:
        """Get processing statistics"""
        return {
            'original_lines': len(self.data),
            'processed_lines': len(self.processed_data),
            'total_characters': sum(len(line) for line in self.data)
        }

def calculate_metrics(data_list: List[str]) -> Dict[str, float]:
    """Calculate various metrics for the data"""
    if not data_list:
        return {'mean': 0.0, 'max': 0.0, 'min': 0.0}
    
    lengths = [len(line) for line in data_list]
    return {
        'mean': sum(lengths) / len(lengths),
        'max': max(lengths),
        'min': min(lengths)
    }

def main():
    """Main function to test the processor"""
    # Test data
    test_filename = "input.txt"
    output_filename = "output.txt"
    
    # Create processor instance
    processor = DataProcessor(test_filename)
    
    # Load data
    print("Loading data...")
    if not processor.load_data():
        print("Failed to load data")
        return 1
    
    # Process data
    print("Processing data...")
    processed_data = processor.process_data()
    
    # Get statistics
    stats = processor.get_statistics()
    print(f"Statistics: {stats}")
    
    # Calculate metrics
    metrics = calculate_metrics(processor.data)
    print(f"Metrics: {metrics}")
    
    # Save results
    print("Saving results...")
    if processor.save_results(output_filename):
        print(f"Results saved to {output_filename}")
    else:
        print("Failed to save results")
        return 1
    
    # Test with some constants
    magic_number = 42
    pi_value = 3.14159
    message = "Processing complete!"
    
    print(f"Magic number: {magic_number}")
    print(f"Pi value: {pi_value}")
    print(f"Message: {message}")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
