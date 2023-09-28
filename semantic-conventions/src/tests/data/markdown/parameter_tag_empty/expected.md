# DB

<!-- semconv db(tag) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.dbms` | string | An identifier for the DBMS (database management system) product | `mssql` | Conditionally Required: for `db.type="sql"` |
| `db.jdbc.driver_classname` | string | The fully-qualified class name of the JDBC driver used to connect. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | Recommended |
| `db.mssql.instance_name` | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/en-us/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [1] | `MSSQLSERVER` | Recommended |
| `db.name` | string | If no tech-specific attribute is defined below, this attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [2] | `customers`; `master` | Conditionally Required: [3] |
| `db.operation` | string | The type of operation that is executed, e.g. the [MongoDB command name](https://docs.mongodb.com/manual/reference/command/#database-operations) such as `findAndModify`. While it would semantically make sense to set this, e.g., to a SQL keyword like `SELECT` or `INSERT`, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property (the back end can do that if required). | `findAndModify` | Conditionally Required: if `db.statement` is not applicable. |
| `db.statement` | string | A database statement for the given database type. [4] | `SELECT * FROM wuser_table`; `SET mykey "WuValue"` | Conditionally Required: if applicable. |

**[1]:** If setting a `db.mssql.instance_name`, `net.peer.port` is no longer required (but still recommended if non-standard).

**[2]:** In some SQL databases, the database name to be used is called "schema name". Redis does not have a database name to used here.

**[3]:** if applicable and no more-specific attribute is defined.

**[4]:** The value may be sanitized to exclude sensitive information.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `net.peer.name`
* `net.peer.ip`

`db.dbms` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `mssql` | Microsoft SQL Server |
| `mysql` | MySQL |
| `oracle` | Oracle |
| `db2` | IBM Db2 |
| `postgresql` | PostgreSQL |
| `redshift` | Amazon Redshift |
| `hive` | Apache Hive |
| `cloudscape` | Cloudscape |
| `hsqlsb` | HyperSQL DataBase |
| `progress` | Progress Database |
| `maxdb` | SAP MaxDB |
| `hanadb` | SAP HANA |
| `ingres` | Ingres |
| `firstsql` | FirstSQL |
| `edb` | EnterpriseDB |
| `cache` | InterSystems Caché |
| `adabas` | Adabas (Adaptable Database System) |
| `firebird` | Firebird |
| `derby` | Apache Derby |
| `filemaker` | FileMaker |
| `informix` | Informix |
| `instantdb` | InstantDB |
| `interbase` | InterBase |
| `mariadb` | MariaDB |
| `netezza` | Netezza |
| `pervasive` | Pervasive PSQL |
| `pointbase` | PointBase |
| `sqlite` | SQLite |
| `sybase` | Sybase |
| `teradata` | Teradata |
| `vertica` | Vertica |
| `h2` | H2 |
| `coldfusion` | ColdFusion IMQ |
<!-- endsemconv -->