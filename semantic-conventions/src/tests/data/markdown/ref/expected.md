# Attributes

<!-- semconv grpc.client(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `rpc.service` | string | The service name, must be equal to the $service part in the span name. | `EchoService` | Required |
| [`net.peer.name`](input_general.md) | string | override brief. [1] | `example.com` | Optional |
| [`net.peer.port`](input_general.md) | int | It describes the server port the client is connecting to | `80`; `8080`; `443` | Required |

**[1]:** override note.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* [`net.peer.ip`](input_general.md)
* [`net.peer.name`](input_general.md), [`net.peer.ip`](input_general.md)
<!-- endsemconv -->
