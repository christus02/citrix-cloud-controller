FROM python
MAINTAINER Raghul Christus (raghul.christus@citrix.com)
RUN apt update && apt install vim -y
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY pkg /citrix-cloud-controller/pkg
COPY src /citrix-cloud-controller/src
CMD ["python", "/citrix-cloud-controller/src/main.py"]
