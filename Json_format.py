import os
import glob
import json

def Json_format(directory_path):
    # Specify the output file path
    output_file_path = 'output.json'
    
    # Initialize a list to store the results
    results = []

    # Get a list of all files in the directory
    
    # file_names = os.listdir(directory_path)
    # file_names.sort()
    files = glob.glob(os.path.join(directory_path, '*'))
    # Check if files are found
    if not files:
        print("No files found in the directory.")
        return

    # Read and print specific lines from each file
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding if needed
            lines = file.readlines()  # Read all lines into a list
            
            # Debug print to check if lines are read correctly
            # print(f"Reading file: {file_path}")
            # print(f"Total lines read: {len(lines)}")
            
            req_lines = []
            selected_lines = [2, 3, 5, 7, 8]  # Lines to print (1-based indexing)
            for i in selected_lines:
                if i-1 < len(lines):
                    req_lines.append(lines[i-1].strip())
            
            dictformat = {
                "usr_sub_id": os.path.basename(file_path),
                "rows": []
            }
            
            if req_lines:
                concept_list = req_lines[0].split(',')
                index_list = req_lines[1].split(',') if len(req_lines) > 1 else []
                gnp_list = req_lines[2].split(',') if len(req_lines) > 2 else []
                dis_list = req_lines[3].split(',') if len(req_lines) > 3 else []
                spk_list = req_lines[4].split(',') if len(req_lines) > 4 else []
                
                no_of_rows = len(concept_list)
                
                for j in range(no_of_rows):
                    inside_dict = {
                        "concept": concept_list[j] if j < len(concept_list) else "",
                        "index": index_list[j] if j < len(index_list) else "",
                        "gnp": gnp_list[j] if j < len(gnp_list) else "",
                        "Discourse": dis_list[j] if j < len(dis_list) else "",
                        "spkview": spk_list[j] if j < len(spk_list) else ""
                    }
                    dictformat['rows'].append(inside_dict)
            
            # Debug print to check the dictformat content
            # print(f"Processed data for file: {file_path}")
            # print(json.dumps(dictformat, indent=4))
            
            results.append(dictformat)
    results.sort(key=lambda x: x['usr_sub_id'])

    # Write the results to the output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    # print(f"Output stored in {output_file_path}")

# if __name__ == "__main__":
#     Json_format()

# # Assuming the main script needs to call Json_format function and pass the appropriate path

# import os
# import glob
# import json

# def Json_format(file_path):
#     # Specify the output file path
#     output_file_path = 'output.json'
    
#     # Initialize a list to store the results
#     results = []

#     with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding if needed
#         lines = file.readlines()  # Read all lines into a list
        
#         req_lines = []
#         selected_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # Lines to extract (1-based indexing)
#         for i in selected_lines:
#             if i-1 < len(lines):
#                 req_lines.append(lines[i-1].strip())
        
#         # Prepare the dictionary format
#         dictformat = {
#             "usr_id": os.path.basename(file_path),
#             "src_sentence": req_lines[0].split(','),
#             "rows": [],
#             "sentence_type": req_lines[10]
#         }
        
#         if req_lines:
#             concept_list = req_lines[1].split(',')
#             index_list = req_lines[2].split(',') if len(req_lines) > 1 else []
#             seman_data = req_lines[3].split(',') if len(req_lines) > 2 else []
#             gnp_list = req_lines[4].split(',') if len(req_lines) > 3 else []
#             depend_data = req_lines[5].split(',') if len(req_lines) > 4 else []
#             dis_list = req_lines[6].split(',') if len(req_lines) > 5 else []
#             spk_list = req_lines[7].split(',') if len(req_lines) > 6 else []
#             scope_data = req_lines[8].split(',') if len(req_lines) > 7 else []
#             construction_data = req_lines[9].split(',') if len(req_lines) > 8 else []

#             no_of_rows = len(concept_list)
            
#             for j in range(no_of_rows):
#                 inside_dict = {
#                     "concept": concept_list[j] if j < len(concept_list) else "",
#                     "index": index_list[j] if j < len(index_list) else "",
#                     "semantics": seman_data[j] if j < len(seman_data) else "",
#                     "gnp": gnp_list[j] if j < len(gnp_list) else "",
#                     "dependency": depend_data[j] if j < len(depend_data) else "",
#                     "Discourse": dis_list[j] if j < len(dis_list) else "",
#                     "spkview": spk_list[j] if j < len(spk_list) else "",
#                     "scope": scope_data[j] if j < len(scope_data) else "",
#                     "construction": construction_data[j] if j < len(construction_data) else ""
                    
                    
#                 }
#                 dictformat['rows'].append(inside_dict)
        
#         results.append(dictformat)
#     results.sort(key=lambda x: x['usr_id'])

#     # Write the results to the output file
#     with open(output_file_path, 'w', encoding='utf-8') as outfile:
#         json.dump(results, outfile, ensure_ascii=False, indent=4)

# # Example call to the function
# if __name__ == "__main__":
#     file_path = "path_to_your_file.txt"  # Replace with the actual file path
#     Json_format(file_path)
