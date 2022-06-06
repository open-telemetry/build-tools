
## Common Attributes

The following attributes SHOULD be included on all HTTP metrics for both server and client. 

<!-- semconv metric.http -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.host` | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). An empty Host header should also be reported, see note. [1] | `www.example.org` | Conditionally Required: See attribute alternatives |
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
| `http.scheme` | string | The URI scheme identifying the used protocol. | `http`; `https` | Conditionally Required: See attribute alternative |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Recommended |

**[1]:** When the header is present but empty the attribute SHOULD be set to the empty string. Note that this is a valid situation that is expected in certain cases, according the aforementioned [section of RFC 7230](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is not set the attribute MUST NOT be set.
<!-- endsemconv -->

## HTTP Client 

### HTTP Client Metrics

<!-- semconv metric.http.client(metric_table,remove_constraints) -->
| Name     | Instrument    | Unit (UCUM) | Description    |
| -------- | ------------- | ----------- | -------------- |
| `http.client.duration` | Histogram | `ms` | Measures the duration of the outbound HTTP request. |
<!-- endsemconv -->

### HTTP Client Attributes

The following attributes SHOULD be included on HTTP Client metrics, where applicable and available.

<!-- semconv metric.http.client -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `net.peer.ip` | string | Remote address of the peer (dotted decimal for IPv4 or [RFC5952](https://tools.ietf.org/html/rfc5952) for IPv6) | `127.0.0.1` | See below |
| `net.peer.name` | string | Remote hostname or similar, see note below. | `example.com` | See below |
| `net.peer.port` | int | Remote port number. | `80`; `8080`; `443` | See below |

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `http.url`
* `http.scheme`, `http.host`, `http.target`
* `http.scheme`, `net.peer.name`, `net.peer.port`, `http.target`
* `http.scheme`, `net.peer.ip`, `net.peer.port`, `http.target`
<!-- endsemconv -->

## HTTP Server

### HTTP Server Metrics

<!-- semconv metric.http.server(metric_table,remove_constraints) -->
| Name     | Instrument    | Unit (UCUM) | Description    |
| -------- | ------------- | ----------- | -------------- |
| `http.server.duration` | Histogram | `ms` | Measures the duration of the inbound HTTP request. |
| `http.server.active_requests` | UpDownCounter | `{requests}` | Measures the number of concurrent HTTP requests that are currently in-flight. |
<!-- endsemconv -->

### HTTP Server Attributes

The following attributes SHOULD be included on HTTP Server metrics, where applicable and available.

<!-- semconv metric.http.server -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.server_name` | string | The primary server name of the matched virtual host. This should be obtained via configuration. If no such configuration can be obtained, this attribute MUST NOT be set ( `net.host.name` should be used instead). [1] | `example.com` | See below |
| `net.host.name` | string | Local hostname or similar, see note below. | `localhost` | See below |
| `net.host.port` | int | Like `net.peer.port` but for the host port. | `35555` | See below |

**[1]:** `http.url` is usually not readily available on the server side but would have to be assembled in a cumbersome and sometimes lossy process from other information (see e.g. open-telemetry/opentelemetry-python/pull/148). It is thus preferred to supply the raw data that is available.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `http.scheme`, `http.host`, `http.target`
* `http.scheme`, `http.server_name`, `net.host.port`, `http.target`
* `http.scheme`, `net.host.name`, `net.host.port`, `http.target`
* `http.url`
<!-- endsemconv -->
