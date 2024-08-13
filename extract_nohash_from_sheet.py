import pandas as pd
import argparse
import os

def extract_columns(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Check if 'Original Sent' column does not have '#' and 'Resolved output' column does not have '#', 'Error', or 'log'
    condition = (~df['Original Sent'].str.contains('#')) & \
                (~df['Revised Output'].str.contains('#')) & \
                (~df['Revised Output'].str.contains('Error', case=False)) & \
                (~df['Revised Output'].str.contains('log', case=False))

    # Filter the DataFrame based on the condition
    filtered_df = df[condition]

    # Select the columns to be written to the output file
    result_df = filtered_df[['Sent Id ', 'Original Sent', 'Revised Output']]

    # Write the result to the output Excel file
    result_df.to_excel(output_file, index=False, header=True)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract specific columns from an Excel file and save to a new file.")
    parser.add_argument('input_file', type=str, help="Path to the input Excel file")

    # Parse arguments
    args = parser.parse_args()

    # Generate output filename based on input filename
    input_file_basename = os.path.basename(args.input_file)
    output_file = os.path.join(os.path.dirname(args.input_file), f"nohash_{input_file_basename}")

    # Call the function with the arguments
    extract_columns(args.input_file, output_file)

# =====================================================================================================

#to identify errors output like sys.exit or log errors
# import pandas as pd
# import argparse
# import os

# def extract_columns(input_file, output_file):
#     # Read the Excel file
#     df = pd.read_excel(input_file)

#     # Check if both columns do not have '#' and if 'Resolved output' contains 'Error' or 'Log'
#     condition = ~df['Original Sent'].str.contains('#') & (df['Revised Output'].str.contains('Error') | df['Revised Output'].str.contains('log'))

#     # Filter the DataFrame based on the condition
#     filtered_df = df[condition]

#     # Select the columns to be written to the output file
#     result_df = filtered_df[['Sent Id ', 'Original Sent', 'Revised Output']]

#     # Write the result to the output Excel file
#     result_df.to_excel(output_file, index=False, header=True)

# if __name__ == "__main__":
#     # Set up argument parser
#     parser = argparse.ArgumentParser(description="Extract specific columns from an Excel file and save to a new file.")
#     parser.add_argument('input_file', type=str, help="Path to the input Excel file")

#     # Parse arguments
#     args = parser.parse_args()

#     # Generate output filename based on input filename
#     input_file_basename = os.path.basename(args.input_file)
#     output_file = os.path.join(os.path.dirname(args.input_file), f"nohash_{input_file_basename}")

#     # Call the function with the arguments
#     extract_columns(args.input_file, output_file)
