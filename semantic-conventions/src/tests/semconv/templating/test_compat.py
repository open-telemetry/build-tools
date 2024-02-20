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

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.compat import CompatibilityChecker, Error

class TestCompatibility(unittest.TestCase):
    def testSuccess(self):
        cur = self.parse_semconv("compat/success/vnext.yaml")
        prev = self.parse_semconv("compat/success/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 0

    def testRemovedAttribute(self):
        cur = self.parse_semconv("compat/removed_attribute/vnext.yaml")
        prev = self.parse_semconv("compat/removed_attribute/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 2
        assert errors[0].signal == "attribute"
        assert errors[0].name == "first.first_attr"
        assert errors[0].message == "was removed"

        assert errors[1].signal == "attribute"
        assert errors[1].name == "first.second_attr"
        assert errors[1].message == "was removed"

    def testAttributeStableToExperimental(self):
        cur = self.parse_semconv("compat/attribute_stable_to_experimental/vnext.yaml")
        prev = self.parse_semconv("compat/attribute_stable_to_experimental/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "attribute"
        assert errors[0].name == "first.second_attr"
        assert errors[0].message == "stability changed from 'StabilityLevel.STABLE' to 'StabilityLevel.EXPERIMENTAL'"

    def testMetricStableToExperimental(self):
        cur = self.parse_semconv("compat/metric_stable_to_experimental/vnext.yaml")
        prev = self.parse_semconv("compat/metric_stable_to_experimental/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "metric"
        assert errors[0].name == "metric_one"
        assert errors[0].message == "stability changed from 'StabilityLevel.STABLE' to 'StabilityLevel.EXPERIMENTAL'"

    def testMetricInstrumentChanged(self):
        cur = self.parse_semconv("compat/metric_instrument_changed/vnext.yaml")
        prev = self.parse_semconv("compat/metric_instrument_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "metric"
        assert errors[0].name == "metric_one"
        assert errors[0].message == "instrument changed from 'counter' to 'histogram'"

    def testMetricUnitChanged(self):
        cur = self.parse_semconv("compat/metric_unit_changed/vnext.yaml")
        prev = self.parse_semconv("compat/metric_unit_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "metric"
        assert errors[0].name == "metric_one"
        assert errors[0].message == "unit changed from 'ms' to 's'"

    def testMetricAttributeAdded(self):
        cur = self.parse_semconv("compat/metric_attribute_added/vnext.yaml")
        prev = self.parse_semconv("compat/metric_attribute_added/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "metric"
        assert errors[0].name == "metric_one"
        assert errors[0].message == "attributes changed from '['first.first_attr']' to '['first.first_attr', 'first.second_attr']'"

    def testTypeChanged(self):
        cur = self.parse_semconv("compat/attribute_type_changed/vnext.yaml")
        prev = self.parse_semconv("compat/attribute_type_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "attribute"
        assert errors[0].name == "first.second_attr"
        assert errors[0].message == "type changed from 'int' to 'string'"

    def testEnumTypeChanged(self):
        cur = self.parse_semconv("compat/enum_type_changed/vnext.yaml")
        prev = self.parse_semconv("compat/enum_type_changed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 2
        assert errors[0].signal == "attribute"
        assert errors[0].name == "first.third_attr"
        assert errors[0].message == "enum type changed from 'string' to 'int'"

        assert errors[1].signal == "attribute"
        assert errors[1].name == "first.third_attr"
        assert errors[1].message == "enum member with value 'one' was removed"

    def testEnumValueRemoved(self):
        cur = self.parse_semconv("compat/enum_value_removed/vnext.yaml")
        prev = self.parse_semconv("compat/enum_value_removed/vprev.yaml")
        checker = CompatibilityChecker(cur, prev)
        errors = checker.check()
        self.print_errors(errors)
        assert len(errors) == 1
        assert errors[0].signal == "attribute"
        assert errors[0].name == "first.third_attr"
        assert errors[0].message == "enum member with value 'one' was removed"

    def parse_semconv(
        self,
        input_dir: str,
    ) -> SemanticConventionSet:

        semconv = SemanticConventionSet(debug=True)

        dirpath = Path(self.get_file_path(input_dir))
        if (dirpath.is_dir()):
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

    def print_errors(self, errors: list[Error]):
        if errors:
            for error in errors:
                print(error)

