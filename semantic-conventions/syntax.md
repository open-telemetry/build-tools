# Semantic Convention YAML Language

First, the syntax with a pseudo [EBNF](https://en.wikipedia.org/wiki/Extended_Backus-Naur_form) grammar is presented.
Then, the semantic of each field is described.

<!-- tocstart -->

<!-- toc -->

- [Semantic Convention YAML Language](#semantic-convention-yaml-language)
  - [JSON Schema](#json-schema)
  - [Syntax](#syntax)
  - [Semantics](#semantics)
    - [Groups](#groups)
    - [Semantic Convention](#semantic-convention)
      - [Span semantic convention](#span-semantic-convention)
      - [Event semantic convention](#event-semantic-convention)
      - [Metric Group semantic convention](#metric-group-semantic-convention)
      - [Metric semantic convention](#metric-semantic-convention)
      - [Attribute group semantic convention](#attribute-group-semantic-convention)
    - [Attributes](#attributes)
      - [Examples (for examples)](#examples-for-examples)
      - [Ref](#ref)
      - [Type](#type)

<!-- tocstop -->

## JSON Schema

A JSON schema description of the syntax is available as [semconv.schema.json](./semconv.schema.json),
see [README.md](./README.md) for how to use it with an editor. The documentation
here in `syntax.md` should be considered more authoritative though. Please keep
`semconv.schema.json` in synch when changing the "grammar" in this file!

## Syntax

All attributes are lower case.

```ebnf
groups ::= semconv
       | semconv groups

semconv ::= id [convtype] brief [note] [prefix] [extends] [stability] [deprecated] attributes [specificfields]

id    ::= string

convtype ::= "span" # Default if not specified
         |   "resource" # see spanspecificfields
         |   "event"    # see eventspecificfields
         |   "metric"   # see metricfields
         |   "attribute_group" # no specific fields defined

brief ::= string
note  ::= string

prefix ::= string

extends ::= string

stability ::= "experimental"
          |   "stable"

deprecated ::= <description>

attributes ::= (id type brief examples | ref [brief] [examples]) [tag] [stability] [deprecated] [required] [sampling_relevant] [note]

# ref MUST point to an existing attribute id
ref ::= id

type ::= simple_type
     |   template_type
     |   enum

simple_type ::= "string"
     |   "int"
     |   "double"
     |   "boolean"
     |   "string[]"
     |   "int[]"
     |   "double[]"
     |   "boolean[]"

template_type ::= "template[" simple_type "]" # As a single string

enum ::= [allow_custom_values] members

allow_custom_values := boolean

members ::= member {member}

member ::= id value [brief] [note] [stability] [deprecated]

requirement_level ::= "required"
         |   "conditionally_required" <condition>
         |   "recommended" [condition] # Default if not specified
         |   "opt_in"

sampling_relevant ::= boolean

examples ::= <example_value> {<example_value>}

any_of ::= id {id}

include ::= id

specificfields ::= spanfields
               |   eventfields
               |   metricfields

spanfields ::= [events] [span_kind]
eventfields ::= [name]

span_kind ::= "client"
          |   "server"
          |   "producer"
          |   "consumer"
          |   "internal"

events ::= id {id} # MUST point to an existing event group

name ::= string

metricfields ::= metric_name instrument unit

metric_name ::= string
instrument ::=  "counter"
            | "histogram"
            | "gauge"
            | "updowncounter"
unit ::= string
```

## Semantics

### Groups

Groups contain the list of semantic conventions and it is the root node of each yaml file.

### Semantic Convention

The field `semconv` represents a semantic convention and it is made by:

- `id`, string that uniquely identifies the semantic convention.
- `type`, optional enum, defaults to `span` (with a warning if not present).
- `brief`, string, a brief description of the semantic convention.
- `note`, optional string, a more elaborate description of the semantic convention.
   It defaults to an empty string.
- `prefix`, optional string, prefix for the attributes for this semantic convention.
   It defaults to an empty string.
- `extends`, optional string, reference another semantic convention `id`.
   It inherits the prefix, and all attributes defined in the specified semantic convention.
- `deprecated`, optional, when present marks the semantic convention as deprecated.
   The string provided as `<description>` MUST specify why it's deprecated and/or what to use instead.
- `attributes`, list of attributes that belong to the semantic convention.

#### Span semantic convention

The following is only valid if `type` is `span` (the default):

- `span_kind`, optional enum, specifies the kind of the span.
- `events`, optional list of strings that specify the ids of
  event semantic conventions associated with this span semantic convention.

#### Event semantic convention

The following is only valid if `type` is `event`:

- `name`, conditionally required string. The name of the event.
  If not specified, the `prefix` is used. If `prefix` is empty (or unspecified),
  `name` is required.

#### Metric Group semantic convention

Metric group inherits all from the base semantic convention, and does not
add any additional fields.

The metric group semconv is a group where related metric attributes
can be defined and then referenced from other `metric` groups using `ref`.

#### Metric semantic convention

The following is only valid if `type` is `metric`:

  - `metric_name`, required, the metric name as described by the [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/data-model.md#timeseries-model).
  - `instrument`, required, the [instrument type]( https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/metrics/api.md#instrument)
  that should be used to record the metric. Note that the semantic conventions must be written
  using the names of the synchronous instrument types (`counter`, `gauge`, `updowncounter` and `histogram`).
  For more details: [Metrics semantic conventions - Instrument types](https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/metrics/semantic_conventions#instrument-types).
  - `unit`, required, the unit in which the metric is measured, which should adhere to
    [the guidelines](https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/metrics/semantic_conventions#instrument-units).

#### Attribute group semantic convention

Attribute group (`attribute_group` type) defines a set of attributes that can be
declared once and referenced by semantic conventions for different signals, for example spans and logs.
Attribute groups don't have any specific fields and follow the general `semconv` semantics.

### Attributes

An attribute is defined by:

- `id`, string that uniquely identifies the attribute. Required.
- `type`, either a string literal denoting the type as a primitive or an array type, a template type or an enum definition (See later).  Required.
   The accepted string literals are:
  * _primitive and array types as string literals:_
    * `"string"`: String attributes.
    * `"int"`: Integer attributes.
    * `"double"`: Double attributes.
    * `"boolean"`: Boolean attributes.
    * `"string[]"`: Array of strings attributes.
    * `"int[]"`: Array of integer attributes.
    * `"double[]"`: Array of double attributes.
    * `"boolean[]"`: Array of booleans attributes.
  * _template type as string literal:_ `"template[<PRIMITIVE_OR_ARRAY_TYPE>]"` (See [below](#template-type))
  See the [specification of Attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md#attribute) for the definition of the value types.
- `stability`, enum - either `stable` or `experimental`, specifies the stability of the attribute. Required.
- `ref`, optional string, reference an existing attribute, see [below](#ref).
- `tag`, optional string, associates a tag ("sub-group") to the attribute.
   It carries no particular semantic meaning but can be used e.g. for filtering
   in the markdown generator.
- `requirement_level`, optional, specifies if the attribute is mandatory.
   Can be "required", "conditionally_required", "recommended" or "opt_in". When omitted, the attribute is "recommended".
   When set to "conditionally_required", the string provided as `<condition>` MUST specify
   the conditions under which the attribute is required.
- `sampling_relevant`, optional boolean,
  specifies if the attribute is (especially) relevant for sampling and
  thus should be set at span start. It defaults to `false`.
- `brief`, `note`, `deprecated`, same meaning as for the whole
  [semantic convention](#semantic-convention), but per attribute.
- `examples`, sequence of example values for the attribute or single example value.
   They are required only for string and string array attributes.
   Example values must be of the same type of the attribute.
   If only a single example is provided, it can directly be reported without encapsulating it into a sequence/dictionary. See [below](#examples-for-examples).

#### Examples (for examples)

Examples for setting the `examples` field:

A single example value for a string attribute. All the following three representations are equivalent:

```yaml
examples: 'this is a single string'
```

or

```yaml
examples: ['this is a single string']
```

or

```yaml
examples:
   - 'this is a single string'
```

Attention, the following will throw a type mismatch error because a string type as example value is expected and not an array of string:

```yaml
examples:
   - ['this is an error']

examples: [['this is an error']]
```

Multiple example values for a string attribute:

```yaml
examples: ['this is a single string', 'this is another one']
```

or

```yaml
examples:
   - 'this is a single string'
   - 'this is another one'
```

A single example value for an array of strings attribute:

```yaml
examples: ['first element of first array', 'second element of first array']
```

or

```yaml
examples:
   - ['first element of first array', 'second element of first array']
```

Attention, the following will throw a type mismatch error because an array of strings as type for the example values is expected and not a string:

```yaml
examples: 'this is an error'
```

Multiple example values for an array of string attribute:

```yaml
examples: [ ['first element of first array', 'second element of first array'], ['first element of second array', 'second element of second array'] ]
```

or

```yaml
examples:
   - ['first element of first array', 'second element of first array']
   - ['first element of second array', 'second element of second array']
```

#### Ref

`ref` MUST have an id of an existing attribute. When it is set, `id`, `type`, `stability`, and `deprecation` MUST NOT be present.
`ref` is useful for specifying that an existing attribute of another semantic convention is part of
the current semantic convention and inherit its `brief`, `note`, and `example` values. However, if these
fields are present in the current attribute definition, they override the inherited values.

#### Type

An attribute type can either be a string, int, double, boolean, array of strings, array of int, array of double,
array of booleans, a template type or an enumeration.

##### Template type

A template type attribute represents a _dictionary_ of attributes with a common attribute name prefix. The syntax for defining template type attributes is the following:

`type: template[<PRIMITIVE_OR_ARRAY_TYPE>]`

The `<PRIMITIVE_OR_ARRAY_TYPE>` is one of the above-mentioned primitive or array types (_not_ an enum) and specifies the type of the `value` in the dictionary.

The following is an example for defining a template type attribute and it's resolution:

```yaml
groups:
  - id: trace.http.common
    type: attribute_group
    brief: "..."
    attributes:
      - id: http.request.header
        type: template[string[]]
        stability: stable
        brief: >
          HTTP request headers, the key being the normalized HTTP header name (lowercase, with `-` characters replaced by `_`), the value being the header values.
        examples: ['http.request.header.content_type=["application/json"]', 'http.request.header.x_forwarded_for=["1.2.3.4", "1.2.3.5"]']
        note: |
          ...
```

In this example the definition will be resolved into a dictionary of attributes `http.request.header.<key>` where `<key>` will be replaced by the actual HTTP header name, and the value of the attributes is of type `string[]` that carries the HTTP header value.

##### Enumeration

If the type is an enumeration, additional fields are required:

- `allow_custom_values`, optional boolean, set to false to not accept values
     other than the specified members. It defaults to `true`.
- `members`, list of enum entries.

An enum entry has the following fields:

- `id`, string that uniquely identifies the enum entry.
- `value`, string, int, or boolean; value of the enum entry.
- `brief`, optional string, brief description of the enum entry value. It defaults to the value of `id`.
- `note`, optional string, longer description. It defaults to an empty string.
- `stability`, required stability level. Attributes marked as experimental cannot have stable members.
- `deprecated`, optional string, similarly to semantic convention and attribute deprecation, marks specific member as deprecated.
