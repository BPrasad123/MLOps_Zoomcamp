# import libraries

import os
import pickle

import mlflow
from flask import Flask, request, jsonify



# load saved model

RUN_ID = 'fd38a9df86b149e69632f44646684e49'
# RUN_ID = os.getenv('RUN_ID')
logged_model = f's3://bhagabat-mlflow-rf-greentaxi/1/{RUN_ID}/artifacts/model'
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

# proprocess data
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


# # genrate prediction
def predict(features):
    preds = model.predict(features)
    return float(preds[0])


# initialize flask application
app = Flask('duration-prediction')


# create endpoint
@app.route('/predict', methods=['POST'])
def predict_endpoint():

    ride = request.get_json()

    features = prepare_features(ride)

    pred = predict(features)

    result = {
        'prediction': pred,
        'Model RUN_ID': RUN_ID
    }

    return jsonify(result)

# only app is run when script is called directly
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
