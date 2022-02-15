## Build
##
FROM golang:1.17-alpine AS build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY *.go ./

RUN go build -o /schemas-tool

## Run
##
FROM alpine:3.13

WORKDIR /

COPY --from=build /schemas-tool /schemas-tool

USER nonroot:nonroot

ENTRYPOINT ["/schemas-tool"]