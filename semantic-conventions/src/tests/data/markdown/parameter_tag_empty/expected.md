# DB

<!-- semconv db(tag) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `db.dbms` | string | An identifier for the DBMS (database management system) product | `mssql` | `Conditionally Required` for `db.type="sql"` | Experimental |
| `db.name` | string | If no tech-specific attribute is defined below, this attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [1] | `customers`; `master` | `Conditionally Required` [2] | Experimental |
| `db.operation` | string | The type of operation that is executed, e.g. the [MongoDB command name](https://docs.mongodb.com/manual/reference/command/#database-operations) such as `findAndModify`. While it would semantically make sense to set this, e.g., to a SQL keyword like `SELECT` or `INSERT`, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property (the back end can do that if required). | `findAndModify` | `Conditionally Required` if `db.statement` is not applicable. | Experimental |
| `db.statement` | string | A database statement for the given database type. [3] | `SELECT * FROM wuser_table`; `SET mykey "WuValue"` | `Conditionally Required` if applicable. | Experimental |
| `db.jdbc.driver_classname` | string | The fully-qualified class name of the JDBC driver used to connect. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | `Recommended` | Experimental |
| `db.mssql.instance_name` | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/en-us/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [4] | `MSSQLSERVER` | `Recommended` | Experimental |

**[1]:** In some SQL databases, the database name to be used is called "schema name". Redis does not have a database name to used here.

**[2]:** if applicable and no more-specific attribute is defined.

**[3]:** The value may be sanitized to exclude sensitive information.

**[4]:** If setting a `db.mssql.instance_name`, `net.peer.port` is no longer required (but still recommended if non-standard).

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `net.peer.name`
* `net.peer.ip`

`db.dbms` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `mssql` | Microsoft SQL Server | Experimental |
| `mysql` | MySQL | Experimental |
| `oracle` | Oracle | Experimental |
| `db2` | IBM Db2 | Experimental |
| `postgresql` | PostgreSQL | Experimental |
| `redshift` | Amazon Redshift | Experimental |
| `hive` | Apache Hive | Experimental |
| `cloudscape` | Cloudscape | Experimental |
| `hsqlsb` | HyperSQL DataBase | Experimental |
| `progress` | Progress Database | Experimental |
| `maxdb` | SAP MaxDB | Experimental |
| `hanadb` | SAP HANA | Experimental |
| `ingres` | Ingres | Experimental |
| `firstsql` | FirstSQL | Experimental |
| `edb` | EnterpriseDB | Experimental |
| `cache` | InterSystems Caché | Experimental |
| `adabas` | Adabas (Adaptable Database System) | Experimental |
| `firebird` | Firebird | Experimental |
| `derby` | Apache Derby | Experimental |
| `filemaker` | FileMaker | Experimental |
| `informix` | Informix | Experimental |
| `instantdb` | InstantDB | Experimental |
| `interbase` | InterBase | Experimental |
| `mariadb` | MariaDB | Experimental |
| `netezza` | Netezza | Experimental |
| `pervasive` | Pervasive PSQL | Experimental |
| `pointbase` | PointBase | Experimental |
| `sqlite` | SQLite | Experimental |
| `sybase` | Sybase | Experimental |
| `teradata` | Teradata | Experimental |
| `vertica` | Vertica | Experimental |
| `h2` | H2 | Experimental |
| `coldfusion` | ColdFusion IMQ | Experimental |
<!-- endsemconv -->