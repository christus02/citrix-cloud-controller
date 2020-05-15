from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

project = 'kops-automation'
region = 'asia-south1'

request = service.forwardingRules().list(project=project, region=region)
while request is not None:
    response = request.execute()

    for forwarding_rule in response['items']:
        # TODO: Change code below to process each `forwarding_rule` resource:
        pprint(forwarding_rule)

    request = service.forwardingRules().list_next(previous_request=request, previous_response=response)
