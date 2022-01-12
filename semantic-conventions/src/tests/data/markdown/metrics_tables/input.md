
## Common Attributes

The following attributes SHOULD be included on all HTTP metrics for both server and client. 

<!-- semconv metric.http -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| [`http.host`](../../trace/semantic_conventions/http.md) | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). An empty Host header should also be reported, see note. [1] | `www.example.org` | See attribute alternatives |
| [`http.method`](../../trace/semantic_conventions/http.md) | string | HTTP request method. | `GET`; `POST`; `HEAD` | Yes |
| [`http.scheme`](../../trace/semantic_conventions/http.md) | string | The URI scheme identifying the used protocol. | `http`; `https` | See attribute alternative |
| [`http.status_code`](../../trace/semantic_conventions/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | No |

**[1]:** When the header is present but empty the attribute SHOULD be set to the empty string. Note that this is a valid situation that is expected in certain cases, according the aforementioned [section of RFC 7230](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is not set the attribute MUST NOT be set.
<!-- endsemconv -->

## HTTP Client 

### HTTP Client Metrics

<!-- semconv metric.http.client(metric_table,remove_constraints) -->
<!-- endsemconv -->

### HTTP Client Attributes

The following attributes SHOULD be included on HTTP Client metrics, where applicable and available.

<!-- semconv metric.http.client -->
<!-- endsemconv -->

## HTTP Server

### HTTP Server Metrics

<!-- semconv metric.http.server(metric_table,remove_constraints) -->
<!-- endsemconv -->

### HTTP Server Attributes

The following attributes SHOULD be included on HTTP Server metrics, where applicable and available.

<!-- semconv metric.http.server -->

<!-- endsemconv -->
