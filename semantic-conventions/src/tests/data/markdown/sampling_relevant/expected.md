# Attributes

<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `http.host` | string | . | `.` | `Recommended` | Experimental |
| `http.method` | string | . | `GET` | `Required` | Experimental |
| `http.scheme` | string | . | `http` | `Recommended` | Experimental |
| `http.status_code` | int | . |  | `Conditionally Required` <condition> | Experimental |
| `http.target` | string | . | `.` | `Recommended` | Experimental |
| `http.url` | string | . [1] | `.` | `Recommended` | Experimental |
| `http.user_agent` | string | . | `.` | `Recommended` | Experimental |
| [`net.peer.ip`](span-general.md) | string | . | `.` | `Recommended` | Experimental |
| [`net.peer.name`](span-general.md) | string | . | `.` | `Recommended` | Experimental |
| [`net.peer.port`](span-general.md) | int | . |  | `Recommended` | Experimental |

**[1]:** `http.url` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case the attribute's value should be `https://www.example.com/`.

The following attributes can be important for making sampling decisions and SHOULD be provided **at span creation time** (if provided at all):

* `http.host`
* `http.method`
* `http.scheme`
* `http.target`
* `http.url`
* [`net.peer.ip`](span-general.md)
* [`net.peer.name`](span-general.md)
* [`net.peer.port`](span-general.md)
<!-- endsemconv -->
