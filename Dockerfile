FROM ctaloi/sipp

WORKDIR /opt/xivo-load-tester
COPY . /opt/xivo-load-tester
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-jinja2

ENTRYPOINT ["./load-tester"]
