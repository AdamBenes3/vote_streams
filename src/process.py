# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)


from src.misra_gries import Misra_Gries

from src.sampling import sampling

from src.vote_generator import vote_generator

from src.error_finders.copeland_error import copeland_error
from src.error_finders.maximin_error import maximin_error
from src.error_finders.plurality_error import plurality_error
from src.error_finders.stv_error import stv_error

from src.process_file import process_file

import tempfile
import ast

class process:
    def wrong_input(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int) -> int:
        """Validates input parameters for processing votes. Returns 1 if validation fails, else 0."""
        try:
            sampling_k = int(sampling_k) if sampling_bool else None
            misra_k = int(misra_k) if misra_bool else None
        except ValueError:
            print("Input Error", "Please enter valid integer values for k.")
            return 1
        if sampling_bool and (sampling_k is None or sampling_k <= 0):
            print("Input Error", "Please enter a valid integer value greater than 0 for k (Sampling).")
            return 1
        if misra_bool and (misra_k is None or misra_k <= 0):
            print("Input Error", "Please enter a valid integer value greater than 0 for k (Misra-Gries).")
            return 1
        if not input_path or not output_path:
            print("Warning", "Paths not properly selected.")
            return
        if (sampling_bool and misra_bool):
            print("Cant enable both Sampling and Misra Gries!")
            return 1
        return 0


    def aply_sampling_or_misra(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int, sample_or_mg: any, votes_file: str, num_votes: int, num_alternatives: int) -> str:
        """Applies either Sampling or Misra-Gries algorithm to process votes. Returns formatted result as a string."""
        with open(os.path.abspath(votes_file), "r") as file:
            for line in file:
                # Skip comments or metadata lines
                if not (line.startswith("#")):
                    line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                    parts = line.split(':')
                    # Number of votes
                    multiplier = int(parts[0])
                    # Vote data
                    vote_data = "1: " + parts[1] + '\n'
                    for _ in range(multiplier):
                        if isinstance(sample_or_mg, sampling):
                            # Apply sampling update
                            sample_or_mg.update_R(vote_data)
                        if isinstance(sample_or_mg, Misra_Gries):
                            # Apply Misra-Gries update
                            sample_or_mg.misra_gries_update(vote_data)
        # Create temporary file to store output and process results
        with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
            if isinstance(sample_or_mg, sampling):
                output_string = "# Sampling used! Num of elements: " + str(num_votes // sampling_k) + '\n'
                output_string += "# Sampling used! k := " + str(sampling_k) + '\n'
                for item in sample_or_mg.S:
                    # Write sampled votes
                    temp_file.write(item)
            if isinstance(sample_or_mg, Misra_Gries):
                output_string = "# Misra Gries used! k := " + str(misra_k) + '\n'
                for item in sample_or_mg.H:
                    # Write Misra-Gries result
                    temp_file.write(item[1])
            temp_file.seek(0)
            output_string += process_file.process_file(temp_file, rule, input_path, num_alternatives)
            return output_string

    def aply_sampling(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int, votes_file: str, num_alternatives: int) -> str:
        """Initializes and applies Sampling algorithm for vote processing. Returns formatted result as a string."""
        # Get number of votes
        num_votes = int(process.get_line_second_part(os.path.abspath(votes_file), "# NUMBER VOTERS:"))
        # Initialize Sampling with required size
        sample = sampling(num_votes // sampling_k)
        return process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, sample, votes_file, num_votes, num_alternatives)

    def aply_misra_gries(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int, votes_file: str, num_alternatives: int) -> str:
        """Initializes and applies Misra-Gries algorithm for vote processing. Returns formatted result as a string."""
        # Get number of votes
        num_votes = int(process.get_line_second_part(os.path.abspath(votes_file), "# NUMBER VOTERS:"))
        # Initialize Misra-Gries
        mg = Misra_Gries(misra_k, True)
        return process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, mg, votes_file, num_votes, num_alternatives)

    def get_line_second_part(file_path: str, line: str) -> str:
        """Extracts lines second part (important part)."""
        try:
            with open(file_path, 'r') as file:
                for this_line in file:
                    # Check if the line starts with the relevant header
                    if this_line.startswith(line):
                        # Extract and return the second part
                        result = this_line.split(":")[1].strip()
                        return result
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
    
    def get_line(file_path: str, line: str) -> str:
        """Extracts line."""
        try:
            with open(file_path, 'r') as file:
                for this_line in file:
                    # Check if the line starts with the relevant header
                    if this_line.startswith(line):
                        # Extract and return the second part
                        return this_line
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")

    

    def procces_generating(output_path: str, num_votes: int, num_candidates: int, vote_type: str) -> int:
        """Generates votes based on specified parameters and saves to a file. Returns 1 if an error occurs, else 0."""
        vote_type = vote_type.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        try:
            with open(output_path, 'w') as file:
                if vote_type == "exp" or vote_type == "exponential":
                    output = vote_generator.simulate_voting(num_votes, num_candidates, "exp", file)
                if vote_type == "zipf" or vote_type == "zipfian":
                    output = vote_generator.simulate_voting(num_votes, num_candidates, "zipf", file)
            return 0
        except Exception as e:
            print(f"Error creating or writing to {output_path}: {e}")
            return 1

    def process_run(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int) -> int:
        """Runs the main vote processing workflow with the specified parameters, including Sampling or Misra-Gries if enabled."""
        error = process.wrong_input(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k)
        if error == 1:
            return 1
        # Normalize rule and other parameters
        rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        if sampling_k != None:
            sampling_k = int(sampling_k)
        if misra_k != None:
            misra_k = int(misra_k)
        # Iterate over the files in the folder
        nr = 0
        if type(input_path) != tuple:
            input_path = [input_path]
        for votes_file in input_path:
            output_string = "# Input path: " + os.path.abspath(votes_file) + "\n"
            output_string += "# Rule choosen: " + rule + "\n"
            # Check if the output path has an extension
            if '.' in output_path:
                # Separate the base file path and extension if it exists
                base_path, ext = output_path.rsplit('.', 1)
                output_filename = f"{base_path}{nr}.{ext}"
            else:
                # If no extension, assume ".txt" by default
                base_path = output_path
                output_filename = f"{base_path}{nr}.txt"
            
            with open(output_filename, 'w') as output_file:
                # Skip the info file
                if (votes_file == "info.txt"):
                    continue
                num_alternatives = int(process.get_line_second_part(os.path.abspath(votes_file), "# NUMBER ALTERNATIVES:"))
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1
                # Apply either sampling or Misra-Gries, or the selected voting rule
                if sampling_bool:
                    output_string += process.aply_sampling(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives)
                    output_file.write(output_string)
                else:
                    if misra_bool:
                        output_string += process.aply_misra_gries(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives)
                        output_file.write(output_string)
                    else:
                        output_string += process_file.process_file(votes_file, rule, input_path, num_alternatives)
                        output_file.write(output_string)
            nr += 1
        return 0

    

    def process_error(input_path1: str, input_path2: str, output_path: str) -> int:
        """Compares two processed files. Outputs results and errors to a specified file."""
        output_string = "# First file:" + os.path.abspath(input_path1) + '\n' + "# Second file:" + os.path.abspath(input_path2) + '\n'

        # Get origin path for first file
        origin_path1 = process.get_line_second_part(input_path1,"# Input path:")

        # Get origin path for second file
        origin_path2 = process.get_line_second_part(input_path2, "# Input path:")

        # Check if the paths do not match
        if (origin_path1 != origin_path2):
            print("Doesnt come from same file.")
            return 1
        
        origin_path = origin_path1

        print(origin_path)

        with open(origin_path, 'r') as file_r:
            # Go to the end of the file and check the last line
            lines = file_r.readlines()
            # If last line is not empty
            if lines[-1][-1] != "\n":
                with open(origin_path, 'a') as file_a:
                    # Add a newline at the end
                    file_a.write("\n")


        # Get rule for first file
        rule1 = process.get_line_second_part(input_path1, "# Rule choosen:")

        # Get rule for second file
        rule2 = process.get_line_second_part(input_path2, "# Rule choosen:")

        # Check if the rules do not match
        if (rule1 != rule2):
            print("Doesnt have same rule.")
            return 1
        
        rule = rule1

        nr_candidates = int(process.get_line_second_part(origin_path1, "# NUMBER ALTERNATIVES:"))
        
        with open(output_path, 'w') as output_file:
            if rule == "copeland":
                with open(input_path1, 'r') as file:
                    # Read all lines and filter out empty lines (after stripping whitespace)
                    non_empty_lines = [line.strip() for line in file if line.strip()]
                    result1 = non_empty_lines[-1] if non_empty_lines else None
                with open(input_path2, 'r') as file:
                    # Read all lines and filter out empty lines (after stripping whitespace)
                    non_empty_lines = [line.strip() for line in file if line.strip()]
                    result2 = non_empty_lines[-1] if non_empty_lines else None
                ERROR = copeland_error.copeland_error(result1, result2, origin_path, nr_candidates)
            if rule == "maximin":
                with open(input_path1, 'r') as file:
                    # Read all lines and filter out empty lines (after stripping whitespace)
                    non_empty_lines = [line.strip() for line in file if line.strip()]
                    result1 = non_empty_lines[-1] if non_empty_lines else None
                with open(input_path2, 'r') as file:
                    # Read all lines and filter out empty lines (after stripping whitespace)
                    non_empty_lines = [line.strip() for line in file if line.strip()]
                    result2 = non_empty_lines[-1] if non_empty_lines else None
                ERROR = maximin_error.maximin_error(result1, result2, origin_path, nr_candidates)
            if rule == "plurality":
                result1 = ast.literal_eval(process.get_line(input_path1, "["))
                result2 = ast.literal_eval(process.get_line(input_path2, "["))
                ERROR = plurality_error.plurality_error(result1, result2, origin_path, nr_candidates)
            if rule == "stv":
                result1 = ast.literal_eval(process.get_line(input_path1, "["))
                result2 = ast.literal_eval(process.get_line(input_path2, "["))
                ERROR = stv_error.stv_error(result1, result2, origin_path, nr_candidates)
            # print(ERROR)
            output_string += "Error: " + str(ERROR)
            output_file.write(output_string + "\n")
        return 0