import os
from flask import Flask, request, jsonify
import base64
import re

app = Flask(__name__)

# Your personal information
USER_ID = "your_full_name_ddmmyyyy"
EMAIL = "your_email@college.edu"
ROLL_NUMBER = "your_roll_number"

@app.route('/bfhl', methods=['POST'])
def process_data():
    data = request.json.get('data', [])
    file_b64 = request.json.get('file_b64', '')

    numbers = [item for item in data if item.isdigit()]
    alphabets = [item for item in data if item.isalpha()]
    highest_lowercase = max([item for item in alphabets if item.islower()], default='')

    file_valid = False
    file_mime_type = ''
    file_size_kb = 0

    if file_b64:
        try:
            file_data = base64.b64decode(file_b64)
            file_valid = True
            file_size_kb = len(file_data) / 1024
            file_mime_type = get_mime_type(file_data)
        except:
            pass

    response = {
        "is_success": True,
        "user_id": USER_ID,
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else [],
        "file_valid": file_valid,
        "file_mime_type": file_mime_type,
        "file_size_kb": round(file_size_kb, 2)
    }

    return jsonify(response)

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

def get_mime_type(file_data):
    # Simple MIME type detection based on file signatures
    if file_data.startswith(b'\xFF\xD8\xFF'):
        return 'image/jpeg'
    elif file_data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif file_data.startswith(b'%PDF'):
        return 'application/pdf'
    else:
        return 'application/octet-stream'

if __name__ == '__main__':
    app.run(debug=True)













