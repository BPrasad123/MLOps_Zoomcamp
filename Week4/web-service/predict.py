# import libraries

import pickle

from flask import Flask, jsonify, request

# load saved model
with open('lin_reg.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


# proprocess data
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


# # genrate prediction
def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]


# initialize flask application
app = Flask('duration-prediction')


# create endpoint
@app.route('/predict', methods=['POST'])
def predict_endpoint():

    ride = request.get_json()

    features = prepare_features(ride)

    pred = predict(features)

    result = {
        'prediction': pred
    }

    return jsonify(result)

# only app is run when script is called directly
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
