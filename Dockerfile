FROM python:3.9

# update core OS packages
RUN apt-get update

# finished updating packages
RUN apt-get autoremove --assume-yes && apt-get clean

# update python libraries and install common dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pyyaml requests prometheus_client

# install application files
WORKDIR "/opt/wxdat"

COPY src .
COPY test test

# host provides config via mounted volume
#COPY etc/wxdat_example.yaml /etc/wxdat.yaml

EXPOSE 9022

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["main.py", "--config", "/etc/wxdat.yaml"]

