# Create a Simple deployment with Citrix ADC VPX as Ingres

### Pre-Requisites:

1. A Cloud Managed Kubernetes Cluster liks GKE, EKS or AKS
2. A Citrix ADC VPX deployed in the same VPC or VNET of the Managed Kubernetes Cluster

## Create Citrix Cloud Controller as a Microservice

```
kubectl create -f citrix-cloud-controller-deployment.yaml
```

In this example, Citrix Cloud Controller is being deployed as a separate deployment. If you choose, Citrix Cloud Controller can also be deployed as a side-car to Citrix Ingress Controller.

The advantage in deploying `Citrix Cloud Controller` as a separate deployment is that, when multiple Citrix Ingress Controller are running in your cluster, you can still have just one Citrix Cloud Controller. This would handle requests from Multiple Citrix Ingress Controllers.

## Create a Citrix Ingress Controller

```
kubectl create -f citrix-ingress-controller.yaml
```

## Create a Sample Microservice (Apache)

Here we are using an Apache deployment and this can be any of the microservice that you wish to load-balance using the Citrix ADC VPX

```
kubectl create -f apache.yaml
```

## Create an Ingress

Finally, let's create an Ingress definition and see the magic

```
kubectl create -f ingress.yaml
```
