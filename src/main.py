#!/usr/bin/env python

# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

def main() -> int:
    
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        return 1
    
    votes_folder = sys.argv[1]
    vote_files = os.listdir(votes_folder)
    rule = sys.argv[2]
    
    print(rule)
    
    # Iterate over the files in the folder
    for votes_file in vote_files:
        # Skip the info file
        if (votes_file == "info.txt"):
            continue
        # Open the file with the votes
        with open(votes_folder + "/" + votes_file, "r") as file:
            for line in file:
                # Skip the metadata
                if (line.startswith("#")):
                    continue
                print(line)
    return 0
    

if __name__ == "__main__":
    sys.exit(main())
