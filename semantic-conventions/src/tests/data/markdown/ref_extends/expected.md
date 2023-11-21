# Spans

<!-- semconv http.client.spans(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`server.address`](input_server.md) | string | Server component of Host header. (overridden brief) [1] | `foo.io` | Required |

**[1]:** Note on the overridden attribute definition.

The following attributes can be important for making sampling decisions and SHOULD be provided **at span creation time** (if provided at all):

* [`server.address`](input_server.md)
<!-- endsemconv -->

# Metrics

<!-- semconv http.client.request.duration.metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.request.duration` | Histogram | `s` | Measures request duration. |
<!-- endsemconv -->

<!-- semconv http.client.request.duration.metric(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`server.address`](input_server.md) | string | Server component of Host header. (overridden brief) [1] | `foo.io` | Required |

**[1]:** Note on the overridden attribute definition.
<!-- endsemconv -->
