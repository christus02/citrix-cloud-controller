# Citrix Cloud Controller

Citrix Cloud Controller provides end-to-end deployment solutions for an Ingress deployed in Kubernetes environment in Cloud.

In cloud managed Kubernetes services like [GKE](https://cloud.google.com/kubernetes-engine), [EKS](https://aws.amazon.com/eks/), [AKS](https://azure.microsoft.com/en-in/services/kubernetes-service/), etc it is often a challenge to expose microservices running inside your Kubernetes cluster to external world.
The one quick solution is to use a Cloud Provider's Load-Balancer. In many cases, this provides basic TCP based load-balancing and lacks many robust load-balancing functionalities like SSL offloading, Content based routing, Rewriting the actual request, rate limiting, etc.

How wonderful it would be if we have a solution that is more easy to deploy than a `type=LoadBalancer` and offers many robust features like SSL Offloading, Content based routing, Rewriting HTTP request and responses, provides Rate Limiting and many more features.

[Citrix Cloud Controller](https://github.com/christus02/citrix-cloud-controller) combined with [Citrix Ingress Controller](https://github.com/citrix/citrix-k8s-ingress-controller)  and [Citrix ADC VPX](https://www.citrix.com/products/citrix-adc/) makes all this possible for you.

Citrix Cloud Controller automatically provisions a Public IP address from the Cloud Provider and Configures the same in the Citrix ADC VPX which would act as an Ingress for all the microservices running inside the Kubernetes Cluster. Once the Ingress is configured the Public IP addresses assigned to the Ingress is also updated to the Ingress Status.

```
$ kubectl  get ing citrix-ingress
NAME             HOSTS                        ADDRESS       PORTS   AGE
citrix-ingress   apache.cloud-controller.ga   <public-ip>   80      1h
```

Also to make the flow complete, Citrix Cloud Controller could also update the DNS for the Ingress Hostname if the DNS is hosted in the same Cloud.

For example, if the host rule in the Ingress has `apache.cloud-controller.ga`, Citrix Cloud Controller automatically creates a `A record` with the Public IP address allocated from the Cloud provider and updates the DNS of the Cloud (`Cloud DNS`, `Route 53`, etc)


# How to Deploy

We have an [examples](examples/README.md) section, where we have given a simple deployment example. This should get you started.
