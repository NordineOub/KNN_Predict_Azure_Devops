from flask import Flask, request, jsonify
import joblib
import numpy as np
import json

# Metrique
from prometheus_client import (
    Counter,
    generate_latest,
    Histogram,
    REGISTRY,
)
PYTHON_REQUESTS_COUNTER = Counter("python_requests", "total requests")
PYTHON_FAILED_REQUESTS_COUNTER = Counter("python_failed_requests", "failed requests")
PYTHON_LATENCIES_HISTOGRAM = Histogram(
    "python_request_latency", "request latency by path"
)




#Importation du modele
knn =joblib.load('knn_Iris.pkl')


app = Flask(__name__)

@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest(REGISTRY), 200

@PYTHON_LATENCIES_HISTOGRAM.time()
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    #json_str = json.dumps({'sepal_length': int(sepal_length)})
   #print(data)

    # Make prediction using the model.
    prediction = knn.predict([[data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]])


    output ="Erreur"
    if prediction[0]==0:
        output = "Iris Setosa"
    if prediction[0]==1:
        output = "Iris Versicolor"
    if prediction[0]==2:
        output = "Iris Virginica"

    return "\n"+output+"\n" +str(prediction[0])





if __name__ == '__main__':
    app.run(port=5000, debug=True)

