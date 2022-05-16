# DB

<!-- semconv db(tag=connection-level,remove_constraints) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.type` | String | Database type. For any SQL database, "sql". For others, the lower-case database category. | `sql` | Required |
| `db.connection_string` | String | The connection string used to connect to the database. [1] | `Server=(localdb)\v11.0;Integrated Security=true;` | Recommended |
| `db.user` | String | Username for accessing the database. | `readonly_user`<br>`reporting_user` | Recommended |
| [net.peer.ip](general.md) | String | None | `127.0.0.1` | Recommended |
| [net.peer.name](general.md) | String | None | `example.com` | Recommended |
| [net.peer.port](general.md) | int | None | `80`<br>`8080`<br>`443` | Recommended |
| [net.transport](general.md) | Enum | None | `IP.TCP` | Recommended |

**[1]:** It is recommended to remove embedded credentials.

`db.type` MUST be one of the following:

| Value  | Description |
|---|---|
| sql | A SQL database |
| cassandra | Apache Cassandra |
| hbase | Apache HBase |
| mongodb | MongoDB |
| redis | Redis |
| couchbase | Couchbase |
| couchdb | CouchDB |

<!-- endsemconv -->
