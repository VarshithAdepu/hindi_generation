from flask import Flask, request, jsonify
from updated.service_old import process_file_data  # Import the service layer function

app = Flask(__name__)

# API Route to process the file and return the result
@app.route('/process', methods=['POST'])
def process_file():
    # Check if 'input_data' is present in the request JSON
    if 'input_data' not in request.json:
        return jsonify({"error": "No input data provided"}), 400
    
    # Get the input data from the request
    input_data = request.json['input_data']
    print(input_data, type(input_data), 'inputdata')

    try:
        # Call the service layer to process the input data
        output = process_file_data(input_data)
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
