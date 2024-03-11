<!-- semconv test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv ref_test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv extends_test(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv stable_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `stable_metric` | Histogram | `s` | stable_metric | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv experimental_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `experimental_metric` | Counter | `{e}` | experimental_metric | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv deprecated_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `deprecated_metric` | UpDownCounter | `{d}` | deprecated_metric | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed. |
<!-- endsemconv -->