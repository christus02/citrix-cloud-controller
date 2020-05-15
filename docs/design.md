# Citrix Cloud Controller - High Level Design Spec

This is a high level design spec of the Citrix Cloud Controller

# New Ingress Event

When CIC receives a new Ingress event, it should perform the below steps:

1. Make sure the Ingress event is intended for Tier-1 or Tier-2 (Ingress class)
2. Follow the usual code path if the Ingress is for Tier-2
3. If Ingress event is for Tier-1, then check for `frontend-ip` annotation
4. If `frontend-ip` annotation is not present, then invoke `citrix-cloud-controller` API to allocate a Public IP from Cloud Provider
5. Modify the Ingress Configuration by adding the `frontend-ip` annotation with the received from `citrix-cloud-controller`
6. Make sure CIC configures the `frontend-ip` on the Tier-1 VPX
7. Add new annotations in the Ingress for DNS updation - `ingress.citrix.com/cloud: gcp` and `ingress.citrix.com/update-cloud-dns: true`
8. If these annotations are present, update the `Host` field provided in the Ingress with the Public IP allocated by `citrix-cloud-controller` in the Cloud Provider DNS

# Annotations for Citrix Cloud Controller

1. `ingress.citrix.com/cloud`

Possible Values are `gcp`, `aws` and `azure`

No Defaults - Mandatory specification

2. `ingress.citrix.com/update-cloud-dns`

Possible Values are `true` and `false`

Default is `false`
