# General

<!-- semconv http.server -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |
|---|---|---|---|---|
| `http.server_name` | String | The primary server name of the matched virtual host. [1] | `example.com` | `Conditionally Required` [2] |
| `http.route` | String | The matched route (path template). | `/users/:userID?` | `Recommended` |
| `http.client_ip` | String | The IP address of the original client behind all proxies, if known (e.g. from [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)). [3] | `83.164.160.102` | `Recommended` |

**[1]:** http.url is usually not readily available on the server side but would have to be assembled in a cumbersome and sometimes lossy process from other information (see e.g. open-telemetry/opentelemetry-python/pull/148). It is thus preferred to supply the raw data that is available.

**[2]:** This should be obtained via configuration. If this attribute can be obtained, this attribute MUST NOT be set ( `net.host.name` should be used instead).

**[3]:** This is not necessarily the same as `net.peer.ip`, which would identify the network-level peer, which may be a proxy.

At least one of the following is required:

* `http.url`
* `http.scheme`, `http.host`, `http.target`
* `http.scheme`, `http.server_name`, [net.host.port](general.md), `http.target`
* `http.scheme`, [net.host.name](general.md), [net.host.port](general.md), `http.target`

<!-- endsemconv -->
