from flask import Flask, request, url_for, jsonify
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import requests
import os
import time
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

def wait_for_operation(service, operation, project, zone=None, region=None):
    while True:
        if region is not None:
            result = service.regionOperations().get(
                project=project,
                region=region,
                operation=operation).execute()
        elif zone is not None:
            result = service.zoneOperations().get(
                project=project,
                zone=zone,
                operation=operation).execute()
        if result['status'] == 'DONE':
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def get_forwarding_rule(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    region = metadata_call('region')
    try:
        request = service.forwardingRules().get(project=project, region=region, forwardingRule=name)
        response = request.execute()
        return_data = {
                'name':response['name'],
                'target':response['target'].split('/')[-1],
                'ip':response['IPAddress'],
                'protocol':response['IPProtocol'],
                'port_range':response['portRange'],
        }
        return (return_data)
    except:
        return False

def create_forwarding_rule(name, target_instance, protocol='TCP', wait=True):
    #projects/kops-automation/zones/asia-south1-a/targetInstances/raghulc
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    region = metadata_call('region')
    target_instance = "projects/"+project+"/zones/"+zone+"/targetInstances/"+target_instance
    forwarding_rule_body = {
            'name': name,
            'IPProtocol': protocol,
            'target': target_instance,
            'loadBalancingScheme': 'EXTERNAL',
            'portRange': '1-65535',
    }
    request = service.forwardingRules().insert(project=project, region=region, body=forwarding_rule_body)
    response = request.execute()
    if wait:
        if response['status'] == 'RUNNING':
            response = wait_for_operation(service, response['name'], project, region=region)
    return (get_forwarding_rule(name))

def delete_forwarding_rule(name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    region = metadata_call('region')
    request = service.forwardingRules().delete(project=project, region=region, forwardingRule=name)
    response = request.execute()
    if wait:
        if response['status'] == 'RUNNING':
            response = wait_for_operation(service, response['name'], project, region=region)
    if get_forwarding_rule(name):
        return False
    else:
        return True

def delete_target_instance(name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    request = service.targetInstances().delete(project=project, zone=zone, targetInstance=name)
    response = request.execute()
    if wait:
        if response['status'] == 'RUNNING':
            response = wait_for_operation(service, response['name'], project, zone=zone)
    if get_target_instance(name):
        return False
    else:
        return True

def create_target_instance(name, instance_ip=None, instance_name=None, natPolicy="NO_NAT", wait=True):
    # Name can be 63 Characters long and can contain [a-z]([-a-z0-9]*[a-z0-9])?
    # Instance Name should in the format of "zones/zone/instances/instance"
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    # If IP provided, get the instance name
    if instance_ip is not None:
        instance_name = get_instance_name_with_ip(instance_ip)
    # If target instance is already existing, then return the name and instance details
    existing_target_instances_list = get_all_target_instances()
    for i in existing_target_instances_list:
        if name == i['name']:
            return i
    # Create new target instance if not already existing
    instance_name = "zones/"+zone+"/instances/"+instance_name
    target_instance_body = {
            "name": name, 
            "natPolicy": natPolicy,
            "instance": instance_name,
    }
    request = service.targetInstances().insert(project=project, zone=zone, body=target_instance_body)
    response = request.execute()
    if wait: 
        if response['status'] == 'RUNNING':
            response = wait_for_operation(service, response['name'], project, zone=zone)
    return (get_target_instance(name))
    
def get_all_target_instances():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    request = service.targetInstances().list(project=project, zone=zone)
    target_instance_list = []
    while request is not None:
        response = request.execute()
        for target_instance in response['items']:
            target_instance_list.append({'name':target_instance['name'], 'instance':target_instance['instance'].split('/')[-1]})
        request = service.targetInstances().list_next(previous_request=request, previous_response=response)
    return target_instance_list

def get_target_instance(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    try:
        get_response = service.targetInstances().get(project=project, zone=zone, targetInstance=name).execute()
        return ({'name':get_response['name'], 'instance':get_response['instance'].split('/')[-1]})
    except:
        return False

def get_instance_name_with_ip(ip):
    # IP of the VPX which was provided by the User
    # Assuming this to the be the primary IP
    instance_list = get_all_instance_ips()
    for i in instance_list:
        if ip == i['ip']:
            return i['name']
    return False

def get_ip_from_instance_name(instance_name):

    # Assumption:
        # VPX runs on a single NIC mode. We will query only the first nic for IP

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    project = metadata_call('project')
    zone = metadata_call('zone')

    request = service.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()

    try:
        ip = response['networkInterfaces'][0]['networkIP']
        name = response['name']
        return ({"name":name, "ip":ip})
    except:
        return False

def get_all_instance_ips():
    # This function returns all the instance NIC0 IP with its name
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata_call('project')
    zone = metadata_call('zone')
    instance_list = []
    request = service.instances().list(project=project, zone=zone)
    while request is not None:
        response = request.execute()
        for instance in response['items']:
            instance_list.append({'name':instance['name'], 'ip':instance['networkInterfaces'][0]['networkIP']})
        request = service.instances().list_next(previous_request=request, previous_response=response)
    return instance_list


# End of Functions

@app.route("/healthz")
def health():
    return jsonify(status=True, success=True, msg="I am Alive!")

@app.route("/metadata/project")
def metadata_project():
    return jsonify(project=metadata_call('project'))

@app.route("/metadata/zone")
def metadata_zone():
    return jsonify(zone=metadata_call('zone'))

@app.route("/metadata/region")
def metadata_region():
    return jsonify(region=metadata_call('region'))

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
@app.route("/forwardingrules/create/<name>/<target>")
def api_create_forwarding_rule(name, target):
    return (jsonify(create_forwarding_rule(name, target)))
@app.route("/forwardingrules/delete/<name>")
def api_delete_forwarding_rule(name):
    return (jsonify(delete_forwarding_rule(name)))
@app.route("/targetinstance/create/<name>/<ip>")
def api_create_target_instance(name, ip):
    return (jsonify(create_target_instance(name, instance_ip=ip)))
@app.route("/targetinstance/delete/<name>")
def api_delete_target_instance(name):
    return (jsonify(delete_target_instance(name)))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
