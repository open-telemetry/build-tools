## DB spans

<!-- semconv database.foo.span(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-requirement-level.md) |
|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` |
| `db.name` | string | Database name. | `the_shop` | `Recommended` |
<!-- endsemconv -->

## DB metrics

<!-- semconv database.foo.duration.metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.foo.duration` | Histogram | `s` | Measures the duration of database Foo calls. |
<!-- endsemconv -->

<!-- semconv database.foo.duration.metric(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-requirement-level.md) |
|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` |
| `db.name` | string | Database name. | `the_shop` | `Recommended` |
<!-- endsemconv -->
