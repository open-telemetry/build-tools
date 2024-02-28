## DB spans

<!-- semconv database.foo.span(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
|---|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` | Experimental |
| `db.name` | string | Database name. | `the_shop` | `Recommended` | Experimental |
<!-- endsemconv -->

## DB metrics

<!-- semconv database.foo.duration.metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.foo.duration` | Histogram | `s` | Measures the duration of database Foo calls. | Experimental |
<!-- endsemconv -->

<!-- semconv database.foo.duration.metric(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
|---|---|---|---|---|---|
| `db.foo.bar` | string | Some property. | `baz` | `Recommended` | Experimental |
| `db.name` | string | Database name. | `the_shop` | `Recommended` | Experimental |
<!-- endsemconv -->
