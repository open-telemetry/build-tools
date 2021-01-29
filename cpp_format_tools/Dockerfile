ARG ALPINE_VERSION=3.13

ARG BUILDIFIER_VERSION=3.5.0
ARG CLANG_VERSION=10.0.1-r0
ARG CMAKE_FORMAT_VERSION=0.6.13

FROM alpine:${ALPINE_VERSION}
LABEL maintainer="The OpenTelemetry Authors"
RUN apk update

ARG CLANG_VERSION
RUN apk add --no-cache clang=${CLANG_VERSION} python3 py3-pip git curl

ARG CMAKE_FORMAT_VERSION
RUN pip3 install cmake_format==${CMAKE_FORMAT_VERSION}

ARG BUILDIFIER_VERSION
RUN curl -L -o /usr/local/bin/buildifier https://github.com/bazelbuild/buildtools/releases/download/${BUILDIFIER_VERSION}/buildifier
RUN chmod +x /usr/local/bin/buildifier

COPY format.sh /
ENTRYPOINT ["sh", "/format.sh"]
