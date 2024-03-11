# RPC.GRPC with int enum

<!-- semconv rpc.grpc -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `rpc.grpc.status_code` | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0`; `1`; `16` | `Required` | Experimental |

`rpc.grpc.status_code` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `0` | ok | Experimental |
| `1` | cancelled | Experimental |
| `2` | unknown | Experimental |
| `3` | invalid_argument | Experimental |
| `4` | deadline_exceeded | Experimental |
| `5` | not_found | Experimental |
| `6` | already_exists | Experimental |
| `7` | permission_denied | Experimental |
| `8` | resource_exhausted | Experimental |
| `9` | failed_precondition | Experimental |
| `10` | aborted | Experimental |
| `11` | out_of_range | Experimental |
| `12` | unimplemented | Experimental |
| `13` | internal | Experimental |
| `14` | unavailable | Experimental |
| `15` | data_loss | Experimental |
| `16` | unauthenticated | Experimental |
<!-- endsemconv -->
