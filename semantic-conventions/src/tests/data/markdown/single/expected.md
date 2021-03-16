# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Yes |
| `http.url` | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` | No |
| `http.target` | string | The full request target as passed in a HTTP request line or equivalent. | `/path/12314/?q=ddds#123` | No |
| `http.host` | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is empty or not present, this attribute should be the same. | `www.example.org` | No |
| `http.scheme` | string | The URI scheme identifying the used protocol. | `http`; `https` | No |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | If and only if one was received/sent |
| `http.status_text` | string | [HTTP reason phrase](https://tools.ietf.org/html/rfc7230#section-3.1.2). | `OK` | No |
| `http.flavor` | string | Kind of HTTP protocol used [1] | `1.0` | No |
| `http.user_agent` | string | Value of the [HTTP User-Agent](https://tools.ietf.org/html/rfc7231#section-5.5.3) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3` | No |

**[1]:** If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

`http.flavor` MUST be one of the following or, if none of the listed values apply, a custom value:

| Value  | Description |
|---|---|
| `1.0` | HTTP 1.0 |
| `1.1` | HTTP 1.1 |
| `2.0` | HTTP 2 |
| `SPDY` | SPDY protocol. |
| `QUIC` | QUIC protocol. |
<!-- endsemconv -->

It is recommended to also use the general [network attributes][], especially `net.peer.ip`. If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

[network attributes]: span-general.md#general-network-connection-attributes
[HTTP response status code]: https://tools.ietf.org/html/rfc7231#section-6
[HTTP reason phrase]: https://tools.ietf.org/html/rfc7230#section-3.1.2
[User-Agent]: https://tools.ietf.org/html/rfc7231#section-5.5.3
