ARG ALPINE_VERSION=3.13

FROM alpine:${ALPINE_VERSION}
LABEL maintainer="The OpenTelemetry Authors"
RUN apk update
RUN apk add --no-cache clang=10.0.1-r0 python3 py3-pip git curl
RUN pip3 install cmake_format==0.6.13
RUN curl -L -o /usr/local/bin/buildifier https://github.com/bazelbuild/buildtools/releases/download/2.2.1/buildifier
RUN chmod +x /usr/local/bin/buildifier

COPY format.sh /
ENTRYPOINT ["sh", "/format.sh"]
