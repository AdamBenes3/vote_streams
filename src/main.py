#!/usr/bin/env python

# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.soc import parse_and_pass
from src.vote_rules.fast_rules.misra_gries_scoring_rules import MGSR

def main() -> int:
    
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print("Two argument expected!")
        return 1
    
    votes_folder = "./../" + sys.argv[1]
    vote_files = os.listdir(votes_folder)
    rule = sys.argv[2]
    
    print("Rule choosen: " + rule)
    
    # x = 1
    
    nr_line = 0
    # Iterate over the files in the folder
    for votes_file in vote_files:
        n = 19
        pap = parse_and_pass(list(range(1, 105 + 1)))
        # Skip the info file
        if (votes_file == "info.txt"):
            continue
        if rule == "soc":
            with open(votes_folder + "/" + votes_file, "r") as file:
                for line in file:
                    # Skip the metadata
                    if (line.startswith("#")):
                        continue
                    
                    # if nr_line == 0:
                    line = line[3:-1]
                        # print(line)
                    pap.input_line(line)
                        # print(pap.result())
                        # nr_line = 1
            result = pap.result()
            print(result)
            print(sorted(result, reverse = True))

        """
        if rule == "stv":
            if x == 1:
                pap = parse_and_pass([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            if x == 2:
                pap = parse_and_pass([1, 2, 3, 4, 5, 6, 7, 8, 9])
            if x == 3:
                pap = parse_and_pass([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        # Open the file with the votes
        with open(votes_folder + "/" + votes_file, "r") as file:
            for line in file:
                # Skip the metadata
                if (line.startswith("#")):
                    continue
                line = line[:-1]
                if rule == "stv":
                    pap.input_line(line)
        if rule == "stv":
            print("File nr. " + str(x) + ": " + str(pap.result()))
        x += 1
        """
    return 0
    

if __name__ == "__main__":
    sys.exit(main())
