from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load your pre-trained model
model = load_model('Cats&DogsClassifier.h5')

# Function to preprocess the image for prediction
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    # Save the image to a temporary file
    image_path = 'temp_image.jpg'
    image_file.save(image_path)

    try:
        # Preprocess the image for prediction
        img_array = preprocess_image(image_path)

        # Make predictions
        predictions = model.predict(img_array)

        if predictions > 0.5:
            prediction = "dog"
        else:
            prediction = "cat"
        
        # Clean up temporary image file
        os.remove(image_path)

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
