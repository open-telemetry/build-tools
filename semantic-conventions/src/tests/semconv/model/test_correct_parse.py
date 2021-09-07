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

from opentelemetry.semconv.model.constraints import Include, AnyOf
from opentelemetry.semconv.model.semantic_attribute import (
    SemanticAttribute,
    StabilityLevel,
)
from opentelemetry.semconv.model.semantic_convention import (
    SemanticConventionSet,
    SpanSemanticConvention,
    EventSemanticConvention,
)


class TestCorrectParse(unittest.TestCase):
    def test_numeric_attributes(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/numeric_attributes.yml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)

        expected = {
            "id": "test",
            "prefix": "test",
            "extends": "",
            "n_constraints": 0,
            "attributes": ["test.one", "test.two"],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)

    def test_extends_prefix(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/extends/http.yaml"))
        semconv.parse(self.load_file("yaml/extends/child.http.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 3)

        base = list(semconv.models.values())[1]
        child = list(semconv.models.values())[2]
        self.assertEqual(base.prefix, "http")
        self.assertEqual(child.prefix, "child.http")

    def test_database(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/database.yaml"))
        self.assertEqual(len(semconv.models), 1)

        expected = {
            "id": "database",
            "prefix": "db",
            "extends": "",
            "n_constraints": 1,
            "attributes": [
                "db.type",
                "db.instance",
                "db.statement",
                "db.url",
                "db.user",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)

    def test_faas(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/faas.yaml"))
        self.assertEqual(len(semconv.models), 5)

        expected = {
            "id": "faas",
            "prefix": "faas",
            "extends": "",
            "n_constraints": 0,
            "attributes": ["faas.trigger", "faas.execution"],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "faas.datasource",
            "prefix": "faas.document",
            "extends": "faas",
            "n_constraints": 0,
            "attributes": [
                "faas.document.collection",
                "faas.document.operation",
                "faas.document.time",
                "faas.document.name",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "faas.http",
            "prefix": "",
            "extends": "faas",
            "n_constraints": 1,
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)
        expected = {
            "id": "faas.pubsub",
            "prefix": "",
            "extends": "faas",
            "n_constraints": 0,
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[3], expected)
        expected = {
            "id": "faas.timer",
            "prefix": "faas",
            "extends": "faas",
            "n_constraints": 0,
            "attributes": ["faas.time", "faas.cron"],
        }
        self.semantic_convention_check(list(semconv.models.values())[4], expected)

    def test_general(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/general.yaml"))
        self.assertEqual(len(semconv.models), 2)

        expected = {
            "id": "network",
            "prefix": "net",
            "extends": "",
            "n_constraints": 0,
            "attributes": [
                "net.transport",
                "net.peer.ip",
                "net.peer.port",
                "net.peer.name",
                "net.host.ip",
                "net.host.port",
                "net.host.name",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "identity",
            "prefix": "enduser",
            "extends": "",
            "n_constraints": 0,
            "attributes": ["enduser.id", "enduser.role", "enduser.scope"],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)

    def test_http(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/http.yaml"))
        self.assertEqual(len(semconv.models), 3)

        expected = {
            "id": "http",
            "prefix": "http",
            "extends": "",
            "n_constraints": 0,
            "attributes": [
                "http.method",
                "http.url",
                "http.target",
                "http.host",
                "http.scheme",
                "http.status_code",
                "http.status_text",
                "http.flavor",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "http.client",
            "prefix": "http",
            "extends": "http",
            "n_constraints": 1,
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "http.server",
            "prefix": "http",
            "extends": "http",
            "n_constraints": 1,
            "attributes": ["http.server_name"],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_resource(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/cloud.yaml"))
        self.assertEqual(len(semconv.models), 1)
        cloud = list(semconv.models.values())[0]
        expected = {
            "id": "cloud",
            "prefix": "cloud",
            "extends": "",
            "n_constraints": 0,
            "attributes": [
                "cloud.provider",
                "cloud.account.id",
                "cloud.region",
                "cloud.zone",
            ],
        }
        self.semantic_convention_check(cloud, expected)

    def test_event(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/event.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        event = list(semconv.models.values())[0]
        expected = {
            "id": "exception",
            "prefix": "exception",
            "extends": "",
            "n_constraints": 1,
            "attributes": [
                "exception.type",
                "exception.message",
                "exception.stacktrace",
                "exception.escaped",
            ],
        }
        self.semantic_convention_check(event, expected)
        constraint = event.constraints[0]
        self.assertTrue(isinstance(constraint, AnyOf))
        constraint: AnyOf
        for choice_index in range(len(constraint.choice_list_ids)):
            attr_list = constraint.choice_list_ids[choice_index]
            for attr_index in range(len(attr_list)):
                attr = attr_list[attr_index]
                self.assertEqual(
                    event.attrs_by_name.get(attr),
                    constraint.choice_list_attributes[choice_index][attr_index],
                )

    def test_span_with_event(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/event.yaml"))
        semconv.parse(self.load_file("yaml/span_event.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 3)
        semconvs = list(semconv.models.values())
        self.assertTrue(isinstance(semconvs[0], EventSemanticConvention))
        self.assertTrue(isinstance(semconvs[1], SpanSemanticConvention))
        self.assertTrue(isinstance(semconvs[2], EventSemanticConvention))
        event_semconv = semconvs[1]
        self.assertEqual(2, len(event_semconv.events))
        self.assertTrue(isinstance(event_semconv.events[0], EventSemanticConvention))
        self.assertTrue(isinstance(event_semconv.events[1], EventSemanticConvention))
        self.assertEqual("exception", event_semconv.events[0].semconv_id)
        self.assertEqual("random.event", event_semconv.events[1].semconv_id)

    def test_rpc(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/rpc.yaml"))
        self.assertEqual(len(semconv.models), 3)

        expected = {
            "id": "rpc",
            "prefix": "rpc",
            "extends": "",
            "n_constraints": 1,
            "attributes": ["rpc.service"],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "grpc.client",
            "prefix": "",
            "extends": "rpc",
            "n_constraints": 0,
            "attributes": ["net.peer.port"],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "grpc.server",
            "prefix": "",
            "extends": "rpc",
            "n_constraints": 0,
            "attributes": ["net.peer.port"],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_markdown_link(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/links.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        s = list(semconv.models.values())[0]
        for attr in s.attributes:
            brief = attr.brief
            self.assertEqual(brief.raw_text, brief.__str__())

    # This fails until ONE-36916 is not addressed
    def test_ref(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/rpc.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)

        client = list(semconv.models.values())[1]
        server = list(semconv.models.values())[2]
        attr: SemanticAttribute
        self.assertIsNotNone(client.attributes[1].ref)
        self.assertIsNotNone(client.attributes[1].attr_type)

        self.assertIsNotNone(server.attributes[1].ref)
        self.assertIsNotNone(server.attributes[1].attr_type)

    def test_extends(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/http.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)

        expected = {
            "id": "http",
            "prefix": "http",
            "extends": "",
            "n_constraints": 0,
            "attributes": [
                "http.method",
                "http.url",
                "http.target",
                "http.host",
                "http.scheme",
                "http.status_code",
                "http.status_text",
                "http.flavor",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "http.client",
            "prefix": "http",
            "extends": "http",
            "n_constraints": 1,
            "attributes": [
                "http.method",
                "http.url",
                "http.target",
                "http.host",
                "http.scheme",
                "http.status_code",
                "http.status_text",
                "http.flavor",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "http.server",
            "prefix": "http",
            "extends": "http",
            "n_constraints": 1,
            "attributes": [
                "http.method",
                "http.url",
                "http.target",
                "http.host",
                "http.scheme",
                "http.status_code",
                "http.status_text",
                "http.flavor",
                "http.user_agent",
                "http.server_name",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_include(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/http.yaml"))
        semconv.parse(self.load_file("yaml/faas.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 10)

        faas_http = [s for s in semconv.models.values() if s.semconv_id == "faas.http"][
            0
        ]
        expected = {
            "id": "faas.http",
            "prefix": "faas",
            "extends": "faas",
            "n_constraints": 2,
            "attributes": [
                # Parent
                "faas.trigger",
                "faas.execution",
                # Include
                "http.method",
                "http.url",
                "http.target",
                "http.host",
                "http.scheme",
                "http.status_code",
                "http.status_text",
                "http.flavor",
                "http.user_agent",
                "http.server_name",
            ],
        }
        self.semantic_convention_check(faas_http, expected)

    def test_deprecation(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/deprecated/http.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)

        self.assertIsNotNone(list(semconv.models.values())[0].attributes[0].deprecated)
        self.assertEqual(
            list(semconv.models.values())[0].attributes[0].deprecated,
            "Use attribute `nonDepecrated`.",
        )
        self.assertIsNone(list(semconv.models.values())[0].attributes[3].deprecated)

    def test_stability(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/stability.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)

        model = list(semconv.models.values())[0]
        self.assertEqual(len(model.attributes), 4)
        self.assertEqual(model.stability, None)

        attr = model.attributes[0]
        self.assertEqual(attr.attr_id, "exp_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes[1]
        self.assertEqual(attr.attr_id, "stable_attr")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)

        attr = model.attributes[2]
        self.assertEqual(attr.attr_id, "deprecated_attr")
        self.assertEqual(attr.stability, StabilityLevel.DEPRECATED)

        attr = model.attributes[3]
        self.assertEqual(attr.attr_id, "def_stability")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)

        model = list(semconv.models.values())[1]
        self.assertEqual(len(model.attributes), 2)
        self.assertEqual(model.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes[0]
        self.assertEqual(attr.attr_id, "test_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes[1]
        self.assertEqual(attr.attr_id, "dep")
        self.assertEqual(attr.stability, StabilityLevel.DEPRECATED)

        model = list(semconv.models.values())[2]
        self.assertEqual(len(model.attributes), 1)
        self.assertEqual(model.stability, StabilityLevel.DEPRECATED)

        attr = model.attributes[0]
        self.assertEqual(attr.attr_id, "test_attr")
        self.assertEqual(attr.stability, StabilityLevel.DEPRECATED)

    def test_populate_other_attributes(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/http.yaml"))
        semconv.parse(self.load_file("yaml/faas.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        models = sorted(semconv.models.values(), key=lambda m: m.semconv_id)
        self.assertEqual(len(models), 10)
        self.assertEqual(len(models[0].constraints), 0)
        self.assertEqual(len(models[1].constraints), 0)

        self.assertEqual(len(models[2].constraints), 2)
        self.assertTrue(isinstance(models[2].constraints[0], Include))
        self.assertEqual(len(models[2].constraints[1].choice_list_attributes), 4)

        self.assertEqual(len(models[3].constraints), 0)
        self.assertEqual(len(models[4].constraints), 0)
        self.assertEqual(len(models[5].constraints), 0)

        self.assertEqual(len(models[6].constraints), 1)
        self.assertEqual(len(models[6].constraints[0].choice_list_attributes), 4)

        self.assertEqual(len(models[7].constraints), 1)
        self.assertEqual(len(models[6].constraints[0].choice_list_attributes), 4)

        self.assertEqual(len(models[8].constraints), 0)
        self.assertEqual(len(models[9].constraints), 0)

    def test_inherited_imported(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/imported-inherited.yaml"))
        semconv.finish()
        models = sorted(semconv.models.values(), key=lambda m: m.semconv_id)
        self.assertEqual(len(models), 6)
        # HTTP
        attrs = models[0].attributes
        self.assertEqual(models[0].semconv_id, "http")
        self.assertEqual(len(attrs), 2)

        self.assertEqual(attrs[0].fqn, "http.method")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.port")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, "net.peer.port")

        # Network
        attrs = models[1].attributes
        self.assertEqual(models[1].semconv_id, "network")
        self.assertEqual(len(attrs), 3)

        self.assertEqual(attrs[0].fqn, "net.peer.ip")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.port")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, None)
        self.assertEqual(attrs[1].note, "not override")

        self.assertEqual(attrs[2].fqn, "net.peer.name")
        self.assertEqual(attrs[2].imported, False)
        self.assertEqual(attrs[2].inherited, False)
        self.assertEqual(attrs[2].ref, None)

        # Base - rpc
        attrs = models[2].attributes
        self.assertEqual(models[2].semconv_id, "rpc")
        self.assertEqual(len(attrs), 4)
        # Included attributes
        self.assertEqual(attrs[0].fqn, "net.peer.ip")
        self.assertEqual(attrs[0].imported, True)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.port")
        self.assertEqual(attrs[1].imported, True)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, None)
        self.assertEqual(attrs[1].note, "not override")

        self.assertEqual(attrs[2].fqn, "net.peer.name")
        self.assertEqual(attrs[2].imported, True)
        self.assertEqual(attrs[2].inherited, False)
        self.assertEqual(attrs[2].ref, None)
        # Defined attributes
        self.assertEqual(attrs[3].fqn, "rpc.service")
        self.assertEqual(attrs[3].imported, False)
        self.assertEqual(attrs[3].inherited, False)
        self.assertEqual(attrs[3].ref, None)

        # Extended - rpc.client
        attrs = models[3].attributes
        self.assertEqual(models[3].semconv_id, "rpc.client")
        self.assertEqual(len(attrs), 6)
        # Parent attributes
        self.assertEqual(attrs[0].fqn, "net.peer.ip")
        self.assertEqual(attrs[0].imported, True)
        self.assertEqual(attrs[0].inherited, True)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.port")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, "net.peer.port")
        self.assertEqual(attrs[1].brief, "override")
        self.assertEqual(attrs[1].note, "not override")

        self.assertEqual(attrs[2].fqn, "net.peer.name")
        self.assertEqual(attrs[2].imported, True)
        self.assertEqual(attrs[2].inherited, True)
        self.assertEqual(attrs[2].ref, None)

        self.assertEqual(attrs[3].fqn, "rpc.service")
        self.assertEqual(attrs[3].imported, False)
        self.assertEqual(attrs[3].inherited, True)
        self.assertEqual(attrs[3].ref, None)
        # Included attributes
        self.assertEqual(attrs[4].fqn, "http.method")
        self.assertEqual(attrs[4].imported, True)
        self.assertEqual(attrs[4].inherited, False)
        self.assertEqual(attrs[4].ref, None)
        # Defined attributes
        self.assertEqual(attrs[5].fqn, "rpc.client.name")
        self.assertEqual(attrs[5].imported, False)
        self.assertEqual(attrs[5].inherited, False)
        self.assertEqual(attrs[5].ref, None)

        # Include on Extended - zother
        attrs = models[4].attributes
        self.assertEqual(models[4].semconv_id, "zother")
        self.assertEqual(len(attrs), 1)
        # Defined attributes
        self.assertEqual(attrs[0].fqn, "zother.hostname")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        # Include on Extended - zz.rpc.client
        attrs = models[5].attributes
        self.assertEqual(models[5].semconv_id, "zz.rpc.client")
        self.assertEqual(len(attrs), 8)
        # Parent attributes
        self.assertEqual(attrs[0].fqn, "net.peer.ip")
        self.assertEqual(attrs[0].imported, True)
        self.assertEqual(attrs[0].inherited, True)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.port")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, True)
        self.assertEqual(attrs[1].ref, "net.peer.port")
        self.assertEqual(attrs[1].brief, "override")
        self.assertEqual(attrs[1].note, "not override")

        self.assertEqual(attrs[2].fqn, "net.peer.name")
        self.assertEqual(attrs[2].imported, True)
        self.assertEqual(attrs[2].inherited, True)
        self.assertEqual(attrs[2].ref, None)

        self.assertEqual(attrs[3].fqn, "rpc.service")
        self.assertEqual(attrs[3].imported, False)
        self.assertEqual(attrs[3].inherited, True)
        self.assertEqual(attrs[3].ref, None)

        self.assertEqual(attrs[4].fqn, "http.method")
        self.assertEqual(attrs[4].imported, True)
        self.assertEqual(attrs[4].inherited, True)
        self.assertEqual(attrs[4].ref, None)

        self.assertEqual(attrs[5].fqn, "rpc.client.name")
        self.assertEqual(attrs[5].imported, False)
        self.assertEqual(attrs[5].inherited, True)
        self.assertEqual(attrs[5].ref, None)
        # Included attributes
        self.assertEqual(attrs[6].fqn, "zother.hostname")
        self.assertEqual(attrs[6].imported, True)
        self.assertEqual(attrs[6].inherited, False)
        self.assertEqual(attrs[6].ref, None)
        # Defined attributes
        self.assertEqual(attrs[7].fqn, "rpc.client.zz.attr")
        self.assertEqual(attrs[7].imported, False)
        self.assertEqual(attrs[7].inherited, False)
        self.assertEqual(attrs[7].ref, None)

    def semantic_convention_check(self, s, expected):
        self.assertEqual(expected["prefix"], s.prefix)
        self.assertEqual(expected["extends"], s.extends)
        self.assertEqual(expected["id"], s.semconv_id)
        self.assertEqual(len(expected["attributes"]), len(s.attributes))
        self.assertEqual(expected["n_constraints"], len(s.constraints))
        self.assertEqual(expected["attributes"], [a.fqn for a in s.attributes])

    _TEST_DIR = os.path.dirname(__file__)

    def load_file(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)


if __name__ == "__main__":
    unittest.main()
