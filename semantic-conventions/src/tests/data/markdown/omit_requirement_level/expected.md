# Common Attributes

<!-- semconv http(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` |
| `http.url` | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` |
| `http.target` | string | The full request target as passed in a HTTP request line or equivalent. | `/path/12314/?q=ddds#123` |
<!-- endsemconv -->
