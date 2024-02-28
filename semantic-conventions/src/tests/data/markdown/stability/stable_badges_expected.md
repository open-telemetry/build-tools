<!-- semconv test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Experimental |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv ref_test -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Experimental |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv extends_test(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
|---|---|---|---|---|---|
| [`test.deprecated_experimental_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.deprecated_stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Deprecated: Removed. |
| [`test.exp_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | Experimental |
| [`test.stable_attr`](stable_badges_expected.md) | boolean |  |  | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv stable_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
| -------- | --------------- | ----------- | -------------- | --------- |
| `stable_metric` | Histogram | `s` | stable_metric | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

<!-- semconv experimental_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
| -------- | --------------- | ----------- | -------------- | --------- |
| `experimental_metric` | Counter | `{e}` | experimental_metric | Experimental |
<!-- endsemconv -->

<!-- semconv deprecated_metric(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | [Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability) |
| -------- | --------------- | ----------- | -------------- | --------- |
| `deprecated_metric` | UpDownCounter | `{d}` | deprecated_metric | Deprecated: Removed. |
<!-- endsemconv -->