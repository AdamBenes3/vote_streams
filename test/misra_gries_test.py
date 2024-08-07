# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import unittest
from collections import Counter

# Import functions to test
from src.misra_gries import misra_gries, misra_gries_with_heap

class misra_gries_test(unittest.TestCase):
    def test_misra_gries1(self):
        # Test case 1
        input_array_1 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_1 = 2
        expected_output_1 = [4]  # Expected output dictionary
        self.assertEqual(misra_gries(k_1, input_array_1).sort(), expected_output_1.sort())
        
    def test_misra_gries2(self):
        # Test case 2
        input_array_2 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_2 = 3
        expected_output_2 = [4, 5]
        self.assertEqual(misra_gries(k_2, input_array_2).sort(), expected_output_2.sort())
        
    def test_misra_gries3(self):
        # Test case 3
        input_array_3 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_3 = 3
        expected_output_3 = ['a', 'd']
        self.assertEqual(misra_gries(k_3, input_array_3).sort(), expected_output_3.sort())
        
    def test_misra_gries4(self):
        # Test case 4
        input_array_4 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_4 = 4
        expected_output_4 = ['a', 'd', 'f']
        self.assertEqual(misra_gries(k_4, input_array_4).sort(), expected_output_4.sort())

    def test_misra_gries_with_heap1(self):
        # Test case 1
        input_array_1 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_1 = 2
        expected_output_1 = [4]  # Expected output dictionary
        self.assertEqual(misra_gries_with_heap(k_1, input_array_1).sort(), expected_output_1.sort())
        
    def test_misra_gries_with_heap2(self):
        # Test case 2
        input_array_2 = [1, 4, 5, 4, 4, 5, 4, 4]
        k_2 = 3
        expected_output_2 = [4, 5]
        self.assertEqual(misra_gries_with_heap(k_2, input_array_2).sort(), expected_output_2.sort())
        
    def test_misra_gries_with_heap3(self):
        # Test case 3
        input_array_3 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_3 = 3
        expected_output_3 = ['a', 'd']
        self.assertEqual(misra_gries_with_heap(k_3, input_array_3).sort(), expected_output_3.sort())
        
    def test_misra_gries_with_heap4(self):
        # Test case 4
        input_array_4 = ['a', 'b', 'a', 'c', 'd', 'e', 'a', 'd', 'f', 'a', 'd']
        k_4 = 4
        expected_output_4 = ['a', 'd', 'f']
        self.assertEqual(misra_gries_with_heap(k_4, input_array_4).sort(), expected_output_4.sort())
        
        

if __name__ == '__main__':
    unittest.main()
