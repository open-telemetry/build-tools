# DB

<!-- semconv db(tag=connection-level) -->
| Attribute  | Type | Description  | Examples  | Required |
|---|---|---|---|---|
| `db.type` | string | Database type. For any SQL database, "sql". For others, the lower-case database category. | `sql` | Yes |
| `db.connection_string` | string | The connection string used to connect to the database. [1] | `Server=(localdb)\v11.0;Integrated Security=true;` | No |
| `db.user` | string | Username for accessing the database. | `readonly_user`; `reporting_user` | No |
| `net.peer.ip` | string | Remote address of the peer (dotted decimal for IPv4 or [RFC5952](https://tools.ietf.org/html/rfc5952) for IPv6) | `127.0.0.1` | See below |
| `net.peer.name` | string | Remote hostname or similar, see note below. | `example.com` | See below |
| `net.peer.port` | int | Remote port number. | `80`; `8080`; `443` | No |

**[1]:** It is recommended to remove embedded credentials.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `net.peer.name`
* `net.peer.ip`

`db.type` MUST be one of the following or, if none of the listed values apply, a custom value:

| Value  | Description |
|---|---|
| `sql` | A SQL database |
| `cassandra` | Apache Cassandra |
| `hbase` | Apache HBase |
| `mongodb` | MongoDB |
| `redis` | Redis |
| `couchbase` | Couchbase |
| `couchdb` | CouchDB |
<!-- endsemconv -->
