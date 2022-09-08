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
    - [Attributes](#attributes)
      - [Examples (for examples)](#examples-for-examples)
      - [Ref](#ref)
      - [Type](#type)
    - [Constraints](#constraints)
      - [Any Of](#any-of)
      - [Include](#include)

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

semconv ::= id [convtype] brief [note] [prefix] [extends] [stability] [deprecated] attributes [constraints] [specificfields] [metrics]

id    ::= string

convtype ::= "span" # Default if not specified
         |   "resource" # see spanspecificfields
         |   "event"    # see eventspecificfields
         |   "metric"   # (currently non-functional)
         |   "scope"

brief ::= string
note  ::= string

prefix ::= string

extends ::= string

stability ::= "deprecated"
          |   "experimental"
          |   "stable"

deprecated ::= <description>

attributes ::= (id type brief examples | ref [brief] [examples]) [tag] [stability] [deprecated] [required] [sampling_relevant] [note]

# ref MUST point to an existing attribute id
ref ::= id

type ::= "string"
     |   "int"
     |   "double"
     |   "boolean"
     |   "string[]"
     |   "int[]"
     |   "double[]"
     |   "boolean[]"
     |   enum

enum ::= [allow_custom_values] members

allow_custom_values := boolean

members ::= member {member}

member ::= id value [brief] [note]

requirement_level ::= "required"
         |   "conditionally_required" <condition>
         |   "recommended" [condition] # Default if not specified
         |   "optional"

# EXPERIMENTAL: Using this is NOT ALLOWED in the specification currently.
sampling_relevant ::= boolean

examples ::= <example_value> {<example_value>}

constraints ::= constraint {constraint}

constraint ::= any_of
           |   include

any_of ::= id {id}

include ::= id

specificfields ::= spanfields
               |   eventfields

spanfields ::= [events] [span_kind]
eventfields ::= [name]

span_kind ::= "client"
          |   "server"
          |   "producer"
          |   "consumer"
          |   "internal"

events ::= id {id} # MUST point to an existing event group

name ::= string

instrument ::=  "Counter" 
            | "Histogram" 
            | "Gauge" 
            | "UpDownCounter" 
            
units ::= string            

metric ::= id instrument units brief

metrics ::= {metric}
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
   It inherits the prefix, constraints, and all attributes defined in the specified semantic convention.
- `stability`, optional enum, specifies the stability of the semantic convention.

   Note that, if `stability` is missing but `deprecated` is present, it will automatically set the `stability` to `deprecated`.
   If `deprecated` is present and `stability` differs from `deprecated`, this will result in an error.
- `deprecated`, optional, specifies if the semantic convention is deprecated.
   The string provided as `<description>` MUST specify why it's deprecated and/or what to use instead.
   See also `stability`.
- `attributes`, list of attributes that belong to the semantic convention.
- `constraints`, optional list, additional constraints (See later). It defaults to an empty list.

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

#### Metric semantic convention

The following is only valid if `type` is `metric`:

- `metrics`, an optional list of metrics that belong to the semantic convention.
  Each individual metric has the following semantics: 
  - `id`, the ID of the metric. The fully qualified name of the metric includes its parent 
    semantic convention prefix like so: `{parent.prefix}.{metric.id}`. 
  - `brief`, a brief description of the metric.
  - `instrument`, the [instrument type]( https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/metrics/semantic_conventions#instrument-types) 
  that *should* be used to record the metric.
  - `units`, the units in which the metric is measured, which should adhere to 
     [UCUM](https://ucum.org/ucum.html). 

### Attributes

An attribute is defined by:

- `id`, string that uniquely identifies the attribute.
- `type`, either a string literal denoting the type or an enum definition (See later).
   The accepted string literals are:

  * `"string"`: String attributes.
  * `"int"`: Integer attributes.
  * `"double"`: Double attributes.
  * `"boolean"`: Boolean attributes.
  * `"string[]"`: Array of strings attributes.
  * `"int[]"`: Array of integer attributes.
  * `"double[]"`: Array of double attributes.
  * `"boolean[]"`: Array of booleans attributes.

  See the [specification of Attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/README.md#attribute) for the definition of the value types.
- `ref`, optional string, reference an existing attribute, see [below](#ref).
- `tag`, optional string, associates a tag ("sub-group") to the attribute.
   It carries no particular semantic meaning but can be used e.g. for filtering
   in the markdown generator.
- `requirement_level`, optional, specifies if the attribute is mandatory.
   Can be "required", "conditionally_required", "recommended" or "optional". When omitted, the attribute is "recommended".
   When set to "conditionally_required", the string provided as `<condition>` MUST specify
   the conditions under which the attribute is required.
- `sampling_relevant`, optional EXPERIMENTAL boolean,
  specifies if the attribute is (especially) relevant for sampling and
  thus should be set at span start. It defaults to `false`.
- `brief`, `note`, `stability`, `deprecated`, same meaning as for the whole
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

`ref` MUST have an id of an existing attribute. When it is set, `id` and `type` MUST NOT be present.
`ref` is useful for specifying that an existing attribute of another semantic convention is part of
the current semantic convention and inherit its `brief`, `note`, and `example` values. However, if these
fields are present in the current attribute definition, they override the inherited values.

#### Type

An attribute type can either be a string, int, double, boolean, array of strings, array of int, array of double,
array of booleans, or an enumeration. If it is an enumeration, additional fields are required:

- `allow_custom_values`, optional boolean, set to false to not accept values
     other than the specified members. It defaults to `true`.
- `members`, list of enum entries.

An enum entry has the following fields:

- `id`, string that uniquely identifies the enum entry.
- `value`, string, int, or boolean; value of the enum entry.
- `brief`, optional string, brief description of the enum entry value. It defaults to the value of `id`.
- `note`, optional string, longer description. It defaults to an empty string.

### Constraints

Allow to define additional requirements on the semantic convention.
Currently, it supports `any_of` and `include`.

#### Any Of

`any_of` accepts a list of sequences. Each sequence contains a list of attribute ids that are required.
`any_of` enforces that all attributes of at least one of the sequences are set.

#### Include

`include` accepts a semantic conventions `id`. It includes as part of this semantic convention all constraints
and required attributes that are not already defined in the current semantic convention.
