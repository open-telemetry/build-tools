# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv network -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `net.host.carrier.icc` | string | host.carrier.icc | `DE` | Recommended |
| `net.host.carrier.mcc` | string | host.carrier.mcc | `310` | Recommended |
| `net.host.carrier.mnc` | string | host.carrier.mnc | `001` | Recommended |
| `net.host.carrier.name` | string | host.carrier.name | `sprint` | Recommended |
| `net.host.connection.subtype` | string | This describes more details regarding the connection.type. It may be the type of cell connection, but it could be used for describing details about a wifi connection. | `2G` | Recommended |
| `net.host.connection.type` | string | unavailable | `wifi` | Recommended |
| `net.host.ip` | string | Like `net.peer.ip` but for the host IP. Useful in case of a multi-IP host. | `192.168.0.1` | Recommended |
| `net.host.name` | string | Local hostname or similar, see note below. | `localhost` | Recommended |
| `net.host.port` | int | Like `net.peer.port` but for the host port. | `35555` | Recommended |
| `net.peer.ip` | string | Remote address of the peer (dotted decimal for IPv4 or [RFC5952](https://tools.ietf.org/html/rfc5952) for IPv6) | `127.0.0.1` | Recommended |
| `net.peer.name` | string | Remote hostname or similar, see note below. | `example.com` | Recommended |
| `net.peer.port` | int | Remote port number. | `80`; `8080`; `443` | Recommended |
| `net.transport` | string | Transport protocol used. See note below. | `IP.TCP` | Recommended |

`net.host.connection.subtype` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `1G` | 1G |
| `2G` | 2G |

`net.host.connection.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `wifi` | wifi [1] |
| `wired` | wired |
| `cell` | cell |
| `unavailable` | unavailable |

**[1]:** Usually 802.11

`net.transport` MUST be one of the following:

| Value  | Description |
|---|---|
| `IP.TCP` | ip.tcp |
| `IP.UDP` | ip.udp |
| `IP` | Another IP-based protocol |
| `Unix` | Unix Domain socket. See below. |
| `pipe` | Named or anonymous pipe. See note below. |
| `inproc` | In-process communication. [1] |
| `other` | Something else (non IP-based). |

**[1]:** Signals that there is only in-process communication not using a "real" network protocol in cases where network attributes would normally be expected. Usually all other network attributes can be left out in that case.
<!-- endsemconv -->
