import os

from opentelemetry.semconv.model.semantic_convention import (
    UnitSemanticConvention,
    parse_semantic_convention_groups,
)


def test_build_units(open_test_file):
    with open_test_file(os.path.join("yaml", "metrics", "units.yaml")) as yaml_file:
        conventions = parse_semantic_convention_groups(yaml_file)

    assert len(conventions) == 1
    convention = conventions[0]

    assert isinstance(convention, UnitSemanticConvention)
    assert convention.id == "units"
    assert convention.brief == "Specification of commonly used units."

    assert len(convention.members) == 3
    assert sorted(convention.members) == sorted(
        ["percent", "nanosecond", "connections"]
    )

    assert convention.members["percent"].id == "percent"
    assert convention.members["percent"].brief == "fraction of a total"
    assert convention.members["percent"].value == "%"

    assert convention.members["nanosecond"].id == "nanosecond"
    assert convention.members["nanosecond"].brief == "time"
    assert convention.members["nanosecond"].value == "NS"

    assert convention.members["connections"].id == "connections"
    assert convention.members["connections"].brief == "connections"
    assert convention.members["connections"].value == "{connections}"
