import time
from googleapiclient import discovery # noqa
from . import clouddns
from . import forwardingrules


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

def set_up():
    forwardingrules.set_up_creds()
    clouddns.set_up_creds()
