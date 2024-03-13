## DB spans

<!-- semconv database.foo.span(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` | Experimental |
| `db.name` | string | Database name. | `the_shop` | `Recommended` | Experimental |
<!-- endsemconv -->

## DB metrics

<!-- semconv database.foo.duration.metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.foo.duration` | Histogram | `s` | Measures the duration of database Foo calls. | Experimental |
<!-- endsemconv -->

<!-- semconv database.foo.duration.metric(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` | Experimental |
| `db.name` | string | Database name. | `the_shop` | `Recommended` | Experimental |
<!-- endsemconv -->
