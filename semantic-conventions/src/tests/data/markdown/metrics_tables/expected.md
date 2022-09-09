# Test Markdown

**`foo.size`**
<!-- semconv metric.foo.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `foo.size` | Histogram | `{bars}` | Measures the size of foo. |
<!-- endsemconv -->
**Attributes for `foo.size`**
<!-- semconv metric.foo.size -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: if and only if one was received/sent. |
<!-- endsemconv -->
