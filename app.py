from flask import Flask, request
import json, logging, datetime


app = Flask(__name__)
FORMAT = ''
logging.basicConfig(filename='app.log', level=logging.DEBUG)


@app.route("/")
def hello():
    app.logger.info("Hello world successfull")
    return "Hello World!"

@app.route("/status")
def status():    
    response = app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info("Status request successfull")
    logging.debug(f"{datetime.datetime.now()}, {request.path} endpoint was reached")
    return json.dumps({"result": "OK - healthy"}), 200, {'ContentType':'application/json'} 

@app.route("/metrics")
def metrics():
    logging.debug(f"{datetime.datetime.now()}, {request.path} endpoint was reached")
    app.logger.info("Metrics request successfull")
    return json.dumps({"data": {'UserCount': 140, 'UserCountActive': 23}}), 200, {'ContentType':'application/json'} 

if __name__ == "__main__":
    app.run(host='0.0.0.0')
