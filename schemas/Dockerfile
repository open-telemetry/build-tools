## Build
##
FROM golang:1.27-alpine@sha256:fa3d596898d9f126af7c01d14ee7597bab3f39cccf392ef36b69fe77cd681f18 AS build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY *.go ./
COPY testdata/* ./testdata/

RUN CGO_ENABLED=0 go test ./...
RUN go build -o /schemas-tool

## Run
##
FROM alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

WORKDIR /

COPY --from=build /schemas-tool /schemas-tool

ENTRYPOINT ["/schemas-tool"]