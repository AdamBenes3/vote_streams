# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.plurality_parse import Plurality_parse
from src.preflib_vote_parsers.stv_parse import STV_parse
from src.preflib_vote_parsers.copeland_parse import Copeland_parse
from src.preflib_vote_parsers.minimax_parse import Minimax_parse

from src.misra_gries import Misra_Gries

from src.sampling import sampling

from src.vote_generator import vote_generator

import tempfile

import time

class Process:

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
        with open(input_path + "/" + votes_file, "r") as file:
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
                for item in sample_or_mg.S:
                    # Write sampled votes
                    temp_file.write(item)
            if isinstance(sample_or_mg, Misra_Gries):
                output_string = "# Misra Gries used! k := " + str(misra_k) + '\n'
                for item in sample_or_mg.H:
                    # Write Misra-Gries result
                    temp_file.write(item)
            temp_file.seek(0)
            output_string += Process.process_file(temp_file, rule, input_path, num_alternatives)
            return output_string

    def aply_sampling(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int, votes_file: str, num_alternatives: int) -> str:
        """Initializes and applies Sampling algorithm for vote processing. Returns formatted result as a string."""
        # Get number of votes
        num_votes = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER VOTERS:"))
        # Initialize Sampling with required size
        sample = sampling(num_votes // sampling_k)
        print("Num of elements: " + str(num_votes // sampling_k))
        return Process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, sample, votes_file, num_votes, num_alternatives)

    def aply_misra_gries(input_path: str, output_path: str, rule: str, sampling_bool: bool, misra_bool: bool, sampling_k: int, misra_k: int, votes_file: str, num_alternatives: int) -> str:
        """Initializes and applies Misra-Gries algorithm for vote processing. Returns formatted result as a string."""
        # Get number of votes
        num_votes = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER VOTERS:"))
        # Initialize Misra-Gries
        mg = Misra_Gries(misra_k, True)
        print("k := " + str(misra_k))
        return Process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, mg, votes_file, num_votes, num_alternatives)

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

    def aply_one_rule(pap: any, file: any) -> str:
        """Applies a voting rule to the provided file. Returns the results formatted as a string."""
        # Measure time
        time_before = time.time()
        for line in file:
            # Process each line using the parser
            Process.process_line(line, pap)
        # Get the result of processing
        result = Process.get_result(pap)
        time_after = time.time()
        output_string = "# Time computing: " + str(time_after - time_before) + "\n"
        output_string += str(result) + "\n"
        return output_string


    def process_line(line: str, pap: any) -> None:
        """Processes a single line in the voting data, sending it to the specified parser (pap) if it contains vote data."""
        # Skip the metadata
        if not (line.startswith("#")):
            line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
            # Send vote line to parser
            pap.input_line(line)

    def get_result(pap: any) -> any:
        """Retrieves and returns the result of processed votes from the parser (pap)."""
        # Get result from the parser
        result = pap.result()
        return result

    def process_file(votes_file: any, rule: str, input_path: str, num_alternatives: int) -> str:
        """Processes a file using a specified voting rule. Returns formatted results as a string."""
        # Initialize parsers for different voting rules
        plurality_parse = Plurality_parse(list(range(1, num_alternatives + 1)))
        stv_parse = STV_parse(list(range(1, num_alternatives + 1)))
        copeland_parse = Copeland_parse([str(x) for x in range(1, num_alternatives + 1)])
        minimax_parse = Minimax_parse([str(x) for x in range(1, num_alternatives + 1)])
        output_string = ""
        if isinstance(votes_file, str):
            # Skip the info file
            if not (votes_file == "info.txt"):
                with open(input_path + "/" + votes_file, "r") as file:
                    if rule == "plurality":
                        output_string = Process.aply_one_rule(plurality_parse, file)
                    if rule == "stv":
                        output_string = Process.aply_one_rule(stv_parse, file)
                    if rule == "copeland":
                        output_string = Process.aply_one_rule(copeland_parse, file)
                    if rule == "minimax":
                        output_string = Process.aply_one_rule(minimax_parse, file)
        else:
            votes_file.seek(0)
            if rule == "plurality":
                output_string = Process.aply_one_rule(plurality_parse, votes_file)
            if rule == "stv":
                output_string = Process.aply_one_rule(stv_parse, votes_file)
            if rule == "copeland":
                output_string = Process.aply_one_rule(copeland_parse, votes_file)
            if rule == "minimax":
                output_string = Process.aply_one_rule(minimax_parse, votes_file)
        return output_string

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
        error = Process.wrong_input(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k)
        if error == 1:
            return 1
        # Normalize rule and other parameters
        rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        sampling_k = int(sampling_k)
        misra_k = int(misra_k)
        # Get list of vote files
        vote_files = os.listdir(input_path)
        # Iterate over the files in the folder
        nr = 0
        for votes_file in vote_files:
            output_string = "# Input path: " + os.path.abspath(input_path) + "/" + votes_file + "\n"
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
                num_alternatives = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER ALTERNATIVES:"))
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1
                # Apply either sampling or Misra-Gries, or the selected voting rule
                if sampling_bool:
                    output_string += Process.aply_sampling(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives)
                    output_file.write(output_string)
                else:
                    if misra_bool:
                        output_string += Process.aply_misra_gries(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives)
                        output_file.write(output_string)
                    else:
                        output_string += Process.process_file(votes_file, rule, input_path, num_alternatives)
                        output_file.write(output_string)
            nr += 1
        return 0

    

    def process_error(input_path1: str, input_path2: str, output_path: str) -> int:
        """Compares two processed files. Outputs results and errors to a specified file."""
        output_string = "# First file:" + os.path.abspath(input_path1) + '\n' + "# Second file:" + os.path.abspath(input_path2) + '\n' + "0"

        # Get origin path for first file
        origin_path1 = Process.get_line_second_part(input_path1,"# Input path:")

        # Get origin path for second file
        origin_path2 = Process.get_line_second_part(input_path2, "# Input path:")

        # Get rule for first file
        rule1 = Process.get_line_second_part(input_path1, "# Rule choosen:")

        # Get rule for second file
        rule2 = Process.get_line_second_part(input_path2, "# Rule choosen:")

        # Check if the paths or rules do not match
        if (origin_path1 != origin_path2):
            print("Doesnt come from same file.")
            return 1
        if (rule1 != rule2):
            print("Doesnt have same rule.")
            return 1
        
        # If no errors, write output string
        origin_path = origin_path1
        rule = rule1
        with open(output_path, 'w') as output_file:
            print(origin_path, rule)
            output_file.write(output_string + "\n")
        return 0