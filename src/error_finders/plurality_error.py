# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)


class plurality_error:
    def plurality_error(result1, result2, origin_path, nr_candidates):
        pass