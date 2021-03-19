# RPC.GRPC with int enum

<!-- semconv rpc.grpc -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `rpc.grpc.status_code` | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0`; `1`; `16` | Yes |

`rpc.grpc.status_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `0` | OK |
| `1` | CANCELLED |
| `2` | UNKNOWN |
| `3` | INVALID_ARGUMENT |
| `4` | DEADLINE_EXCEEDED |
| `5` | NOT_FOUND |
| `6` | ALREADY_EXISTS |
| `7` | PERMISSION_DENIED |
| `8` | RESOURCE_EXHAUSTED |
| `9` | FAILED_PRECONDITION |
| `10` | ABORTED |
| `11` | OUT_OF_RANGE |
| `12` | UNIMPLEMENTED |
| `13` | INTERNAL |
| `14` | UNAVAILABLE |
| `15` | DATA_LOSS |
| `16` | UNAUTHENTICATED |
<!-- endsemconv -->
