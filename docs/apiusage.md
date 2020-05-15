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
