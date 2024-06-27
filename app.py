from flask import Flask, request, jsonify
from flask_cors import CORS
#from pymycobot.mycobot import MyCobot
import os
import pymongo
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['mycobot']
collection = db['images']

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Store image path in MongoDB
        collection.insert_one({'filename': filename, 'filepath': filepath})
        
        # Process the image
        processed_filepath = process_image(filepath)
        
        # Draw the image on canvas
        draw_image_on_canvas(processed_filepath)
        
        return jsonify({"message": "File uploaded and processed successfully"}), 200
    return jsonify({"error": "File upload failed"}), 500

def process_image(filepath):
    # Load the image
    image = cv2.imread(filepath)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Save the processed image
    processed_filepath = filepath.replace('.', '_gray.')
    cv2.imwrite(processed_filepath, gray_image)
    return processed_filepath

def draw_image_on_canvas(filepath):
    # Initialize MyCobot
    mc = MyCobot('/dev/ttyAMA0', 1000000)
    
    # Load and process the image
    image = cv2.imread(filepath)
    height, width = image.shape[:2]
    
    # Example loop to move MyCobot
    for y in range(0, height, 10):
        for x in range(0, width, 10):
            if image[y, x] < 128:  # Example threshold for black pixel
                mc.send_angles([x, y, 0, 0, 0, 0], 80)  # Example coordinates
                mc.pump_on()  # Example command to start painting
            else:
                mc.pump_off()  # Example command to stop painting

    mc.release_all_servos()

if __name__ == '__main__':
    app.run(debug=True)
