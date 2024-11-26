# Package Sorting System

A Python implementation of a package sorting system for a robotic automation factory. This system helps robotic arms dispatch packages to the correct stack based on their physical properties (volume, dimensions, and mass).

> **NOTE**: Tried to use Replit: curiously, the webpage didn't want to respond to my mouse clicks.

## Problem Description

The system sorts packages into three categories based on their properties:

- **STANDARD**: Normal packages that are neither bulky nor heavy
- **SPECIAL**: Packages that are either bulky or heavy (but not both)
- **REJECTED**: Packages that are both bulky and heavy

### Classification Rules

A package is classified as:
- **Bulky** if either:
  - Volume (Width × Height × Length) ≥ 1,000,000 cm³, OR
  - Any dimension ≥ 150 cm
- **Heavy** if:
  - Mass ≥ 20 kg

## Implementation Details

The solution is implemented in Python with a robust, production-ready approach:

### Core Features

1. **Input Validation**:
   - Handles numeric and string inputs (including Unicode numbers)
   - Validates against minimum and maximum bounds
   - Removes whitespace from string inputs
   - Comprehensive type checking

2. **Error Handling**:
   - Custom `PackageError` exception with descriptive messages
   - Handles overflow errors
   - Validates special float values (inf, nan)
   - Proper bounds checking

3. **Performance Optimizations**:
   - Cached properties for volume and maximum dimension calculations
   - Efficient string normalization
   - Memory-efficient implementation

### Code Structure

The implementation consists of two main files:

1. `package_sorter.py`: Contains the main sorting logic
   - `Package` class for robust package handling
   - `sort()` function for simple interface
   - Constants for all threshold values

2. `test_package_sorter.py`: Comprehensive test suite
   - Basic functionality tests
   - Edge case handling
   - Input validation
   - Precision tests

## Usage

### Basic Usage

```python
from package_sorter import sort

# Standard package
result = sort(100, 100, 50, 10)  # Returns "STANDARD"

# Bulky package (by dimension)
result = sort(150, 50, 50, 10)   # Returns "SPECIAL"

# Heavy package
result = sort(100, 100, 50, 20)  # Returns "SPECIAL"

# Rejected package (both bulky and heavy)
result = sort(150, 150, 150, 25) # Returns "REJECTED"
```

### Advanced Features

```python
# String input handling
result = sort("100", "100", "50", "10")  # Returns "STANDARD"

# Unicode number support
result = sort("１００", "100", "50", "10")  # Returns "STANDARD"

# Whitespace handling
result = sort(" 100 ", "100", "50", "10")  # Returns "STANDARD"
```

## Running Tests

To run the comprehensive test suite:

```bash
python3 -m unittest test_package_sorter.py -v
```

The test suite includes:
- Standard package scenarios
- Bulky package scenarios (both by volume and dimension)
- Heavy package scenarios
- Rejected package scenarios
- Edge cases at classification thresholds
- String input handling
- Floating-point precision cases
- Invalid input handling

## Requirements

- Python 3.6 or higher (for type hints support)
- No additional dependencies required

## Limitations and Bounds

- Maximum dimension: 1000 cm
- Maximum mass: 1000 kg
- Minimum values: Greater than system float epsilon
- All measurements must be positive, finite numbers
