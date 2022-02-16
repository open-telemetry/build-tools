# Schema File Tool

A lightweight schema tool Docker image, published as otel/build-tool-schemas to Docker Hub.

## Usage

Command line options:
--file path to the schema file to check
--version expected schema version number. Optional. If provided the schema version is checked inside the file. 

To check that a file is a valid Schema file do this:

```bash
docker run --rm -v<some-path>:<some-path> -w<some-path> otel/build-tool-schemas [OPTION] --file=<some-path>/<schemafilepath> [other options]
```

For help try:

```bash
docker run --rm otel/build-tool-schemas --help
```

## Contributing

To build the Docker image locally run:

```bash
docker build schemas/. -t build-tool-schemas
```

To run the Docker image locally and check schema file version 1.9.0 do this:

```bash
docker run -v=/your-path-to-spec-repo/opentelemetry-specification/schemas/:/schemas build-tool-schemas --file /schemas/1.9.0 --version=1.9.0
```
