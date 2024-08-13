# import re

# def comment_print_statements(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     with open(file_path, 'w') as file:
#         for line in lines:
#             # Check if the line contains a print statement
#             if re.search(r'^\s*print\s*\(.*\)', line):
#                 # Comment out the line
#                 line = f'# {line}'
#             file.write(line)

# # Example usage:
# file_path = 'common_v3.py'
# comment_print_statements(file_path)

# import re

# def remove_comments(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     with open(file_path, 'w') as file:
#         for line in lines:
#             # Check if the line is a comment
#             if not re.match(r'^\s*#', line):
#                 file.write(line)

# # Example usage:
# file_path = 'common_v3.py'
# remove_comments(file_path)
# ======================================================================

import re

def remove_extra_newlines(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Use a regular expression to replace multiple newlines with a single newline
    content = re.sub(r'\n\s*\n+', '\n\n', content)

    with open(file_path, 'w') as file:
        file.write(content)

# Example usage:
file_path = 'bulk_common_v3.py'
remove_extra_newlines(file_path)
# =====================================================================

# def remove_comments_from_file(input_file, output_file):
#     with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             stripped_line = line.strip()
#             if not stripped_line.startswith('#'):
#                 outfile.write(line)

# # Example usage
# input_file = '/home/varshith/USR_FILES/hindi_gen/bulk_common_v3.py'
# output_file = '/home/varshith/USR_FILES/hindi_gen/bulk_common_v4.py'
# remove_comments_from_file(input_file, output_file)

# =========================================================================

# import os

# def rename_files(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.startswith(" "):
#             new_filename = filename.replace(" ", "")
#             try:
#                 os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
#                 print(f"Renamed: {filename} to {new_filename}")
#             except Exception as e:
#                 print(f"Error renaming {filename}: {e}")

# # Specify the folder path
# folder_path = "/home/varshith/hindi_gen/1ch_nios"

# # Rename files in the specified folder
# rename_files(folder_path)

# =======================================================================


# import os

# def process_files_in_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if os.path.isfile(file_path):
#             process_file(file_path)

# def process_file(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     if len(lines) < 10:
#         # Ensure there are at least 10 lines
#         lines.extend(["\n"] * (10 - len(lines)))
    
#     # Replace "affirmative" with "%affirmative" in the 10th line
#     if 'affirmative' in lines[9] and '%affirmative' not in lines[9]:
#         lines[9] = lines[9].replace('affirmative', '%affirmative').rstrip('\n') + '\n'
#     elif '%affirmative' not in lines[9]:
#         lines[9] = lines[9].rstrip('\n') + '%affirmative\n'
    
#     if len(lines) < 11:
#         # Ensure there are at least 11 lines
#         lines.extend(["\n"] * (11 - len(lines)))
    
#     # Replace "nil" with "*nil" in the 11th line
#     if 'nil' in lines[10] and '*nil' not in lines[10]:
#         lines[10] = lines[10].replace('nil', '*nil').rstrip('\n') + '\n'
#     elif '*nil' not in lines[10]:
#         lines[10] = lines[10].rstrip('\n') + '*nil\n'

#     # Write the modified lines back to the file
#     with open(file_path, 'w') as file:
#         file.writelines(lines)

# # Specify the folder path
# folder_path = 'isma/isma_story1'
# process_files_in_folder(folder_path)

# ==========================================================


# import os

# def process_files_in_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if os.path.isfile(file_path):
#             process_file(file_path)

# def process_file(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     # Remove %affirmative and *nil from all lines
#     lines = [line.replace('%affirmative', '').replace('*nil', '').rstrip() + '\n' for line in lines]

#     # Write the modified lines back to the file
#     with open(file_path, 'w') as file:
#         file.writelines(lines)

# # Specify the folder path
# folder_path = 'isma/isma_story1'
# process_files_in_folder(folder_path)
