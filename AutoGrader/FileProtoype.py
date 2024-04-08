import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class FileFinderApp:
    def __init__(self, root):
        self.root = root
        root.title("File Finder")

        # Frame for source directory selection
        self.source_dir_frame = tk.Frame(root)
        self.directory_label = tk.Label(self.source_dir_frame, text="Select source directory:")
        self.directory_label.pack(side=tk.LEFT)
        self.select_button = tk.Button(self.source_dir_frame, text="Browse", command=self.browse_directory)
        self.select_button.pack(side=tk.LEFT)
        self.source_dir_frame.pack()

        # Label to display the selected source directory
        self.selected_source_dir_label = tk.Label(root, text="No source directory selected")
        self.selected_source_dir_label.pack()

        # Frame for output directory selection
        self.output_dir_frame = tk.Frame(root)
        self.output_dir_label = tk.Label(self.output_dir_frame, text="Select output directory:")
        self.output_dir_label.pack(side=tk.LEFT)
        self.select_output_dir_button = tk.Button(self.output_dir_frame, text="Browse", command=self.browse_output_directory)
        self.select_output_dir_button.pack(side=tk.LEFT)
        self.output_dir_frame.pack()

        # Label to display the selected output directory
        self.selected_output_dir_label = tk.Label(root, text="No output directory selected")
        self.selected_output_dir_label.pack()

        # File list as a Listbox
        self.file_list_frame = tk.Frame(root)
        self.file_list_box = tk.Listbox(self.file_list_frame, height=10, width=50)
        self.file_scroll = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_list_box.yview)
        self.file_list_box.config(yscrollcommand=self.file_scroll.set)
        self.file_list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)

        # Compile and run button
        self.compile_run_button = tk.Button(root, text="Compile and Run Selected File", command=self.compile_and_run_selected_file)
        self.compile_run_button.pack()

        self.directory = ""  # Source files directory
        self.output_directory = ""  # Output files directory (initialized to empty)

    def browse_directory(self):
        new_dir = filedialog.askdirectory()
        if new_dir:  # Update the source directory only if a new one was selected
            self.directory = new_dir
            self.update_source_dir_label()  # Update the label with the new source directory
            if not self.output_directory:  # Set output directory to source directory by default
                self.output_directory = self.directory
                self.update_output_dir_label()  # Update the label with the new output directory
            self.search_files()

    def browse_output_directory(self):
        new_dir = filedialog.askdirectory()
        if new_dir:  # Update the output directory only if a new one was selected
            self.output_directory = new_dir
            self.update_output_dir_label()  # Update the label with the new output directory

    def update_source_dir_label(self):
        # This method updates the label to display the currently selected source directory
        self.selected_source_dir_label.config(text=f"Source Directory: {self.directory}")

    def update_output_dir_label(self):
        # This method updates the label to display the currently selected output directory
        self.selected_output_dir_label.config(text=f"Output Directory: {self.output_directory}")

    def search_files(self):
        if self.directory:
            self.file_list_box.delete(0, tk.END)  # Clear the list box
            for file in os.listdir(self.directory):
                if file.endswith(".java") or file.endswith(".py") or file.endswith(".cpp"):
                    self.file_list_box.insert(tk.END, file)
                    
    def compile_and_run_selected_file(self):
        selected_index = self.file_list_box.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a file from the list.")
            return
        selected_file = self.file_list_box.get(selected_index[0])
        file_path = os.path.join(self.directory, selected_file)
        if selected_file.endswith(".java"):
            class_name = selected_file[:-5]  # Remove '.java'
            self.compile_and_run_java(file_path, class_name, self.directory)
        elif selected_file.endswith(".py"):
            self.run_python_file(file_path)
        elif selected_file.endswith(".cpp"):
            self.compile_and_run_cpp(file_path, selected_file)
        else:
            messagebox.showinfo("Unsupported File", "Currently, only Java, Python, and C++ files can be compiled and run.")

    def compile_and_run_cpp(self, cpp_file, file_name):
        try:
            # Compile C++ program (ensure g++ is installed and in your PATH)
            executable_name = file_name.replace('.cpp', '')
            compile_command = ['g++', cpp_file, '-o', os.path.join(self.output_directory, executable_name)]
            subprocess.run(compile_command, check=True, text=True, capture_output=True)
            
            # Run the compiled C++ program
            run_command = os.path.join(self.output_directory, executable_name)
            run_cpp = subprocess.run(run_command, check=True, text=True, capture_output=True)
            
            # Save output to file
            output_file_path = os.path.join(self.output_directory, executable_name + ".txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(run_cpp.stdout)
            messagebox.showinfo("Program Output", f"Output saved to {output_file_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error occurred: {e.stderr}")    
                    
    def run_python_file(self, python_file):
        try:
            # Run the Python script
            run_python = subprocess.run(['python', python_file], check=True, text=True, capture_output=True)
            # Change here: Use self.output_directory instead of self.directory
            output_file_path = os.path.join(self.output_directory, os.path.basename(python_file).replace('.py', '') + ".txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(run_python.stdout)
            messagebox.showinfo("Program Output", f"Output saved to {output_file_path}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error occurred: {e.stderr}")


    def clear_output_text(self):
        # If you choose to use the text area for output
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')

    def append_text(self, text):
        # If you choose to use the text area for output
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text + '\n')
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileFinderApp(root)
    root.mainloop()
