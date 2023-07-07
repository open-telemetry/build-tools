# Custom HTTP Semantic Conventions

<!-- semconv custom_http -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `custom_http.request.header.<key>` | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase, with - characters replaced by _), the value being the header values. | ``http.request.header.content_type=["application/json"]`` | Recommended |
| `custom_http.request.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
<!-- endsemconv -->
