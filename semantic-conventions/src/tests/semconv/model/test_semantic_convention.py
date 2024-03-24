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

import os

from opentelemetry.semconv.model.semantic_convention import (
    SpanKind,
    parse_semantic_convention_groups,
)
from opentelemetry.semconv.model.utils import ValidationContext


def test_parse_basic(open_test_file):
    with open_test_file(os.path.join("yaml", "basic_example.yml")) as yaml_file:
        conventions = parse_semantic_convention_groups(
            yaml_file, ValidationContext(open_test_file, True)
        )

    assert conventions is not None
    assert len(conventions) == 2

    first, second = conventions  # pylint:disable=unbalanced-tuple-unpacking

    assert first.semconv_id == "first_group_id"
    assert first.brief == "first description"
    assert first.note == "longer description"
    assert first.prefix == "first"
    assert first.extends == ""
    assert first.span_kind == SpanKind.SERVER

    assert second.semconv_id == "second_group_id"
    assert second.brief == "second description"
    assert second.note == "longer description"
    assert second.prefix == "second"
    assert second.span_kind == SpanKind.CLIENT
    assert second.extends == "first_group_id"
