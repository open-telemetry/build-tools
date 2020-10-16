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

from opentelemetry.semconv.templating.markdown import MarkdownRenderer
from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet

import shutil

_EXPECTED = """# Heading

<!-- semconv first_group_id -->
| Attribute  | Type | Description  | Example  | Required |
|---|---|---|---|---|
| `first.attr_one` | boolean | short description |  | No |
<!-- endsemconv -->

## Subheading

<!-- semconv second_group_id -->
| Attribute  | Type | Description  | Example  | Required |
|---|---|---|---|---|
| `second.attr_two` | string | short description | `example_one`<br>`example_two` | No |
<!-- endsemconv -->"""


# def test_markdown_renderer_to_markdown_attr(tmp_path_factory, test_file_path):
#     tmp_dir = tmp_path_factory.mktemp('markdown')
#     markdown_path = shutil.copy(test_file_path('basic_example.md'), tmp_dir)
#
#     semantic_conventions = SemanticConventionSet(debug = True)
#     semantic_conventions.parse(test_file_path('basic_example.yml'))
#
#     renderer = MarkdownRenderer(tmp_dir, semantic_conventions)
#     renderer.render_md()
#
#     result = open(markdown_path).read()
#     assert result == _EXPECTED
