# Test

<!-- semconv event -->
The event name MUST be `exception`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exception.escaped` | boolean | SHOULD be set to true if the exception event is recorded at a point where it is known that the exception is escaping the scope of the span. [1] |  | Recommended |
| `exception.message` | string | The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` | See below |
| `exception.stacktrace` | string | A stacktrace. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` | Recommended |
| `exception.type` | string | The type of the exception. | `java.net.ConnectException`; `OSError` | See below |

**[1]:** An exception is considered to have escaped.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `exception.type`
* `exception.message`
<!-- endsemconv -->
