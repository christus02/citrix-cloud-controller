# Using Citrix Cloud Controller API

This guide details the procedure to consume the Citrix Cloud Controller API

Citrix Cloud Controller has an in-built API server running which would respond to API requests in a JSON format. APIs are REST in nature

# List of Available APIs

## Health Check of the Controller

| API ENDPOINT | METHOD | REQUEST JSON BODY | RESPONSE | COMMENTS | 
| --- | --- | --- | --- | --- |
| `/healthz` | GET | None | `{"msg":"I am Alive!","status":true,"success":true,"cloud":"gcp"}` | None |

## VIP 

| API ENDPOINT | METHOD | REQUEST JSON BODY | RESPONSE | COMMENTS |
| --- | --- | --- | --- | --- |
| `/vip` | GET | None |  JSON of all configured VIP <br> To retrieve all configured VIPs | None |
| `/vip/vip-name` | GET | None |  JSON of the a specific vip `vip-name` <br> To retrieve a VIP usings it NAME | None |
| `/vip/vip-ip` | GET | None |  JSON of the a specific vip `vip-ip` <br> To retrieve a VIP using its IP | None |
| `/vip` | POST | `{'name':'ingress-name', 'nsip':'NS_IP'}` |  JSON of the created VIP | None |
| `/vip/vip-name` | DELETE | None | JSON returning the status of the delete operation <br> Delete VIP using Name | None |
| `/vip/vip-ip` | DELETE | None | JSON returning the status of the deletion operation <br> Delete VIP using IP | None |

## DNS

| API ENDPOINT | METHOD | REQUEST JSON BODY | RESPONSE | COMMENTS |
| --- | --- | --- | --- | --- |
| `/dns` | GET | None | JSON of all configured DNS records <br> To retrieve all configured DNS | None |
| `/dns/dns-name` | GET | None | JSON of the specified DNS name (ingress-name) <br> To retrieve a DNS record using its name | None |
| `/dns` | POST | `{}` | JSON of the created DNS record | None |
| `/dns/dns-name` | DELETE | None | JSON returning the status of the deletion operation | None |



## Example Usage:

**Note:**
1. Here the scope is only in the same region or vpc where the Kubernetes cluster is deployed
2. `citrix-cloud-controller` is the name of the Citrix Cloud Controller Kubernetes Service
3. The APIs below were fired from another pod running in the cluster

## API Usage of `vip` Endpoint

### List all configured Public IPs

Request:

```bash
curl -X GET http://citrix-cloud-controller/vip
```

Response:

```json
[{"externalIP":"X.X.X.X","ingressName":"ingress-1","instanceName":"instance-1","internalIP":"X.X.X.X","portRange":"1-65535","protocol":"TCP"},
{"externalIP":"X.X.X.X","ingressName":"ingress-2","instanceName":"instance-2","internalIP":"X.X.X.X","portRange":"1-65535","protocol":"UDP"}]
```

### Describe a specific Public IP

Request:

```bash
curl -X GET http://citrix-cloud-controller/vip/X.X.X.X
```

Response:

```json
{"externalIP":"X.X.X.X","ingressName":"ingress-1","instanceName":"instance-1","internalIP":"X.X.X.X","portRange":"1-65535","protocol":"TCP"}
```

### To Create a new Public IP

To create a new Public IP, make sure the request method is `POST` and you have json formatted `POST` data having the below fields:
```
name: Name of the Ingress
ip: IP of the Citrix ADC VPX
```

Request:

```bash
curl -X POST -H "Content-Type: application/json" http://citrix-cloud-controller/vip -d '{"name": "ingress-3", "ip": "Y.Y.Y.Y"}'
```

Response:

```json
{"externalIP":"X.X.X.X","ingressName":"ingress-3","instanceName":"instance-3","internalIP":"X.X.X.X","portRange":"1-65535","protocol":"TCP"}
```

### To Delete a configured Public IP

To delete a already configured or existing public IP, make sure the request method is `DELETE`

Request:

```bash
curl -X DELETE http://citrix-cloud-controller/vip/X.X.X.X
```

Response:

```json
true
```

## API Usage of `dns` Endpoint

### List all configured DNS entries

Request:

```bash
curl -X GET http://citrix-cloud-controller/dns
```

Response:

```json
[{"ip":["X.X.X.X"],"name":"apache-1.cloud-controller.ga.","ttl":300,"type":"A"},{"ip":["X.X.X.X"],"name":"apache-2.cloud-controller.ga.","ttl":30,"type":"A"}]
```

### Describe a specific DNS entry

Request:

```bash
curl -X GET http://citrix-cloud-controller/dns/apache-1.cloud-controller.ga
```

Response:

```json
{"record":{"ip":["X.X.X.X"],"name":"apache-1.cloud-controller.ga.","ttl":30,"type":"A"}}
```
### To Create a new DNS entry

To create a new DNS entry, make sure the request method is `POST` and you have json formatted `POST` data having the below fields:

```
ip: Public IP to be used as A record
hostname: Hostname of the microservice
```

Request:

```bash
curl -X POST -H "Content-Type: application/json" http://citrix-cloud-controller/dns -d '{"ip": "X.X.X.X", "hostname": "apache-3.cloud-controller.ga"}'
```

Response:

```json
{"record":{"ip":["X.X.X.X"],"name":"apache-3.cloud-controller.ga.","ttl":30,"type":"A"},"status":"done"}
```

### To Delete a DNS entry

To delete a already configured or existing DNS entry, make sure the request method is `DELETE`

Request:

```bash
curl -X DELETE -H "Content-Type: application/json" http://citrix-cloud-controller/dns/apache-3.cloud-controller.ga
```

Response:
```json
true
```
