# Attributes

<!-- semconv faas.http(full) -->
| Attribute  | Type | Description  | Example  | Required |
|---|---|---|---|---|
| `faas.trigger` | string | Type of the trigger on which the function is executed. | `datasource` | Yes |
| `faas.execution` | string | The execution id of the current function execution. | `af9d5aa4-a685-4c5f-a22b-444f80b3cc28` | No |
| `http.method` | string | HTTP request method. | `GET` or `POST` or `HEAD` | Yes |
| `http.url` | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` | See below |
| `http.target` | string | The full request target as passed in a HTTP request line or equivalent. | `/path/12314/?q=ddds#123` | See below |
| `http.host` | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is empty or not present, this attribute should be the same. | `www.example.org` | You should always have this. |
| `http.scheme` | string | The URI scheme identifying the used protocol. | `http` or `https` | See below |
| `http.status_code` | number | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | If and only if one was received/sent. |
| `http.status_text` | string | [HTTP reason phrase](https://tools.ietf.org/html/rfc7230#section-3.1.2). | `OK` | No |
| `http.flavor` | string | Kind of HTTP protocol used [1] | `1.0` | No |
| `http.user_agent` | string | Value of the [HTTP User-Agent](https://tools.ietf.org/html/rfc7231#section-5.5.3) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3` | No |
| [`http.server_name`](http.md) | string | The primary server name of the matched virtual host. [2] | `example.com` | Conditional [3] |
| [`http.route`](http.md) | string | The matched route (path template). | `/users/:userID?` | No |
| [`http.client_ip`](http.md) | string | The IP address of the original client behind all proxies, if known (e.g. from [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)). [4] | `83.164.160.102` | No |

**[1]:** If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

**[2]:** http.url is usually not readily available on the server side but would have to be assembled in a cumbersome and sometimes lossy process from other information (see e.g. open-telemetry/opentelemetry-python/pull/148). It is thus preferred to supply the raw data that is available.

**[3]:** This should be obtained via configuration. If this attribute can be obtained, this attribute MUST NOT be set ( `net.host.name` should be used instead).

**[4]:** This is not necessarily the same as `net.peer.ip`, which would identify the network-level peer, which may be a proxy.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `http.url`
* `http.scheme`, `http.host`, `http.target`
* `http.scheme`, [`http.server_name`](http.md), `net.host.port`, `http.target`
* `http.scheme`, `net.host.name`, `net.host.port`, `http.target`
<!-- endsemconv -->
