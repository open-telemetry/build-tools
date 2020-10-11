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

from opentelemetry.semconv.model.semantic_convention import SemanticConvention, SpanKind


def test_parse_basic(open_test_file):
    with open_test_file("basic_example.yml") as yaml_file:
        conventions = SemanticConvention.parse(yaml_file)

    assert conventions is not None
    assert len(conventions) == 2

    first, second = conventions

    assert first.semconv_id == "first_group_id"
    assert first.brief == "first description"
    assert first.note == "longer description"
    assert first.prefix == "first"
    assert first.extends == ""
    assert first.span_kind == SpanKind.SERVER

    assert second.semconv_id == "second_group_id"
    assert second.brief == "second description"
    assert second.note == "longer description"
    assert second.prefix == ""
    assert second.span_kind == SpanKind.CLIENT
    assert second.extends == "first_group_id"
