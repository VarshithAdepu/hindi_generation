# import re

# def extract_data(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = file.read()

#     # Regular expression to capture the <sent_id> block with its content
#     sent_id_pattern = re.compile(r'(<sent_id= [^>]+>.*?</sent_id>)', re.DOTALL)

#     # Find all matches for the <sent_id> blocks
#     matches = sent_id_pattern.findall(data)

#     with open(output_file, 'w', encoding='utf-8') as output:
#         for match in matches:
#             # Write the full <sent_id> block (including the opening and closing tags)
#             output.write(match.strip() + "\n\n")

# # Example usage
# extract_data('updated/nios_9ch_new_cnx.txt', 'output.txt')

# =====================================
import openpyxl

# File paths
input_file = "output.txt"  # Replace with the path to your input file
output_file = "1.xlsx"  # Path to save the output Excel file

# Create a new workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Sentences"

# Read data from the input file
with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

# Split the data into segments based on <sent_id>
segments = content.strip().split("\n\n")  # Separate by blank lines

# Write each segment into a new row in the Excel sheet
for row_index, segment in enumerate(segments, start=1):
    # Write the entire segment into one cell
    sheet.cell(row=row_index, column=1).value = segment.strip()

# Save the workbook
workbook.save(output_file)

print(f"Data has been successfully stored in '{output_file}'.")

