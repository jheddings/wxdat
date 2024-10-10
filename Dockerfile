FROM python:3.13

COPY src poetry.lock pyproject.toml README.md /tmp/wxdat/
RUN pip3 install /tmp/wxdat/ && rm -Rf /tmp/wxdat

# commands must be presented as an array, otherwise it will be launched
# using a shell, which causes problems handling signals for shutdown (#15)
ENTRYPOINT ["python3", "-m", "wxdat"]

# allow local callers to change the config file
CMD ["--config=/etc/wxdat.yaml"]
