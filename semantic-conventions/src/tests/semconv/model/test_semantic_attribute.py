#   Copyright The OpenTelemetry Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from opentelemetry.semconv.model.semantic_attribute import SemanticAttribute


def test_parse(load_yaml):
    yaml = load_yaml("semantic_attributes.yml")
    attributes = SemanticAttribute.parse("prefix", "", yaml.get("attributes"))

    assert len(attributes) == 3

    expected_keys = sorted(
        ["prefix.attribute_one", "prefix.attribute_two", "prefix.attribute_three",]
    )
    actual_keys = sorted(list(attributes.keys()))

    assert actual_keys == expected_keys

    first_attribute = attributes["prefix.attribute_one"]
    assert first_attribute.attr_id == "attribute_one"
    assert first_attribute.tag == "tag-one"
    assert first_attribute.ref is None
    assert first_attribute.attr_type == "string"
    assert first_attribute.brief == "this is the description of the first attribute"
    assert first_attribute.examples == ["This is a good example of the first attribute"]


def test_parse_deprecated(load_yaml):
    yaml = load_yaml("semantic_attributes_deprecated.yml")
    attributes = SemanticAttribute.parse("", "", yaml.get("attributes"))

    assert len(attributes) == 1
    assert list(attributes.keys()) == [".deprecated_attribute"]

    assert (
        attributes[".deprecated_attribute"].deprecated == "don't use this one anymore"
    )
