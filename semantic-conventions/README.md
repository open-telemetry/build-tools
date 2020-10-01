# Semantic Convention generator + Docker

A docker image to process Semantic Convention YAML models.

## Usage

The image can be used to generate Markdown tables or code.

```bash
docker run --rm -v<yaml-path>:<some-path> -v<output-path>:<some-path> otel/semconvgen [OPTION]
```

For help try:

```bash
docker run --rm otel/semconvgen -h
```

## Markdown Tables

Tables can be generated using the command:

```bash
docker run --rm otel/semconvgen --yaml-root {yaml_folder} markdown --markdown-root {markdown_folder}
```

Where `{yaml_folder}` is the absolute path to the directory containing the yaml files and
`{markdown_folder}` the absolute path to the directory containing the markdown definitions
(`specification` for [opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification/tree/master/)).

The tool will automatically replace the tables with the up to date definition of the semantic conventions.
To do so, the tool looks for special tags in the markdown.

```
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

## Code Generator

The image supports [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templates to generate code from the models.

For example, the following template is used by the [opentelemetry-java-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/master/instrumentation-api/src/main/java/io/opentelemetry/instrumentation/api/typedspan)
to generate Java classes. [Template Link.](https://gist.github.com/thisthat/7e34742f4a7f1b5df57118f859a19c3b)

The image can generate code with the following command:

```bash
docker run --rm otel/semconvgen --yaml-root {yaml_folder} code --template {jinja-file} --output {output-file}
```

By default, all models are fed into the specified template at once, i.e. only a single file is generated.
This is helpful to generate constants for the semantic attributes, [example from opentelemetry-java](https://github.com/open-telemetry/opentelemetry-java/blob/master/api/src/main/java/io/opentelemetry/trace/attributes/SemanticAttributes.java).

If the parameter `--file-per-group {pattern}` is set, a single yaml model is fed into the template
and the value of `pattern` is resolved from the model and attached as prefix to the output argument.
This way, multiple files are generated. The value of `pattern` can be one of the following:

- `semconv_id`: The id of the semantic convention.
- `prefix`: The prefix with which all attributes starts with.
- `extends`: The id of the parent semantic convention.

Finally, additional value can be passed to the template in form of `key=value` pairs separated by
comma using the `--parameters [{key=value},]+` flag.

For example, to generate the typed spans used by the [opentelemetry-java-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/master/instrumentation-api/src/main/java/io/opentelemetry/instrumentation/api/typedspan), the following command can be used:

```bash
docker run --rm otel/semconvgen --yaml-root ${yamls} code --template typed_span_class.java.j2 --file-per-group semconv_id -o ${output}/Span.java
```
