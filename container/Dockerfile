FROM python
MAINTAINER Raghul Christus (raghul.christus@citrix.com)
RUN apt update && apt install vim -y
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY controller.py /
CMD ["python", "/controller.py"]
