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
This is helpful to generate constants for the semantic attributes, [example from opentelemetry-java](https://github.com/open-telemetry/semantic-conventions-java#generating-semantic-conventions).

If the parameter `--file-per-group {pattern}` is set, a single yaml model is fed into the template
and the value of `pattern` is resolved from the model and may be used in the output argument.
This way, multiple files are generated. The value of `pattern` can be one of the following:

- `semconv_id`: The id of the semantic convention.
- `prefix`: The prefix with which all attributes starts with.
- `extends`: The id of the parent semantic convention.
- `root_namespace`: The root namespace of attribute to group by.

The `--output` parameter, when `--file-per-group` is used is evaluated as a template. The following variables are provided to output:

- `prefix`: A prefix name for files, determined from the grouping. e.g. `http`, `database`, `user-agent`.
- `pascal_prefix`: A Pascal-case prefix name for files. e.g. `Http`, `Database`, `UserAgent`.
- `camel_prefix`: A camel-case prefix name for files. e.g. `http`, `database`, `userAgent`.
- `snake_prefix`: A snake-case prefix name for files. e.g. `http`, `database`, `user_agent`.

For example, you could do the following:

```bash
docker run --rm \
  -v ${SCRIPT_DIR}/opentelemetry-specification/semantic_conventions/trace:/source \
  -v ${SCRIPT_DIR}/templates:/templates \
  -v ${ROOT_DIR}/semconv/src/main/java/io/opentelemetry/semconv/trace/attributes/:/output \
  otel/semconvgen:$GENERATOR_VERSION \
  --yaml-root /source \
  code \
  --template /templates/SemanticAttributes.java.j2 \
  --file-per-group root_namespace \
  --output "/output/{{pascal_prefix}}Attributes.java" \
  ...other parameters...
```

Finally, additional value can be passed to the template in form of `key=value` pairs separated by
comma using the `--parameters [{key=value},]+` or `-D` flag.

### Customizing Jinja's Whitespace Control

The image also supports customizing
[Whitespace Control in Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control)
via the additional flag `--trim-whitespace`. Providing the flag will enable both `lstrip_blocks` and `trim_blocks`.

### Enabling/disabling support for colored diffs in error messages
The `COLORED_DIFF` environment variable is set in the `semantic-conventions` `Dockerfile`.  When this environment varibale is set, errors related to reformatting tables will show a "colored diff" using standard ANSI control characters. While this should be supported natively in any modern terminal environment, you may unset this variable if issues arise.  Doing so will enable a "fall back" of non-colored inline diffs showing what was "added" and what was "removed", followed by the exact tokens added/removed encased in single quotes.

## Version compatibility check

You can check compatibility between the local one specified with `--yaml-root` and sepcific OpenTelemetry semantic convention version using the following command:

```bash
docker run --rm otel/semconvgen --yaml-root {yaml_folder} compatibility --previous-version {semconv version}
```

The `{semconv version}` (e.g. `1.24.0`) is the previously released version of semantic conventions.

Following checks are performed

- On all attributes and metrics (experimental and stable):
  - attributes and metrics must not be removed
  - enum attribute members must not be removed

- On stable attributes and attribute templates:
  - stability must not be changed
  - the type of attribute must not be changed
  - enum attribute: type of value must not be changed

- On stable enum attribute members:
  - stability must not be changed
  - `id` and `value` must not be changed

- On stable metrics:
  - stability must not be changed
  - instrument and unit must not be changed
  - new attributes should not be added.
    This check does not take into account opt-in attributes. Adding new attributes to metric is not always breaking,
    so it's considered non-critical and it's possible to suppress it with `--ignore-warnings`


### Accessing Semantic Conventions in the template

When template is processed, it has access to a set of variables that depends on the `--file-per-group` value (or lack of it).
You can access properties of these variables and call Jinja or Python functions defined on them.

#### Single file (no `--file-per-group` pattern is provided)

Processes all parsed semantic conventions

- `semconvs` - the dictionary containing parsed `BaseSemanticConvention` instances with semconv `id` as a key
- `attributes_and_templates` - the dictionary containing all attributes (including template ones) grouped by their root namespace.
  Each element in the dictionary is a list of attributes that share the same root namespace. Attributes that don't have a namespace
  appear under `""` key. Attributes and templates are sorted by attribute name.
- `attributes` - the list of all attributes from all parsed semantic conventions. Does not include template attributes.
- `attribute_templates` - the list of all attribute templates from all parsed semantic conventions.
- `metrics` - the list of all metric semantic conventions sorted by metric name.

#### The `root_namespace` pattern

Processes a single namespace and is called for each namespace detected.

- `attributes_and_templates` - the list containing all attributes (including template ones) in the given root namespace.
- `root_namespace` - the root namespace being processed.

#### Other patterns

Processes a single pattern value and is called for each distinct value.

- `semconv` - the instance of parsed `BaseSemanticConvention` being processed.

### Filtering and mapping

Jinja templates has a notion of [filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-filters) allowing to transform objects or filter lists.

Semconvgen supports following additional filters to simplify common operations in templates.

#### `SemanticAttribute` operations

1. `is_definition` - Checks if the attribute is the original definition of the attribute and not a reference.
2. `is_deprecated` - Checks if the attribute is deprecated. The same check can also be done with `(attribute.stability | string())  == "StabilityLevel.DEPRECATED"`
3. `is_experimental` - Checks if the attribute is experimental. The same check can also be done with `(attribute.stability | string())  == "StabilityLevel.EXPERIMENTAL"`
4. `is_stable` - Checks if the attribute is experimental. The same check can also be done with `(attribute.stability | string())  == "StabilityLevel.STABLE"`
5. `is_template` - Checks if the attribute is a template attribute.

#### String operations

1. `first_up` - Upper-cases the first character in the string. Does not modify anything else
2. `regex_replace(text, pattern, replace)` - Makes regex-based replace in `text` string using `pattern``
3. `to_camelcase` - Converts a string to camel case (using `.` and `_` as words delimiter in the original string).
   The first character of every word is upper-cased, other characters are lower-cased. E.g. `foo.bAR_baz` becomes `fooBarBaz`
4. `to_const_name` - Converts a string to Python or Java constant name (SNAKE_CASE) replacing `.` or `-` with `_`. E.g.
   `foo.bAR-baz` becomes `FOO_BAR_BAZ`.
5. `to_doc_brief` - Trims whitespace and removes dot at the end. E.g. ` Hello world.\t` becomes `Hello world`

#### `BaseSemanticConvention` operations

1. `is_metric` - Checks if semantic convention describes a metric.
