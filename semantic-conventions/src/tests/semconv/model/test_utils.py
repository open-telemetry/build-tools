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
import pytest

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.utils import validate_id, validate_values

_POSITION = [10, 2]


@pytest.mark.parametrize(
    "semconv_id",
    [
        "abc.def",  # all lowercase letters
        "abc.de_fg",  # lowercase letters, plus underscore
        "abc.de-fg",  # lowercase letters, plus dash
        "abc.def.ghi.jkl.mno"
        "abc.de0.fg9",  # lots of nested groups  # including numbers
        "abc.123.ab9.de_fg.hi-jk",
    ],
)
def test_validate_id__valid(semconv_id):
    # valid ids are namespaced, dot separated. The topmost name must start with
    # a lowercase letter. The rest of the id may contain only lowercase letters,
    # numbers, underscores, and dashes

    validate_id(semconv_id, _POSITION)


@pytest.mark.parametrize(
    "semconv_id", ["123", "ABC", "abc+def", "ab<", "ab^", "abc.de\xfe"]
)
def test_validate_id__invalid(semconv_id):
    with pytest.raises(ValidationError) as err:
        validate_id(semconv_id, _POSITION)

    assert err.value.message.startswith("Invalid id")


@pytest.mark.parametrize(
    "allowed, mandatory",
    [
        [["id", "brief", "note", "prefix", "span_kind", "attributes"], []],
        [["id", "brief", "note", "prefix", "span_kind", "attributes"], ["id"]],
        [
            ["id", "brief", "note", "prefix", "span_kind", "attributes"],
            ["id", "brief", "note", "prefix", "span_kind", "attributes"],
        ],
    ],
)
def test_validate_values(load_yaml, allowed, mandatory):
    conventions = load_yaml("basic_example.yml")
    yaml = conventions["groups"][0]

    validate_values(yaml, allowed, mandatory)


@pytest.mark.parametrize(
    "allowed, mandatory, expected_message",
    [
        [
            [],
            [],
            "Invalid keys: ['id', 'brief', 'note', 'prefix', 'span_kind', 'attributes']",
        ],
        [
            ["id", "brief", "note", "prefix", "span_kind"],
            [],
            "Invalid keys: ['attributes']",
        ],
        [
            ["id", "brief", "note", "prefix", "span_kind"],
            [],
            "Invalid keys: ['attributes']",
        ],
        [
            ["id", "brief", "note", "prefix", "span_kind", "attributes"],
            ["another_key"],
            "Missing keys: ['another_key']",
        ],
    ],
)
def test_validate_values__invalid(load_yaml, allowed, mandatory, expected_message):
    conventions = load_yaml("basic_example.yml")
    yaml = conventions["groups"][0]

    with pytest.raises(ValidationError) as err:
        validate_values(yaml, allowed, mandatory)

    assert err.value.message == expected_message
