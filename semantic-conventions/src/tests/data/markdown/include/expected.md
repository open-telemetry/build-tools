# Test Markdown

<!-- semconv faas.http(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `faas.trigger` | string | Type of the trigger on which the function is executed. | `datasource` | `Required` | Experimental |
| `http.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | `Required` | Experimental |
| [`http.server_name`](input_http.md) | string | The primary server name of the matched virtual host. [1] | `example.com` | `Conditionally Required` [2] | Experimental |
| `http.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` if and only if one was received/sent | Experimental |
| `faas.execution` | string | The execution id of the current function execution. | `af9d5aa4-a685-4c5f-a22b-444f80b3cc28` | `Recommended` | Experimental |
| `http.host` | string | The value of the [HTTP host header](https://tools.ietf.org/html/rfc7230#section-5.4). When the header is empty or not present, this attribute should be the same. | `www.example.org` | See below | Experimental |
| `http.recommended_attribute` | string | brief | `foo` | `Recommended` short note | Experimental |
| `http.recommended_attribute_long_note` | string | brief | `bar` | `Recommended` [3] | Experimental |
| `http.scheme` | string | The URI scheme identifying the used protocol. | `http`; `https` | See below | Experimental |
| `http.status_text` | string | [HTTP reason phrase](https://tools.ietf.org/html/rfc7230#section-3.1.2). | `OK` | `Recommended` | Experimental |
| `http.target` | string | The full request target as passed in a HTTP request line or equivalent. | `/path/12314/?q=ddds#123` | See below | Experimental |
| `http.url` | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` | See below | Experimental |
| `http.user_agent` | string | Value of the [HTTP User-Agent](https://tools.ietf.org/html/rfc7231#section-5.5.3) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3` | `Recommended` | Experimental |

**[1]:** This is an example

- of note
- with list

**[2]:** This should be obtained via configuration. If this attribute can be obtained, this attribute MUST NOT be set ( `net.host.name` should be used instead).

**[3]:** some very long note that should be written under the semconv table

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `http.url`
* `http.scheme`, `http.host`, `http.target`
* `http.scheme`, [`http.server_name`](input_http.md), `net.host.port`, `http.target`
* `http.scheme`, `net.host.name`, `net.host.port`, `http.target`

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write. | Experimental |
| `http` | To provide an answer to an inbound HTTP request | Experimental |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system. | Experimental |
| `timer` | A function is scheduled to be executed regularly. | Experimental |
| `other` | other | Experimental |
<!-- endsemconv -->
