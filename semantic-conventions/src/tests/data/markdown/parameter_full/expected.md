# Attributes

<!-- semconv faas.http(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `faas.trigger` | string | Type of the trigger on which the function is executed. | `datasource` | `Required` | Experimental |
| `faas.execution` | string | The execution id of the current function execution. | `af9d5aa4-a685-4c5f-a22b-444f80b3cc28` | `Recommended` | Experimental |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write. | Experimental |
| `http` | To provide an answer to an inbound HTTP request | Experimental |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system. | Experimental |
| `timer` | A function is scheduled to be executed regularly. | Experimental |
| `other` | other | Experimental |
<!-- endsemconv -->
