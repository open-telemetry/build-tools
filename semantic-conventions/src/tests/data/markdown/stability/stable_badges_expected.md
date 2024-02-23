<!-- semconv test -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | Required |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | Required |
<!-- endsemconv -->

<!-- semconv ref_test -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | Required |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | Required |
<!-- endsemconv -->

<!-- semconv extends_test(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br> |  | Required |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | Required |
| [`test.stable_attr`](stable_badges_expected.md) | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br> |  | Required |
<!-- endsemconv -->

<!-- semconv stable_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `stable_metric` | Histogram | `s` | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>stable_metric |
<!-- endsemconv -->

<!-- semconv experimental_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `experimental_metric` | Counter | `{e}` | experimental_metric |
<!-- endsemconv -->

<!-- semconv deprecated_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `deprecated_metric` | UpDownCounter | `{d}` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>deprecated_metric |
<!-- endsemconv -->