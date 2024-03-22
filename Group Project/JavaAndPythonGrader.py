# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:05:28 2024

@author: Loren
"""

import subprocess

def test_python():
    with open('teacher.txt', 'r') as file:
        teacher_content = file.read()

    script_path = 'test-case.py'  
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    student_content = result.stdout.strip()

    return teacher_content, student_content

def test_java():
    def compile_and_run_java(java_file, class_name, java_src_dir):
        try:
            # Compile the Java program
            subprocess.run(['javac', java_file], check=True, text=True, capture_output=True)
            # Run the compiled Java program, ensure to run from the directory containing the class files
            run_java = subprocess.run(['java', class_name], check=True, text=True, capture_output=True, cwd=java_src_dir)
            return run_java.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error occurred: {e.stderr}"

    java_src_dir = '/Users/Loren/Documents/College/Senior Year/Semester 2/Senior Seminar/GroupProj'
    java_file = f'{java_src_dir}/Hello.java'
    class_name = 'Hello'  # Make sure this matches the class name in your Java file

    return compile_and_run_java(java_file, class_name, java_src_dir)

def main():
    choice = input("Enter 'python' to test Python code or 'java' to test Java code: ").lower()
    
    if choice == 'python':
        teacher_content, student_content = test_python()
        if teacher_content == student_content:
            print(f"You are correct\nTeacher = {teacher_content}\nStudent = {student_content}")
        else:
            print(f"You are incorrect\nTeacher = {teacher_content}\nStudent = {student_content}")
    elif choice == 'java':
        java_output = test_java()
        print(java_output)
    else:
        print("Invalid choice. Please enter 'python' or 'java'.")

if __name__ == "__main__":
    main()
