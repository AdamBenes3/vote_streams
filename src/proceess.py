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

class Process:

    def wrong_input(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k):
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


    def aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, sample_or_mg, votes_file, num_votes, num_alternatives):
        with open(input_path + "/" + votes_file, "r") as file:
            for line in file:
                if not (line.startswith("#")):
                    line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                    
                    parts = line.split(':')
                    multiplier = int(parts[0])
                    vote_data = "1: " + parts[1] + '\n'
                    # print(vote_data)
                    for _ in range(multiplier):
                        if isinstance(sample_or_mg, sampling):
                            sample_or_mg.update_R(vote_data)
                        if isinstance(sample_or_mg, Misra_Gries):
                            sample_or_mg.misra_gries_update(vote_data)

        with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as temp_file:
            if isinstance(sample_or_mg, sampling):
                output_string = "# Sampling used! Num of elements: " + str(num_votes // sampling_k) + '\n'
                for item in sample_or_mg.S:
                    temp_file.write(item)
            if isinstance(sample_or_mg, Misra_Gries):
                output_string = "# Misra Gries used! k := " + str(misra_k) + '\n'
                for item in sample_or_mg.H:
                    temp_file.write(item)
            temp_file.seek(0)
            output_string += Process.process_file(temp_file, rule, input_path, num_alternatives)
            return output_string

    def aply_sampling(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives):
        num_votes = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER VOTERS:"))
        sample = sampling(num_votes // sampling_k)
        print("Num of elements: " + str(num_votes // sampling_k))
        return Process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, sample, votes_file, num_votes, num_alternatives)

    def aply_misra_gries(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, votes_file, num_alternatives):
        num_votes = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER VOTERS:"))
        mg = Misra_Gries(misra_k, True)
        print("k := " + str(misra_k))
        return Process.aply_sampling_or_misra(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k, mg, votes_file, num_votes, num_alternatives)

    def get_line_second_part(file_path, line):
        """Extracts lines second part (important part)."""
        try:
            with open(file_path, 'r') as file:
                for this_line in file:
                    # Check if the line starts with the relevant header
                    if this_line.startswith(line):
                        result = this_line.split(":")[1].strip()
                        return result
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
            return None

    def aply_one_rule(pap, file):
        for line in file:
            Process.process_line(line, pap)
        result = Process.get_result(pap)
        output_string = str(result) + "\n"
        output_string += str(sorted(result, reverse = True)) + "\n"
        return output_string


    def process_line(line, pap):
        # Skip the metadata
        if not (line.startswith("#")):
            line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
            pap.input_line(line)

    def get_result(pap):
        result = pap.result()
        return result

    def process_file(votes_file, rule, input_path, num_alternatives):
        plurality_parse = Plurality_parse(list(range(1, num_alternatives + 1)))
        stv_parse = STV_parse(list(range(1, num_alternatives + 1)))
        copeland_parse = Copeland_parse([str(x) for x in range(1, num_alternatives + 1)])
        minimax_parse = Minimax_parse([str(x) for x in range(1, num_alternatives + 1)])
        output_string = ""
        # Skip the info file
        if isinstance(votes_file, str):
            if not (votes_file == "info.txt"):
                with open(input_path + "/" + votes_file, "r") as file:
                    if rule == "plurality":
                        output_string = Process.aply_rule(plurality_parse, file)
                    if rule == "stv":
                        output_string = Process.aply_one_rule(stv_parse, file)
                    if rule == "copeland":
                        output_string = Process.aply_one_rule(copeland_parse, file)
                    if rule == "minimax":
                        output_string = Process.aply_one_rule(minimax_parse, file)
                    
        else:
            votes_file.seek(0)
            if rule == "plurality":
                output_string = Process.aply_rule(plurality_parse, votes_file)
            if rule == "stv":
                output_string = Process.aply_one_rule(stv_parse, votes_file)
            if rule == "copeland":
                output_string = Process.aply_one_rule(copeland_parse, votes_file)
            if rule == "minimax":
                output_string = Process.aply_one_rule(minimax_parse, votes_file)
        return output_string

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

    def process_run(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k):
        error = Process.wrong_input(input_path, output_path, rule, sampling_bool, misra_bool, sampling_k, misra_k)
        if error == 1:
            return     
        rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        sampling_k = int(sampling_k)
        misra_k = int(misra_k)
        with open(output_path, 'w') as output_file:
            vote_files = os.listdir(input_path)
            output_string = "# Input path: " + os.path.abspath(input_path) + "\n"
            output_string += "# Rule choosen: " + rule + "\n"
            # Iterate over the files in the folder
            for votes_file in vote_files:
                if (votes_file == "info.txt"):
                    continue
                num_alternatives = int(Process.get_line_second_part(input_path + "/" + votes_file, "# NUMBER ALTERNATIVES:"))
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1
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

    

    def process_error(input_path1, input_path2, output_path):
        output_string = "# First file:" + os.path.abspath(input_path1) + '\n' + "# Second file:" + os.path.abspath(input_path2) + '\n' + "0"
        origin_path1 = Process.get_line_second_part(input_path1,"# Input path:")
        origin_path2 = Process.get_line_second_part(input_path2, "# Input path:")
        rule1 = Process.get_line_second_part(input_path1, "# Rule choosen:")
        rule2 = Process.get_line_second_part(input_path2, "# Rule choosen:")
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
            output_file.write(output_string + "\n")