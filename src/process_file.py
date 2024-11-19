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

import time

class Process_file:
    def aply_one_rule(pap: any, file: any) -> str:
        """Applies a voting rule to the provided file. Returns the results formatted as a string."""
        # Measure time
        time_before = time.time()
        isLine = False
        for line in file:
            isLine = True
            # Process each line using the parser
            Process_file.process_line(line, pap)
        # Get the result of processing
        result = Process_file.get_result(pap)
        time_after = time.time()
        output_string = "# Time computing: " + str(time_after - time_before) + "\n"
        if isLine:
            output_string += str(result) + "\n"
        else:
            output_string += "# There was 0 votes in input\n"
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

    def choose_rule(rule: str, file: any, plurality_parse: any, stv_parse: any, copeland_parse: any, minimax_parse: any) -> str:
        output_string = ""
        if rule == "plurality":
            output_string = Process_file.aply_one_rule(plurality_parse, file)
        if rule == "stv":
            output_string = Process_file.aply_one_rule(stv_parse, file)
        if rule == "copeland":
            output_string = Process_file.aply_one_rule(copeland_parse, file)
        if rule == "minimax":
            output_string = Process_file.aply_one_rule(minimax_parse, file)
        return output_string

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
                with open(os.path.abspath(votes_file), "r") as file:
                    output_string = Process_file.choose_rule(rule, file, plurality_parse, stv_parse, copeland_parse, minimax_parse)
        else:
            votes_file.seek(0)
            output_string = Process_file.choose_rule(rule, votes_file, plurality_parse, stv_parse, copeland_parse, minimax_parse)
        return output_string