# Test Markdown

**`foo.size`**
<!-- semconv metric.foo.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `foo.size` | Histogram | `{bars}` | Measures the size of foo. [1] | Stable |

**[1]:** Some notes on metric.foo.size
<!-- endsemconv -->

**Attributes for `foo.size`**
<!-- semconv metric.foo.size -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Required` | Experimental |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` if and only if one was received/sent. | Experimental |
<!-- endsemconv -->

**`foo.active_eggs`**
<!-- semconv metric.foo.active_eggs(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `foo.active_eggs` | UpDownCounter | `{cartons}` | Measures how many eggs are currently active. | Deprecated: Removed. |
<!-- endsemconv -->

**Attributes for `foo.active_eggs`**
<!-- semconv metric.foo.active_eggs -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `bar.egg.type` | string | Type of egg. [1] | `chicken`; `emu`; `dragon` | `Conditionally Required` if available to instrumentation. | Experimental |
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Opt-In` | Experimental |

**[1]:** Some notes on attribute
<!-- endsemconv -->
