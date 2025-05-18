import os
import subprocess
import shutil
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'picture'
OUTPUT_FOLDER = 'Output/Panoptic_Results'
TARGET_FOLDER = os.path.join(OUTPUT_FOLDER, 'target')
TARGET_FILE = os.path.join(UPLOAD_FOLDER, 'target.jpg')
DESCRIPTION_FOLDER = 'output_final'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TARGET_FOLDER, exist_ok=True) 
os.makedirs(DESCRIPTION_FOLDER, exist_ok=True)

def clear_directory(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    
    clear_directory(TARGET_FOLDER)

    # Save the uploaded image as 'target.jpg'
    file.save(TARGET_FILE)
    
    # Run the command to process the image
    command = f'python FoodSAM/panoptic.py --img_path {TARGET_FILE} --output {OUTPUT_FOLDER}'
    subprocess.run(command, shell=True)
    
    # After processing the image, run describe.py
    describe_command = 'python describe.py'
    subprocess.run(describe_command, shell=True)
    
    # Fetch description and path to the speech file
    description_file_path = os.path.join(DESCRIPTION_FOLDER, 'description.txt')
    speech_file_path = os.path.join(DESCRIPTION_FOLDER, 'speech.mp3')

    # Read description content
    with open(description_file_path, 'r') as file:
        description_content = file.read()

    # Construct response with description and URL to the speech file
    response_data = {
        'description': description_content,
        'speech_url': f'/speech-file'
    }
    print(jsonify(response_data))
    return jsonify(response_data)

@app.route('/speech-file', methods=['GET'])
def get_speech_file():
    return send_from_directory(DESCRIPTION_FOLDER, 'speech.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)