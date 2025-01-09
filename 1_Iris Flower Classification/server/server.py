from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 
import pickle
import numpy as np
import os

# Set the template folder path to the root-level templates folder
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'), 
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
CORS(app)  # This will allow all cross-origin requests

# Load the trained model
def load_model():
    with open('./model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Flask will look in the root-level templates folder

# Route to get the flower prediction
@app.route('/get_flower_name', methods=['POST'])
def get_flower_name():
    try:
        # Get data from POST request
        data = request.get_json()
        input_data = np.array(data['input'])  # assuming input is a list of feature values
        
        # Load the model and make prediction
        model = load_model()
        prediction = model.predict([input_data])
        
        # Map the numeric prediction to a flower name (assuming this is the Iris dataset)
        flower_names = ['setosa', 'versicolor', 'virginica']
        predicted_flower = flower_names[int(prediction[0])]
        
        # Return the prediction as a JSON response
        return jsonify({'flower_name': predicted_flower})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
