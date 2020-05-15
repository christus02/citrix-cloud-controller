import requests
import os
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def get_with_ip(ip):
	# IP of the VPX which was provided by the User
	# Assuming this to the be the primary IP
	instance_list = get_all_instance_ips()
	for i in instance_list:
		if ip == i['ip']:
		    return i['name']
    return False

def get_all():
    # This function returns all the instance NIC0 IP with its name
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    instance_list = []
    request = service.instances().list(project=project, zone=zone)
    while request is not None:
        response = request.execute()
        for instance in response['items']:
            instance_list.append({'name':instance['name'], 'ip':instance['networkInterfaces'][0]['networkIP']})
        request = service.instances().list_next(previous_request=request, previous_response=response)
    return instance_list
