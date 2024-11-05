#!/usr/bin/env python

# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.proceess import Process

import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile


# Show main menu
def show_main(frame_main, frame_generate, frame_run):
    frame_generate.pack_forget()
    frame_run.pack_forget()
    frame_main.pack(padx=20, pady=20)

# Function for "Generating Votes"
def generate_votes(frame_main, frame_generate, frame_run):
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


        tk.Button(frame_generate, text="Submit", command=lambda: submit_generate(frame_main, frame_generate, frame_run), bg="#4CAF50", fg="white").pack(pady=(0, 10))
        tk.Button(frame_generate, text="Back", command=lambda: show_main(frame_main, frame_generate, frame_run), bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

    # Pack the frame
    frame_generate.pack()

def submit_generate(frame_main, frame_generate, frame_run):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        num_votes = int(generate_votes.entry_votes.get())
        num_candidates = int(generate_votes.entry_candidates.get())
        vote_type = generate_votes.vote_type_var.get()
        
        if not file_path:
            messagebox.showwarning("Warning", "No file path selected.")
            return
        
        # Call the function to process generating votes
        Process.procces_generating(file_path, num_votes, num_candidates, vote_type)
        messagebox.showinfo("Success", f"Votes saved to {file_path}")
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Invalid input: {ve}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return

# Function for "Running Algorithm"
def run_algorithm(frame_main, frame_generate, frame_run):
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

        tk.Button(frame_run, text="Choose Files and Run", command=lambda: submit_run(frame_main, frame_generate, frame_run), bg="#4CAF50", fg="white").pack(pady=(0, 10))
        tk.Button(frame_run, text="Back", command=lambda: show_main(frame_main, frame_generate, frame_run), bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

    # Pack
    frame_run.pack()

def submit_run(frame_main, frame_generate, frame_run):
    load_path = filedialog.askdirectory()
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    vote_type = run_algorithm.vote_type_var.get()
    sampling_enabled = run_algorithm.sampling_var.get()
    
    if not load_path or not save_path:
        messagebox.showwarning("Warning", "Paths not properly selected.")
        return
    
    # Call the function to process running the algorithm
    Process.process_run(load_path, save_path, vote_type, sampling_enabled)
    messagebox.showinfo("Success", "Algorithm run completed.")

def main() -> int:
    root = tk.Tk()
    root.title("Voting System Application")

    # Configure main window background
    root.configure(bg="#f0f0f0")

    frame_main = tk.Frame(root, bg="#f0f0f0")
    frame_main.pack(padx=20, pady=20)

    frame_generate = tk.Frame(root, bg="#f0f0f0")
    frame_run = tk.Frame(root, bg="#f0f0f0")


    # Main menu setup
    tk.Label(frame_main, text="Voting System Application", font=("Arial", 20), bg="#f0f0f0").pack(pady=(0, 20))
    tk.Button(frame_main, text="Generate Votes", command=lambda: generate_votes(frame_main, frame_generate, frame_run), bg="#2196F3", fg="white").pack(pady=10)
    tk.Button(frame_main, text="Run Algorithm", command=lambda: run_algorithm(frame_main, frame_generate, frame_run), bg="#2196F3", fg="white").pack(pady=10)

    root.mainloop()
    return 0

if __name__ == "__main__":
    main()