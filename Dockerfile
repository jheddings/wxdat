FROM python:3.11

RUN mkdir -p /opt/wxdat

COPY src poetry.lock pyproject.toml README.md /tmp/wxdat/
RUN pip3 install /tmp/wxdat/ && rm -Rf /tmp/wxdat

WORKDIR "/opt/wxdat"

# commands must be presented as an array, otherwise it will be launched
# using a shell, which causes problems handling signals for shutdown (#15)
ENTRYPOINT ["python3", "-m", "wxdat"]

# allow local callers to change the config file
CMD ["--config=/opt/wxdat/wxdat.yaml"]
