from flask import Flask, request, url_for, jsonify
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import requests
import os
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Globals 
METADATA_ENDPOINT = 'http://metadata.google.internal'
PROJECT_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/project/project-id'
ZONE_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/instance/zone'
HEADERS = {'Metadata-Flavor': 'Google'}
CREDENTIALS = GoogleCredentials.get_application_default()

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

def list_forwardingrules():
    service = discovery.build('compute', 'v1', credentials=CREDENTIALS)
    project = metadata_call('project')
    region = metadata_call('region')
    request = service.forwardingRules().list(project=project, region=region)
    forwardingrules = []
    while request is not None:
        response = request.execute()
        for forwarding_rule in response['items']:
            forwardingrules.append({'name':forwarding_rule['name'], 'IPAddress':forwarding_rule['IPAddress']})
        request = service.forwardingRules().list_next(previous_request=request, previous_response=response)
    return forwardingrules

def check_forwardingrule_exists_with_name(name):
    forwardingrules = list_forwardingrules()
    for rule in forwardingrules:
        if rule['name'] == name:
            return (True)
    return (False)

def check_forwardingrule_exists_with_ip(ip):
    forwardingrules = list_forwardingrules()
    for rule in forwardingrules:
        if rule['IPAddress'] == ip:
            return (True)
    return (False)

# End of Functions

@app.route("/healthz")
def health():
    return jsonify(status=True, success=True, msg="I am Alive!")

@app.route("/metadata/project")
def metadata_project():
    return jsonify(project=metadata_call('project'))

@app.route("/metadata/zone")
def metadata_zone():
    return jsonify(project=metadata_call('zone'))

@app.route("/metadata/region")
def metadata_region():
    return jsonify(project=metadata_call('region'))

@app.route("/forwardingrules/exists/name/<name>")
def fowardingrules_name_exists(name):
    if check_forwardingrule_exists_with_name(name):
        return jsonify(exists=True)
    else:
        return jsonify(exists=False)

@app.route("/forwardingrules/exists/ip/<ip>")
def fowardingrules_ip_exists(ip):
    if check_forwardingrule_exists_with_ip(ip):
        return jsonify(exists=True)
    else:
        return jsonify(exists=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
