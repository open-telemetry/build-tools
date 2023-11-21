# Attributes

<!-- semconv grpc.client(full) -->
| Attribute  | [Type](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md#attribute) | Description  | Examples  | [Requirement Level](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-requirement-level.md) |
|---|---|---|---|---|
| [`net.peer.name`](input_general.md) | string | override brief. [1] | `example.com` | Opt-In |
| [`net.peer.port`](input_general.md) | int | It describes the server port the client is connecting to | `80`; `8080`; `443` | `Required` |
| [`net.sock.peer.addr`](input_general.md) | string | Remote socket peer address. | `127.0.0.1`; `/tmp/mysql.sock` | `Required` |
| [`net.sock.peer.port`](input_general.md) | int | Remote socket peer port. | `16456` | `Conditionally Required` <condition> |
| `rpc.service` | string | The service name, must be equal to the $service part in the span name. | `EchoService` | `Required` |

**[1]:** override note.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* [`net.peer.ip`](input_general.md)
* [`net.peer.name`](input_general.md), [`net.peer.ip`](input_general.md)
<!-- endsemconv -->
