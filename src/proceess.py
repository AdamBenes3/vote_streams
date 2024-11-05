# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.soc import parse_and_pass
from src.vote_rules.fast_rules.misra_gries_scoring_rules import MGSR

from src.sampling import sampling

from src.vote_generator import vote_generator

import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile


class Process:

    def get_number_of_alternatives(file_path):
        """Extracts the number of alternatives from the given file."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Check if the line starts with the relevant header
                    if line.startswith("# NUMBER ALTERNATIVES:"):
                        # Extract the number after the colon
                        num_alternatives = int(line.split(":")[1].strip())
                        return num_alternatives
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
            return None

    def get_number_of_votes(file_path):
        """Extracts the number of votes from the given file."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Check if the line starts with the relevant header
                    if line.startswith("# NUMBER VOTERS:"):
                        # Extract the number after the colon
                        num_votes = int(line.split(":")[1].strip())
                        return num_votes
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
            return None


    def procces_generating(output_path, num_votes, num_candidates, vote_type):

        vote_type = vote_type.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

        try:
            output = ""
            if vote_type == "exp" or vote_type == "exponential":
                output = vote_generator.simulate_voting(num_votes, num_candidates, "exp")
            if vote_type == "zipf" or vote_type == "zipfian":
                output = vote_generator.simulate_voting(num_votes, num_candidates, "zipf")
            with open(output_path, 'w') as file:
                file.write(output)
        except Exception as e:
            print(f"Error creating or writing to {output_path}: {e}")
            return 1

    def process_line(line, pap):
        # Skip the metadata
        if not (line.startswith("#")):
            line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
            line = line[2:]
            pap.input_line(line)
            result = pap.result()
            return result

    def process_file(votes_file, rule, input_path, num_alternatives):
        output_string = ""
        pap = parse_and_pass(list(range(1, num_alternatives + 1)))
        # Skip the info file
        if isinstance(votes_file, str):
            if not (votes_file == "info.txt"):
                if rule == "soc":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            result = Process.process_line(line, pap)
                    output_string += str(result) + "\n"
                    output_string += str(sorted(result, reverse = True)) + "\n"
                    return output_string
        else:
            if rule == "soc":
                votes_file.seek(0)
                for line in votes_file:
                    result = Process.process_line(line, pap)
                output_string += str(result) + "\n"
                output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string

    def process_run(input_path, output_path, rule, sampling_bool):

        rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

        
        with open(output_path, 'w') as output_file:
            output_string = ""

            vote_files = os.listdir(input_path)
            
            output_string += "Rule choosen: " + rule + "\n"
            
            # Iterate over the files in the folder
            for votes_file in vote_files:

                num_alternatives = Process.get_number_of_alternatives(input_path + "/" + votes_file)
                
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1
                
                if sampling_bool:
                    num_votes = Process.get_number_of_votes(input_path + "/" + votes_file)
                    pap = parse_and_pass(list(range(1, num_alternatives + 1)))
                    # Skip the info file
                    if (votes_file == "info.txt"):
                        continue
                    sample = sampling(num_votes // 3)
                    print("Num of ellements: " + str(num_votes // 3))
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            if not (line.startswith("#")):
                                line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                                sample.update_R(line + '\n')

                    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
                        for item in sample.S:
                            temp_file.write(item)
                        temp_file.seek(0)
                        
                        output_string += Process.process_file(temp_file, rule, input_path, num_alternatives)
                        output_file.write(output_string)          
                else:
                    output_string += Process.process_file(votes_file, rule, input_path, num_alternatives)
                    output_file.write(output_string)
