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
from unittest.mock import patch

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.markdown import MarkdownRenderer, VisualDiffer
from opentelemetry.semconv.templating.markdown.options import MarkdownOptions


class TestCorrectMarkdown(unittest.TestCase):
    def testRef(self):
        self.check("markdown/ref/")

    def testRefExtends(self):
        self.check("markdown/ref_extends/")

    def testRefEmbed(self):
        self.check("markdown/ref_embed/")

    def testDeprecated(self):
        self.check("markdown/deprecated/")

    def testStableBadges(self):
        self.check(
            "markdown/stability/",
            MarkdownOptions(
                disable_deprecated_badge=True, disable_experimental_badge=True
            ),
            expected_name="stable_badges_expected.md",
        )

    def testExperimentalAndStableBadges(self):
        self.check(
            "markdown/stability/",
            MarkdownOptions(),
            expected_name="all_badges_expected.md",
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

    def test_extend_grandparent(self):
        self.check("markdown/extend_grandparent/")

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

    def test_omit_requirement_level(self):
        self.check("markdown/omit_requirement_level/")

    def testSamplingRelevant(self):
        self.check("markdown/sampling_relevant/")

    def test_attribute_group(self):
        self.check("markdown/attribute_group/")

    def test_attribute_templates(self):
        self.check("markdown/attribute_templates/")

    def test_sorting(self):
        self.check("markdown/sorting/")

    def testVisualDiffer(self):
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-1.md"),
            encoding="utf8",
        ) as fin:
            sample_1 = fin.read()
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-2.md"),
            encoding="utf8",
        ) as fin:
            sample_2 = fin.read()
        with open(
            self.get_file_path(
                "markdown/table_generation_conflict/expected-no-colors.md"
            ),
            encoding="utf8",
        ) as fin:
            expected = fin.read()
        actual = VisualDiffer.visual_diff(sample_1, sample_2)
        with open(
            self.get_file_path(
                "markdown/table_generation_conflict/expected-no-colors.md"
            ),
            "w+",
            encoding="utf8",
        ) as out:
            out.writelines(actual)
        self.assertEqual(expected, actual)

    @patch.dict(os.environ, {"COLORED_DIFF": "false"})
    def testVisualDifferExplicitNoColors(self):
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-1.md"),
            encoding="utf8",
        ) as fin:
            sample_1 = fin.read()
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-2.md"),
            encoding="utf8",
        ) as fin:
            sample_2 = fin.read()
        with open(
            self.get_file_path(
                "markdown/table_generation_conflict/expected-no-colors.md"
            ),
            encoding="utf8",
        ) as fin:
            expected = fin.read()
        actual = VisualDiffer.visual_diff(sample_1, sample_2)
        self.assertEqual(expected, actual)

    @patch.dict(os.environ, {"COLORED_DIFF": "true"})
    def testColoredVisualDiffer(self):
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-1.md"),
            encoding="utf8",
        ) as fin:
            sample_1 = fin.read()
        with open(
            self.get_file_path("markdown/table_generation_conflict/input-2.md"),
            encoding="utf8",
        ) as fin:
            sample_2 = fin.read()
        with open(
            self.get_file_path(
                "markdown/table_generation_conflict/expected-with-colors.md",
            ),
            encoding="utf8",
        ) as fin:
            expected = fin.read()
        actual = VisualDiffer.visual_diff(sample_1, sample_2)
        self.assertEqual(expected, actual)

    def check(
        self,
        input_dir: str,
        options=MarkdownOptions(
            disable_experimental_badge=True,
            disable_deprecated_badge=True,
            disable_stable_badge=True,
        ),
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
        print(result)
        assert result == (dirpath / expected_name).read_text(encoding="utf-8")
        return None

    _TEST_DIR = os.path.dirname(__file__)

    def get_file_path(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)
