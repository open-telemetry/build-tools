# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv network -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `net.transport` | string | Transport protocol used. See note below. | `IP.TCP` | No |
| `net.host.connection.type` | string | unavailable | `wifi` | No |
| `net.host.connection.subtype` | string | This describes more details regarding the connection.type. It may be the type of cell connection, but it could be used for describing details about a wifi connection. | `4G` | No |
| `net.host.carrier.name` | string | host.carrier.name | `sprint` | No |
| `net.host.carrier.mcc` | string | host.carrier.mcc | `310` | No |
| `net.host.carrier.mnc` | string | host.carrier.mnc | `001` | No |
| `net.host.carrier.icc` | string | host.carrier.icc | `DE` | No |
| `net.peer.ip` | string | Remote address of the peer (dotted decimal for IPv4 or [RFC5952](https://tools.ietf.org/html/rfc5952) for IPv6) | `127.0.0.1` | No |
| `net.peer.port` | int | Remote port number. | `80`; `8080`; `443` | No |
| `net.peer.name` | string | Remote hostname or similar, see note below. | `example.com` | No |
| `net.host.ip` | string | Like `net.peer.ip` but for the host IP. Useful in case of a multi-IP host. | `192.168.0.1` | No |
| `net.host.port` | int | Like `net.peer.port` but for the host port. | `35555` | No |
| `net.host.name` | string | Local hostname or similar, see note below. | `localhost` | No |

`net.transport` MUST be one of the following:

| Value  | Description |
|---|---|
| `IP.TCP` | IP.TCP |
| `IP.UDP` | IP.UDP |
| `IP` | Another IP-based protocol |
| `Unix` | Unix Domain socket. See below. |
| `pipe` | Named or anonymous pipe. See note below. |
| `inproc` | In-process communication. [1] |
| `other` | Something else (non IP-based). |

**[1]:** Signals that there is only in-process communication not using a "real" network protocol in cases where network attributes would normally be expected. Usually all other network attributes can be left out in that case.

`net.host.connection.type` MUST be one of the following or, if none of the listed values apply, a custom value:

| Value  | Description |
|---|---|
| `wifi` | wifi |
| `wired` | wired |
| `cell` | cell |
| `unavailable` | unavailable |

`net.host.connection.subtype` MUST be one of the following or, if none of the listed values apply, a custom value:

| Value  | Description |
|---|---|
| `1G` | 1G
 |
| `2G` | 2G
 |
| `3G` | 3G
 |
| `4G` | 4G
 |
| `5G` | 5G
 |
<!-- endsemconv -->
