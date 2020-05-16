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
    try:
        request = service.managedZones().list(project=project)
        while request is not None:
            response = request.execute()

            for managed_zone in response['managedZones']:
                managed_zone_list.append({'name':  managed_zone['name'],
                                          'dns_name': managed_zone['dnsName']})

            request = service.managedZones().list_next(previous_request=request, previous_response=response)

        return managed_zone_list
    except:
        return False

def create_dns_zones(name, dns_name, description=""):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')
    managed_zone_body = {
        "name": name,
        "dnsName": dns_name+".",
        "description": description
    }

    try:
        response = service.managedZones().create(project=project, body=managed_zone_body).execute()
        return response
    except:
        return False

def delete_dns_zones(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    try:
        response = service.managedZones().delete(project=project, managedZone=name).execute()
        return response
    except:
        return False

def get_dns_zones_with_name(name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    try:
        response = service.managedZones().get(project=project, managedZone=name).execute()
        return ({'name':response['name'], 'dns_name':response['dnsName'], 'description':response['description']})
    except:
        return False

def get_all_dns_records(zone_name):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    record_list = []
    try:
        request = service.resourceRecordSets().list(project=project, managedZone=zone_name)
        while request is not None:
            response = request.execute()

            for resource_record_set in response['rrsets']:
                record_list.append({'name': resource_record_set['name'],
                                    'type': resource_record_set['type'],
                                    'ttl': resource_record_set['ttl'],
                                    'ip': resource_record_set['rrdatas']})
            request = service.resourceRecordSets().list_next(previous_request=request, previous_response=response)

        return record_list
    except:
        return False

def create_dns_records(zone_name, name, ip, record_type="A", ttl=30):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('dns', 'v1', credentials=credentials)
    project = metadata.get('project')

    change_body = {
        "additions": [
        {
          "name": name+".",
          "type": record_type,
          "ttl": ttl,
          "rrdatas": [ip]
        }]
    }

    try:
        response = service.changes().create(project=project, managedZone=zone_name, body=change_body).execute()
        return response
    except:
        return False

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

    try:
        response = service.changes().create(project=project, managedZone=zone_name, body=change_body).execute()
        return response
    except:
        return False

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
