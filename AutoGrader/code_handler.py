import subprocess
import os
import tkinter as tk
from tkinter import filedialog

selected_script_files = []
selected_reference_file = ""

def get_file_name_with_extension(file_path):
    return os.path.basename(file_path)

def compare_files(script_files, reference_file, output_file, additional_inputs=None):
    with open(output_file, 'w') as log_file:
        for script_file in script_files:
            # Construct the command to execute the script file
            command = ['python', script_file]
            
            # If additional inputs are provided, append them to the command
            if additional_inputs:
                command.extend(additional_inputs)
            
            # Execute the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True)
            script_output = result.stdout.strip()
            script_errors = result.stderr.strip()  # capturing stderr for potential errors
            
            # Read the content of the reference file
            with open(reference_file, 'r') as file:
                reference_content = file.read().strip()

            # Compare the script output with the reference content
            if script_output == reference_content:
                log_file.write(f"{get_file_name_with_extension(script_file)}: Correct\n")
            else:
                log_file.write(f"{get_file_name_with_extension(script_file)}: Incorrect\n")
            
            # Write script errors to log
            if script_errors:
                log_file.write(f"Errors in {get_file_name_with_extension(script_file)}: {script_errors}\n")

def select_script_files():
    global selected_script_files
    selected_script_files = filedialog.askopenfilenames(title="Select script files")
    if selected_script_files:
        script_files_label.config(text="Selected Script Files: " + ", ".join(map(get_file_name_with_extension, selected_script_files)))
    else:
        script_files_label.config(text="No script files selected.")

def select_reference_file():
    global selected_reference_file
    selected_reference_file = filedialog.askopenfilename(title="Select reference file")
    if selected_reference_file:
        reference_file_label.config(text="Selected Reference File: " + get_file_name_with_extension(selected_reference_file))
    else:
        reference_file_label.config(text="No reference file selected.")

def browse_files():
    if selected_script_files and selected_reference_file:
        output_file = filedialog.asksaveasfilename(title="Save results log as")
        if output_file:
            additional_inputs = []  # Additional inputs provided by the teacher (if any)
            # Check if additional parameters are provided and add them to the command
            if additional_inputs_entry.get():
                additional_inputs.extend(additional_inputs_entry.get().split())
            
            compare_files(selected_script_files, selected_reference_file, output_file, additional_inputs)
            result_label.config(text="Grading completed. Results logged in file: " + output_file)
        else:
            result_label.config(text="Output file not selected.")
    else:
        result_label.config(text="Please select both script files and a reference file.")

# GUI
root = tk.Tk()
root.title("Code Grader")

# Instructions label
instructions_label = tk.Label(root, text="Please select script files and a reference file to grade against.", font=("Helvetica", 14))
instructions_label.pack(pady=10)

# Button to select script files
select_script_button = tk.Button(root, text="Select Script Files", font=("Helvetica", 12), command=select_script_files)
select_script_button.pack(pady=5)

# Label to display selected script files
script_files_label = tk.Label(root, text="", font=("Helvetica", 12))
script_files_label.pack()

# Button to select reference file
select_reference_button = tk.Button(root, text="Select Reference File", font=("Helvetica", 12), command=select_reference_file)
select_reference_button.pack(pady=5)

# Label to display selected reference file
reference_file_label = tk.Label(root, text="", font=("Helvetica", 12))
reference_file_label.pack()

# Entry for additional inputs
additional_inputs_label = tk.Label(root, text="Additional Inputs (space-separated):", font=("Helvetica", 12))
additional_inputs_label.pack()

additional_inputs_entry = tk.Entry(root, font=("Helvetica", 12))
additional_inputs_entry.pack()

# Button to browse files
browse_button = tk.Button(root, text="Grade Files", font=("Helvetica", 12), command=browse_files)
browse_button.pack(pady=10)

# Label to display result
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
