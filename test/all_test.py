import unittest

# Import test classes from separate files
from misra_gries_test import misra_gries_test
from sampling_test import sampling_test
from stv_test import stv_test

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(misra_gries_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(sampling_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(stv_test))

    # Run the test suite
    unittest.TextTestRunner().run(suite)
