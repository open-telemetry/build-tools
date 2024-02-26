# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv http -->

| Attribute name | Notes and examples                                           | `Required`? |
| :------------- | :----------------------------------------------------------- | --------- |
| `http.method` | HTTP request method. E.g. `"GET"`. | `Required` |
| `http.url` | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | Defined later. |
| `http.target` | The full request target as passed in a [HTTP request line][] or equivalent, e.g. `"/path/12314/?q=ddds#123"`. | Defined later. |
| `http.host` | The value of the [HTTP host header][]. When the header is empty or not present, this attribute should be the same. | Defined later. |
| `http.scheme` | The URI scheme identifying the used protocol: `"http"` or `"https"` | Defined later. |
| `http.status_code` | [HTTP response status code][]. E.g. `200` (integer) | `Conditionally Required` if and only if one was received/sent. |
| `http.status_text` | [HTTP reason phrase][]. E.g. `"OK"` | `Recommended` |
| `http.flavor` | Kind of HTTP protocol used: `"1.0"`, `"1.1"`, `"2"`, `"SPDY"` or `"QUIC"`. |  No |
| `http.user_agent` | Value of the HTTP [User-Agent][] header sent by the client. | `Recommended` |

<!-- endsemconv -->

It is recommended to also use the general [network attributes][], especially `net.peer.ip`. If `net.transport` is not specified, it can be assumed to be `IP.TCP` except if `http.flavor` is `QUIC`, in which case `IP.UDP` is assumed.

[network attributes]: span-general.md#general-network-connection-attributes
[HTTP response status code]: https://tools.ietf.org/html/rfc7231#section-6
[HTTP reason phrase]: https://tools.ietf.org/html/rfc7230#section-3.1.2
[User-Agent]: https://tools.ietf.org/html/rfc7231#section-5.5.3
