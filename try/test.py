import googleapiclient.discovery

# Functions
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


# Main
project = 'kops-automation'
zone = 'asia-south1-a'
compute = googleapiclient.discovery.build('compute', 'v1')
instances = list_instances(compute, project, zone)
print('Instances in project %s and zone %s:' % (project, zone))
for instance in instances:
    print(' - ' + instance['name'])
