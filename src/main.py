#!/usr/bin/env python

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
        print("This line: " + line)
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
                        result = process_line(line, pap)
                output_string += str(result) + "\n"
                output_string += str(sorted(result, reverse = True)) + "\n"
                return output_string
    else:
        if rule == "soc":
            print("This file looks liek this: " + str(votes_file.readlines()))
            votes_file.seek(0)
            for line in votes_file:
                result = process_line(line, pap)
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

            num_alternatives = get_number_of_alternatives(input_path + "/" + votes_file)
            
            if num_alternatives is None:
                print("Could not find the number of alternatives.")
                return 1
            
            if sampling_bool:
                num_votes = get_number_of_votes(input_path + "/" + votes_file)
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
                    
                    output_string += process_file(temp_file, rule, input_path, num_alternatives)
                    output_file.write(output_string)          
            else:
                output_string += process_file(votes_file, rule, input_path, num_alternatives)
                output_file.write(output_string)


def main() -> int:
    root = tk.Tk()
    root.title("Voting System Application")

    # Configure main window background
    root.configure(bg="#f0f0f0")

    frame_main = tk.Frame(root, bg="#f0f0f0")
    frame_main.pack(padx=20, pady=20)

    frame_generate = tk.Frame(root, bg="#f0f0f0")
    frame_run = tk.Frame(root, bg="#f0f0f0")

    # Show main menu
    def show_main():
        frame_generate.pack_forget()
        frame_run.pack_forget()
        frame_main.pack(padx=20, pady=20)

    # Function for "Generating Votes"
    def generate_votes():
        # Clear
        frame_main.pack_forget()
        frame_run.pack_forget()
        frame_generate.pack(padx=20, pady=20)


        # Ensure elements are only created once
        if not hasattr(generate_votes, 'title_label'):
            generate_votes.title_label = tk.Label(frame_generate, text="Generate Votes", font=("Arial", 16), bg="#f0f0f0")
            generate_votes.title_label.pack(pady=(0, 10))

        
        if not hasattr(generate_votes, 'entry_votes'):
            tk.Label(frame_generate, text="Number of Votes:", bg="#f0f0f0").pack()
            generate_votes.entry_votes = tk.Entry(frame_generate)
            generate_votes.entry_votes.pack(pady=(0, 10))

            tk.Label(frame_generate, text="Number of Candidates:", bg="#f0f0f0").pack()
            generate_votes.entry_candidates = tk.Entry(frame_generate)
            generate_votes.entry_candidates.pack(pady=(0, 10))

            tk.Label(frame_generate, text="Type of vote distribution:", bg="#f0f0f0", font=("Arial", 14)).pack(anchor="w", padx=10)

            generate_votes.vote_type_var = tk.StringVar(value="Exp")
            tk.Radiobutton(frame_generate, text="Exponential distribution", variable=generate_votes.vote_type_var, value="Exp", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=20)
            tk.Radiobutton(frame_generate, text="Zipfian distribution", variable=generate_votes.vote_type_var, value="Zipf", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=20)


            tk.Button(frame_generate, text="Submit", command=submit_generate, bg="#4CAF50", fg="white").pack(pady=(0, 10))
            tk.Button(frame_generate, text="Back", command=show_main, bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

        # Pack the frame
        frame_generate.pack()

    def submit_generate():
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            num_votes = int(generate_votes.entry_votes.get())
            num_candidates = int(generate_votes.entry_candidates.get())
            vote_type = generate_votes.vote_type_var.get()
            
            if not file_path:
                messagebox.showwarning("Warning", "No file path selected.")
                return
            
            # Call the function to process generating votes
            procces_generating(file_path, num_votes, num_candidates, vote_type)
            messagebox.showinfo("Success", f"Votes saved to {file_path}")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return

    # Function for "Running Algorithm"
    def run_algorithm():
        # Clear
        frame_main.pack_forget()
        frame_generate.pack_forget()
        frame_run.pack(padx=20, pady=20)

        # Ensure elements are only created once
        if not hasattr(run_algorithm, 'title_label'):
            run_algorithm.title_label = tk.Label(frame_run, text="Run Algorithm", font=("Arial", 16), bg="#f0f0f0")
            run_algorithm.title_label.pack(pady=(0, 10))
        
        if not hasattr(run_algorithm, 'vote_type_var'):
            tk.Label(frame_run, text="Type of Vote File (e.g., SOI, SOC):", bg="#f0f0f0").pack()
            run_algorithm.vote_type_var = tk.StringVar(value="SOI")
            tk.Entry(frame_run, textvariable=run_algorithm.vote_type_var).pack(pady=(0, 10))

            run_algorithm.sampling_var = tk.BooleanVar(value=False)
            tk.Checkbutton(frame_run, text="Enable Sampling", variable=run_algorithm.sampling_var, bg="#f0f0f0").pack(pady=(0, 10))

            tk.Button(frame_run, text="Choose Files and Run", command=submit_run, bg="#4CAF50", fg="white").pack(pady=(0, 10))
            tk.Button(frame_run, text="Back", command=show_main, bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

        # Pack
        frame_run.pack()

    def submit_run():
        load_path = filedialog.askdirectory()
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        vote_type = run_algorithm.vote_type_var.get()
        sampling_enabled = run_algorithm.sampling_var.get()
        
        if not load_path or not save_path:
            messagebox.showwarning("Warning", "Paths not properly selected.")
            return
        
        # Call the function to process running the algorithm
        process_run(load_path, save_path, vote_type, sampling_enabled)
        messagebox.showinfo("Success", "Algorithm run completed.")

    # Main menu setup
    tk.Label(frame_main, text="Voting System Application", font=("Arial", 20), bg="#f0f0f0").pack(pady=(0, 20))
    tk.Button(frame_main, text="Generate Votes", command=generate_votes, bg="#2196F3", fg="white").pack(pady=10)
    tk.Button(frame_main, text="Run Algorithm", command=run_algorithm, bg="#2196F3", fg="white").pack(pady=10)

    root.mainloop()
    return 0

if __name__ == "__main__":
    main()