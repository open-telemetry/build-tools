FROM python:3.12-alpine
LABEL maintainer="The OpenTelemetry Authors"
ADD *.whl /semconvgen/
WORKDIR /semconvgen
RUN rm -f README.md
RUN apk --update add --virtual build-dependencies build-base \
  && pip install -U ./semconvgen-*.whl \
  && apk del build-dependencies \
  && rm *.whl
ENV COLORED_DIFF true
ENTRYPOINT ["gen-semconv"]
