FROM python:2.7
MAINTAINER Rickard Dybeck <r.dybeck@gmail.com>


COPY docker/multimedia.list /etc/apt/sources.list.d/
RUN apt-get update && \
    apt-get install -y --force-yes deb-multimedia-keyring libavcodec-dev libavformat-dev libswscale-dev cython

WORKDIR /opt/fa

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY setup.py .
COPY serve.py .
COPY unsorted ./unsorted

CMD ["/opt/fa/serve.py"]
