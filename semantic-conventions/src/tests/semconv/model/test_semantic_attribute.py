from opentelemetry.semconv.model.semantic_attribute import SemanticAttribute


def test_parse(load_yaml):
    yaml = load_yaml("semantic_attributes.yml")
    attributes = SemanticAttribute.parse("prefix", yaml.get("attributes"))

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
