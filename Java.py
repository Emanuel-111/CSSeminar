import subprocess

def compile_and_run_java(java_file, class_name, java_src_dir):
    try:
        # Compile the Java program
        subprocess.run(['javac', java_file], check=True, text=True, capture_output=True)
        # Run the compiled Java program, ensure to run from the directory containing the class files
        run_java = subprocess.run(['java', class_name], check=True, text=True, capture_output=True, cwd=java_src_dir)
        print(run_java.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

#Remember to change this directory to whatever java file you have!
java_src_dir = '/Users/emanuelluna/eclipse-workspace/Intro/src'
java_file = f'{java_src_dir}/Hello.java'
class_name = 'Hello'  # Make sure this matches the class name in your Java file

compile_and_run_java(java_file, class_name, java_src_dir)

