import unittest
import math
import sys
from package_sorter import sort, PackageError, Package

class TestPackageSorter(unittest.TestCase):
    def test_standard_package(self):
        """Test a standard package (not bulky, not heavy)"""
        result = sort(100, 100, 50, 10)
        self.assertEqual(result, "STANDARD")
        
    def test_bulky_by_volume(self):
        """Test a package that is bulky by volume but not heavy"""
        result = sort(100, 100, 100, 10)  # 1,000,000 cm³
        self.assertEqual(result, "SPECIAL")
        
    def test_bulky_by_dimension(self):
        """Test a package that is bulky by dimension but not heavy"""
        result = sort(150, 50, 50, 10)
        self.assertEqual(result, "SPECIAL")
        
    def test_heavy_package(self):
        """Test a package that is heavy but not bulky"""
        result = sort(100, 100, 50, 20)
        self.assertEqual(result, "SPECIAL")
        
    def test_rejected_package(self):
        """Test a package that is both bulky and heavy"""
        result = sort(150, 150, 150, 25)
        self.assertEqual(result, "REJECTED")
        
    def test_edge_cases(self):
        """Test edge cases at the boundaries"""
        # Exactly at volume threshold (1,000,000 cm³)
        self.assertEqual(sort(100, 100, 100, 19), "SPECIAL")
        # Exactly at weight threshold (20 kg)
        self.assertEqual(sort(100, 100, 50, 20), "SPECIAL")
        # Exactly at dimension threshold (150 cm)
        self.assertEqual(sort(150, 50, 50, 19), "SPECIAL")

    def test_string_inputs(self):
        """Test string input handling"""
        # Normal string numbers
        self.assertEqual(sort("100", "100", "50", "10"), "STANDARD")
        
        # String numbers with whitespace
        self.assertEqual(sort(" 100 ", "100", "50", "10"), "STANDARD")
        
        # Unicode numbers (１００ is Unicode full-width "100")
        self.assertEqual(sort("１００", "100", "50", "10"), "STANDARD")
        
    def test_precision_edge_cases(self):
        """Test floating-point precision edge cases"""
        # Very close to thresholds
        self.assertEqual(sort(100, 100, 50, 19.999999999), "STANDARD")
        self.assertEqual(sort(149.999999999, 50, 50, 10), "STANDARD")
        
        # Very small valid numbers
        epsilon = sys.float_info.epsilon
        self.assertEqual(sort(1, 1, 1, epsilon * 2), "STANDARD")
        
        # Very large numbers (but within limits)
        self.assertEqual(sort(999, 999, 999, 999), "REJECTED")
        
    def test_invalid_inputs(self):
        """Test various invalid inputs"""
        invalid_cases = [
            # Below minimum
            (sys.float_info.epsilon/2, 100, 100, 10, "Must be greater than"),
            (100, sys.float_info.epsilon/2, 100, 10, "Must be greater than"),
            
            # Above maximum
            (Package.MAX_DIMENSION + 1, 100, 100, 10, "exceeds maximum limit"),
            (100, 100, 100, Package.MAX_MASS + 1, "exceeds maximum limit"),
            
            # Invalid strings
            ("abc", 100, 100, 10, "Must be a valid number"),
            (100, "12.34.56", 100, 10, "Must be a valid number"),
            
            # Invalid types
            ([], 100, 100, 10, "Must be a valid number"),
            (100, {}, 100, 10, "Must be a valid number"),
            (100, 100, None, 10, "Must be a valid number"),
            
            # Special float values
            (float('inf'), 100, 100, 10, "Must be a finite number"),
            (100, float('-inf'), 100, 10, "Must be a finite number"),
            (100, 100, float('nan'), 10, "Must be a finite number")
        ]
        
        for width, height, length, mass, expected_msg in invalid_cases:
            with self.subTest(f"Testing invalid input: {width}, {height}, {length}, {mass}"):
                with self.assertRaises(PackageError) as context:
                    sort(width, height, length, mass)
                self.assertIn(expected_msg, str(context.exception))

if __name__ == '__main__':
    unittest.main()
