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

import io
import os
import unittest

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.markdown import MarkdownRenderer


class TestCorrectMarkdown(unittest.TestCase):
    def testRef(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/ref/general.yaml"))
        semconv.parse(self.load_file("markdown/ref/rpc.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        md = self.load_file("markdown/ref/input/input_rpc.md")
        with open(md, "r") as markdown:
            content = markdown.read()
        renderer = MarkdownRenderer(self.load_file("markdown/ref/input"), semconv)
        output = io.StringIO()
        renderer._render_single_file(content, md, output)
        with open(self.load_file("markdown/ref/expected.md"), "r") as markdown:
            expected = markdown.read()

        assert output.getvalue() == expected

    def testInclude(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/include/faas.yaml"))
        semconv.parse(self.load_file("markdown/include/http.yaml"))
        semconv.parse(self.load_file("markdown/include/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        md = self.load_file("markdown/include/input/input_faas.md")
        with open(md, "r") as markdown:
            content = markdown.read()
        renderer = MarkdownRenderer(self.load_file("markdown/include/input"), semconv)
        output = io.StringIO()
        renderer._render_single_file(content, md, output)
        with open(self.load_file("markdown/include/expected.md"), "r") as markdown:
            expected = markdown.read()

        assert output.getvalue() == expected

    def testDeprecated(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/deprecated/http.yaml"))
        semconv.parse(self.load_file("markdown/deprecated/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/deprecated/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/deprecated/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/deprecated/",
            "markdown/deprecated/input.md",
            content,
            expected,
        )

    def testSingle(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/single/http.yaml"))
        semconv.parse(self.load_file("markdown/single/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/single/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/single/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/single/",
            "markdown/single/input.md",
            content,
            expected,
        )

    def testEmpty(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/empty/http.yaml"))
        semconv.parse(self.load_file("markdown/empty/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/empty/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/empty/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv, "markdown/empty/", "markdown/empty/input.md", content, expected
        )

    def testExampleArray(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/example_array/http.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        with open(self.load_file("markdown/example_array/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/example_array/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv, "markdown/example_array/", "markdown/example_array/input.md", content, expected
        )

    def testMultiple(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/multiple/http.yaml"))
        semconv.parse(self.load_file("markdown/multiple/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/multiple/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/multiple/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/multiple/",
            "markdown/multiple/input.md",
            content,
            expected,
        )

    def testEnumInt(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/enum_int/rpc.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        with open(self.load_file("markdown/enum_int/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/enum_int/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/enum_int/",
            "markdown/enum_int/input.md",
            content,
            expected,
        )

    def testExtendConstraint(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/extend_constraint/database.yaml"))
        semconv.parse(self.load_file("markdown/extend_constraint/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/extend_constraint/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/extend_constraint/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/extend_constraint/",
            "markdown/extend_constraint/input.md",
            content,
            expected,
        )

    def test_error_missing_end(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/missing_end_tag/http.yaml"))
        semconv.parse(self.load_file("markdown/missing_end_tag/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/missing_end_tag/input.md"), "r") as markdown:
            content = markdown.read()
        with self.assertRaises(Exception) as ex:
            renderer = MarkdownRenderer(self.load_file("markdown/missing_end_tag/"), semconv)
            renderer._render_single_file(
                content, "markdown/missing_end_tag/input.md", io.StringIO()
            )
        self.assertEqual("Missing ending <!-- endsemconv --> tag", ex.exception.args[0])

    def test_error_wrong_id(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/wrong_semconv_id/http.yaml"))
        semconv.parse(self.load_file("markdown/wrong_semconv_id/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)
        with open(self.load_file("markdown/wrong_semconv_id/input.md"), "r") as markdown:
            content = markdown.read()
        with self.assertRaises(Exception) as ex:
            renderer = MarkdownRenderer(self.load_file("markdown/wrong_semconv_id/"), semconv)
            renderer._render_single_file(
                content, "markdown/wrong_semconv_id/input.md", io.StringIO()
            )
        self.assertEqual("Semantic Convention ID db not found", ex.exception.args[0])

    def test_empty_table(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/empty_table/http.yaml"))
        semconv.parse(self.load_file("markdown/empty_table/faas.yaml"))
        semconv.parse(self.load_file("markdown/empty_table/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/empty_table/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/empty_table/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/empty_table/",
            "markdown/empty_table/input.md",
            content,
            expected,
        )

    def test_parameter_full(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_full/http.yaml"))
        semconv.parse(self.load_file("markdown/parameter_full/faas.yaml"))
        semconv.parse(self.load_file("markdown/parameter_full/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/parameter_full/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/parameter_full/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/parameter_full/",
            "markdown/parameter_full/input.md",
            content,
            expected,
        )

    def test_parameter_tag(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_tag/database.yaml"))
        semconv.parse(self.load_file("markdown/parameter_tag/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)
        with open(self.load_file("markdown/parameter_tag/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/parameter_tag/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/parameter_tag/",
            "markdown/parameter_tag/input.md",
            content,
            expected,
        )

    def test_parameter_tag_empty(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_tag_empty/database.yaml"))
        semconv.parse(self.load_file("markdown/parameter_tag_empty/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)
        with open(self.load_file("markdown/parameter_tag_empty/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/parameter_tag_empty/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/parameter_tag_empty/",
            "markdown/parameter_tag_empty/input.md",
            content,
            expected,
        )

    def test_parameter_tag_no_attr(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_tag_no_attr/database.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        with open(
            self.load_file("markdown/parameter_tag_no_attr/input.md"), "r"
        ) as markdown:
            content = markdown.read()
        with open(
            self.load_file("markdown/parameter_tag_no_attr/expected.md"), "r"
        ) as markdown:
            expected = markdown.read()
        with self.assertRaises(Exception) as ex:
            self.check_render(
                semconv,
                "markdown/parameter_tag_no_attr/",
                "markdown/parameter_tag_no_attr/input.md",
                content,
                expected,
            )
        self.assertEqual(
            "No attributes retained for 'db' filtering by 'wrong'", ex.exception.args[0]
        )

    def test_parameter_remove_constraint(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_remove_constraint/database.yaml"))
        semconv.parse(self.load_file("markdown/parameter_remove_constraint/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)
        with open(self.load_file("markdown/parameter_remove_constraint/input.md"), "r") as markdown:
            content = markdown.read()
        with open(
            self.load_file("markdown/parameter_remove_constraint/expected.md"), "r"
        ) as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/parameter_remove_constraint/",
            "markdown/parameter_remove_constraint/input.md",
            content,
            expected,
        )

    def test_parameter_empty(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_empty/http.yaml"))
        semconv.parse(self.load_file("markdown/parameter_empty/faas.yaml"))
        semconv.parse(self.load_file("markdown/parameter_empty/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/parameter_empty/input.md"), "r") as markdown:
            content = markdown.read()
        with open(self.load_file("markdown/parameter_empty/expected.md"), "r") as markdown:
            expected = markdown.read()
        self.check_render(
            semconv,
            "markdown/parameter_empty/",
            "markdown/parameter_empty/input.md",
            content,
            expected,
        )

    def test_wrong_parameter(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_wrong/http.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong/faas.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/parameter_wrong/input.md"), "r") as markdown:
            content = markdown.read()
        expected = ""
        with self.assertRaises(ValueError) as ex:
            self.check_render(
                semconv,
                "markdown/parameter_wrong/",
                "markdown/parameter_wrong/input.md",
                content,
                expected,
            )
            self.fail()
        e = ex.exception
        msg = e.args[0]
        self.assertIn("Unexpected parameter", msg)
        self.assertIn("`invalid`", msg)

    def test_wrong_syntax(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_wrong_syntax/http.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong_syntax/faas.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong_syntax/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/parameter_wrong_syntax/input.md"), "r") as markdown:
            content = markdown.read()
        expected = ""
        with self.assertRaises(ValueError) as ex:
            self.check_render(
                semconv,
                "markdown/parameter_wrong_syntax/",
                "markdown/parameter_wrong_syntax/input.md",
                content,
                expected,
            )
            self.fail()
        e = ex.exception
        msg = e.args[0]
        self.assertIn("Wrong syntax", msg)

    def test_wrong_duplicate(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("markdown/parameter_wrong_duplicate/http.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong_duplicate/faas.yaml"))
        semconv.parse(self.load_file("markdown/parameter_wrong_duplicate/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 7)
        with open(self.load_file("markdown/parameter_wrong_duplicate/input.md"), "r") as markdown:
            content = markdown.read()
        expected = ""
        with self.assertRaises(ValueError) as ex:
            self.check_render(
                semconv,
                "markdown/parameter_wrong_duplicate/",
                "markdown/parameter_wrong_duplicate/input.md",
                content,
                expected,
            )
            self.fail()
        e = ex.exception
        msg = e.args[0]
        self.assertIn("Parameter", msg)
        self.assertIn("already defined", msg)

    def test_units(self):
        semconv = SemanticConventionSet(debug=True)
        semconv.parse(self.load_file("yaml/metrics/units.yaml"))
        semconv.finish()

        assert len(semconv.models) == 1

        content = self.read_file("markdown/metrics/units_input.md")
        expected = self.read_file("markdown/metrics/units_output.md")
        self.check_render(
            semconv,
            "markdown/metrics/",
            "markdown/metrics/units_input.md",
            content,
            expected
            )

    def check_render(self, semconv, folder, file_name, content: str, expected: str):
        renderer = MarkdownRenderer(self.load_file(folder), semconv)
        output = io.StringIO()
        renderer._render_single_file(content, self.load_file(file_name), output)
        result = output.getvalue()

        assert result == expected

    _TEST_DIR = os.path.dirname(__file__)

    def read_file(self, filename):
        with open(self.load_file(filename), 'r') as test_file:
            return test_file.read()

    def load_file(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)
