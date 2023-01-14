FROM python:3.11

RUN mkdir -p /opt/wxdat

COPY src poetry.lock pyproject.toml README.md /tmp/wxdat/
RUN pip3 install /tmp/wxdat/ && rm -Rf /tmp/wxdat

WORKDIR "/opt/wxdat"

COPY etc/wxdat.yaml /opt/wxdat/

EXPOSE 8077

CMD /usr/local/bin/python3 -m wxdat --config=/opt/wxdat/wxdat.yaml
