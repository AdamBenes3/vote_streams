# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats
from typing import Union, List
from datetime import datetime

def generate_exponential_distribution(lambda_ : int, number_bins : int, number_items : int,
 max_: float = None, min_ : int = 0, print_ : bool= False, plot : bool= False, normalize_result : bool = True) -> Union[float, List]:
    """
    Generates an exponential distribution with the specified parameters.

    Args:
        lambda_ (int): Rate parameter of the exponential distribution.
        number_bins (int): Number of bins for the result.
        number_items (int): Total number of items to generate.
        max_ (int, optional): Maximum value for the range. Defaults to None.
        min_ (int, optional): Minimum value for the range. Defaults to 0.
        print_ (bool, optional): Whether to print the result. Defaults to False.
        plot (bool, optional): Whether to plot the result. Defaults to False.
        normalize_result (bool, optional): Whether to normalize the result. Defaults to False.

    Returns:
        Union[float, List]: Normalized or non-normalized result based on the normalize_result flag.
    """

    if max_ is None:
        max_ = 5 * (1 / lambda_)
    # Generate random numbers from an exponential distribution
    x_points = np.linspace(min_, max_, number_bins + 1)[1:]

    # Compute expected frequencies using the exponential CDF
    cumulative_expected = stats.expon.cdf(x_points, scale=1/lambda_) * number_items

    # Compute the differences between consecutive CDF values
    result = np.diff(cumulative_expected, prepend=0)
    result *= number_items / result.sum()

    # Normalize the observed and expected frequencies
    result_normalized = result / number_items

    if print_:
        # Printing
        print(f"Result: {result}")
        print(f"Sum: {result.sum()}")
    
    if plot:
        # Plotting
        categories = np.arange(1, number_bins + 1)
        nth = 3
        x_ticks_positions = categories[::nth]
        x_ticks_labels = categories[::nth]

        plt.figure(figsize=(10, 6))
        plt.bar(categories + 0.2, result_normalized, width=0.4, label='Model', align='center')
        plt.xlabel('Category')
        plt.ylabel('Normalized Frequency')
        plt.title('Result')
        plt.xticks(ticks=x_ticks_positions, labels=x_ticks_labels)
        plt.legend()
        plt.show()
    # Return list
    if normalize_result:
        return result_normalized
    else:
        return result

def simulate_exponential_voting(number_voters, number_of_alternatives):
    lambda_ = 0.03508771929824561 # Seems good
    number_items = 1000000
    probabilities = generate_exponential_distribution(lambda_, number_of_alternatives, number_items)

    print(probabilities)
    print()
    print()

    votes_per_voter = len(probabilities)

    vote_indices = np.random.choice(
        np.arange(1, votes_per_voter + 1),
        size=(number_voters, votes_per_voter),
        p=probabilities
    )

    current_date = datetime.now().strftime("%Y-%m-%d")


    file_output = f"""
# FILE NAME: simulated-votes
# TITLE: Simulated Voting Data
# DESCRIPTION: Generated based on a given probability distribution
# DATA TYPE: 
# MODIFICATION TYPE: original
# RELATES TO: 
# RELATED FILES: 
# PUBLICATION DATE: {current_date}
# MODIFICATION DATE: {current_date}
# NUMBER ALTERNATIVES: {number_of_alternatives}
# NUMBER VOTERS: {number_voters}
# NUMBER UNIQUE ORDERS: 
"""

    for i in range(1, votes_per_voter + 1):
        file_output += f"# ALTERNATIVE NAME {i}: alternative_{i}\n"

    for i, votes in enumerate(vote_indices, start=1):
        vote_line = ", ".join(map(str, votes))
        file_output += f"1: {vote_line}\n"

    file_output = file_output[:-1]

    return file_output

print(simulate_exponential_voting(100, 8))