import os

import pytest

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_convention import (
    UnitSemanticConvention,
    parse_semantic_convention_groups,
)
from opentelemetry.semconv.model.utils import ValidationContext


def test_build_units(open_test_file):
    with open_test_file(os.path.join("yaml", "metrics", "units.yaml")) as yaml_file:
        conventions = parse_semantic_convention_groups(
            yaml_file, ValidationContext(open_test_file, True)
        )

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


def test_build_units_bad(open_test_file):
    with pytest.raises(ValidationError) as excinfo, open_test_file(
        os.path.join("yaml", "metrics", "units_bad_with_attributes.yaml")
    ) as yaml_file:
        parse_semantic_convention_groups(
            yaml_file, ValidationContext(open_test_file, True)
        )
    assert "attributes" in str(excinfo.value)
