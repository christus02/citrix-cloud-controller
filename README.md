# Citrix Cloud Controller

Citrix Cloud Controller provides complete end-to-end deployment solutions for Ingresses deployed on Kubernetes Clusters in cloud environments.

In cloud managed Kubernetes services like [GKE](https://cloud.google.com/kubernetes-engine), [EKS](https://aws.amazon.com/eks/), [AKS](https://azure.microsoft.com/en-in/services/kubernetes-service/) , it is often a challenge to expose microservices which run inside the Kubernetes cluster to external world.
One quick solution would be to use a Cloud Provider's Load-Balancer. In many cases, this only provides basic TCP based load-balancing and lacks many robust load-balancing functionalities like SSL offloading, Content based routing, Rewriting the actual request, rate limiting, etc.

It would be amazing if we had a solution that is as easy to deploy as adding `type=LoadBalancer`and which would also offer robust features like SSL Offloading, Content based routing, Rewriting HTTP request and responses, Rate Limiting and much more.

[Citrix Cloud Controller](https://github.com/christus02/citrix-cloud-controller) combined with [Citrix Ingress Controller](https://github.com/citrix/citrix-k8s-ingress-controller) and [Citrix ADC VPX](https://www.citrix.com/products/citrix-adc/) makes all this possible.

Citrix Cloud Controller provisions a Public IP address on the Cloud Provider and [Citrix Ingress Controller](https://github.com/citrix/citrix-k8s-ingress-controller) uses this Public IP to configure the Citrix ADC VPX.
Citrix ADC VPX would act as an Ingress Loadbalancer for all the microservices running inside the Kubernetes Cluster.
Once the Ingress is configured the Ingress object status is also updated with the provisioned Public IP.

```
$ kubectl  get ing citrix-ingress
NAME             HOSTS                        ADDRESS       PORTS   AGE
citrix-ingress   apache.cloud-controller.ga   <public-ip>   80      1h
```

To complete the flow, Citrix Cloud Controller can also update the DNS for the Ingress Hostname if the DNS is hosted in the same Cloud.

For example, if the host rule in the Ingress is `apache.cloud-controller.ga`, Citrix Cloud Controller automatically creates a `A record` with the Public IP address allocated from the Cloud provider and updates the DNS of the Cloud (`Cloud DNS`, `Route 53`, etc)


# How to Deploy

We have an [examples](examples/README.md) section, where we have given a simple deployment example. This should get you started.
