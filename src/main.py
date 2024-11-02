#!/usr/bin/env python

# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.soc import parse_and_pass
from src.vote_rules.fast_rules.misra_gries_scoring_rules import MGSR

#!/usr/bin/env python

# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.preflib_vote_parsers.soc import parse_and_pass
from src.vote_rules.fast_rules.misra_gries_scoring_rules import MGSR

import tkinter as tk
from tkinter import filedialog, messagebox

def ProccesGenerating(output_path, num_votes, num_candidates, vote_type):
    try:
        with open(output_path, 'w') as file:
            file.write("# testing\n")
    except Exception as e:
        print(f"Error creating or writing to {output_path}: {e}")
        return 1

def ProcessRun(input_path, output_path, rule):
    try:
        with open(output_path, 'w') as file:
            output_string = ""

            vote_files = os.listdir(input_path)
            
            output_string += "Rule choosen: " + rule
            
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
                    output_string += result
                    output_string += sorted(result, reverse = True)
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
            file.write(output_string)
    except Exception as e:
        print(f"Error creating or writing to {output_path}: {e}")
        return 1


def main() -> int:
    # Function for "Generating Votes"
    def generate_votes():
        def submit_generate():
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                num_votes = int(entry_votes.get())
                num_candidates = int(entry_candidates.get())
                vote_type = vote_type_var.get()
                
                if not file_path:
                    messagebox.showwarning("Warning", "No file path selected.")
                    return 1
                
                # Call the function to process generating votes
                ProccesGenerating(file_path, num_votes, num_candidates, vote_type)
                messagebox.showinfo("Success", f"Votes saved to {file_path}")
            except ValueError as ve:
                messagebox.showerror("Input Error", f"Invalid input: {ve}")
                return 1
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                return 1
        
        # Window setup for "Generate Votes"
        try:
            generate_window = tk.Toplevel(root)
            generate_window.title("Generate Votes")
            
            tk.Label(generate_window, text="Number of Votes:").pack()
            entry_votes = tk.Entry(generate_window)
            entry_votes.pack()
            
            tk.Label(generate_window, text="Number of Candidates:").pack()
            entry_candidates = tk.Entry(generate_window)
            entry_candidates.pack()
            
            tk.Label(generate_window, text="Type of Vote (e.g., SOI, SOC):").pack()
            vote_type_var = tk.StringVar(value="SOI")
            tk.Entry(generate_window, textvariable=vote_type_var).pack()
            
            tk.Button(generate_window, text="Submit", command=submit_generate).pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create 'Generate Votes' window: {e}")
            return 1

    # Function for "Running Algorithm"
    def run_algorithm():
        def submit_run():
            try:
                load_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                save_path = filedialog.askdirectory()
                vote_type = vote_type_var.get()
                
                if not load_path or not save_path:
                    messagebox.showwarning("Warning", "Paths not properly selected.")
                    return 1
                
                # Call the function to process running the algorithm
                ProcessRun(load_path, save_path, vote_type)
                messagebox.showinfo("Success", "Algorithm run completed.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                return 1
        
        # Window setup for "Run Algorithm"
        try:
            run_window = tk.Toplevel(root)
            run_window.title("Run Algorithm")
            
            tk.Label(run_window, text="Type of Vote File (e.g., SOI, SOC):").pack()
            vote_type_var = tk.StringVar(value="SOI")
            tk.Entry(run_window, textvariable=vote_type_var).pack()
            
            tk.Button(run_window, text="Choose Files and Run", command=submit_run).pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create 'Run Algorithm' window: {e}")
            return 1

    # Main window setup
    try:
        root = tk.Tk()
        root.title("Voting System Application")

        tk.Button(root, text="Generate Votes", command=generate_votes).pack(pady=10)
        tk.Button(root, text="Run Algorithm", command=run_algorithm).pack(pady=10)

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred in the main window: {e}")
        return 1

    return 0
    

if __name__ == "__main__":
    sys.exit(main())
