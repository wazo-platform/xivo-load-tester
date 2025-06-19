FROM ctaloi/sipp

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-jinja2

WORKDIR /opt/xivo-load-tester
COPY . /opt/xivo-load-tester

ENTRYPOINT ["./load-tester"]
