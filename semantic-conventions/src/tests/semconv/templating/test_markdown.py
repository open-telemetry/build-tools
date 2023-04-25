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
from pathlib import Path
from typing import Optional, Sequence

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.markdown import MarkdownRenderer
from opentelemetry.semconv.templating.markdown.options import MarkdownOptions


class TestCorrectMarkdown(unittest.TestCase):
    def testRef(self):
        self.check("markdown/ref/")

    def testInclude(self):
        self.check("markdown/include/")

    def testDeprecated(self):
        self.check("markdown/deprecated/")

    def testStability(self):
        self.check("markdown/stability/", expected_name="labels_expected.md")
        self.check(
            "markdown/stability/",
            MarkdownOptions(enable_stable=True, enable_frozen=True, use_badge=True),
            expected_name="badges_expected.md",
        )

    def testSingle(self):
        self.check("markdown/single/")

    def testEmpty(self):
        self.check("markdown/empty/")

    def testExampleArray(self):
        self.check("markdown/example_array/")

    def testMultiple(self):
        self.check("markdown/multiple/")

    def testMultipleEnum(self):
        self.check("markdown/multiple_enum/")

    def testEnumInt(self):
        self.check("markdown/enum_int/")

    def testExtendConstraint(self):
        self.check("markdown/extend_constraint/")

    def test_error_missing_end(self):
        ex = self.check("markdown/missing_end_tag/", assert_raises=ValueError)
        self.assertEqual("Missing ending <!-- endsemconv --> tag", ex.args[0])

    def test_error_wrong_id(self):
        ex = self.check("markdown/wrong_semconv_id/", assert_raises=ValueError)
        self.assertEqual("Semantic Convention ID db not found", ex.args[0])

    def test_empty_table(self):
        self.check("markdown/empty_table/")

    def test_parameter_full(self):
        self.check("markdown/parameter_full/")

    def test_parameter_tag(self):
        self.check("markdown/parameter_tag/")

    def test_parameter_tag_empty(self):
        self.check("markdown/parameter_tag_empty/")

    def test_parameter_tag_no_attr(self):
        ex = self.check("markdown/parameter_tag_no_attr/", assert_raises=ValueError)
        self.assertEqual(
            "No attributes retained for 'db' filtering by 'wrong'", ex.args[0]
        )

    def test_parameter_remove_constraint(self):
        self.check("markdown/parameter_remove_constraint/")

    def test_parameter_empty(self):
        self.check("markdown/parameter_empty/")

    def test_wrong_parameter(self):
        ex = self.check("markdown/parameter_wrong/", assert_raises=ValueError)
        msg = ex.args[0]
        self.assertIn("Unexpected parameter", msg)
        self.assertIn("`invalid`", msg)

    def test_wrong_syntax(self):
        ex = self.check("markdown/parameter_wrong_syntax/", assert_raises=ValueError)
        msg = ex.args[0]
        self.assertIn("Wrong syntax", msg)

    def test_wrong_duplicate(self):
        ex = self.check("markdown/parameter_wrong_duplicate/", assert_raises=ValueError)
        msg = ex.args[0]
        self.assertIn("Parameter", msg)
        self.assertIn("already defined", msg)

    def test_units(self):
        self.check("markdown/metrics_unit/", extra_yaml_dirs=["yaml/metrics/"])

    def test_event(self):
        self.check("markdown/event/")

    def test_event_noprefix(self):
        self.check("markdown/event_noprefix/")

    def test_event_renamed(self):
        self.check("markdown/event_renamed/")

    def test_metric_tables(self):
        self.check(
            "markdown/metrics_tables",
            extra_yaml_files=[
                "yaml/general.yaml",
                "yaml/http.yaml",
                "yaml/metrics.yaml",
            ],
        )

    def testSamplingRelevant(self):
        self.check("markdown/sampling_relevant/")

    def test_scope(self):
        self.check("markdown/scope/")

    def test_attribute_group(self):
        self.check("markdown/attribute_group/")

    def check(
        self,
        input_dir: str,
        options=MarkdownOptions(),
        *,
        expected_name="expected.md",
        extra_yaml_dirs: Sequence[str] = (),
        extra_yaml_files: Sequence[str] = (),
        assert_raises=None
    ) -> Optional[BaseException]:
        dirpath = Path(self.get_file_path(input_dir))
        if not dirpath.is_dir():
            raise ValueError(
                "Input dir does not exist (or is not a dir): " + str(dirpath)
            )
        semconv = SemanticConventionSet(debug=True)
        for fname in dirpath.glob("*.yaml"):
            print("Parsing", fname)
            semconv.parse(fname)
        for extra_dir in extra_yaml_dirs:
            for fname in Path(self.get_file_path(extra_dir)).glob("*.yaml"):
                print("Parsing", fname)
                semconv.parse(fname)
        for fname in map(self.get_file_path, extra_yaml_files):
            print("Parsing ", fname)
            semconv.parse(fname)

        semconv.finish()

        inputpath = dirpath / "input.md"

        output = io.StringIO()

        def do_render():
            renderer = MarkdownRenderer(str(dirpath), semconv, options)
            renderer._render_single_file(
                inputpath.read_text(encoding="utf-8"), str(inputpath), output
            )

        if assert_raises:
            with self.assertRaises(assert_raises) as ex:
                do_render()
            return ex.exception
        do_render()
        result = output.getvalue()
        assert result == (dirpath / expected_name).read_text(encoding="utf-8")
        return None

    _TEST_DIR = os.path.dirname(__file__)

    def get_file_path(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)
