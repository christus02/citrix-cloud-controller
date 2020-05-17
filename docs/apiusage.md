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




# OLD ENDPOINTS - WILL BE REMOVED 

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

```bash
curl -X GET http://localhost:8080/vip/35.200.132.201
```
```json
{"externalIP":"35.200.132.201","ingressName":"raghulc-1","instanceName":"cluster-1-vpx","internalIP":"35.200.132.201","portRange":"1-65535","protocol":"TCP"}
```

```bash
curl -X GET http://localhost:8080/vip/raghulc-1
```
```json
{"externalIP":"35.200.132.201","ingressName":"raghulc-1","instanceName":"cluster-1-vpx","internalIP":"35.200.132.201","portRange":"1-65535","protocol":"TCP"}
```
```bash
curl -X GET http://localhost:8080/vip
```
```json
[{"externalIP":"35.200.247.32","ingressName":"a1338d356955611eab8d242010aa000e","instanceName":"","internalIP":"35.200.247.32","portRange":"8080-8080","protocol":"TCP"},
{"externalIP":"34.93.125.249","ingressName":"ada9fc00096cc11ea8fd342010aa0008","instanceName":"","internalIP":"34.93.125.249","portRange":"80-80","protocol":"TCP"},
{"externalIP":"35.244.11.249","ingressName":"ipsec-cluster-1-vpx","instanceName":"cluster-1-vpx","internalIP":"35.244.11.249","portRange":"1-65535","protocol":"UDP"},
{"externalIP":"35.200.182.103","ingressName":"ipsec-cluster-2-vpx","instanceName":"cluster-2-vpx","internalIP":"35.200.182.103","portRange":"1-65535","protocol":"UDP"},
{"externalIP":"35.200.132.201","ingressName":"raghulc-1","instanceName":"cluster-1-vpx","internalIP":"35.200.132.201","portRange":"1-65535","protocol":"TCP"}]
```
```bash
curl -X POST -H "Content-Type: application/json" http://localhost:8080/vip -d '{"name": "raghulc-2", "ip": "10.160.0.5"}'
```
```json
{"externalIP":"35.244.21.148","ingressName":"raghulc-2","instanceName":"cluster-1-vpx","internalIP":"35.244.21.148","portRange":"1-65535","protocol":"TCP"}
```
```bash
curl -X DELETE http://localhost:8080/vip/35.244.21.148
```
```json
true
```

### Sample Output for all the curl commands
```bash
curl http://localhost:5001/healthz
curl http://localhost:5001/metadata/project
curl http://localhost:5001/metadata/zone
curl http://localhost:5001/metadata/region
```
```json
{"msg":"I am Alive!","status":true,"success":true}
{"project":"kops-automation"}
{"zone":"asia-south1-a"}
{"region":"asia-south1"}
```
```bash
curl -X GET -G http://localhost:5001/forwardingrules/create --data-urlencode 'ip=10.160.0.5' --data-urlencode 'name=raghulc-2'
```
```json
{"forwarding_rule":{"IPAddress":"35.244.21.148","IPProtocol":"TCP","name":"raghulc-2","portRange":"1-65535","target":"raghulc-2"},"target_instance":{"instance":"cluster-1-vpx","name":"raghulc-2"}}
```
```bash
curl http://localhost:5001/forwardingrules/delete?name=raghulc-2
```
```json
true
```
```bash
curl http://localhost:5001/forwardingrules/get?name=raghulc-1
```
```json
{"IPAddress":"35.200.132.201","IPProtocol":"TCP","name":"raghulc-1","portRange":"1-65535","target":"raghulc-1"}
```
```bash
curl http://localhost:5001/forwardingrules/get
```
```json
[{"IPAddress":"35.200.247.32","IPProtocol":"TCP","name":"a1338d356955611eab8d242010aa000e","portRange":"8080-8080","target":"a1338d356955611eab8d242010aa000e"},
{"IPAddress": "34.93.125.249","IPProtocol":"TCP","name":"ada9fc00096cc11ea8fd342010aa0008","portRange":"80-80","target":"ada9fc00096cc11ea8fd342010aa0008"},
{"IPAddress":"35.244.11.249","IPProtocol":"UDP","name":"ipsec-cluster-1-vpx","portRange":"1-65535","target":"target-cluster-1-vpx"},
{"IPAddress":"35.200.182.103","IPProtocol":"UDP","name":"ipsec-cluster-2-vpx","portRange":"1-65535","target":"target-cluster-2-vpx"},
{"IPAddress":"35.200.132.201","IPProtocol":"TCP","name":"raghulc-1","portRange":"1-65535","target":"raghulc-1"}]
```

```bash
curl -X GET http://localhost:5001/forwardingrules/get --data-urlencode 'ip=35.200.132.201'
```
```json
{"IPAddress":"35.200.132.201","IPProtocol":"TCP","name":"raghulc-1","portRange":"1-65535","target":"raghulc-1"}
```

```bash
curl -X GET http://localhost:8080/dns
```
```json
[{"ip":["2.2.2.2"],"name":"abc.thisistemp.com.","ttl":300,"type":"A"},{"ip":["1.1.1.1"],"name":"xyz.thisistest.com.","ttl":30,"type":"A"}]
```

```bash
curl -X GET http://localhost:8080/dns/xyz.thisistest.com
```
```json
{"ip":["1.1.1.1"],"name":"xyz.thisistest.com.","ttl":30,"type":"A"}
```

```bash
curl -X POST -H "Content-Type: application/json" http://localhost:8080/dns -d '{"ip": "3.3.3.3", "hostname": "abc.thisisdummy.net"}'
```
```json
{"record":{"ip":["3.3.3.3"],"name":"abc.thisisdummy.com.","ttl":30,"type":"A"},"status":"done"}
```

```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8080/dns/abc.thisisdummy.net
```
```json
true
```
