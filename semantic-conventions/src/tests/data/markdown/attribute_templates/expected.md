# Custom HTTP Semantic Conventions

<!-- semconv custom_http(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |
|---|---|---|---|---|
| `custom_http.request.header.<key>` | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase, with - characters replaced by _), the value being the header values. | ``http.request.header.content_type=["application/json"]`` | `Recommended` |
| `custom_http.request.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Required` |
| `general.some_general_attribute.<key>` | string | This is a general attribute. | ``some_general_attribute.some_key="abc"`` | `Recommended` |
| `referenced_http.request.referenced.header.<key>` | string[] | This is a referenced attribute. | ``http.request.header.content_type=["application/json"]`` | `Recommended` |
<!-- endsemconv -->
