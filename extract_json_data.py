import json

def extract_discourse_values(json_file_path,file_name):
    # Read the JSON file
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize a list to store discourse values
    discourse_values = []

    # Iterate through each usr_sub_id entry
    for entry in data:
        usr_sub_id = entry.get('usr_id')
        rows = entry.get('rows', [])
        
        # Collect discourse values from each row
        for row in rows:
            discourse_value = row.get('Discourse', '')
            # print(discourse_value,'dvvv')
            if discourse_value :  # Check if discourse_value is not empty
                discourse_id=discourse_value.split('.')[0]
                if file_name==discourse_id:
                    # discourse_values.append(
                    #     # "usr_sub_id": usr_sub_id,
                    #     discourse_value
                    # )
                    
                    return discourse_value

    # Print the collected discourse values
    # for discourse in discourse_values:
    #     print(f"usr_sub_id: {discourse['usr_sub_id']}, Discourse: {discourse['Discourse']}")


    # Optionally return the collected discourse values if needed
    

if __name__ == "__main__":
    json_file_path = 'output.json'  # Replace with the path to your JSON file
    # discourse_data = extract_discourse_values(json_file_path)
