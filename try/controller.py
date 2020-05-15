from flask import Flask, request, url_for, jsonify
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import requests

# Globals 
METADATA_ENDPOINT = 'http://metadata.google.internal'
PROJECT_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/project/project-id'
ZONE_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/instance/zone'
HEADERS = {'Metadata-Flavor': 'Google'}

app = Flask(__name__)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5001))

# Functions 

def metadata_call(entity):
    if entity == "project":
        endpoint = PROJECT_ENDPOINT
        response = requests.get(endpoint, headers=HEADERS)
        return (response.text)
    elif (entity == "zone" or entity == "region"):
        endpoint = ZONE_ENDPOINT
        response = requests.get(endpoint, headers=HEADERS)
        if entity == "zone":
            zone = response.text.split('/')[-1] # The last index is the zone - Example: projects/565214722813/zones/asia-south1-a
            return (zone)
        elif entity == "region":
            region = response.text.split('/')[-1][:-2]
            return (region)


# End of Functions

@app.route("/healthz")
def health():
    return jsonify(status=True, success=True, msg="I am Alive!")

@app.route("/metadata/project")
    return jsonify(project=metadata_call('project'))
@app.route("/metadata/zone")
    return jsonify(project=metadata_call('zone'))
@app.route("/metadata/region")
    return jsonify(project=metadata_call('region'))





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
