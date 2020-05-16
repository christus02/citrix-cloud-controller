import requests
import os
import time
from googleapiclient import discovery
from urllib.parse import urlparse
from . import helper
from . import metadata
from oauth2client.client import GoogleCredentials
import sys

CREDENTIALS = GoogleCredentials.get_application_default()

def get_all_dns_zones():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    managed_zone_list = []
    request = service.managedZones().list(project=project)
    while request is not None:
        response = request.execute()

        for managed_zone in response['managedZones']:
            managed_zone_list.append({'name':  managed_zone['name'],
                                      'dns_name': managed_zone['dnsName']})

        request = service.managedZones().list_next(previous_request=request, previous_response=response)

    return managed_zone_list

def create_dns_zones(name, dns_name, description=""):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')
    managed_zone_body = {
        "name": name,
        "dnsName": dns_name+".",
        "description": description
    }

    request = service.managedZones().create(project=project, body=managed_zone_body)
    response = request.execute()
    return response

def delete_dns_zones(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    request = service.managedZones().delete(project=project, managedZone=name)
    response = request.execute()
    return response

def get_dns_zones_with_name(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

#    try:
    get_response = service.managedZones().get(project=project, managedZone=name).execute()
    return ({'name':get_response['name'], 'dns_name':get_response['dnsName'], 'description':get_response['description']})
#    except:
#        return False

def get_all_dns_records(zone_name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    record_list = []
    request = service.resourceRecordSets().list(project=project, managedZone=zone_name)
    while request is not None:
        response = request.execute()

        for resource_record_set in response['rrsets']:
            record_list.append({'name': resource_record_set['name'],
				'type': resource_record_set['type'],
				'ttl': resource_record_set['ttl'],
				'ip': resource_record_set['rrdatas']})
        # TODO: Change code below to process each `resource_record_set` resource:
        request = service.resourceRecordSets().list_next(previous_request=request, previous_response=response)

    return record_list

def create_dns_records(zone_name, name, ip, record_type="A", ttl=30):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    change_body = {
    # TODO: Add desired entries to the request body.
        "additions": [
        {
          "name": name+".",
          "type": record_type,
          "ttl": ttl,
          "rrdatas": [ip]
        }]
    }

    request = service.changes().create(project=project, managedZone=zone_name, body=change_body)
    response = request.execute()

    return response

def delete_dns_records(zone_name, name, ip, record_type, ttl):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    change_body = {
    # TODO: Add desired entries to the request body.
        "deletions": [
        {
          "name": name+".",
          "type": record_type,
          "ttl": ttl,
          "rrdatas": [ip]
        }]
    }

    request = service.changes().create(project=project, managedZone=zone_name, body=change_body)
    response = request.execute()

    return response

def record_exists_in_zone(zone_name, record_name, record_type):
    records = get_all_dns_records(zone_name)
    for record in records:
        if record['name'] == record_name+'.' and record['type'] == record_type:
            return record
    return None

def zone_exists(dns_name):
    zones = get_all_dns_zones()
    for zone in zones:
        if zone['dns_name'] == dns_name+".":
            return zone
    return None
