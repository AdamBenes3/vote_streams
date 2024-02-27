import unittest
from collections import Counter

# Add parent directory to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import functions to test
from src.misra_gries import misra_gries

class sampling_test(unittest.TestCase):
    def test_misra_gries(self):
        # Test case 1
        input_array_1 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_1 = 2
        expected_output_1 = [4]  # Expected output dictionary
        self.assertEqual(misra_gries(k_1, input_array_1), expected_output_1)
        
        # Test case 2
        input_array_2 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_2 = 3
        expected_output_2 = [4, 5]
        self.assertEqual(misra_gries(k_2, input_array_2), expected_output_2)
        
        # Test case 3
        input_array_3 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_3 = 3
        expected_output_3 = ['a', 'd']
        self.assertEqual(misra_gries(k_3, input_array_3), expected_output_3)
        
        # Test case 4
        input_array_4 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_4 = 4
        expected_output_4 = ['a', 'd']
        self.assertEqual(misra_gries(k_4, input_array_4), expected_output_4)
        
        

if __name__ == '__main__':
    unittest.main()