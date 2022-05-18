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

from ruamel.yaml.constructor import DuplicateKeyError

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_convention import (
    SemanticConventionSet,
    parse_semantic_convention_groups,
)


class TestCorrectErrorDetection(unittest.TestCase):
    def test_invalid_keys(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/invalid.keys.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid key", msg)
        self.assertIn("not_existing", msg)
        self.assertEqual(e.line, 4)

    def test_invalid_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/invalid_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid value for semantic convention type", msg)
        self.assertEqual(e.line, 3)

    def test_resource_no_kind(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/resource_spankind.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid keys: ['span_kind']", msg)
        self.assertEqual(e.line, 4)

    def test_invalid_id(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/invalid.id.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid id", msg)
        self.assertIn("semantic convention ids must match", msg)
        self.assertEqual(e.line, 2)

    def test_missing_attr_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/missing_attr_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("missing key", msg)
        self.assertIn("type", msg)
        self.assertEqual(e.line, 7)

    def test_empty_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/empty_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("missing keys: ['type']", msg)
        self.assertEqual(e.line, 8)

    def test_missing_semconv_id(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/missing_semconv_id.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("missing key", msg)
        self.assertIn("id", msg)
        self.assertEqual(e.line, 2)

    def test_top_level_keys_constraint(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/multi_value_cnstr.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "invalid entry in constraint array - multiple top-level keys", msg
        )
        self.assertEqual(e.line, 10)

    def test_no_id_ref(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/no_attr_id_ref.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("at least one of id or ref is required", msg)
        self.assertEqual(e.line, 7)

    def test_no_override_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/ref_with_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("must not declare a type", msg)
        self.assertIn("'test'", msg)
        self.assertEqual(e.line, 8)

    def test_invalid_key_in_constraint(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_cnstr.yaml")
            self.fail()
        e = ex.exception
        msg = e.message
        self.assertIn("Invalid key", msg)
        self.assertIn("myNewCnst", msg)
        self.assertEqual(e.line, 10)

    def test_invalid_stability(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/stability/wrong_value.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("is not allowed as a stability marker", msg)
        self.assertEqual(e.line, 10)

    def test_invalid_stability_with_deprecated(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/stability/stability_deprecated.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("there is a deprecation message but the stability is set to", msg)
        self.assertEqual(e.line, 11)

    def test_invalid_semconv_stability_with_deprecated(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/stability/semconv_stability_deprecated.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "semantic convention stability set to deprecated but attribute", msg
        )
        self.assertEqual(e.line, 11)

    def test_invalid_deprecated_empty_string(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/deprecated/deprecation_empty_string.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "a string that specifies why the attribute is deprecated and/or what to use instead!",
            msg,
        )
        self.assertEqual(e.line, 10)

    def test_invalid_deprecated_boolean(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/deprecated/deprecation_boolean.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "a string that specifies why the attribute is deprecated and/or what to use instead!",
            msg,
        )
        self.assertEqual(e.line, 10)

    def test_invalid_deprecated_number(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/deprecated/deprecation_number.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "a string that specifies why the attribute is deprecated and/or what to use instead!",
            msg,
        )
        self.assertEqual(e.line, 10)

    def test_invalid_value_required(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_requirement.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("required field is not allowed", msg)
        self.assertIn("maybe", msg)
        self.assertEqual(e.line, 10)

    def test_invalid_value_sampling(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_sampling.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("sampling_relevant field is not allowed", msg)
        self.assertIn("maybe", msg)
        self.assertEqual(e.line, 11)

    def test_invalid_span_kind(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_span_kind.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid value for span_kind", msg)
        self.assertIn("ambarabacci", msg)
        self.assertEqual(e.line, 5)

    def test_empty_enum(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/empty/empty_enum.yaml")
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("enumeration without members", msg)
        self.assertEqual(e.line, 11)

    def test_empty_example_array(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/empty/empty_example_boolean_array.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("non array examples for boolean[]", msg)
        self.assertEqual(e.line, 8)

    def test_empty_example_enum_bool(self):
        self.open_yaml("yaml/errors/empty/empty_example_enum.yaml")
        self.open_yaml("yaml/errors/empty/empty_example_boolean.yaml")

    def test_empty_example_string(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/empty/empty_example_string.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("empty examples for string are not allowed", msg)
        self.assertEqual(e.line, 8)

    def test_enum_invalid_keys(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/enum/enum_with_extra_keys.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid keys", msg)
        self.assertIn("ambarabacci", msg)
        self.assertEqual(e.line, 10)

    def test_enum_member_invalid_keys(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/enum/enum_member_with_extra_keys.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid keys", msg)
        self.assertIn("type", msg)
        self.assertEqual(e.line, 13)

    def test_enum_with_double_values(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/enum/enum_with_double_values.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid value used in enum", msg)
        self.assertEqual(e.line, 11)

    def test_examples_wrong_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example.types.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected int", msg)
        self.assertIn("is was <class 'str'>", msg)
        self.assertEqual(e.line, 12)

    def test_example_wrong_double_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_double_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected double", msg)
        self.assertIn("is was <class 'int'>", msg)
        self.assertEqual(e.line, 11)

    def test_examples_bool(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_bool.yaml")
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected boolean", msg)
        self.assertIn("is was <class 'str'>", msg)
        self.assertEqual(e.line, 12)

    def test_examples_bool_array(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_bool_array.yaml")
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected boolean[]", msg)
        self.assertIn("is was <class 'int'>", msg)
        self.assertEqual(e.line, 12)

    def test_examples_wrong_type_array(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_number_array.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected int", msg)
        self.assertIn("is was <class 'str'>", msg)
        self.assertEqual(e.line, 12)

    def test_examples_wrong_type_array_single(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_number_array_single.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("non array examples", msg)
        self.assertEqual(e.line, 8)

    def test_examples_string(self):
        self.open_yaml("yaml/errors/examples/example_single_string.yaml")

    def test_examples_string_wrong_type(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_string.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected string", msg)
        self.assertIn("is was <class 'int'>", msg)
        self.assertEqual(e.line, 12)

    def test_examples_string_wrong_type_array(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_string_array.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("example with wrong type", msg)
        self.assertIn("expected string", msg)
        self.assertIn("is was <class 'int'>", msg)
        self.assertEqual(e.line, 12)

    def test_examples_wrong_type_value(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/examples/example_wrong_type.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("invalid type", msg)
        self.assertEqual(e.line, 9)

    def test_attribute_id_clash(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/id_clash/http.yaml")
            self.fail()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("is already present at line 8", msg)
        self.assertEqual(e.line, 16)

    def test_attribute_id_clash_inherited(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/errors/id_clash/httpInherited.yaml"))
        semconv.finish()
        self.assertTrue(semconv.errors)

    def test_id_clash(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/errors/id_clash/span_faas.yaml"))
        semconv.parse(self.load_file("yaml/errors/id_clash/resource_faas.yaml"))
        semconv.finish()
        self.assertTrue(semconv.errors)

    def test_fqn_clash(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/errors/id_clash/resource_faas.yaml"))
        semconv.parse(self.load_file("yaml/errors/id_clash/resource2_faas.yaml"))
        semconv.finish()
        self.assertTrue(semconv.errors)

    def test_validate_anyof_attributes(self):
        with self.assertRaises(ValidationError) as ex:
            semconv = SemanticConventionSet(debug=False)
            semconv.parse(self.load_file("yaml/errors/validate_anyof.yaml"))
            semconv.finish()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("any_of attribute", msg)
        self.assertIn("does not exists", msg)
        self.assertEqual(e.line, 15)

    def test_missing_event(self):
        with self.assertRaises(ValidationError) as ex:
            semconv = SemanticConventionSet(debug=False)
            semconv.parse(self.load_file("yaml/errors/events/missing_event.yaml"))
            semconv.finish()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("as event but the latter cannot be found!", msg)
        self.assertEqual(e.line, 2)

    def test_wrong_event_type(self):
        with self.assertRaises(ValidationError) as ex:
            semconv = SemanticConventionSet(debug=False)
            semconv.parse(self.load_file("yaml/errors/events/no_event_type.yaml"))
            semconv.finish()
        e = ex.exception
        msg = e.message.lower()
        self.assertIn(
            "as event but the latter is not a semantic convention for events", msg
        )
        self.assertEqual(e.line, 2)

    def test_nameless_event(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/events/nameless_event.yaml")
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("at least one of name or prefix", msg)
        self.assertEqual(e.line, 2)

    def test_condition_missing_conditionally_required_attribute(self):
        with self.assertRaises(ValidationError) as ex:
            self.open_yaml("yaml/errors/wrong_conditionally_required_no_condition.yaml")
        e = ex.exception
        msg = e.message.lower()
        self.assertIn("missing message for conditionally required field!", msg)
        self.assertEqual(e.line, 11)

    def test_multiple_requirement_levels(self):
        with self.assertRaises(DuplicateKeyError):
            self.open_yaml("yaml/errors/wrong_multiple_requirement_levels.yaml")

    def open_yaml(self, path):
        with open(self.load_file(path), encoding="utf-8") as file:
            return parse_semantic_convention_groups(file)

    _TEST_DIR = os.path.dirname(__file__)

    def load_file(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)
