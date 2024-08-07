# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from typing import Union, List

def generate_random_number_exponential_distribution(lmbd : int, size : int = 1) -> Union[int, List]:
    # Generate random numbers from an exponential distribution
    random_numbers = np.random.exponential(scale=1/lmbd, size=size)
    random_numbers_int = random_numbers.round().astype(int)
    if size == 1:
        return random_numbers_int[0]
    return random_numbers_int.tolist()
