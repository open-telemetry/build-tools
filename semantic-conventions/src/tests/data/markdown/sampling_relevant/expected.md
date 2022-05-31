# Attributes

<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.method` | string | . | `GET` | Required |
| `http.url` | string | . | `.` | Recommended |
| `http.target` | string | . | `.` | Recommended |
| `http.host` | string | . | `.` | Recommended |
| `http.scheme` | string | . | `http` | Recommended |
| `http.status_code` | int | . |  | Conditionally Required: <condition> |
| `http.user_agent` | string | . | `.` | Recommended |
| [`net.peer.ip`](span-general.md) | string | . | `.` | Recommended |
| [`net.peer.name`](span-general.md) | string | . | `.` | Recommended |
| [`net.peer.port`](span-general.md) | int | . |  | Recommended |

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
