ARG ALPINE_VERSION=3.12
ARG PYTHON_VERSION=3.8.5

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}
LABEL maintainer="The OpenTelemetry Authors"
ADD . /semconvgen/
WORKDIR semconvgen
RUN rm -f README.md
RUN apk --update add --virtual build-dependencies build-base \
  && pip install -r requirements.txt \
  && apk del build-dependencies

RUN python setup.py install
ENTRYPOINT ["gen-semconv"]