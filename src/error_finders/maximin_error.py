# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import tempfile
import shutil
import atexit
from typing import List

from src.process_file import process_file


class maximin_error:
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

    def turn_one(result1 : List[str], result2 : List[str], tempt_file : str, nr_candidates : int) -> List[str]:
        """
        Processes a single iteration of the maximin algorithm adjustment.

        Args:
            result1 (str): Current result from the maximin computation.
            result2 (str): Target result to match.
            tempt_file (str): Path to the temporary file used for computations.
            nr_candidates (int): Number of candidates in the election.

        Returns:
            str: Updated result1 after processing the file.
        """
        result_as_string = str(result2)
        with open(tempt_file, 'a') as tmp:
            tmp.write("1: " + result_as_string + '\n')
        # This updates result1 based on the new contents of the temporary file.
        result1 = process_file.process_file(tempt_file, "maximin", tempt_file, nr_candidates)
        result1 = maximin_error.remove_comment_lines(result1)
        return result1

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

    def maximin_error(result1 : List[str], result2 : List[str], origin_path : str, nr_candidates : int) -> int:
        """
        Iteratively adjusts the maximin computation until the results match.

        Args:
            result1 (str): Initial result from the maximin computation.
            result2 (str): Target result to achieve.
            origin_path (str): Path to the original file containing voting data.
            nr_candidates (int): Number of candidates in the election.

        Returns:
            int: The number of iterations (errors) required to make the results match.
        """
        tempt_file = maximin_error.create_temp_copy(origin_path)
        ERROR = 0
        while result1 != result2:
            ERROR += 1
            # Perform a single adjustment iteration.
            result1 = maximin_error.turn_one(result1, result2, tempt_file, nr_candidates)
        if maximin_error.get_count(tempt_file):
            with open(tempt_file, 'r') as tmp:
                for line in tmp:
                    print(line, end="")
        return ERROR