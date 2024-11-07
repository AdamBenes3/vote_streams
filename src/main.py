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

class Main:
    def clear_frame(frame : tk.Frame) -> None:
        """Clears all widgets from the specified frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def show_main(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Displays the main menu frame and hides the initial frame."""
        frame_init.pack_forget()
        frame_main.pack(padx=20, pady=20)

    def generate_votes(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Sets up the interface for generating votes."""
        frame_main.pack_forget()
        frame_init.pack_forget()
        frame_init.pack(padx=20, pady=20)

        Main.clear_frame(frame_init)


        Main.generate_votes.title_label = tk.Label(frame_init, text="Generate Votes", font=("Arial", 16), bg="#f0f0f0")
        Main.generate_votes.title_label.pack(pady=(0, 10))

        
        tk.Label(frame_init, text="Number of Votes:", bg="#f0f0f0").pack()
        Main.generate_votes.entry_votes = tk.Entry(frame_init)
        Main.generate_votes.entry_votes.pack(pady=(0, 10))

        tk.Label(frame_init, text="Number of Candidates:", bg="#f0f0f0").pack()
        Main.generate_votes.entry_candidates = tk.Entry(frame_init)
        Main.generate_votes.entry_candidates.pack(pady=(0, 10))

        tk.Label(frame_init, text="Type of vote distribution:", bg="#f0f0f0", font=("Arial", 14)).pack(anchor="w", padx=10)

        Main.generate_votes.vote_type_var = tk.StringVar(value="Exp")
        tk.Radiobutton(frame_init, text="Exponential distribution", variable=Main.generate_votes.vote_type_var, value="Exp", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=20)
        tk.Radiobutton(frame_init, text="Zipfian distribution", variable=Main.generate_votes.vote_type_var, value="Zipf", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=20)


        tk.Button(frame_init, text="Submit", command=lambda: Main.submit_generate(frame_main, frame_init), bg="#4CAF50", fg="white").pack(pady=(0, 10))
        tk.Button(frame_init, text="Back", command=lambda: Main.show_main(frame_main, frame_init), bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

        frame_init.pack()

    def submit_generate(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Submits the generate votes form, saves results to a file, and handles errors."""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            num_votes = int(generate_votes.entry_votes.get())
            num_candidates = int(generate_votes.entry_candidates.get())
            vote_type = generate_votes.vote_type_var.get()
            
            if not file_path:
                messagebox.showwarning("Warning", "No file path selected.")
                return
            
            Process.procces_generating(file_path, num_votes, num_candidates, vote_type)
            messagebox.showinfo("Success", f"Votes saved to {file_path}")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return

    def run_algorithm(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Sets up the interface for running an algorithm with specified parameters."""
        frame_main.pack_forget()
        frame_init.pack_forget()
        frame_init.pack(padx=20, pady=20)

        Main.clear_frame(frame_init)

        Main.run_algorithm.title_label = tk.Label(frame_init, text="Run Algorithm", font=("Arial", 16), bg="#f0f0f0")
        Main.run_algorithm.title_label.pack(pady=(0, 10))
        
        tk.Label(frame_init, text="Type of Vote Rule (e.g., STV, Plurality):", bg="#f0f0f0").pack()
        Main.run_algorithm.vote_type_var = tk.StringVar(value="STV")
        tk.Entry(frame_init, textvariable=Main.run_algorithm.vote_type_var).pack(pady=(0, 10))

        Main.run_algorithm.sampling_var = tk.BooleanVar(value=False)
        Main.run_algorithm.sampling_check = tk.Checkbutton(frame_init, text="Enable Sampling", variable=Main.run_algorithm.sampling_var, bg="#f0f0f0")
        Main.run_algorithm.sampling_check.pack(pady=(0, 10))

        Main.run_algorithm.sampling_k_entry = tk.Entry(frame_init)
        tk.Label(frame_init, text="Enter k for Sampling:", bg="#f0f0f0").pack(pady=(0, 5))
        Main.run_algorithm.sampling_k_entry.pack(pady=(0, 10))

        Main.run_algorithm.misra_var = tk.BooleanVar(value=False)
        Main.run_algorithm.misra_check = tk.Checkbutton(frame_init, text="Enable Misra-Gries", variable=Main.run_algorithm.misra_var, bg="#f0f0f0")
        Main.run_algorithm.misra_check.pack(pady=(0, 10))

        Main.run_algorithm.misra_k_entry = tk.Entry(frame_init)
        tk.Label(frame_init, text="Enter k for Misra-Gries:", bg="#f0f0f0").pack(pady=(0, 5))
        Main.run_algorithm.misra_k_entry.pack(pady=(0, 10))

        tk.Button(frame_init, text="Choose Files and Run", command=lambda: Main.submit_run(frame_main, frame_init), bg="#4CAF50", fg="white").pack(pady=(0, 10))
        tk.Button(frame_init, text="Back", command=lambda: Main.show_main(frame_main, frame_init), bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

        frame_init.pack()

    def submit_run(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Submits the algorithm parameters and executes the algorithm with specified options."""
        load_path = filedialog.askdirectory()
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        vote_type = Main.run_algorithm.vote_type_var.get()
        sampling_enabled = Main.run_algorithm.sampling_var.get()
        misra_enabled = Main.run_algorithm.misra_var.get()
        
        try:
            sampling_k = int(Main.run_algorithm.sampling_k_entry.get()) if sampling_enabled else None
            misra_k = int(Main.run_algorithm.misra_k_entry.get()) if misra_enabled else None
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for k.")
            return

        if sampling_enabled and (sampling_k is None or sampling_k <= 0):
            messagebox.showerror("Input Error", "Please enter a valid integer value greater than 0 for k (Sampling).")
            return
            
        if misra_enabled and (misra_k is None or misra_k <= 0):
            messagebox.showerror("Input Error", "Please enter a valid integer value greater than 0 for k (Misra-Gries).")
            return
        
        if not load_path or not save_path:
            messagebox.showwarning("Warning", "Paths not properly selected.")
            return
        
        Process.process_run(load_path, save_path, vote_type, sampling_enabled, misra_enabled, sampling_k, misra_k)
        messagebox.showinfo("Success", "Algorithm run completed.")

    def error_find(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Sets up the interface for error finding functionality."""
        frame_main.pack_forget()
        frame_init.pack_forget()
        frame_init.pack(padx=20, pady=20)

        Main.clear_frame(frame_init)

        Main.error_find.title_label = tk.Label(frame_init, text="Error find", font=("Arial", 16), bg="#f0f0f0")
        Main.error_find.title_label.pack(pady=(0, 10))
        
        tk.Button(frame_init, text="Choose Files and Run", command=lambda: Main.submit_error_find(frame_main, frame_init), bg="#4CAF50", fg="white").pack(pady=(0, 10))
        tk.Button(frame_init, text="Back", command=lambda: Main.show_main(frame_main, frame_init), bg="#f44336", fg="white").pack(pady=(0, 10))  # Back button

        frame_init.pack()

    def submit_error_find(frame_main: tk.Frame, frame_init: tk.Frame) -> None:
        """Submits error-finding operation on selected files and saves the output."""
        load_path1 = filedialog.askopenfilename()
        load_path2 = filedialog.askopenfilename()
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        if not load_path1 or not load_path2 or not save_path:
            messagebox.showwarning("Warning", "Paths not properly selected.")
            return
        
        Process.process_error(load_path1, load_path2, save_path)
        messagebox.showinfo("Success", "Algorithm run completed.")

    def print_help_message() -> None:
        """Prints help message describing command-line argument usage."""
        print("""Argumets are:
-g save_path num_votes num_candidates generate_distribution

-r load_path_folder save_path vote_type sampling_enable misra_enable k
    (for the \"enable\" write 1 for true and 0 for false)
    (k is used for either divide the number of votes when sampling for example k = 2 is \"half of the votes\" or for misra gries as a parametr)

-e load_path1 load_path2 save_path""")

    def main() -> int:
        """Main function to handle both command-line arguments and GUI setup."""
        args = sys.argv[1:]

        if len(args) > 0:
            if args[0] == "generate" or args[0] == "-g":
                if len(args) != 5:
                    Main.print_help_message()
                    return 1
                Process.procces_generating(args[1], int(args[2]), int(args[3]), args[4])
                return 0
            if args[0] == "run" or args[0] == "-r":
                if len(args) != 7:
                    Main.print_help_message()
                    return 1
                arg4 = True if int(args[4]) == 1 else False
                arg5 = True if int(args[5]) == 1 else False
                Process.process_run(args[1], args[2], args[3], arg4, arg5, args[6], args[6])
                return 0
            if args[0] == "error" or args[0] == "-e":
                if len(args) != 4:
                    Main.print_help_message()
                    return 1
                Process.process_error(args[1], args[2], args[3])
                return 0
            else:
                Main.print_help_message()
                return 1
            

        root = tk.Tk()
        root.title("Voting System Application")

        root.configure(bg="#f0f0f0")

        frame_main = tk.Frame(root, bg="#f0f0f0")
        frame_main.pack(padx=20, pady=20)

        frame_init = tk.Frame(root, bg="#f0f0f0")

        tk.Label(frame_main, text="Voting System Application", font=("Arial", 20), bg="#f0f0f0").pack(pady=(0, 20))
        tk.Button(frame_main, text="Generate Votes", command=lambda: Main.generate_votes(frame_main, frame_init), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(frame_main, text="Run Algorithm", command=lambda: Main.run_algorithm(frame_main, frame_init), bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(frame_main, text="Error finder", command=lambda: Main.error_find(frame_main, frame_init), bg="#2196F3", fg="white").pack(pady=10)

        root.mainloop()
        return 0

if __name__ == "__main__":
    Main.main()