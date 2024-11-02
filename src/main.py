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


def ProccesGenerating(output_path, num_votes, num_candidates, vote_type):

    vote_type = vote_type.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

    try:
        with open(output_path, 'w') as file:
            file.write("# testing\n")
    except Exception as e:
        print(f"Error creating or writing to {output_path}: {e}")
        return 1

def ProcessRun(input_path, output_path, rule):

    rule = rule.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

    try:
        with open(output_path, 'w') as output_file:
            output_string = ""

            vote_files = os.listdir(input_path)
            
            output_string += "Rule choosen: " + rule + "\n"
            
            # Iterate over the files in the folder
            for votes_file in vote_files:

                num_alternatives = get_number_of_alternatives(input_path + "/" + votes_file)
                
                if num_alternatives is None:
                    print("Could not find the number of alternatives.")
                    return 1

                pap = parse_and_pass(list(range(1, num_alternatives + 1)))
                # Skip the info file
                if (votes_file == "info.txt"):
                    continue
                if rule == "soc":
                    with open(input_path + "/" + votes_file, "r") as file:
                        for line in file:
                            # Skip the metadata
                            if (line.startswith("#")):
                                continue

                            line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
                            line = line[2:]
                            pap.input_line(line)
                    result = pap.result()
                    output_string += str(result) + "\n"
                    output_string += str(sorted(result, reverse = True)) + "\n"
            output_file.write(output_string)
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
                load_path = filedialog.askdirectory()
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                vote_type = vote_type_var.get()
                
                if not load_path or not save_path:
                    messagebox.showwarning("Warning", "Paths not properly selected.")
                    return 1
                
                # Call the function to process running the algorithm
                ProcessRun(load_path, save_path, vote_type)
                messagebox.showinfo("Success", "Algorithm run completed.")
            except ValueError as ve:
                messagebox.showerror("Input Error", f"Invalid input: {ve}")
                return 1
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
