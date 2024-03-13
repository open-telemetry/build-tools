# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv http -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Required` | Experimental |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` if and only if one was received/sent | Experimental |
| `http.flavor` | string | Kind of HTTP protocol used [1] | `1.0` | `Recommended` | Deprecated: Use attribute `flavor_new` instead. |
| `http.host` | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is empty or not present, this attribute should be the same. | `www.example.org` | `Recommended` | Experimental |
| `http.scheme` | string | The URI scheme identifying the used protocol. | `http`; `https` | `Recommended` | Experimental |
| `http.status_text` | string | [HTTP reason phrase](https://tools.ietf.org/html/rfc7230#section-3.1.2). | `OK` | `Recommended` | Deprecated: Use attribute `status_description` instead. |
| `http.target` | string | The full request target as passed in a HTTP request line or equivalent. | `/path/12314/?q=ddds#123` | `Recommended` | Experimental |
| `http.url` | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` | `Recommended` | Experimental |
| `http.user_agent` | string | Value of the [HTTP User-Agent](https://tools.ietf.org/html/rfc7231#section-5.5.3) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3` | `Recommended` | Experimental |

**[1]:** If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

`http.flavor` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `1.0` | HTTP 1.0 | Experimental |
| `1.1` | HTTP 1.1 | Experimental |
| `2.0` | HTTP 2 | Experimental |
| `SPDY` | SPDY protocol. | Experimental |
| `QUIC` | QUIC protocol. | Experimental |
<!-- endsemconv -->

It is recommended to also use the general [network attributes][], especially `net.peer.ip`. If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

[network attributes]: span-general.md#general-network-connection-attributes
[HTTP response status code]: https://tools.ietf.org/html/rfc7231#section-6
[HTTP reason phrase]: https://tools.ietf.org/html/rfc7230#section-3.1.2
[User-Agent]: https://tools.ietf.org/html/rfc7231#section-5.5.3
