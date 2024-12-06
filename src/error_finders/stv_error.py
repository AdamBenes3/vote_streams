# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import tempfile
import shutil
import atexit
import ast
from typing import List, Union

from src.process_file import process_file

class stv_error:

    def find_difference(origin_path : str, P : str, last_P_1 : str) -> int:
        """
        Finds the difference between how many times P and last_P_1 were ranked first.

        Args:
            origin_path (str): Path to the file containing voting data.
            P (int): Identifier for the first alternative to check.
            last_P_1 (int): Identifier for the second alternative to check.

        Returns:
            difference (int): Difference between count_P and count_last_P_1.
        """
        count_P = 0
        count_last_P_1 = 0

        with open(origin_path, 'r') as file:
            for line in file:
                # Skip lines that start with '#' as they are comments or metadata.
                if line.startswith('#'):
                    continue
                
                # Extract the rankings from the line.
                try:
                    times, rankings = line.split(":")
                    rankings = rankings.strip().split(",")
                    
                    # Check if P or last_P_1 is ranked first.
                    if int(rankings[0]) == P:
                        count_P += int(times)
                    if int(rankings[0]) == last_P_1:
                        count_last_P_1 += int(times)
                except ValueError:
                    # Ignore lines that do not conform to the expected format.
                    continue

        # Calculate the difference.
        difference = count_P - count_last_P_1

        return difference

    def remove_comment_lines(input_string : str) -> str:
        """
        Removes lines starting with '#' from the input string.
        """
        # Split the string into lines, filter out lines starting with '#', and join the result
        filtered_lines = [line for line in input_string.splitlines() if not line.strip().startswith("#")]
        return "\n".join(filtered_lines)

    def create_temp_copy(file_path : str) -> str:
        """
        Create a temporary copy of the file and ensure it is deleted after the program ends.
        """
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        
        # Copy the content of the original file to the temporary file
        shutil.copy(file_path, temp_file.name)
        
        # Register cleanup function to delete the temp file at program exit
        def cleanup_temp_file():
            try:
                os.remove(temp_file.name)
                print(f"Temporary file deleted: {temp_file.name}")
            except FileNotFoundError:
                pass
    
        atexit.register(cleanup_temp_file)
        
        print(f"Temporary file created at: {temp_file.name}")
        return temp_file.name

    def turn_one(result1 : List[str], current_index : int, tempt_file : str, nr_candidates : int, how_many_times : int, ERROR : int) -> Union[List[str], int]:
        """
        Processes a single iteration of the STV algorithm adjustment.

        Args:
            result1 (list): Current result from the STV computation as a list of candidates.
            current_index (int): Index of the candidate to process in the current result.
            tempt_file (str): Path to the temporary file used for computations.
            nr_candidates (int): Number of candidates in the election.
            how_many_times (int) : Number of times that the vote should be there.
            ERROR (int) : Error value.

        Returns:
            list: Updated result1 after processing the specified candidate.
            ERROR (int) : Value of error.
        """
        with open(tempt_file, 'a') as tmp:
            if how_many_times > 0:
                for _ in range(how_many_times):
                    ERROR += 1
                    tmp.write("1: " + str(result1[current_index]) + '\n')
        # Process the temporary file using the STV method.
        result1 = process_file.process_file(tempt_file, "stv", tempt_file, nr_candidates)
        result1 = stv_error.remove_comment_lines(result1)
        result1 = ast.literal_eval(result1)
        return result1, ERROR

    def mismatch_action(P, result1 : List[str], tempt_file : str, nr_candidates : int, i : int, ERROR : int, origin_path : str) -> Union[int, int]:
        """
        Resolves a mismatch between `result1` and `result2` by adjusting the position of a candidate.

        Args:
            P (any): Candidate from `result2` that is not in the correct position in `result1`.
            result1 (list): Current result from the STV computation as a list of candidates.
            result2 (list): Target result to match, as a list of candidates.
            tempt_file (str): Path to the temporary file used for computations.
            nr_candidates (int): Number of candidates in the election.
            i (int): Index (from the end) of the mismatched candidate in the results.
            ERROR (int): Current count of errors (iterations).
            origin_path (str) : Path to the origin file.

        Returns:
            tuple: Updated `result1` and incremented `ERROR`.
        """
        last_P_1 = result1[-i]
        # Adjust result1 until P is correctly positioned relative to last_P_1.
        while result1.index(P) < result1.index(last_P_1):
            how_many_times = stv_error.find_difference(origin_path, P, last_P_1)
            if how_many_times == 0:
                how_many_times = 1
            result1, ERROR = stv_error.turn_one(result1, result1.index(last_P_1), tempt_file, nr_candidates, how_many_times, ERROR)
        return result1, ERROR

    def get_count(file_path : str) -> bool:
        """
        Get if the number of lines is more then 100.
        """
        line_count = 0
        with open(file_path, 'rb') as f:
            for _ in f:
                line_count += 1
                if line_count > 100:
                    return False
        return True

    def stv_error(result1 : List[str], result2 : List[str], origin_path : str, nr_candidates : int) -> int:
        """
        Iteratively adjusts the STV computation until `result1` matches `result2`.

        Args:
            result1 (list): Initial result from the STV computation as a list of candidates.
            result2 (list): Target result to achieve, as a list of candidates.
            origin_path (str): Path to the original file containing voting data.
            nr_candidates (int): Number of candidates in the election.

        Returns:
            int: The number of iterations (errors) required to make the results match.
        """
        tempt_file = stv_error.create_temp_copy(origin_path)
        ERROR = 0
        while result1 != result2:
            for i in range(1, len(result2) + 1):
                # Compare candidates in reverse order.
                if result1[-i] != result2[-i]:
                    # If a mismatch is detected, resolve it.
                    P = result2[-i]
                    result1, ERROR = stv_error.mismatch_action(P, result1, tempt_file, nr_candidates, i, ERROR, origin_path)
                    break
        if stv_error.get_count(tempt_file):
            with open(tempt_file, 'r') as tmp:
                for line in tmp:
                    print(line, end="")
        return ERROR