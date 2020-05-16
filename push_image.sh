sudo docker build -t citrix-cloud-controller .
sudo docker tag citrix-cloud-controller:latest asia.gcr.io/kops-automation/citrix-cloud-controller:v2
sudo docker push asia.gcr.io/kops-automation/citrix-cloud-controller:v2
