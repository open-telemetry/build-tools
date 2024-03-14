# Common Attributes

<!-- Re-generate TOC with `TODO: ADD cmd` -->
<!-- semconv network -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `net.host.carrier.icc` | string | host.carrier.icc | `DE` | `Recommended` | Experimental |
| `net.host.carrier.mcc` | string | host.carrier.mcc | `310` | `Recommended` | Experimental |
| `net.host.carrier.mnc` | string | host.carrier.mnc | `001` | `Recommended` | Experimental |
| `net.host.carrier.name` | string | host.carrier.name | `sprint` | `Recommended` | Experimental |
| `net.host.connection.subtype` | string | This describes more details regarding the connection.type. It may be the type of cell connection, but it could be used for describing details about a wifi connection. | `2G` | `Recommended` | Experimental |
| `net.host.connection.type` | string | unavailable | `wifi` | `Recommended` | Experimental |
| `net.host.ip` | string | Like `net.peer.ip` but for the host IP. Useful in case of a multi-IP host. | `192.168.0.1` | `Recommended` | Experimental |
| `net.host.name` | string | Local hostname or similar, see note below. | `localhost` | `Recommended` | Experimental |
| `net.host.port` | int | Like `net.peer.port` but for the host port. | `35555` | `Recommended` | Experimental |
| `net.peer.ip` | string | Remote address of the peer (dotted decimal for IPv4 or [RFC5952](https://tools.ietf.org/html/rfc5952) for IPv6) | `127.0.0.1` | `Recommended` | Experimental |
| `net.peer.name` | string | Remote hostname or similar, see note below. | `example.com` | `Recommended` | Experimental |
| `net.peer.port` | int | Remote port number. | `80`; `8080`; `443` | `Recommended` | Experimental |
| `net.transport` | string | Transport protocol used. See note below. | `IP.TCP` | `Recommended` | Experimental |

`net.host.connection.subtype` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `1G` | 1G | Experimental |
| `2G` | 2G | Experimental |

`net.host.connection.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `wifi` | wifi [1] | Experimental |
| `wired` | wired | Experimental |
| `cell` | cell | Experimental |
| `unavailable` | unavailable | Experimental |

**[1]:** Usually 802.11

`net.transport` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `IP.TCP` | ip.tcp | Experimental |
| `IP.UDP` | ip.udp | Experimental |
| `IP` | Another IP-based protocol | Experimental |
| `Unix` | Unix Domain socket. See below. | Experimental |
| `pipe` | Named or anonymous pipe. See note below. | Experimental |
| `inproc` | In-process communication. [1] | Experimental |
| `other` | Something else (non IP-based). | Experimental |

**[1]:** Signals that there is only in-process communication not using a "real" network protocol in cases where network attributes would normally be expected. Usually all other network attributes can be left out in that case.
<!-- endsemconv -->
