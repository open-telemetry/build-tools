# Contributing

Read OpenTelemetry project [contributing
guide](https://github.com/open-telemetry/community/blob/master/CONTRIBUTING.md)
for general information about the project.

## Prerequisites

- Docker

## Creating a new PR

If there is a `CHANGELOG.md` file in the component you are updating,
please make sure to add an entry for your change in the "Unreleased" section.

## Release instructions for maintainers

1. Add new desired version number in all `CHANGELOG.md` files (instead of "Unreleased") and ensure no (relevant) entries are missing
   - This currently only applies to [semantic-conventions/CHANGELOG.md](./semantic-conventions/CHANGELOG.md)
2. Create the release at <https://github.com/open-telemetry/build-tools/releases/new>
   1. Tag: `v0.xx.y`
   2. Title: `Release version 0.xx.y`
   3. Click on _Generate release notes_
   4. Structure release notes with the headings used in former release notes (since one release applies to multiple distinct components)
   5. Verify that the release looks like expected and hit _Publish release_
3. Verify the release
   - Ensure all workflows in <https://github.com/open-telemetry/build-tools/actions> succeeded (branch = the new version tag)
   - Ensure all images were pushed to <https://hub.docker.com/u/otel> as expected. Currently these are:
     - <https://hub.docker.com/r/otel/semconvgen/tags>
     - <https://hub.docker.com/r/otel/build-tool-schemas/tags>
     - <https://hub.docker.com/r/otel/build-protobuf/tags>
     - <https://hub.docker.com/r/otel/cpp_format_tools/tags>
4. Update the respective version references in the <https://github.com/open-telemetry/opentelemetry-specification> repository, if needed
