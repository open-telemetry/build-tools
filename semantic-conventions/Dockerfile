ARG ALPINE_VERSION=3.12
ARG PYTHON_VERSION=3.8.5

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}
LABEL maintainer="The OpenTelemetry Authors"
ADD *.whl /semconvgen/
WORKDIR /semconvgen
RUN rm -f README.md
RUN apk --update add --virtual build-dependencies build-base \
  && pip install -U ./semconvgen-*.whl \
  && apk del build-dependencies \
  && rm *.whl
ENTRYPOINT ["gen-semconv"]
