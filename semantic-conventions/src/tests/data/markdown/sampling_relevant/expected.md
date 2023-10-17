# Attributes

<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.host` | string | . | `.` | Recommended |
| `http.method` | string | . | `GET` | Required |
| `http.scheme` | string | . | `http` | Recommended |
| `http.status_code` | int | . |  | Conditionally Required <condition> |
| `http.target` | string | . | `.` | Recommended |
| `http.url` | string | . [1] | `.` | Recommended |
| `http.user_agent` | string | . | `.` | Recommended |
| [`net.peer.ip`](span-general.md) | string | . | `.` | Recommended |
| [`net.peer.name`](span-general.md) | string | . | `.` | Recommended |
| [`net.peer.port`](span-general.md) | int | . |  | Recommended |

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
