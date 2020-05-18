import os
from flask import Flask, request, jsonify

app = Flask(__name__)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 8080))


@app.route("/healthz", methods=['GET'])
def health():
    return jsonify({"status": True, "success": True, "msg": "I am Alive!", "cloud": None})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"status": True, "success": False, "msg": "CCC couldn't identify cloud platform."})


def run_server():
    app.run(host='0.0.0.0', port=FLASK_PORT)
