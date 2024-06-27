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
from typing import List, cast

from opentelemetry.semconv.model.semantic_attribute import StabilityLevel
from opentelemetry.semconv.model.semantic_convention import (
    EventSemanticConvention,
    MetricSemanticConvention,
    SemanticConventionSet,
    SpanSemanticConvention,
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
            "attributes": [
                "db.instance",
                "db.statement",
                "db.type",
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
            "attributes": ["faas.trigger", "faas.execution"],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "faas.datasource",
            "prefix": "faas.document",
            "extends": "faas",
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
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)
        expected = {
            "id": "faas.pubsub",
            "prefix": "",
            "extends": "faas",
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[3], expected)
        expected = {
            "id": "faas.timer",
            "prefix": "faas",
            "extends": "faas",
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
            "attributes": [
                "net.host.ip",
                "net.host.name",
                "net.host.port",
                "net.peer.ip",
                "net.peer.name",
                "net.peer.port",
                "net.transport",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "identity",
            "prefix": "enduser",
            "extends": "",
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
            "attributes": [
                "http.method",
                "http.status_code",
                "http.flavor",
                "http.host",
                "http.scheme",
                "http.status_text",
                "http.target",
                "http.url",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "http.client",
            "prefix": "http",
            "extends": "http",
            "attributes": [],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "http.server",
            "prefix": "http",
            "extends": "http",
            "attributes": ["http.server_name"],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_metrics(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/metrics.yaml"))
        self.assertEqual(len(semconv.models), 3)
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.parse(self.load_file("yaml/http.yaml"))

        metric_semconvs = cast(
            List[MetricSemanticConvention], list(semconv.models.values())
        )

        expected = {
            "id": "metric.foo",
            "prefix": "bar",
            "extends": "",
            "stability": StabilityLevel.EXPERIMENTAL,
            "attributes": ["bar.egg.type"],
        }
        self.semantic_convention_check(metric_semconvs[0], expected)

        expected = {
            "id": "metric.foo.size",
            "prefix": "foo",
            "extends": "",
            "stability": StabilityLevel.STABLE,
            "metric_name": "foo.size",
            "unit": "{bars}",
            "instrument": "histogram",
            "attributes": [
                "http.method",
                "http.status_code",
            ],
        }
        self.semantic_convention_check(metric_semconvs[1], expected)
        self.assertEqual(metric_semconvs[1].unit, expected["unit"])
        self.assertEqual(metric_semconvs[1].instrument, expected["instrument"])
        self.assertEqual(metric_semconvs[1].metric_name, expected["metric_name"])

        expected = {
            "id": "metric.foo.active_eggs",
            "prefix": "foo",
            "extends": "",
            "stability": StabilityLevel.EXPERIMENTAL,
            "metric_name": "foo.active_eggs",
            "unit": "{cartons}",
            "deprecated": "Removed.",
            "instrument": "updowncounter",
            "attributes": [
                "bar.egg.type",
                "http.method",
            ],
        }
        self.semantic_convention_check(metric_semconvs[2], expected)
        self.assertEqual(metric_semconvs[2].unit, expected["unit"])
        self.assertEqual(metric_semconvs[2].instrument, expected["instrument"])
        self.assertEqual(metric_semconvs[2].metric_name, expected["metric_name"])

    def test_resource(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/cloud.yaml"))
        self.assertEqual(len(semconv.models), 1)
        cloud = list(semconv.models.values())[0]
        expected = {
            "id": "cloud",
            "prefix": "cloud",
            "extends": "",
            "attributes": [
                "cloud.account.id",
                "cloud.provider",
                "cloud.region",
                "cloud.zone",
            ],
        }
        self.semantic_convention_check(cloud, expected)

    def test_event(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/event.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 4)
        event = list(semconv.models.values())[0]
        expected = {
            "id": "exception",
            "prefix": "exception",
            "extends": "",
            "attributes": [
                "exception.escaped",
                "exception.message",
                "exception.stacktrace",
                "exception.type",
            ],
        }
        self.semantic_convention_check(event, expected)

        experimental_event = list(semconv.models.values())[1]
        expected = {
            "id": "experimental_event",
            "prefix": "experimental_event",
            "extends": "",
            "stability": StabilityLevel.EXPERIMENTAL,
            "attributes": [
                "experimental_event.foo",
            ],
        }
        self.semantic_convention_check(experimental_event, expected)

        stable_event = list(semconv.models.values())[2]
        expected = {
            "id": "stable_event",
            "prefix": "stable_event",
            "extends": "",
            "stability": StabilityLevel.STABLE,
            "attributes": [],
        }
        self.semantic_convention_check(stable_event, expected)

        deprecated_event = list(semconv.models.values())[3]
        expected = {
            "id": "deprecated_event",
            "prefix": "deprecated_event",
            "extends": "",
            "stability": StabilityLevel.STABLE,
            "deprecated": "Removed.",
            "attributes": [],
        }
        self.semantic_convention_check(deprecated_event, expected)

    def test_span_with_event(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/event.yaml"))
        semconv.parse(self.load_file("yaml/span_event.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)
        semconvs = list(semconv.models.values())
        self.assertTrue(isinstance(semconvs[0], EventSemanticConvention))
        self.assertTrue(isinstance(semconvs[1], EventSemanticConvention))
        self.assertTrue(isinstance(semconvs[2], EventSemanticConvention))
        self.assertTrue(isinstance(semconvs[3], EventSemanticConvention))
        self.assertTrue(isinstance(semconvs[4], SpanSemanticConvention))
        self.assertTrue(isinstance(semconvs[5], EventSemanticConvention))
        span_semconv = semconvs[4]
        self.assertEqual(2, len(span_semconv.events))
        self.assertTrue(isinstance(span_semconv.events[0], EventSemanticConvention))
        self.assertTrue(isinstance(span_semconv.events[1], EventSemanticConvention))
        self.assertEqual("exception", span_semconv.events[0].semconv_id)
        self.assertEqual("random.event", span_semconv.events[1].semconv_id)

    def test_rpc(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/rpc.yaml"))
        self.assertEqual(len(semconv.models), 3)

        expected = {
            "id": "rpc",
            "prefix": "rpc",
            "extends": "",
            "attributes": ["rpc.service"],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "grpc.client",
            "prefix": "",
            "extends": "rpc",
            "attributes": ["net.peer.port"],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "grpc.server",
            "prefix": "",
            "extends": "rpc",
            "attributes": ["net.peer.port"],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_markdown_link(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/links.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 1)
        s = list(semconv.models.values())[0]
        for attr in s.attributes_and_templates:
            brief = attr.brief
            self.assertEqual(brief.raw_text, str(brief))

    # This fails until ONE-36916 is not addressed
    def test_ref(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/rpc.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 5)

        client = list(semconv.models.values())[1]
        server = list(semconv.models.values())[2]

        self.assertIsNotNone(client.attrs_by_name["net.peer.port"].ref)
        self.assertIsNotNone(client.attrs_by_name["net.peer.port"].attr_type)

        self.assertIsNotNone(server.attrs_by_name["net.peer.port"].ref)
        self.assertIsNotNone(server.attrs_by_name["net.peer.port"].attr_type)

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
            "attributes": [
                "http.method",
                "http.status_code",
                "http.flavor",
                "http.host",
                "http.scheme",
                "http.status_text",
                "http.target",
                "http.url",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[0], expected)
        expected = {
            "id": "http.client",
            "prefix": "http",
            "extends": "http",
            "attributes": [
                "http.method",
                "http.status_code",
                "http.flavor",
                "http.host",
                "http.scheme",
                "http.status_text",
                "http.target",
                "http.url",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[1], expected)
        expected = {
            "id": "http.server",
            "prefix": "http",
            "extends": "http",
            "attributes": [
                "http.method",
                "http.server_name",
                "http.status_code",
                "http.flavor",
                "http.host",
                "http.scheme",
                "http.status_text",
                "http.target",
                "http.url",
                "http.user_agent",
            ],
        }
        self.semantic_convention_check(list(semconv.models.values())[2], expected)

    def test_deprecation(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/deprecated/http.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 3)

        method_attr_original = list(semconv.models.values())[0].attrs_by_name[
            "http.method"
        ]
        self.assertIsNotNone(method_attr_original.deprecated)
        self.assertEqual(
            method_attr_original.deprecated,
            "Use attribute `nonDepecrated`.",
        )

        method_attr_client = list(semconv.models.values())[1].attrs_by_name[
            "http.method"
        ]
        self.assertEqual(method_attr_client.deprecated, method_attr_original.deprecated)

        method_attr_server = list(semconv.models.values())[2].attrs_by_name[
            "http.method"
        ]
        self.assertEqual(method_attr_server.deprecated, method_attr_original.deprecated)

        self.assertIsNone(
            list(semconv.models.values())[0].attrs_by_name["http.target"].deprecated
        )

    def test_stability(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/stability.yaml"))
        semconv.finish()
        self.assertEqual(len(semconv.models), 6)

        model = list(semconv.models.values())[0]
        self.assertEqual(len(model.attributes_and_templates), 2)
        self.assertIsNone(model.stability)

        attr = model.attributes_and_templates[0]
        self.assertEqual(attr.attr_id, "exp_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes_and_templates[1]
        self.assertEqual(attr.attr_id, "stable_attr")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)

        model = list(semconv.models.values())[1]
        self.assertEqual(len(model.attributes_and_templates), 2)
        self.assertIsNone(model.stability)

        attr = model.attributes_and_templates[0]
        self.assertEqual(attr.attr_id, "exp_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes_and_templates[1]
        self.assertEqual(attr.attr_id, "stable_attr")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)

        model = list(semconv.models.values())[2]
        attr = model.attributes_and_templates[0]
        self.assertEqual(attr.attr_id, "exp_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

        attr = model.attributes_and_templates[1]
        self.assertEqual(attr.attr_id, "stable_attr")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)

        model = list(semconv.models.values())[3]
        attr = model.attributes_and_templates[0]
        self.assertEqual(attr.attr_id, "stable_deprecated_attr")
        self.assertEqual(attr.stability, StabilityLevel.STABLE)
        self.assertIsNotNone(attr.deprecated)

        attr = model.attributes_and_templates[1]
        self.assertEqual(attr.attr_id, "test_attr")
        self.assertEqual(attr.stability, StabilityLevel.EXPERIMENTAL)

    def test_populate_other_attributes(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/http.yaml"))
        semconv.parse(self.load_file("yaml/faas.yaml"))
        semconv.parse(self.load_file("yaml/general.yaml"))
        semconv.finish()
        models = sorted(semconv.models.values(), key=lambda m: m.semconv_id)
        self.assertEqual(len(models), 10)

    def test_inherited_imported(self):
        semconv = SemanticConventionSet(debug=False)
        semconv.parse(self.load_file("yaml/imported-inherited.yaml"))
        semconv.finish()
        models = sorted(semconv.models.values(), key=lambda m: m.semconv_id)
        self.assertEqual(len(models), 6)
        # HTTP
        attrs = models[0].attributes_and_templates
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
        attrs = models[1].attributes_and_templates
        self.assertEqual(models[1].semconv_id, "network")
        self.assertEqual(len(attrs), 3)

        self.assertEqual(attrs[0].fqn, "net.peer.ip")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        self.assertEqual(attrs[1].fqn, "net.peer.name")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, None)

        self.assertEqual(attrs[2].fqn, "net.peer.port")
        self.assertEqual(attrs[2].imported, False)
        self.assertEqual(attrs[2].inherited, False)
        self.assertEqual(attrs[2].ref, None)
        self.assertEqual(attrs[2].note, "not override")

        # Base - rpc
        attrs = models[2].attributes_and_templates
        self.assertEqual(models[2].semconv_id, "rpc")
        self.assertEqual(len(attrs), 1)

        self.assertEqual(attrs[0].fqn, "rpc.service")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        # Extended - rpc.client
        attrs = models[3].attributes_and_templates
        self.assertEqual(models[3].semconv_id, "rpc.client")
        self.assertEqual(len(attrs), 3)

        self.assertEqual(attrs[0].fqn, "net.peer.port")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, "net.peer.port")
        self.assertEqual(attrs[0].brief, "override")
        self.assertEqual(attrs[0].note, "not override")

        self.assertEqual(attrs[1].fqn, "rpc.client.name")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, False)
        self.assertEqual(attrs[1].ref, None)

        self.assertEqual(attrs[2].fqn, "rpc.service")
        self.assertEqual(attrs[2].imported, False)
        self.assertEqual(attrs[2].inherited, True)
        self.assertEqual(attrs[2].ref, None)

        # Include on Extended - zother
        attrs = models[4].attributes_and_templates
        self.assertEqual(models[4].semconv_id, "zother")
        self.assertEqual(len(attrs), 1)

        self.assertEqual(attrs[0].fqn, "zother.hostname")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, False)
        self.assertEqual(attrs[0].ref, None)

        # Include on Extended - zz.rpc.client
        attrs = models[5].attributes_and_templates
        self.assertEqual(models[5].semconv_id, "zz.rpc.client")
        self.assertEqual(len(attrs), 4)

        self.assertEqual(attrs[0].fqn, "net.peer.port")
        self.assertEqual(attrs[0].imported, False)
        self.assertEqual(attrs[0].inherited, True)
        self.assertEqual(attrs[0].ref, "net.peer.port")
        self.assertEqual(attrs[0].brief, "override")
        self.assertEqual(attrs[0].note, "not override")

        self.assertEqual(attrs[1].fqn, "rpc.client.name")
        self.assertEqual(attrs[1].imported, False)
        self.assertEqual(attrs[1].inherited, True)
        self.assertEqual(attrs[1].ref, None)

        self.assertEqual(attrs[2].fqn, "rpc.client.zz.attr")
        self.assertEqual(attrs[2].imported, False)
        self.assertEqual(attrs[2].inherited, False)
        self.assertEqual(attrs[2].ref, None)

        self.assertEqual(attrs[3].fqn, "rpc.service")
        self.assertEqual(attrs[3].imported, False)
        self.assertEqual(attrs[3].inherited, True)
        self.assertEqual(attrs[3].ref, None)

    def semantic_convention_check(self, s, expected):
        self.assertEqual(expected["prefix"], s.prefix)
        self.assertEqual(expected.get("stability"), s.stability)
        self.assertEqual(expected.get("deprecated"), s.deprecated)
        self.assertEqual(expected["extends"], s.extends)
        self.assertEqual(expected["id"], s.semconv_id)
        self.assertEqual(len(expected["attributes"]), len(s.attributes))
        self.assertEqual(expected["attributes"], [a.fqn for a in s.attributes])

    _TEST_DIR = os.path.dirname(__file__)

    def load_file(self, filename):
        return os.path.join(self._TEST_DIR, "..", "..", "data", filename)
