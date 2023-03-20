# Changelog

Please update the changelog as part of any significant pull request.

## Unreleased

## v0.18.0

- Allow multiple semconv in --only flag
  ([#157](https://github.com/open-telemetry/build-tools/pull/157))
  
## v0.17.0

- Rename Optional attribute requirement level to Opt-In
  ([#135](https://github.com/open-telemetry/build-tools/pull/135))

## v0.16.0

- No changes.

## v0.15.1

- Move footnotes back together with the rendered table in Markdown
  ([#131](https://github.com/open-telemetry/build-tools/pull/131))

## v0.15.0

- Add a semantic convention type for Metrics ("metric" and "metric_group") 
  ([#79](https://github.com/open-telemetry/build-tools/pull/79))
- Add a semantic convention type for generic attribute group ("attribute_group")
  ([#124](https://github.com/open-telemetry/build-tools/pull/124)).

## v0.14.0

- Add a semantic convention type for Instrumentation Scope ("scope")
  ([#114](https://github.com/open-telemetry/build-tools/pull/114)).

## v0.13.0

- Allow customising whitespace control in Jinja templates
  ([#101](https://github.com/open-telemetry/build-tools/pull/101)).
- Clarify warning about convention group type & fix line number
  ([#109](https://github.com/open-telemetry/build-tools/pull/109)).

## v0.12.1

- Apply requirement level and msg of referenced attribute by default ([#102](https://github.com/open-telemetry/build-tools/pull/102)).

## v0.12.0

- **BREAKING**: Introduced attribute requirement levels ([#92](https://github.com/open-telemetry/build-tools/pull/92)):
  - Schema: Attribute property `required` is removed and replaced by `requirement_level`, supported values are changed to `required` (previously `always`), `conditionally_required` (previously `conditional`), `recommended`, and `optional`.
  - Templates: `opentelemetry.semconv.model.semantic_attribute.Required` enum is replaced by `RequirementLevel` with supported values listed above, `required_msg` is renamed to `requirement_level_msg`

## v0.8.0

- Add `name` field for events. It defaults to the `prefix`
  ([#67](https://github.com/open-telemetry/build-tools/pull/67)).
- Better explanation for sampling_relevant attributes
  ([#70](https://github.com/open-telemetry/build-tools/pull/70)).

## v0.7.0

- Support sampling_relevant attribute fields
  ([#68](https://github.com/open-telemetry/build-tools/pull/68)).

## v0.6.0

- Enforce enum member IDs follow the same rules as other IDs
  ([#64](https://github.com/open-telemetry/build-tools/pull/64)).
- Improve some enum-related error messages to point to more precise
  locations
  (also [#64](https://github.com/open-telemetry/build-tools/pull/64)).

## v0.5.0

- Add event semantic convention type & events span field
  ([#57](https://github.com/open-telemetry/build-tools/pull/57)).

## v0.4.0

- Add stability fields. (#35)
- Add Markdown render for code generation.

## v0.3.1

- Fix markdown generator for int enums. (#36)

## v0.3.0

- BREAKING CHANGE: Removed `number` and `number[]` attribute types in favor of `int`, `int[]`, `double` and `double[]`. (#30)
