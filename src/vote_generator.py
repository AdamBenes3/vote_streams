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

class vote_generator():
    def generate_exponential_distribution(lambda_ : int, number_bins : int, number_items : int, 
    max_: float = None, min_ : int = 0, print_ : bool= False, plot : bool= False, normalize_result : bool = True) -> Union[float, List]:
        """
        Generates an Exponential distribution with the specified parameters.

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

    def generate_zipfian_distribution(alpha: float, number_bins: int, number_items: int, 
    max_: float = None, min_: int = 1, print_: bool = False, plot: bool = False, normalize_result: bool = True) -> Union[float, List]:
        """
        Generates a Zipfian distribution with the specified parameters.

        Args:
            alpha (float): The parameter that characterizes the Zipf distribution (greater than 1).
            number_bins (int): Number of bins for the result.
            number_items (int): Total number of items to generate.
            max_ (int, optional): Maximum value for the range. Defaults to None.
            min_ (int, optional): Minimum value for the range. Defaults to 1.
            print_ (bool, optional): Whether to print the result. Defaults to False.
            plot (bool, optional): Whether to plot the result. Defaults to False.
            normalize_result (bool, optional): Whether to normalize the result. Defaults to True.

        Returns:
            Union[float, List]: Normalized or non-normalized result based on the normalize_result flag.
        """

        if max_ is None:
            max_ = number_bins + min_ - 1
        
        # Generate ranks for the Zipfian distribution
        ranks = np.arange(min_, max_ + 1)

        # Compute the expected frequencies using the Zipf PMF
        zipf_pmf = 1 / np.power(ranks, alpha)
        zipf_pmf /= zipf_pmf.sum()  # Normalize to create a probability distribution

        # Scale probabilities by number of items
        result = zipf_pmf * number_items

        if normalize_result:
            result_normalized = result / number_items
        else:
            result_normalized = result

        if print_:
            print(f"Result: {result}")
            print(f"Sum: {result.sum()}")

        if plot:
            plt.figure(figsize=(10, 6))
            categories = np.arange(1, number_bins + 1)
            nth = 3
            x_ticks_positions = categories[::nth]
            x_ticks_labels = categories[::nth]

            plt.bar(categories + 0.2, result_normalized[:number_bins], width=0.4, label='Model', align='center')
            plt.xlabel('Category')
            plt.ylabel('Normalized Frequency')
            plt.title('Zipfian Distribution')
            plt.xticks(ticks=x_ticks_positions, labels=x_ticks_labels)
            plt.legend()
            plt.show()

        if normalize_result:
            return result_normalized
        else:
            return result

    def simulate_voting(number_voters, number_of_alternatives, type_dist):
        lambda_ = 0.035  # Parameter for exponential distribution
        alpha_ = 1  # Parameter for Zipfian distribution
        number_items = 1000000

        # Generate probabilities based on the selected distribution type
        if type_dist == "exp":
            probabilities = vote_generator.generate_exponential_distribution(lambda_, number_of_alternatives, number_items)
        elif type_dist == "zipf":
            probabilities = vote_generator.generate_zipfian_distribution(alpha_, number_of_alternatives, number_items)
        else:
            raise ValueError("Invalid distribution type. Use 'exp' or 'zipf'.")

        # Normalize probabilities
        probabilities /= probabilities.sum()

        vote_indices = []

        for _ in range(number_voters):
            remaining_candidates = np.arange(1, number_of_alternatives + 1)
            current_probabilities = probabilities.copy()
            vote_order = []

            for _ in range(number_of_alternatives):
                # Choose a candidate
                chosen_candidate = np.random.choice(remaining_candidates, p=current_probabilities)

                # Append
                vote_order.append(chosen_candidate)

                # Remove chosen candidate
                mask = remaining_candidates != chosen_candidate
                remaining_candidates = remaining_candidates[mask]
                current_probabilities = current_probabilities[mask]

                # Rescale
                if current_probabilities.size > 0:
                    current_probabilities /= current_probabilities.sum()

            vote_indices.append(vote_order)

        current_date = datetime.now().strftime("%Y-%m-%d")

        # Prepare file output with metadata and votes
        file_output = f"""# FILE NAME: simulated-votes
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

        for i in range(1, number_of_alternatives + 1):
            file_output += f"# ALTERNATIVE NAME {i}: alternative_{i}\n"

        for i, votes in enumerate(vote_indices, start=1):
            vote_line = ", ".join(map(str, votes))
            file_output += f"1: {vote_line}\n"

        # Trim the last newline if needed
        file_output = file_output[:-1]

        return file_output
