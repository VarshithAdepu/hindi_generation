# import subprocess
# import os
# import argparse

# output_list = []

# def run_bulk_generator(file_path, output_list):
#     try:
#         # Command to run the bulk_generator.py script
#         command = ['python3', 'bulk_generate_input_modularize_new.py', file_path]
        
#         # Run the command
#         result = subprocess.run(command, check=True, text=True, capture_output=True)
        
#         # Print the output from the command
#         print(f"Running {file_path}:")
#         print("Output:", result.stdout)
#         print("Errors:", result.stderr)
        
#         # Append the output to the output_list
#         output_list.append(result.stdout.strip())

#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred while running the bulk_generator script on {file_path}: {e}")
#         print("Output:", e.output)
#         print("Errors:", e.stderr)

# def process_all_files_in_directory(directory, output_list):
#     # List all files in the given directory and sort them
#     filenames = sorted(os.listdir(directory))
    
#     for filename in filenames:
#         file_path = os.path.join(directory, filename)
#         if os.path.isfile(file_path):
#             print(f"Processing file: {file_path}")
#             run_bulk_generator(file_path, output_list)
#             print("------------------------------------------------")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Run bulk_generator on all files in a directory.')
#     parser.add_argument('directory', type=str, help='The directory containing files to process')

#     args = parser.parse_args()
    
#     process_all_files_in_directory(args.directory, output_list)
    
#     with open('output_file.txt', 'w') as file:
#         for item in output_list:
#             print(item)
#             file.write(str(item) + '\n')
#         print('written successfully')
# ========================================================================================

# import subprocess
# import os
# import argparse
# # from common_v3 import *

# output_list1 = []

# def run_bulk_generator(file_path, output_list1):
#     try:
#         # Command to run the bulk_generate_input_modularize_new.py script
#         command = ['python3', 'generate_input_modularize_new.py', file_path]
#         # command = ['python3', 'bulk_generate_input_modularize_new.py', file_path]
        
#         # Run the command
#         result = subprocess.run(command, check=True, text=True, capture_output=True)
        
#         # Split the output into lines and take the last line
#         last_output_line = result.stdout.strip().splitlines()[-1]
        
#         # Print the output from the command
#         print(f"Running {file_path}:")
#         print("Last Output Line:", last_output_line)
#         print("Errors:", result.stderr)
        
#         # Append the last output line to the output_list
#         # Check if "log" is in the last output line
#         if "log" in last_output_line:
#             output_list1.append(f"File '{os.path.basename(file_path)}: {last_output_line}")
#         else:
#             output_list1.append(last_output_line)
#             # nakeval_balki(output_list)

#     except subprocess.CalledProcessError as e:
#         # If an error occurs, print and append the error message along with the file name
#         # error_message = f"Error occurred while running {file_path}: {e}\nOutput: {e.output}\nErrors: {e.stderr}"
#         error_message = f"Error occurred while running {file_path}: {e}"
        
#         print(error_message)
#         output_list1.append(error_message)

# def process_all_files_in_directory(directory, output_list1):
#     # List all files in the given directory and sort them
#     filenames = sorted(os.listdir(directory))
    
#     for filename in filenames:
#         file_path = os.path.join(directory, filename)
#         if os.path.isfile(file_path):
#             print(f"Processing file: {file_path}")
#             run_bulk_generator(file_path, output_list1)
#             print("------------------------------------------------")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Run bulk_generate_input_modularize_new on all files in a directory.')
#     parser.add_argument('directory', type=str, help='The directory containing files to process')

#     args = parser.parse_args()
    
#     output_file = f"output_{os.path.basename(os.path.normpath(args.directory))}.txt"
    
#     process_all_files_in_directory(args.directory, output_list1)
    
    
#     with open(output_file, 'w') as file:
#         for item in output_list1:
#             print(item)
#             file.write(str(item) + '\n')
#         print(f'Written successfully to {output_file}')

# ==============================================================================

import subprocess
import os
import argparse
import openpyxl

output_list1 = []

def run_bulk_generator(file_path, output_list1):
    try:
        # Command to run the bulk_generate_input_modularize_new.py script
        command = ['python3', 'generate_input_modularize_new.py', file_path]
        # command = ['python3', 'bulk_generate_input_modularize_new.py', file_path]
        
        # Run the command
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        
        # Split the output into lines and take the last line
        last_output_line = result.stdout.strip().splitlines()[-1]
        
        # Print the output from the command
        print(f"Running {file_path}:")
        print("Last Output Line:", last_output_line)
        print("Errors:", result.stderr)
        
        # Append the last output line to the output_list
        # Check if "log" is in the last output line
        if "log" in last_output_line:
            output_list1.append((os.path.basename(file_path), last_output_line))
        else:
            output_list1.append((os.path.basename(file_path), last_output_line))
            # nakeval_balki(output_list)

    except subprocess.CalledProcessError as e:
        # If an error occurs, print and append the error message along with the file name
        error_message = f"Error occurred while running {file_path}: {e}"
        
        print(error_message)
        output_list1.append((os.path.basename(file_path), error_message))

def process_all_files_in_directory(directory, output_list1):
    # List all files in the given directory and sort them
    filenames = sorted(os.listdir(directory))
    
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            run_bulk_generator(file_path, output_list1)
            print("------------------------------------------------")

def write_to_excel(output_file, output_list1):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"
    
    # Write headers
    ws.append(["Sent Id ", "Revised Output"])
    
    # Write data
    for item in output_list1:
        ws.append(list(item))
    
    # Save the workbook
    wb.save(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run bulk_generate_input_modularize_new on all files in a directory.')
    parser.add_argument('directory', type=str, help='The directory containing files to process')

    args = parser.parse_args()
    
    txt_output_file = f"output_{os.path.basename(os.path.normpath(args.directory))}.txt"
    xlsx_output_file = f"output_{os.path.basename(os.path.normpath(args.directory))}.xlsx"
    
    process_all_files_in_directory(args.directory, output_list1)
    
    with open(txt_output_file, 'w') as file:
        for item in output_list1:
            print(item)
            file.write(f"{item[0]}: {item[1]}\n")
        print(f'Written successfully to {txt_output_file}')
    
    write_to_excel(xlsx_output_file, output_list1)
    print(f'Written successfully to {xlsx_output_file}')


# import subprocess
# import os
# import argparse

# output_list = []

# def run_bulk_generator(file_path, output_list):
#     try:
#         # Command to run the bulk_generate_input_modularize_new.py script
#         command = ['python3', 'bulk_generate_input_modularize_new.py', file_path]
        
#         # Run the command
#         result = subprocess.run(command, check=True, text=True, capture_output=True)
        
#         # Split the output into lines and take the last line
#         last_output_line = result.stdout.strip().splitlines()[-1]
        
#         # Print the output from the command
#         print(f"Running {file_path}:")
#         print("Last Output Line:", last_output_line)
#         print("Errors:", result.stderr)
        
#         # Append the last output line to the output_list
        
        
#         # Check if "log" is in the last output line
#         if "log" in last_output_line:
#             output_list.append(f"File '{os.path.basename(file_path)}' contains 'log'")
#         else:
#             output_list.append(last_output_line)

#     except subprocess.CalledProcessError as e:
#         # If an error occurs, print and append the error message along with the file name
#         error_message = f"Error occurred while running {file_path}: {e}"
#         print(error_message)
#         output_list.append(error_message)

# def process_all_files_in_directory(directory, output_list):
#     # List all files in the given directory and sort them
#     filenames = sorted(os.listdir(directory))
    
#     for filename in filenames:
#         file_path = os.path.join(directory, filename)
#         if os.path.isfile(file_path):
#             print(f"Processing file: {file_path}")
#             run_bulk_generator(file_path, output_list)
#             print("------------------------------------------------")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Run bulk_generate_input_modularize_new on all files in a directory.')
#     parser.add_argument('directory', type=str, help='The directory containing files to process')

#     args = parser.parse_args()
    
#     process_all_files_in_directory(args.directory, output_list)
    
#     with open('output_file.txt', 'w') as file:
#         for item in output_list:
#             print(item)
#             file.write(str(item) + '\n')
#         print('Written successfully to output_file.txt')
