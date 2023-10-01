# Flask backend
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from .predictor import predict_fight_outcome, model, fighter_profiles
from .fighter_query import retrieve_fighter


app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    fighter1 = data['fighter1']
    fighter2 = data['fighter2']
    prediction = predict_fight_outcome(model=model, fighter1=fighter1, fighter2=fighter2, fighter_profiles=fighter_profiles)
    if prediction:
        fighter1_data = retrieve_fighter(fighter_name=fighter1)
        fighter2_data = retrieve_fighter(fighter_name=fighter2)
    else:
        return "Fighter not found, check your spelling!", 404

    returnObj = {
        "prediction": prediction,
        "fighter1": fighter1_data,
        "fighter2": fighter2_data
    }

    return jsonify(returnObj)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(host='0.0.0.0', debug=False, port=port)