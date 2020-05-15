import requests

METADATA_ENDPOINT = 'http://metadata.google.internal'
PROJECT_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/project/project-id'
ZONE_ENDPOINT = METADATA_ENDPOINT + '/computeMetadata/v1/instance/zone'
HEADERS = {'Metadata-Flavor': 'Google'}

def call(entity):
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


if __name__ == "__main__":
    print ("Project: "+ call('project'))
    print ("Zone: "+ call('zone'))
    print ("Region: "+ call('region'))

