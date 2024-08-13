import re
import os

def extract_and_create_files(input_file_path, output_folder):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Regex pattern to match each set of text
    pattern = re.compile(r'<sent_id= (.*?)>(.*?)</sent_id>', re.DOTALL)

    # Find all matches
    matches = pattern.findall(content)

    for match in matches:
        sentence_id = match[0]
        text_content = match[1].strip()
        
        # Create a file with the sentence_id as the filename in the output folder
        with open(os.path.join(output_folder, f"{sentence_id}.txt"), 'w', encoding='utf-8') as output_file:
            output_file.write(text_content)

# Path to the input file
input_file_path = 'vertical_nios_1ch.txt'
# Path to the output folder
output_folder = 'csv_nios_1ch'
extract_and_create_files(input_file_path, output_folder)
