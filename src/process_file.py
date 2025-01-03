# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.plurality_parse import plurality_parse
from src.preflib_vote_parsers.stv_parse import stv_parse
from src.preflib_vote_parsers.copeland_parse import copeland_parse
from src.preflib_vote_parsers.maximin_parse import maximin_parse

import time

class process_file:
    def aply_one_rule(pap: any, file: any) -> str:
        """Applies a voting rule to the provided file. Returns the results formatted as a string."""
        # Measure time
        time_before = time.time()
        isLine = False
        for line in file:
            isLine = True
            # Process each line using the parser
            process_file.process_line(line, pap)
        # Get the result of processing
        result = process_file.get_result(pap)
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

    def choose_rule(rule: str, file: any, plurality_parse: any, stv_parse: any, copeland_parse: any, maximin_parse: any) -> str:
        output_string = ""
        if rule == "plurality":
            output_string = process_file.aply_one_rule(plurality_parse, file)
        if rule == "stv":
            output_string = process_file.aply_one_rule(stv_parse, file)
        if rule == "copeland":
            output_string = process_file.aply_one_rule(copeland_parse, file)
        if rule == "maximin":
            output_string = process_file.aply_one_rule(maximin_parse, file)
        return output_string

    def process_file(votes_file: any, rule: str, input_path: str, num_alternatives: int) -> str:
        """Processes a file using a specified voting rule. Returns formatted results as a string."""
        # Initialize parsers for different voting rules
        _plurality_parse = plurality_parse(list(range(1, num_alternatives + 1)))
        _stv_parse = stv_parse(list(range(1, num_alternatives + 1)))
        _copeland_parse = copeland_parse([str(x) for x in range(1, num_alternatives + 1)])
        _maximin_parse = maximin_parse([str(x) for x in range(1, num_alternatives + 1)])
        output_string = ""
        if isinstance(votes_file, str):
            # Skip the info file
            if not (votes_file == "info.txt"):
                with open(os.path.abspath(votes_file), "r") as file:
                    output_string = process_file.choose_rule(rule, file, _plurality_parse, _stv_parse, _copeland_parse, _maximin_parse)
        else:
            votes_file.seek(0)
            output_string = process_file.choose_rule(rule, votes_file, _plurality_parse, _stv_parse, _copeland_parse, _maximin_parse)
        return output_string