# Test Markdown

**`foo.size`**
<!-- semconv metric.foo.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `foo.size` | Histogram | `{bars}` | Measures the size of foo. |
<!-- endsemconv -->
**Attributes for `foo.size`**
<!-- semconv metric.foo.size -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.flavor` | string | Kind of HTTP protocol used. [1] | `1.0` | Recommended |
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: if and only if one was received/sent. |

**[1]:** If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.
<!-- endsemconv -->
