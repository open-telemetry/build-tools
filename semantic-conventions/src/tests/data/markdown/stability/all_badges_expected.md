<!-- semconv test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.exp_attr`](stable_badges_expected.md) | boolean | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br> |  | `Required` |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | `Required` |
| [`test.stable_enum_attr`](stable_badges_expected.md) | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> | `one` | `Recommended` |

`test.stable_enum_attr` MUST be one of the following:

| Value  | Description |
|---|---|
| `one` | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>member one |
| `two` | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br>member two |
| `three` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>member three |
| `four` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>member four |
<!-- endsemconv -->

<!-- semconv ref_test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.exp_attr`](stable_badges_expected.md) | boolean | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br> |  | `Required` |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | `Required` |
| [`test.stable_enum_attr`](stable_badges_expected.md) | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> | `one` | `Recommended` |
<!-- endsemconv -->

<!-- semconv extends_test(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | `Required` |
| [`test.exp_attr`](stable_badges_expected.md) | boolean | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br> |  | `Required` |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | `Required` |
| [`test.stable_enum_attr`](stable_badges_expected.md) | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> | `one` | `Recommended` |

`test.stable_enum_attr` MUST be one of the following:

| Value  | Description |
|---|---|
| `one` | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>member one |
| `two` | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br>member two |
| `three` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>member three |
| `four` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>member four |
<!-- endsemconv -->

<!-- semconv stable_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `stable_metric` | Histogram | `s` | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>stable_metric |
<!-- endsemconv -->

<!-- semconv experimental_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `experimental_metric` | Counter | `{e}` | ![Experimental](https://img.shields.io/badge/-experimental-blue)<br>experimental_metric |
<!-- endsemconv -->

<!-- semconv deprecated_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `deprecated_metric` | UpDownCounter | `{d}` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>deprecated_metric |
<!-- endsemconv -->