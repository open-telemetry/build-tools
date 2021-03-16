# Attributes

<!-- semconv grpc.client(full) -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `rpc.service` | string | The service name, must be equal to the $service part in the span name. | `EchoService` | Yes |
| [`net.peer.port`](input_general.md) | int | It describes the server port the client is connecting to | `80`; `8080`; `443` | Yes |

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* [`net.peer.ip`](input_general.md)
* [`net.peer.name`](input_general.md), [`net.peer.ip`](input_general.md)
<!-- endsemconv -->
