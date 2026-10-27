## Build
##
FROM golang:1.27-alpine@sha256:d200d2dd76b03a99b52651fd1325aff7dcd35422c35c01bac56571b0507f3deb AS build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY *.go ./
COPY testdata/* ./testdata/

RUN CGO_ENABLED=0 go test ./...
RUN go build -o /schemas-tool

## Run
##
FROM alpine:3.24@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

WORKDIR /

COPY --from=build /schemas-tool /schemas-tool

ENTRYPOINT ["/schemas-tool"]