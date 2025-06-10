import base64
from flask import Flask, jsonify, render_template, request
from config import key  # Ensure the API key is in your config file
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Correct API URL for text-to-image generation
CLIPDROP_API_URL = 'https://clipdrop-api.co/text-to-image/v1'

@app.route('/')
def index():
    return render_template('Genrate-image.html')  # Serve the HTML file

@app.route('/generateimages', methods=['POST'])
def generate_images():
    prompt = request.json.get('prompt')  # Get the 'prompt' from the POST request body

    headers = {
        'x-api-key': key,  # Send the API key in the header
    }

    # Prepare the data to be sent in the form
    files = {
        'prompt': (None, prompt, 'text/plain')  # 'prompt' as the form field
    }

    try:
        # Make the POST request to Clipdrop API with 'multipart/form-data'
        response = requests.post(CLIPDROP_API_URL, headers=headers, files=files)

        # Check if the request was successful
        response.raise_for_status()

        # If the request is successful, encode the returned image to base64
        image_data = base64.b64encode(response.content).decode('utf-8')

        # Return the base64 image as a response
        return jsonify({
            'image': f'data:image/png;base64,{image_data}'
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
