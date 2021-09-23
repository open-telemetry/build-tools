# Changelog

Please update the changelog as part of any significant pull request.

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
