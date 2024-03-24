# Spans

<!-- semconv http.client.spans(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`server.address`](input_server.md) | string | Server component of Host header. (overridden brief) [1] | `foo.io` | `Required` | Experimental |

**[1]:** Note on the overridden attribute definition.

The following attributes can be important for making sampling decisions and SHOULD be provided **at span creation time** (if provided at all):

* [`server.address`](input_server.md)
<!-- endsemconv -->

# Metrics

<!-- semconv http.client.request.duration.metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `http.client.request.duration` | Histogram | `s` | Measures request duration. | Experimental |
<!-- endsemconv -->

<!-- semconv http.client.request.duration.metric(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`server.address`](input_server.md) | string | Server component of Host header. (overridden brief) [1] | `foo.io` | `Required` | Experimental |

**[1]:** Note on the overridden attribute definition.
<!-- endsemconv -->
