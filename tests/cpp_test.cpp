/*
 * C++ Test File for PyMorph Obfuscation
 * Test file with proper .cpp extension
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iomanip>

class DataProcessor {
private:
    std::string filename;
    std::vector<std::string> data;
    std::vector<std::string> processed_data;
    
public:
    // Constructor
    DataProcessor(const std::string& fname) : filename(fname) {}
    
    // Load data from file
    bool loadData() {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Error: File " << filename << " not found" << std::endl;
            return false;
        }
        
        std::string line;
        while (std::getline(file, line)) {
            if (!line.empty()) {
                data.push_back(line);
            }
        }
        
        file.close();
        return true;
    }
    
    // Process the loaded data
    std::vector<std::string> processData() {
        processed_data.clear();
        for (const auto& line : data) {
            std::string processed_line = "PROCESSED: " + line;
            std::transform(processed_line.begin(), processed_line.end(), 
                          processed_line.begin(), ::toupper);
            processed_data.push_back(processed_line);
        }
        return processed_data;
    }
    
    // Save processed data to file
    bool saveResults(const std::string& output_filename) {
        std::ofstream file(output_filename);
        if (!file.is_open()) {
            std::cerr << "Error: Cannot create output file" << std::endl;
            return false;
        }
        
        for (const auto& line : processed_data) {
            file << line << std::endl;
        }
        
        file.close();
        return true;
    }
    
    // Get processing statistics
    struct Statistics {
        int original_lines;
        int processed_lines;
        int total_characters;
        double average_length;
    };
    
    Statistics getStatistics() const {
        Statistics stats;
        stats.original_lines = data.size();
        stats.processed_lines = processed_data.size();
        stats.total_characters = std::accumulate(data.begin(), data.end(), 0,
            [](int sum, const std::string& line) { return sum + line.length(); });
        stats.average_length = stats.original_lines > 0 ? 
            static_cast<double>(stats.total_characters) / stats.original_lines : 0.0;
        return stats;
    }
    
    // Get filename
    std::string getFilename() const {
        return filename;
    }
    
    // Get data size
    size_t getDataSize() const {
        return data.size();
    }
};

// Utility functions
namespace utils {
    double calculateMean(const std::vector<std::string>& data) {
        if (data.empty()) return 0.0;
        
        int total = std::accumulate(data.begin(), data.end(), 0,
            [](int sum, const std::string& line) { return sum + line.length(); });
        return static_cast<double>(total) / data.size();
    }
    
    int findMaxLength(const std::vector<std::string>& data) {
        if (data.empty()) return 0;
        
        auto max_it = std::max_element(data.begin(), data.end(),
            [](const std::string& a, const std::string& b) {
                return a.length() < b.length();
            });
        return max_it->length();
    }
    
    int findMinLength(const std::vector<std::string>& data) {
        if (data.empty()) return 0;
        
        auto min_it = std::min_element(data.begin(), data.end(),
            [](const std::string& a, const std::string& b) {
                return a.length() < b.length();
            });
        return min_it->length();
    }
}

// Constants
const int MAGIC_NUMBER = 42;
const double PI_VALUE = 3.14159;
const std::string PROCESSING_MESSAGE = "Processing complete!";

int main() {
    // Test parameters
    const std::string test_filename = "input.txt";
    const std::string output_filename = "output.txt";
    
    // Create processor instance
    DataProcessor processor(test_filename);
    
    // Load data
    std::cout << "Loading data..." << std::endl;
    if (!processor.loadData()) {
        std::cerr << "Failed to load data" << std::endl;
        return 1;
    }
    
    // Process data
    std::cout << "Processing data..." << std::endl;
    std::vector<std::string> processed_data = processor.processData();
    
    // Get statistics
    DataProcessor::Statistics stats = processor.getStatistics();
    std::cout << "Statistics:" << std::endl;
    std::cout << "  Original lines: " << stats.original_lines << std::endl;
    std::cout << "  Processed lines: " << stats.processed_lines << std::endl;
    std::cout << "  Total characters: " << stats.total_characters << std::endl;
    std::cout << "  Average length: " << std::fixed << std::setprecision(2) 
              << stats.average_length << std::endl;
    
    // Calculate additional metrics
    std::cout << "Additional metrics:" << std::endl;
    std::cout << "  Mean length: " << utils::calculateMean(processor.getDataSize() > 0 ? 
        std::vector<std::string>{"dummy"} : std::vector<std::string>()) << std::endl;
    std::cout << "  Max length: " << utils::findMaxLength(processed_data) << std::endl;
    std::cout << "  Min length: " << utils::findMinLength(processed_data) << std::endl;
    
    // Save results
    std::cout << "Saving results..." << std::endl;
    if (processor.saveResults(output_filename)) {
        std::cout << "Results saved to " << output_filename << std::endl;
    } else {
        std::cerr << "Failed to save results" << std::endl;
        return 1;
    }
    
    // Display constants
    std::cout << "Constants:" << std::endl;
    std::cout << "  Magic number: " << MAGIC_NUMBER << std::endl;
    std::cout << "  Pi value: " << PI_VALUE << std::endl;
    std::cout << "  Message: " << PROCESSING_MESSAGE << std::endl;
    
    // Test some calculations
    int test_value = 100;
    double result = test_value * PI_VALUE / MAGIC_NUMBER;
    std::cout << "Test calculation: " << result << std::endl;
    
    std::cout << "Program completed successfully!" << std::endl;
    return 0;
}
