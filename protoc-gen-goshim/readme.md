# protobuf-gen-goshim

This tool replaces Go type definitions with imports.

## usage

Run the protoc compiler with the -goshim_out option, specifying the old and new package paths, and the output directory.

```shell
protoc -goshim_out=old=go.opentelemetry.io/proto/otlp,new=go.opentelemetry.io/proto/slim/otlp:./dir file.proto
```

### output

The generated Go code imports the new package and aliases the types, instead of redefining them.

```go
// Code generated by protoc-gen-goshim. DO NOT EDIT.

package v1

import slim "go.opentelemetry.io/proto/slim/otlp/logs/v1"

type (
	LogsData       = slim.LogsData
)
```

This feature is related to an issue in the OpenTelemetry Go project: <https://github.com/open-telemetry/opentelemetry-go/issues/2579>