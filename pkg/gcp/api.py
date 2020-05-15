from flask import Flask, request, url_for, jsonify
import os
from features import *


app = Flask(__name__)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5001))

@app.route("/healthz")
def health():
	return jsonify(status=True, success=True, msg="I am Alive!")

# METADATA
@app.route("/metadata/project")
def metadata_project():
	return jsonify(project=metadata.get('project'))

@app.route("/metadata/zone")
def metadata_zone():
	return jsonify(zone=metadata.get('zone'))

@app.route("/metadata/region")
def metadata_region():
	return jsonify(region=metadata.get('region'))

# FORWARDING RULES
# TODO: Change this to a get call.
# Sample URL: http://IP/forwardingrules/get?{ip/name}=<something>
@app.route("/forwardingrules/get")
def fowardingrules_get():
	if 'ip' in request.args:
		fr = forwardingrules.get_with_ip(request.args['name'])
	elif 'name' in request.args:
		fr = forwardingrules.get_with_name(request.args['name'])
	elif not bool(request.args):
		fr = forwardingrules.list()

	return jsonify(fr)

# TODO: Make this do the part of creating target instances
# Sample URL: http://IP/forwardingrules/create?ip=<ip>&name=<name>
@app.route("/forwardingrules/create")
def api_create_forwarding_rule():
	if 'ip' not in request.args or 'name' not in request.args:
		return jsonify(False)
	ip = request.args['ip']
	name = request.args['name']
	created_items = {}
	created_items['target_instance'] = targetinstances.create(name, instance_ip=ip)
	if created_items['target_instance']:
		created_items['forwarding_rule'] = forwardingrules.create(name, created_items['target_instance']['name'])
	else:
		return jsonify(False)
	return (jsonify(created_items))

# TODO: Make this do the part of deleting target instances
@app.route("/forwardingrules/delete")
def api_delete_forwarding_rule(name):
	if 'name' not in request.args:
		return jsonify(False)
	return (jsonify(targetinstances.delete(name) and forwardingrules.delete(name)))

def run_server:
	app.run(host='0.0.0.0', port=FLASK_PORT)
