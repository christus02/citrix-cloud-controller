from googleapiclient import discovery
from . import helper
from . import metadata
from oauth2client.client import GoogleCredentials

CREDENTIALS = GoogleCredentials.get_application_default()


def list_forwardingrules():
    service = discovery.build('compute', 'v1', credentials=CREDENTIALS)
    project = metadata.get('project')
    region = metadata.get('region')
    request = service.forwardingRules().list(project=project, region=region)
    forwardingrules = []
    while request is not None:
        response = request.execute()
        for forwarding_rule in response['items']:
            filter_keys = ['name', 'target', 'IPAddress', 'IPProtocol', 'portRange']
            filtered_data = {filter_key: forwarding_rule[filter_key] for filter_key in filter_keys}
            filtered_data['target'] = forwarding_rule['target'].split('/')[-1]
            forwardingrules.append(filtered_data)
        request = service.forwardingRules().list_next(previous_request=request, previous_response=response)
    return forwardingrules


def get_with_name(name):
    forwardingrules = list_forwardingrules()
    for rule in forwardingrules:
        if rule['name'] == name:
            return rule
    return {}


def get_with_ip(ip):
    forwardingrules = list_forwardingrules()
    for rule in forwardingrules:
        if rule['IPAddress'] == ip:
            return rule
    return {}


def create(name, target_instance, protocol='TCP', wait=True):
    # projects/kops-automation/zones/asia-south1-a/targetInstances/raghulc
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    zone = metadata.get('zone')
    region = metadata.get('region')
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
            response = helper.wait_for_operation(service, response['name'], project, region=region)
    return (get_with_name(name))


def delete(name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = metadata.get('project')
    region = metadata.get('region')
    try:
        request = service.forwardingRules().delete(project=project, region=region, forwardingRule=name)
        response = request.execute()
    except Exception:
        return False
    if wait:
        if response['status'] == 'RUNNING':
            response = helper.wait_for_operation(service, response['name'], project, region=region)
    return not bool(get_with_name(name))
