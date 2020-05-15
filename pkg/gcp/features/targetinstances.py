import requests
import os
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from helper import *

def delete(name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    request = service.targetInstances().delete(project=project, zone=zone, targetInstance=name)
    response = request.execute()
    if wait:
        if response['status'] == 'RUNNING':
            response = helper.wait_for_operation(service, response['name'], project, zone=zone)
    if get_with_name(name):
        return False
    else:
        return True

def create(name, instance_ip=None, instance_name=None, natPolicy="NO_NAT", wait=True):
    # Name can be 63 Characters long and can contain [a-z]([-a-z0-9]*[a-z0-9])?
    # Instance Name should in the format of "zones/zone/instances/instance"
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    # If IP provided, get the instance name
    if instance_ip is not None:
        instance_name = get_instance_name_with_ip(instance_ip)
    # If target instance is already existing, then return the name and instance details
    existing_target_instances_list = get_all()
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
            response = helper.wait_for_operation(service, response['name'], project, zone=zone)
    return (get_with_name(name))
    
def get_all():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    request = service.targetInstances().list(project=project, zone=zone)
    target_instance_list = []
    while request is not None:
        response = request.execute()
        for target_instance in response['items']:
            target_instance_list.append({'name':target_instance['name'], 'instance':target_instance['instance'].split('/')[-1]})
        request = service.targetInstances().list_next(previous_request=request, previous_response=response)
    return target_instance_list

def get_with_name(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    try:
        get_response = service.targetInstances().get(project=project, zone=zone, targetInstance=name).execute()
        return ({'name':get_response['name'], 'instance':get_response['instance'].split('/')[-1]})
    except:
        return False
