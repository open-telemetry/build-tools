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
import unittest
from pathlib import Path

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.compatibility import CompatibilityChecker, Problem


class TestCompatibility(unittest.TestCase):
    def testSuccess(self):
        cur = self.parse_semconv("compat/success/vnext.yaml")
        prev = self.parse_semconv("compat/success/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        self.assert_errors([], problems)

    def testRemovedAttribute(self):
        cur = self.parse_semconv("compat/removed_attribute/vnext.yaml")
        prev = self.parse_semconv("compat/removed_attribute/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()

        expected_errors = [
            Problem("attribute", "first.first_attr", "was removed"),
            Problem("attribute", "first.second_attr", "was removed"),
            Problem("attribute", "first.fifth_attr_template", "was removed"),
        ]
        self.assert_errors(expected_errors, problems)

    def testAttributeStableToExperimental(self):
        cur = self.parse_semconv("compat/attribute_stable_to_experimental/vnext.yaml")
        prev = self.parse_semconv("compat/attribute_stable_to_experimental/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "attribute",
                "first.second_attr",
                "stability changed from 'StabilityLevel.STABLE' to 'StabilityLevel.EXPERIMENTAL'",
            ),
            Problem(
                "attribute",
                "first.fifth_attr_template",
                "stability changed from 'StabilityLevel.STABLE' to 'StabilityLevel.EXPERIMENTAL'",
            ),
        ]
        self.assert_errors(expected_errors, problems)

    def testMetricStableToExperimental(self):
        cur = self.parse_semconv("compat/metric_stable_to_experimental/vnext.yaml")
        prev = self.parse_semconv("compat/metric_stable_to_experimental/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "metric",
                "metric_one",
                "stability changed from 'StabilityLevel.STABLE' to 'StabilityLevel.EXPERIMENTAL'",
            )
        ]
        self.assert_errors(expected_errors, problems)

    def testMetricInstrumentChanged(self):
        cur = self.parse_semconv("compat/metric_instrument_changed/vnext.yaml")
        prev = self.parse_semconv("compat/metric_instrument_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "metric",
                "metric_one",
                "instrument changed from 'counter' to 'histogram'",
            )
        ]
        self.assert_errors(expected_errors, problems)

    def testMetricUnitChanged(self):
        cur = self.parse_semconv("compat/metric_unit_changed/vnext.yaml")
        prev = self.parse_semconv("compat/metric_unit_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem("metric", "metric_one", "unit changed from 'ms' to 's'")
        ]
        self.assert_errors(expected_errors, problems)

    def testMetricAttributeAdded(self):
        cur = self.parse_semconv("compat/metric_attribute_added/vnext.yaml")
        prev = self.parse_semconv("compat/metric_attribute_added/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "metric",
                "metric_one",
                "attributes changed from '['first.first_attr']' to '['first.first_attr', 'first.second_attr']'",
                critical=False,
            )
        ]
        self.assert_errors(expected_errors, problems)

    def testTypeChanged(self):
        cur = self.parse_semconv("compat/attribute_type_changed/vnext.yaml")
        prev = self.parse_semconv("compat/attribute_type_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "attribute", "first.second_attr", "type changed from 'int' to 'string'"
            ),
            Problem(
                "attribute",
                "first.fifth_attr_template",
                "type changed from 'template[string[]]' to 'template[int[]]'",
            ),
        ]
        self.assert_errors(expected_errors, problems)

    def testEnumTypeChanged(self):
        cur = self.parse_semconv("compat/enum_type_changed/vnext.yaml")
        prev = self.parse_semconv("compat/enum_type_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "attribute",
                "first.third_attr",
                "enum type changed from 'string' to 'int'",
            ),
            Problem(
                "attribute",
                "first.third_attr",
                "enum member with value 'one' was removed",
            ),
        ]
        self.assert_errors(expected_errors, problems)

    def testEnumValueRemoved(self):
        cur = self.parse_semconv("compat/enum_value_removed/vnext.yaml")
        prev = self.parse_semconv("compat/enum_value_removed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        problems = checker.check()
        expected_errors = [
            Problem(
                "attribute",
                "first.third_attr",
                "enum member with value 'one' was removed",
            )
        ]
        self.assert_errors(expected_errors, problems)

    def parse_semconv(
        self,
        input_dir: str,
    ) -> SemanticConventionSet:

        semconv = SemanticConventionSet(debug=True)

        dirpath = Path(self.get_file_path(input_dir))
        if dirpath.is_dir():
            for fname in dirpath.glob("*.yaml"):
                print("Parsing", fname)
                semconv.parse(fname)
        else:
            semconv.parse(dirpath)

        assert not semconv.has_error()
        semconv.finish()
        return semconv

    _TEST_DIR = os.path.dirname(__file__)

    def get_file_path(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)

    def assert_errors(self, expected: list[Problem], actual: list[Problem]):
        assert len(expected) == len(actual)
        for a in actual:
            print(a)
            assert a in expected
