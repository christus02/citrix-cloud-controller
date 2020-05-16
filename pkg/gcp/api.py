import sys, os

from flask import Flask, request, url_for, jsonify
import os
from . import features
import re

regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

def is_IP(IP):
    if(re.search(regex, IP)):
        return True
    else:
        return False

def get_vip_from_fr_ti(fr, ti):
    data = {
            "externalIP":fr["IPAddress"],
            "internalIP":fr["IPAddress"],
            "protocol":fr["IPProtocol"],
            "ingressName":fr["name"],
            "portRange":fr["portRange"],
            "instanceName":""
            }
    if ti:
        data['instanceName'] = ti["instance"]
    return data

app = Flask(__name__)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 8080))

@app.route("/healthz", methods = ['GET'])
def health():
    return jsonify({"status":True, "success":True, "msg":"I am Alive!", "cloud":"gcp"})

# METADATA
@app.route("/metadata/project", methods = ['GET'])
def metadata_project():
	return jsonify(project=features.metadata.get('project'))

@app.route("/metadata/zone", methods = ['GET'])
def metadata_zone():
	return jsonify(zone=features.metadata.get('zone'))

@app.route("/metadata/region", methods = ['GET'])
def metadata_region():
	return jsonify(region=features.metadata.get('region'))

# FORWARDING RULES
# TODO: Change this to a get call.
# Sample URL: http://IP/forwardingrules/get?{ip/name}=<something>
@app.route("/forwardingrules/get")
def fowardingrules_get(request):
	if 'ip' in request.args:
		fr = features.forwardingrules.get_with_ip(request.args['ip'])
	elif 'name' in request.args:
		fr = features.forwardingrules.get_with_name(request.args['name'])
	elif not bool(request.args):
		fr = features.forwardingrules.list_forwardingrules()

	return jsonify(fr)

# TODO: Make this do the part of creating target instances
# Sample URL: http://IP/forwardingrules/create?ip=<ip>&name=<name>
@app.route("/forwardingrules", methods = ['GET', 'POST', 'DELETE'])
def api_forwarding_rules():
        if request.method == "GET":
            return(fowardingrules_get(request))
        elif request.method == "POST":
            return(api_create_forwarding_rule(request))
        elif request.method == "DELETE":
            return(api_delete_forwarding_rule(request))
        else:
            return jsonify(status=False, msg="Unsupported Request Method")

# Sample URL: http://IP/forwardingrules/create?ip=<ip>&name=<name>
@app.route("/vip", methods = ['GET', 'POST'])
def api_for_vips():
    if request.method == "GET":
        frl = features.forwardingrules.list_forwardingrules()
        list_vips = []
        for fr in frl:
            ti = features.targetinstances.get_with_name(fr['target'])
            if not ti:
                ti = {}
            list_vips.append(get_vip_from_fr_ti(fr, ti))
        return(jsonify(list_vips))
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            return jsonify(status=False, msg="Posted data not in json format")
        if 'ip' not in data or 'name' not in data:
            return jsonify(status=False, msg="Both ip and name are required")
        ip = data['ip']
        name = data['name']
        created_items = {}
        created_items['target_instance'] = features.targetinstances.create(name, instance_ip=ip)
        if created_items['target_instance']:
            created_items['forwarding_rule'] = features.forwardingrules.create(name, created_items['target_instance']['name'])
        else:
            return jsonify(False)
        if not created_items['forwarding_rule']:
            return jsonify(False)
        data_to_be_returned = get_vip_from_fr_ti(created_items['forwarding_rule'], created_items['target_instance'])
        return (jsonify(data_to_be_returned))
    else:
        return jsonify(status=False, msg="Unsupported Request Method")

# Sample URL: http://IP/forwardingrules/create?ip=<ip>&name=<name>
@app.route("/vip/<item>", methods = ['GET', 'DELETE'])
def api_for_one_vip(item):
    if request.method == "GET":
        if is_IP(item):
            fr = features.forwardingrules.get_with_ip(item)
        else:
            fr = features.forwardingrules.get_with_name(item)
        if not fr:
            return(jsonify(status=False, msg=item+" not found"))
        ti = features.targetinstances.get_with_name(fr['target'])
        return(jsonify(get_vip_from_fr_ti(fr, ti)))
    elif request.method == "DELETE":
        if is_IP(item):
            fr = features.forwardingrules.get_with_ip(item)
            if fr:
                item = fr['name']
            else:
                return(jsonify(status=False, msg="VIP doesn't exist"))
        fr_item = features.forwardingrules.delete(item)
        ti_item = features.targetinstances.delete(item)
        return (jsonify(fr_item and ti_item))
    else:
        return jsonify(status=False, msg="Unsupported Request Method")

@app.route("/forwardingrules/create")
def api_create_forwarding_rule(request):
	if 'ip' not in request.args or 'name' not in request.args:
		return jsonify(False)
	ip = request.args['ip']
	name = request.args['name']
	created_items = {}
	created_items['target_instance'] = features.targetinstances.create(name, instance_ip=ip)
	if created_items['target_instance']:
		created_items['forwarding_rule'] = features.forwardingrules.create(name, created_items['target_instance']['name'])
	else:
		return jsonify(False)
	return (jsonify(created_items))

# TODO: Make this do the part of deleting target instances
@app.route("/forwardingrules/delete")
def api_delete_forwarding_rule(request):
        if 'name' not in request.args:
            return jsonify(False)
        name = request.args['name']
        fr = True
        fr = features.forwardingrules.delete(name)
        ti = features.targetinstances.delete(name)
        return (jsonify(fr and ti))

# Flask Exception Handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(status=False, error=404, text=str(e)), 404
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(status=False, error=500, text=str(e)), 500

def run_server():
	app.run(host='0.0.0.0', port=FLASK_PORT)
