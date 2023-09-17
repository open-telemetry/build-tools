# Spans

<!-- semconv http.client.spans(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`server.address`](input_server.md) | string | Server component of Host header. | `foo` | Required |

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

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
| [`server.address`](input_server.md) | string | Server component of Host header. | `foo` | Required |
<!-- endsemconv -->
