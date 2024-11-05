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

import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile


class Process:

    def get_rule(file_path):
        """Extracts rule."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Check if the line starts with the relevant header
                    if line.startswith("# Rule choosen:"):
                        result = line.split(":")[1].strip()
                        return result
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
            return None

    def get_origin_file(file_path):
        """Extracts the origin of the file."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Check if the line starts with the relevant header
                    if line.startswith("# Input path:"):
                        result = line.split(":")[1].strip()
                        return result
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
            return None

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
            pap.input_line(line)

    def get_result(pap):
        result = pap.result()
        return result

    def process_file(votes_file, rule, input_path, num_alternatives):
        output_string = ""
        plurality_parse = Plurality_parse(list(range(1, num_alternatives + 1)))
        stv_parse = STV_parse(list(range(1, num_alternatives + 1)))
        copeland_parse = Copeland_parse([str(x) for x in range(1, num_alternatives + 1)])
        minimax_parse = Minimax_parse([str(x) for x in range(1, num_alternatives + 1)])
        # Skip the info file
        if isinstance(votes_file, str):
            if not (votes_file == "info.txt"):
                if rule == "plurality":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            Process.process_line(line, plurality_parse)
                    result = Process.get_result(plurality_parse)
                    output_string += str(result) + "\n"
                    output_string += str(sorted(result, reverse = True)) + "\n"
                    return output_string
                if rule == "stv":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            Process.process_line(line, stv_parse)
                    result = Process.get_result(stv_parse)
                    output_string += str(result) + "\n"
                    # output_string += str(sorted(result, reverse = True)) + "\n"
                    return output_string
                if rule == "copeland":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            Process.process_line(line, copeland_parse)
                    result = Process.get_result(copeland_parse)
                    output_string += str(result) + "\n"
                    # output_string += str(sorted(result, reverse = True)) + "\n"
                    return output_string
                if rule == "minimax":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            Process.process_line(line, minimax_parse)
                    result = Process.get_result(minimax_parse)
                    output_string += str(result) + "\n"
                    # output_string += str(sorted(result, reverse = True)) + "\n"
                    return output_string
                print("Not valid rule")
        else:
            if rule == "plurality":
                votes_file.seek(0)
                for line in votes_file:
                    Process.process_line(line, plurality_parse)
                result = Process.get_result(plurality_parse)
                output_string += str(result) + "\n"
                output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string
            if rule == "stv":
                votes_file.seek(0)
                for line in votes_file:
                    Process.process_line(line, stv_parse)
                result = Process.get_result(stv_parse)
                output_string += str(result) + "\n"
                # output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string
            if rule == "copeland":
                votes_file.seek(0)
                for line in votes_file:
                    Process.process_line(line, copeland_parse)
                result = Process.get_result(copeland_parse)
                output_string += str(result) + "\n"
                # output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string
            if rule == "minimax":
                votes_file.seek(0)
                for line in votes_file:
                    Process.process_line(line, minimax_parse)
                result = Process.get_result(minimax_parse)
                output_string += str(result) + "\n"
                # output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string
            print("Not valid rule")

    def process_run(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k):

        try:
            sampling_k = int(sampling_k) if sampling_bool else None
            misra_k = int(misra_k) if misra_bool else None
        except ValueError:
            print("Input Error", "Please enter valid integer values for k.")
            return

        if sampling_bool and (sampling_k is None or sampling_k <= 0):
            print("Input Error", "Please enter a valid integer value greater than 0 for k (Sampling).")
            return
            
        if misra_bool and (misra_k is None or misra_k <= 0):
            print("Input Error", "Please enter a valid integer value greater than 0 for k (Misra-Gries).")
            return
        
        if not input_path or not output_path:
            print("Warning", "Paths not properly selected.")
            return

        if (sampling_bool and misra_bool):
            print("Cant enable both Sampling and Misra Gries!")
            return

        rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

        
        with open(output_path, 'w') as output_file:
            output_string = ""

            vote_files = os.listdir(input_path)
            
            output_string += "# Input path: " + os.path.abspath(input_path) + "\n"
            output_string += "# Rule choosen: " + rule + "\n"
            
            # Iterate over the files in the folder
            for votes_file in vote_files:

                num_alternatives = Process.get_number_of_alternatives(input_path + "/" + votes_file)
                
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1
                
                if sampling_bool:
                    num_votes = Process.get_number_of_votes(input_path + "/" + votes_file)
                    # Skip the info file
                    if (votes_file == "info.txt"):
                        continue
                    sample = sampling(num_votes // sampling_k)
                    print("Num of elements: " + str(num_votes // sampling_k))
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            if not (line.startswith("#")):
                                line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                                
                                parts = line.split(':')
                                multiplier = int(parts[0])
                                vote_data = "1: " + parts[1] + '\n'
                                # print(vote_data)
                                for _ in range(multiplier):
                                    sample.update_R(vote_data)

                    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
                        for item in sample.S:
                            temp_file.write(item)
                        temp_file.seek(0)
                        output_string += "# Sampling used! Num of elements: " + str(num_votes // sampling_k) + '\n'
                        output_string += Process.process_file(temp_file, rule, input_path, num_alternatives)
                        output_file.write(output_string)
                else:
                    if misra_bool:
                        num_votes = Process.get_number_of_votes(input_path + "/" + votes_file)
                        # Skip the info file
                        if (votes_file == "info.txt"):
                            continue
                        mg = Misra_Gries(misra_k, True)
                        print("k := " + str(misra_k))
                        with open(input_path + "/" + votes_file, "r") as file:
                            for line in file:
                                if not (line.startswith("#")):
                                    line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                                    
                                    parts = line.split(':')
                                    multiplier = int(parts[0])
                                    vote_data = "1: " + parts[1] + '\n'
                                    # print(vote_data)
                                    for _ in range(multiplier):
                                        mg.misra_gries_update(vote_data)

                        with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
                            for item in mg.H:
                                temp_file.write(item[1])

                            temp_file.seek(0)
                            output_string += "# Misra Gries used! k := " + str(misra_k) + '\n'
                            output_string += Process.process_file(temp_file, rule, input_path, num_alternatives)
                            output_file.write(output_string) 
                    else:
                        output_string += Process.process_file(votes_file, rule, input_path, num_alternatives)
                        output_file.write(output_string)

                

    def process_error(input_path1, input_path2, output_path):
        output_string = "# First file:" + os.path.abspath(input_path1) + '\n' + "# Second file:" + os.path.abspath(input_path2) + '\n' + "0"
        origin_path1 = Process.get_origin_file(input_path1)
        origin_path2 = Process.get_origin_file(input_path2)
        rule1 = Process.get_rule(input_path1)
        rule2 = Process.get_rule(input_path2)
        if (origin_path1 != origin_path2):
            print("Doesnt come from same file.")
            return
        if (rule1 != rule2):
            print("Doesnt have same rule.")
            return
        origin_path = origin_path1
        rule = rule1
        with open(output_path, 'w') as output_file:
            print(origin_path, rule)
            output_file.write(output_string)