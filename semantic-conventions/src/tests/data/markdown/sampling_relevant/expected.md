# Attributes

<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `http.method` | string | . | `GET` | Yes |
| `http.url` | string | . | `.` | No |
| `http.target` | string | . | `.` | No |
| `http.host` | string | . | `.` | No |
| `http.scheme` | string | . | `http` | No |
| `http.status_code` | int | . |  | . |
| `http.user_agent` | string | . | `.` | No |
| [`net.peer.ip`](span-general.md) | string | . | `.` | No |
| [`net.peer.name`](span-general.md) | string | . | `.` | No |
| [`net.peer.port`](span-general.md) | int | . |  | No |

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* `http.method`
* `http.url`
* `http.target`
* `http.host`
* `http.scheme`
* [`net.peer.ip`](span-general.md)
* [`net.peer.name`](span-general.md)
* [`net.peer.port`](span-general.md)
<!-- endsemconv -->
