# Open the file in read mode
with open('/home/varshith/hindi_gen/print_stmt.txt', 'r') as file:
    # Read the contents of the file
    text = file.read()

# Split the text into lines
lines = text.split("\n")

# Find the maximum length of the text before the colon
max_length_before_colon = max([line.index(":") for line in lines if ":" in line])

# Format the lines
formatted_lines = [f"{line[:line.index(':')]:<{max_length_before_colon}} : {line[line.index(':')+1:]}\n" if ":" in line else line for line in lines]

# Join the formatted lines
formatted_text = "\n".join(formatted_lines)

# Write the formatted text back to the file
with open('/home/varshith/hindi_gen/print_stmt.txt', 'w') as file:
    file.write(formatted_text)
