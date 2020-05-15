# Using Citrix Cloud Controller API

This guide details the procedure to consume the Citrix Cloud Controller API

Citrix Cloud Controller has an in-built API server running which would respond to API requests in a JSON format. APIs are REST in nature

# List of Available APIs

## Health Check of the Controller

| API ENDPOINT | METHOD | REQUEST PARAMETERS | RESPONSE | COMMENTS | 
| --- | --- | --- | --- | --- |
| `/healthz` | GET | None | `{"msg":"I am Alive!","status":true,"success":true}` | None |


## Metadata

| API ENDPOINT | METHOD | REQUEST PARAMETERS | RESPONSE | COMMENTS |
| --- | --- | --- | --- | --- |
| `/metadata/project` | GET | None | `{"project":"kops-automation"}` | None |
| `/metadata/zone` | GET | None | `{"zone":"asia-south1-a"}` | None |
| `/metadata/region` | GET | None | `{"region":"asia-south1"}` | None |

## Google Cloud

### Forwarding Rules

| API ENDPOINT | METHOD | REQUEST PARAMETERS | RESPONSE | COMMENTS |
| --- | --- | --- | --- | --- |
| `/forwardingrules/get?{ip/name}=<ip/name>` | GET | `name`: Name of a forwarding Rule <br> `ip`: IP of a Forwarding Rule | Forwarding rule in the form of a dictionary | If no query string is provided in the URL, all the Forwarding rules are returned. |
| `forwardingrules/create?ip=<ip>&name=<name>` | GET | `name`: Name of the ingress <br> `ip`: IP of the ADC | Dictionary of all the items created | If a resource is not created, an empty dictionary will be the value of the resource key. |
