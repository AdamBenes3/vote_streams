# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import unittest

# Import test classes from separate files
from test.misra_gries_test import misra_gries_test
from test.sampling_test import sampling_test
from test.stv_test import stv_test
from test.plurality_test import plurality_test
from test.graph_voting_test import graph_voting_test

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(misra_gries_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(sampling_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(stv_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(plurality_test))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(graph_voting_test))

    # Run the test suite
    unittest.TextTestRunner().run(suite)
