## Build
##
FROM golang:1.27-alpine@sha256:4c9fe60190a2a3350ddc51de80d0224b8a6698d12bdfc999fee45ea9d6c46dbc AS build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY *.go ./
COPY testdata/* ./testdata/

RUN CGO_ENABLED=0 go test ./...
RUN go build -o /schemas-tool

## Run
##
FROM alpine:3.24@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b

WORKDIR /

COPY --from=build /schemas-tool /schemas-tool

ENTRYPOINT ["/schemas-tool"]