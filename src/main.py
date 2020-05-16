import sys, os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pkg'))

from pkg.gcp import api as gcp_api
from pkg.aws import api as aws_api
from pkg.azure import api as azure_api

def get_cloud():
    # Returns what cloud you are running in
    # Possible returns = "gcp", "aws", "azure"
    METADATA_SERVER_ENDPOINT = "http://169.254.169.254"
    response = requests.get(METADATA_SERVER_ENDPOINT)
    server_header = response.headers['Server']
    if server_header == "Metadata Server for VM":
        return "gcp"
    elif server_header == "EC2ws":
        return "aws"
    elif server_header == "Microsoft":
        return "azure"
    else:
        return ""

# Define what cloud you are running in
CLOUD = get_cloud()
api_dict = {'gcp': gcp_api, 'aws': aws_api, 'azure': azure_api}

# Define the API Endpoints here
if CLOUD.lower() in api_dict:
    api_dict[CLOUD.lower()].run_server()
else:
    print(CLOUD + "Not supported. Coming soon...")
