# Semantic Convention generator + Docker

A docker image to process Semantic Convention YAML models.

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for information on making changes to this repository.

## Usage

The image can be used to generate Markdown tables or code.

```bash
docker run --rm -v<yaml-path>:<some-path> -v<output-path>:<some-path> otel/semconvgen [OPTION]
```

For help try:

```bash
docker run --rm otel/semconvgen -h
```

## Model definition language (YAML input)

The expected YAML input file format is documented in [syntax.md](./syntax.md).

There is also a JSON schema definition available for the YAML files, which can
be used e.g. in VS code to get validation and auto-completion: [semconv.schema.json](./semconv.schema.json).
For example, with the `redhat.vscode-yaml` plugin, use the following snippet in your VS Code `settings.json` to apply it
to the test YAML files:

```json
{
    "yaml.schemas": {
        "./semantic-conventions/semconv.schema.json": [
            "semantic-conventions/src/tests/**/*.yaml"
        ]
    }
}
```

## Markdown Tables

Tables can be generated using the command:

```bash
docker run --rm otel/semconvgen --yaml-root {yaml_folder} markdown --markdown-root {markdown_folder}
```

Where `{yaml_folder}` is the absolute path to the directory containing the yaml files and
`{markdown_folder}` the absolute path to the directory containing the markdown definitions
(`specification` for [opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification/tree/main/)).

The tool will automatically replace the tables with the up to date definition of the semantic conventions.
To do so, the tool looks for special tags in the markdown.

```markdown
<!-- semconv {semantic_convention_id} -->
<!-- endsemconv -->
```

Everything between these two tags will be replaced with the table definition.
The `{semantic_convention_id}` MUST be the `id` field in the yaml files of the semantic convention
for which we want to generate the table.
After `{semantic_convention_id}`, optional parameters enclosed in parentheses can be added to customize the output:

- `tag={tag}`: prints only the attributes that have `{tag}` as a tag;
- `full`: prints attributes and constraints inherited from the parent semantic conventions or from included ones;
- `ref`: prints attributes that are referenced from another semantic convention;
- `remove_constraint`: does not print additional constraints of the semantic convention.

### Examples

These examples assume that a semantic convention with the id `http.server` extends another semantic convention with the id `http`.

`<!-- semconv http.server -->` will print only the attributes and constraints of the `http.server` semantic
convention.

`<!-- semconv http.server(full) -->` will print the attributes and constraints of the `http` semantic
convention and also the attributes and constraints of the `http.server` semantic convention.

`<!-- semconv http.server() -->` is equivalent to `<!-- semconv http.server -->`.

`<!-- semconv http.server(tag=network) -->` will print the constraints and attributes of the `http.server` semantic
convention that have the tag `network`.

`<!-- semconv http.server(tag=network, full) -->` will print the constraints and attributes of both `http` and `http.server`
semantic conventions that have the tag `network`.

`<!-- semconv metric.http.server.active_requests(metric_table) -->` will print a table describing a single metric 
`http.server.active_requests`. 

## Code Generator

The image supports [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templates to generate code from the models.

For example, opentelemetry-java generates typed constants for semantic conventions. Refer to https://github.com/open-telemetry/semantic-conventions-java for all semantic conventions.

The commands used to generate that are
[here in the semantic-conventions-java repo](https://github.com/open-telemetry/semantic-conventions-java/blob/2be178a7fd62d1073fa9b4f0f0520772a6496e0b/build.gradle.kts#L96-L141)

By default, all models are fed into the specified template at once, i.e. only a single file is generated.
This is helpful to generate constants for the semantic attributes, [example from opentelemetry-java](https://github.com/open-telemetry/opentelemetry-java/tree/main/buildscripts/semantic-convention).

If the parameter `--file-per-group {pattern}` is set, a single yaml model is fed into the template
and the value of `pattern` is resolved from the model and attached as prefix to the output argument.
This way, multiple files are generated. The value of `pattern` can be one of the following:

- `semconv_id`: The id of the semantic convention.
- `prefix`: The prefix with which all attributes starts with.
- `extends`: The id of the parent semantic convention.

Finally, additional value can be passed to the template in form of `key=value` pairs separated by
comma using the `--parameters [{key=value},]+` or `-D` flag.

### Customizing Jinja's Whitespace Control

The image also supports customising
[Whitespace Control in Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control)
via the additional flag `--trim-whitespace`. Providing the flag will enable both `lstrip_blocks` and `trim_blocks`.
