import subprocess
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from tkinter import PhotoImage
import traceback


selected_script_files = []
selected_reference_file = ""
selected_additional_inputs = ""

def get_file_name_with_extension(file_path):
    return os.path.basename(file_path)

def compare_files(script_files, reference_file, output_file, additional_inputs=None):
    with open(output_file, 'w') as log_file:
        with open(reference_file, 'r') as ref_file:
            reference_content = ref_file.readlines()

            for script_file in script_files:
                # Get the file extension
                file_extension = os.path.splitext(script_file)[1].lower()

                # Construct the command based on the file extension
                if file_extension == '.py':  # Python script
                    command = ['python', script_file]
                elif file_extension == '.java':  # Java program
                    command = ['java', '-classpath', '.', script_file[:-5]]  # Assuming the class file is in the same directory
                elif file_extension == '.cpp':  # C++ program
                    command = ['g++', '-o', 'temp', script_file]  # Compile the C++ file
                    compile_result = subprocess.run(command, capture_output=True, text=True)
                    if compile_result.returncode == 0:
                        command = ['./temp']
                    else:
                        log_file.write(f"Compilation error in {get_file_name_with_extension(script_file)}: {compile_result.stderr}\n")
                        continue  # Skip this file if compilation failed
                else:
                    log_file.write(f"Unsupported file type: {get_file_name_with_extension(script_file)}\n")
                    continue  # Skip this file if unsupported

                # If additional inputs are provided, read the content and append it to the command
                if additional_inputs:
                    with open(additional_inputs, 'r') as additional_file:
                        additional_content = additional_file.readlines()
                        for additional_arguments, reference_case in zip(additional_content, reference_content):
                            additional_arguments = additional_arguments.strip().split()
                            reference_case = reference_case.strip()
                            command_extended = command.copy()  # Make a copy of the command for each additional case
                            command_extended.extend(additional_arguments)

                            # Execute the command and capture the output
                            result = subprocess.run(command_extended, capture_output=True, text=True, input=None)
                            script_output = result.stdout.strip()
                            script_errors = result.stderr.strip()  # capturing stderr for potential errors

                            # Compare the script output with the reference content
                            if script_output == reference_case:
                                log_file.write(f"{get_file_name_with_extension(script_file)}: Correct - Input: {' '.join(additional_arguments)} - Output: {script_output}\n")
                            else:
                                log_file.write(f"{get_file_name_with_extension(script_file)}: Incorrect - Input: {' '.join(additional_arguments)} - Output: {script_output}\n")
                            
                            # Write script errors to log
                            if script_errors:
                                log_file.write(f"Errors in {get_file_name_with_extension(script_file)} - Input: {' '.join(additional_arguments)}: {script_errors}\n")

                else:
                    # If no additional inputs provided, execute script without additional arguments
                    result = subprocess.run(command, capture_output=True, text=True, input=None)
                    script_output = result.stdout.strip()
                    script_errors = result.stderr.strip()  # capturing stderr for potential errors

                    # Compare the script output with the reference content
                    for reference_case in reference_content:
                        reference_case = reference_case.strip()
                        if script_output == reference_case:
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

def select_additional_inputs():
    global selected_additional_inputs
    selected_additional_inputs = filedialog.askopenfilename(title="Select additional inputs")
    if selected_additional_inputs:
        additional_inputs.config(text="Selected Additional Inputs: " + get_file_name_with_extension(selected_additional_inputs))
    else:
        additional_inputs.config(text="No additional inputs selected.")

def browse_files():
    if selected_script_files and selected_reference_file:
        output_file = filedialog.asksaveasfilename(title="Save results log as")
        if output_file:
            # Check if additional parameters are provided and add them to the command
            compare_files(selected_script_files, selected_reference_file, output_file, selected_additional_inputs)
            result_label.config(text="Grading completed. Results logged in file: " + output_file)
        else:
            result_label.config(text="Output file not selected.")
    else:
        result_label.config(text="Please select both script files and a reference file.")



def create_code_gui():
    try:
        # Create the GUI
        root = tk.Tk()
        root.title("Code Grader")

        global background_photo, top_photo, bottom_photo

        # Load images
        print("Loading images...")
        background_image = Image.open("background.jpg")
        top_image = Image.open("top_image.jpg")
        bottom_image = Image.open("bottom_image.jpg")

        # Resize images to fit the window using LANCZOS resampling method
        background_image = background_image.resize((800, 600), Image.LANCZOS)
        top_image = top_image.resize((800, 100), Image.LANCZOS)
        bottom_image = bottom_image.resize((800, 100), Image.LANCZOS)

        # Convert images to Tkinter-compatible format and store as attributes of the root window
        print("Converting images to Tkinter-compatible format...")
        root.background_photo = ImageTk.PhotoImage(background_image)
        root.top_photo = ImageTk.PhotoImage(top_image)
        root.bottom_photo = ImageTk.PhotoImage(bottom_image)


        print("Images loaded successfully.")

        # Create background label 
        '''
        background_label = tk.Label(root, image=root.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create top image label
        top_image_label = tk.Label(root, image=root.top_photo)
        top_image_label.place(x=0, y=0, relwidth=1, relheight=0.1)

        # Create bottom image label
        bottom_image_label = tk.Label(root, image=bottom_photo)
        bottom_image_label.place(x=0, rely=0.9, relwidth=1, relheight=0.1)

        '''
        # Instructions label
        instructions_label = tk.Label(root, text="Please select script files, a reference file, and additional inputs (if any) to grade against.", font=("Helvetica", 14))
        instructions_label.pack(pady=10)

        # Button to select script files
        select_script_button = tk.Button(root, text="Select Script Files", font=("Helvetica", 12), command=select_script_files)
        select_script_button.pack(pady=5)

        # Label to display selected script files
        global script_files_label
        script_files_label = tk.Label(root, text="", font=("Helvetica", 12))
        script_files_label.pack()

        # Button to select reference file
        select_reference_button = tk.Button(root, text="Select Reference File", font=("Helvetica", 12), command=select_reference_file)
        select_reference_button.pack(pady=5)

        # Label to display selected reference file
        global reference_file_label
        reference_file_label = tk.Label(root, text="", font=("Helvetica", 12))
        reference_file_label.pack()

        # Button to select additional inputs
        select_additional_inputs_button = tk.Button(root, text="Select Additional Inputs", font=("Helvetica", 12), command=select_additional_inputs)
        select_additional_inputs_button.pack(pady=5)

        # Label to display selected additional inputs
        global additional_inputs
        additional_inputs = tk.Label(root, text="", font=("Helvetica", 12))
        additional_inputs.pack()

        # Button to browse files
        browse_button = tk.Button(root, text="Grade Files", font=("Helvetica", 12), command=browse_files)
        browse_button.pack(pady=10)

        # Label to display result
        global result_label
        result_label = tk.Label(root, text="", font=("Helvetica", 12))
        result_label.pack(pady=10)

        root.mainloop()
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()  # Print the traceback for further debugging


# Call create_code_gui when this script is executed directly
if __name__ == "__main__":
    create_code_gui()
