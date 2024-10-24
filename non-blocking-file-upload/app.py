from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/upload-video": {"origins": "http://127.0.0.1:3000"}})


# Path to save uploaded videos
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-video', methods=['POST'])
def upload_video():
    # Check if video part exists in the request
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']

    # Check if the filename is not empty
    if video_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file to the designated folder
    video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename))
    
    return jsonify({"message": "Upload successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
