# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import tempfile
import shutil
import atexit
import ast

from src.process_file import Process_file

class stv_error:
    def remove_comment_lines(input_string):
        """
        Removes lines starting with '#' from the input string.
        """
        # Split the string into lines, filter out lines starting with '#', and join the result
        filtered_lines = [line for line in input_string.splitlines() if not line.strip().startswith("#")]
        return "\n".join(filtered_lines)

    def create_temp_copy(file_path):
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

    def turn_one(result1, current_index, tempt_file, nr_candidates):
        with open(tempt_file, 'a') as tmp:
            # print("Co máme tu: " + str(result1[current_index]))
            tmp.write("1: " + str(result1[current_index]) + '\n')
        result1 = Process_file.process_file(tempt_file, "stv", tempt_file, nr_candidates)
        result1 = stv_error.remove_comment_lines(result1)
        result1 = ast.literal_eval(result1)
        # print("RESULT: " + str(result1))
        with open(tempt_file, 'r') as tmp:
            for line in tmp:
                # print(line)
                pass
        return result1

    def mismatch_action(P, result1, result2, tempt_file, nr_candidates, i, ERROR):
        index_of_P_1 = result1.index(P)
        index_of_P_2 = result2.index(P)
        current_index = len(result1) - 1
        last_P_1 = result1[-i]
        print("P: " + str(P))
        print("result1.index(P): " + str(index_of_P_1))
        print("result2.index(P): " + str(index_of_P_2))
        print("Before:", result1, result2)
        while result1.index(P) < result1.index(last_P_1):
            ERROR += 1
            result1 = stv_error.turn_one(result1, result1.index(last_P_1), tempt_file, nr_candidates)
        # print("A co tady: ", result1, result2)
        return result1, ERROR

    # Process.stv_error([1, 2, 3], [3, 2, 1])
    def stv_error(result1, result2, origin_path, nr_candidates):
        tempt_file = stv_error.create_temp_copy(origin_path)
        ERROR = 0
        while result1 != result2:
        # for _ in range(1, 4):
            for i in range(1, len(result2) + 1):
                # print("i: " + str(i))
                if result1[-i] != result2[-i]:
                    # print("i: " + str(i))
                    P = result2[-i]
                    result1, ERROR = stv_error.mismatch_action(P, result1, result2, tempt_file, nr_candidates, i, ERROR)
                    break
            print("After:", result1, result2)
        with open(tempt_file, 'r') as tmp:
            for line in tmp:
                print(line, end="")
                # pass
        # print(result1, result2)
        return ERROR