import subprocess
import os

#with open('teacher.txt', 'r') as file:
 #   file_content = file.read()


#script_path = 'cplus.cpp'  
#result = subprocess.run(['python', script_path], capture_output=True, text=True)
#printed_string = result.stdout.strip()

#if printed_string == file_content:
 #   print("The string matches the content of the text file.")
#else:
 #   print("The string does not match the content of the text file.")
 # Save the C++ code to a file
cpp_filename = "hello.cpp"
with open(cpp_filename, "w") as file:
    file.write(cpp_code)

# Compile the C++ code using os.system
compile_command = f"g++ {cpp_filename} -o hello"
os.system(compile_command)

# Run the compiled C++ executable using os.system
run_command = "./hello"
os.system(run_command)