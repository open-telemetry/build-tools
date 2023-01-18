FROM python:3.8.5-alpine3.12
LABEL maintainer="The OpenTelemetry Authors"
ADD *.whl /semconvgen/
WORKDIR /semconvgen
RUN rm -f README.md
RUN apk --update add --virtual build-dependencies build-base \
  && pip install -U ./semconvgen-*.whl \
  && apk del build-dependencies \
  && rm *.whl
ENTRYPOINT ["gen-semconv"]
