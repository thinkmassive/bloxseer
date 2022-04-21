from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

import json
import random
import time
import urllib.request

app = Flask(__name__)
#app.config["DEBUG"] = True

metrics = PrometheusMetrics(app)
metrics.info('api_info', 'API info', version='0.1-alpha')

# Not currently used, served by Aperture static files
@app.route('/')
def home():
    return "Welcome to bloxseer\n"

@app.route('/health')
def health():
    return "OK\n"

@app.route('/event')
def event():
    return "TODO: list of events\n"

@app.route('/new')
def new():
    return "TODO: new event form\n"

@app.route('/price')
def price():
    response = ''
    with urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json") as url:
        coindesk_json = url.read().decode()
        data = json.loads(coindesk_json)
        response = data['bpi']['USD']['rate']
    return response

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

app.run()
