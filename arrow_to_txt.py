# import pyarrow as pa
# import pyarrow.ipc as ipc

# # Path to your file
# file_path = "data-00196-of-00197.arrow"

# # Open the file
# with pa.memory_map(file_path, 'r') as source:
#     reader = ipc.open_stream(source)
#     table = reader.read_all()

# # Convert to pandas DataFrame if needed
# df = table.to_pandas()

# # Print the data
# print(df)
# import pyarrow as pa
# import pyarrow.ipc as ipc

# # Path to your .arrow file
# file_path = "/home/user/varsh/dataset_hi/c4_hi.txt/train/data-00195-of-00197.arrow"

# # Output .txt file
# output_file = "/home/user/varsh/dataset_hi/c4_hi.txt/hindi_texts.txt"

# # Open the .arrow file and read the data
# with pa.memory_map(file_path, 'r') as source:
#     reader = ipc.open_stream(source)
#     table = reader.read_all()

# # Convert to Pandas DataFrame
# df = table.to_pandas()

# # Extract the 'text' column and write to a .txt file
# with open(output_file, 'w', encoding='utf-8') as file:
#     for text in df['text']:
#         file.write(text)

# print(f"Hindi text has been successfully written to {output_file}.")
import os
import pyarrow as pa
import pyarrow.ipc as ipc

# Folder containing the .arrow files
folder_path = "/home/user/varsh/dataset_hi/c4_hi.txt/train"

# Output .txt file
output_file = "/home/user/varsh/dataset_hi/hindi_texts.txt"

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as output:
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".arrow"):
            print(filename)
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")

            # Open the .arrow file and read the data
            with pa.memory_map(file_path, 'r') as source:
                reader = ipc.open_stream(source)
                table = reader.read_all()

            # Convert to Pandas DataFrame
            df = table.to_pandas()

            # Extract the 'text' column and write to the .txt file
            for text in df['text']:
                output.write(text)  # Ensure each text ends with a newline

print(f"Hindi text has been successfully written to {output_file}.")
