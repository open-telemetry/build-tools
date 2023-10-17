# Test Markdown

**`foo.size`**
<!-- semconv metric.foo.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `foo.size` | Histogram | `{bars}` | Measures the size of foo. [1] |

**[1]:** Some notes on metric.foo.size
<!-- endsemconv -->

**Attributes for `foo.size`**
<!-- semconv metric.foo.size -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-requirement-level.md) |
|---|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Required` |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` if and only if one was received/sent. |
<!-- endsemconv -->

**`foo.active_eggs`**
<!-- semconv metric.foo.active_eggs(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `foo.active_eggs` | UpDownCounter | `{cartons}` | Measures how many eggs are currently active. |
<!-- endsemconv -->

**Attributes for `foo.active_eggs`**
<!-- semconv metric.foo.active_eggs -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-requirement-level.md) |
|---|---|---|---|---|
| `bar.egg.type` | string | Type of egg. [1] | `chicken`; `emu`; `dragon` | `Conditionally Required` if available to instrumentation. |
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Opt-In |

**[1]:** Some notes on attribute
<!-- endsemconv -->
