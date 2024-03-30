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

import sys
import typing
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple, Union

from ruamel.yaml import YAML

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_attribute import (
    AttributeType,
    RequirementLevel,
    SemanticAttribute,
)
from opentelemetry.semconv.model.unit_member import UnitMember
from opentelemetry.semconv.model.utils import (
    ValidatableYamlNode,
    ValidationContext,
    check_no_missing_keys,
    validate_id,
)


class SpanKind(Enum):
    EMPTY = 1
    CLIENT = 2
    SERVER = 3
    CONSUMER = 4
    PRODUCER = 5
    INTERNAL = 6

    @staticmethod
    def parse(span_kind_value):
        if span_kind_value is None:
            return SpanKind.EMPTY
        kind_map = {
            "client": SpanKind.CLIENT,
            "server": SpanKind.SERVER,
            "producer": SpanKind.PRODUCER,
            "consumer": SpanKind.CONSUMER,
            "internal": SpanKind.INTERNAL,
        }
        return kind_map.get(span_kind_value)


def parse_semantic_convention_type(type_value):
    # Gracefully transition to the new types
    if type_value is None:
        return SpanSemanticConvention
    return CONVENTION_CLS_BY_GROUP_TYPE.get(type_value)


def parse_semantic_convention_groups(yaml_file, validation_ctx):
    yaml = YAML().load(yaml_file)
    models = []
    for group in yaml["groups"]:
        models.append(SemanticConvention(group, validation_ctx))
    return models


def SemanticConvention(group, validation_ctx):
    type_value = group.get("type")
    semconv_id = group.get("id")
    if type_value is None:
        line = group.lc.data["id"][0] + 1
        doc_url = "https://github.com/open-telemetry/build-tools/blob/main/semantic-conventions/syntax.md#groups"
        print(
            f"Please set the type for group '{group['id']}' on line {line} - defaulting to type 'span'. See {doc_url}",
            file=sys.stderr,
        )

    convention_type = parse_semantic_convention_type(type_value)
    if convention_type is None:
        position = group.lc.data["type"] if "type" in group else group.lc.data["id"]
        msg = f"Invalid value for semantic convention type: {group.get('type')}"
        validation_ctx.raise_or_warn(position, msg, semconv_id)

    # First, validate that the correct fields are available in the yaml
    convention_type.validate_keys(group, validation_ctx)
    model = convention_type(group, validation_ctx)
    # Also, validate that the value of the fields is acceptable
    model.validate_values()
    return model


class BaseSemanticConvention(ValidatableYamlNode):
    """Contains the model extracted from a yaml file"""

    allowed_keys: Tuple[str, ...] = (
        "id",
        "type",
        "brief",
        "note",
        "prefix",
        "stability",
        "extends",
        "attributes",
        "deprecated",
    )

    GROUP_TYPE_NAME: str

    @property
    def attributes(self):
        return self._get_attributes(False)

    @property
    def attribute_templates(self):
        return self._get_attributes(True)

    @property
    def attributes_and_templates(self):
        return self._get_attributes(None)

    def _get_attributes(self, templates: Optional[bool]):
        if not hasattr(self, "attrs_by_name"):
            return []

        def comparison_key(attr):
            if attr.requirement_level:
                return attr.requirement_level.value, attr.fqn
            return RequirementLevel.RECOMMENDED.value, attr.fqn

        return sorted(
            [
                attr
                for attr in self.attrs_by_name.values()
                if templates is None
                or templates == AttributeType.is_template_type(attr.attr_type)
            ],
            key=comparison_key,
        )

    def __init__(self, group, validation_ctx):
        super().__init__(group, validation_ctx)

        self.semconv_id = self.id
        self.note = group.get("note", "").strip()
        self.prefix = group.get("prefix", "").strip()
        self.validation_ctx = validation_ctx
        position_data = group.lc.data
        self.stability = SemanticAttribute.parse_stability(
            group.get("stability"), position_data, self.semconv_id, validation_ctx
        )
        self.deprecated = SemanticAttribute.parse_deprecated(
            group.get("deprecated"), position_data, self.semconv_id, validation_ctx
        )
        self.extends = group.get("extends", "").strip()
        self.events = group.get("events", ())
        self.attrs_by_name = SemanticAttribute.parse(
            self.prefix, group.get("attributes"), validation_ctx
        )

    def contains_attribute(self, attr: "SemanticAttribute"):
        for local_attr in self.attributes_and_templates:
            if local_attr.attr_id is not None:
                if local_attr.fqn == attr.fqn:
                    return True
            if local_attr == attr:
                return True
        return False

    def validate_values(self):
        super().validate_values()
        if self.prefix:
            validate_id(self.prefix, self._position, self.validation_ctx)


class ResourceSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "resource"


class ScopeSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "scope"


class AttributeGroupConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "attribute_group"


class SpanSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "span"

    allowed_keys = BaseSemanticConvention.allowed_keys + (
        "events",
        "span_kind",
    )

    def __init__(self, group, validation_ctx):
        super().__init__(group, validation_ctx)
        self.span_kind = SpanKind.parse(group.get("span_kind"))
        if self.span_kind is None:
            position = group.lc.data["span_kind"]
            msg = f"Invalid value for span_kind: {group.get('span_kind')}"
            validation_ctx.raise_or_warn(position, msg, group.get("id"))


class EventSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "event"

    allowed_keys = BaseSemanticConvention.allowed_keys + ("name",)

    def __init__(self, group, validation_ctx):
        super().__init__(group, validation_ctx)
        self.name = group.get("name", self.prefix)
        if not self.name:
            validation_ctx.raise_or_warn(
                self._position,
                "Event must define at least one of name or prefix",
                group.get("id"),
            )


class UnitSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "units"

    allowed_keys = (  # We completely override base semantic keys here.
        "id",
        "type",
        "brief",
        "members",
    )

    def __init__(self, group, validation_ctx):
        super().__init__(group, validation_ctx)
        self.members = UnitMember.parse(group.get("members"), validation_ctx)


class MetricGroupSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "metric_group"


class MetricSemanticConvention(MetricGroupSemanticConvention):
    GROUP_TYPE_NAME = "metric"

    allowed_keys: Tuple[str, ...] = BaseSemanticConvention.allowed_keys + (
        "metric_name",
        "unit",
        "instrument",
    )

    canonical_instrument_name_by_yaml_name: Dict[str, str] = {
        "counter": "Counter",
        "updowncounter": "UpDownCounter",
        "histogram": "Histogram",
        "gauge": "Gauge",
    }

    allowed_instruments: Tuple[str, ...] = tuple(
        canonical_instrument_name_by_yaml_name.keys()
    )

    def __init__(self, group, validation_ctx):
        super().__init__(group, validation_ctx)
        self.metric_name = group.get("metric_name")
        self.unit = group.get("unit")
        self.instrument = group.get("instrument")
        self.validation_ctx = validation_ctx

        namespaces = self.metric_name.split(".")
        self.root_namespace = namespaces[0] if len(namespaces) > 1 else ""
        self.validate(group)

    def validate(self, yaml):
        check_no_missing_keys(
            yaml,
            ["metric_name", "unit", "instrument", "stability"],
            self.validation_ctx,
        )

        if self.instrument not in self.allowed_instruments:
            self.validation_ctx.raise_or_warn(
                self._position,
                f"Instrument '{self.instrument}' is not a valid instrument name",
                self.metric_name,
            )


@dataclass
class SemanticConventionSet:
    """Contains the list of models.
    From this structure we will generate md/constants/etc with a pretty print of the structure.
    """

    debug: bool
    models: typing.Dict[str, BaseSemanticConvention] = field(default_factory=dict)
    errors: bool = False
    validation_ctx: Optional[ValidationContext] = None

    def parse(self, file, validation_ctx=None):
        self.validation_ctx = validation_ctx or ValidationContext(file, True)
        with open(file, "r", encoding="utf-8") as yaml_file:
            try:
                semconv_models = parse_semantic_convention_groups(
                    yaml_file, self.validation_ctx
                )
                for model in semconv_models:
                    if model.semconv_id in self.models:
                        self.errors = True
                        print(f"\nError parsing {file}:", file=sys.stderr)
                        print(
                            f"Semantic convention '{model.semconv_id}' is already defined.",
                            file=sys.stderr,
                        )
                    self.models[model.semconv_id] = model
            except ValidationError as e:
                self.errors = True
                print(f"\nError parsing {file}:", file=sys.stderr)
                print(e, file=sys.stderr)
                print()

    def has_error(self):
        return self.errors

    def check_unique_fqns(self):
        group_by_fqn: typing.Dict[str, str] = {}
        for model in self.models.values():
            for attr in model.attributes_and_templates:
                if not attr.ref:
                    if attr.fqn in group_by_fqn:
                        self.errors = True
                        print(
                            f"Attribute {attr.fqn} of Semantic convention '{model.semconv_id}'"
                            "is already defined in {group_by_fqn.get(attr.fqn)}.",
                            file=sys.stderr,
                        )
                    group_by_fqn[attr.fqn] = model.semconv_id

    def finish(self):
        """Resolves values referenced from other models using `ref` and `extends` attributes
        AFTER all models were parsed.
        Here, sanity checks for `ref/extends` attributes are performed.
        """
        # Before resolving attributes, we verify that no duplicate exists.
        self.check_unique_fqns()
        fixpoint = False
        index = 0
        tmp_debug = self.debug
        # This is a hot spot for optimizations
        while not fixpoint:
            fixpoint = True
            if index > 0:
                self.debug = False
            for semconv in self.models.values():
                fixpoint_ref = self.resolve_ref(semconv)
                fixpoint = fixpoint and fixpoint_ref
            index += 1
        self.debug = tmp_debug
        # After we resolve any local dependency, we can resolve parent/child relationship
        self._populate_extends()
        # From string containing attribute ids to SemanticAttribute objects
        self._populate_events()

    def _populate_extends(self):
        """
        This internal method goes through every semantic convention to resolve parent/child relationships.
        :return: None
        """
        unprocessed = self.models.copy()
        # Iterate through the list and remove the semantic conventions that have been processed.
        while len(unprocessed) > 0:
            semconv = next(iter(unprocessed.values()))
            self._populate_extends_single(semconv, unprocessed)

    def _populate_extends_single(self, semconv, unprocessed):
        """
        Resolves the parent/child relationship for a single Semantic Convention. If the parent **p** of the input
        semantic convention **i** has in turn a parent **pp**, it recursively resolves **pp** before processing **p**.
        :param semconv: The semantic convention for which resolve the parent/child relationship.
        :param unprocessed: The list of remaining semantic conventions to process.
        :return: A list of remaining semantic convention to process.
        """
        # Resolve parent of current Semantic Convention
        if semconv.extends:
            extended = self.models.get(semconv.extends)
            if extended is None:
                self.validation_ctx.raise_or_warn(
                    semconv._position,
                    f"Semantic Convention {semconv.semconv_id} extends "
                    f"{semconv.extends} but the latter cannot be found!",
                    semconv.semconv_id,
                )

            # Process hierarchy chain
            not_yet_processed = extended.extends in unprocessed
            if extended.extends and not_yet_processed:
                # Recursion on parent if was not already processed
                parent_extended = self.models.get(extended.extends)
                self._populate_extends_single(parent_extended, unprocessed)

            # inherit prefix
            if not semconv.prefix:
                semconv.prefix = extended.prefix
            # Attributes
            parent_attributes = {}
            for ext_attr in extended.attributes_and_templates:
                parent_attributes[ext_attr.fqn] = ext_attr.inherit_attribute()

            parent_attributes.update(semconv.attrs_by_name)
            semconv.attrs_by_name = parent_attributes

        # delete from remaining semantic conventions to process
        del unprocessed[semconv.semconv_id]

    def _populate_events(self):
        for semconv in self.models.values():
            events: typing.List[EventSemanticConvention] = []
            for event_id in semconv.events:
                event = self.models.get(event_id)
                if event is None:
                    self.validation_ctx.raise_or_warn(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} has "
                        "{event_id} as event but the latter cannot be found!",
                        event_id,
                    )
                if not isinstance(event, EventSemanticConvention):
                    self.validation_ctx.raise_or_warn(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} has {event_id} as event but"
                        " the latter is not a semantic convention for events!",
                        event_id,
                    )
                events.append(event)
            semconv.events = events

    def resolve_ref(self, semconv):
        fixpoint_ref = True
        attr: SemanticAttribute
        for attr in semconv.attributes:
            if attr.ref is not None and attr.attr_id is None:
                attr = self._fill_inherited_attribute(attr, semconv)
                # There are changes
                fixpoint_ref = False
                ref_attr = self._lookup_attribute(attr.ref)
                if not ref_attr:
                    self.validation_ctx.raise_or_warn(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} reference `{attr.ref}` but it cannot be found!",
                        semconv.semconv_id,
                    )
                attr = self._merge_attribute(attr, ref_attr)
        return fixpoint_ref

    def _fill_inherited_attribute(self, attr, semconv):
        if attr.attr_id is not None:
            return attr

        if attr.ref in semconv.attrs_by_name.keys():
            attr = self._merge_attribute(attr, semconv.attrs_by_name[attr.ref])
        if semconv.extends in self.models:
            attr = self._fill_inherited_attribute(attr, self.models[semconv.extends])
        return attr

    def _merge_attribute(self, child, parent):
        child.attr_type = parent.attr_type
        child.stability = parent.stability
        child.deprecated = parent.deprecated
        if not child.brief:
            child.brief = parent.brief
        if not child.requirement_level:
            child.requirement_level = parent.requirement_level
            if not child.requirement_level_msg:
                child.requirement_level_msg = parent.requirement_level_msg
        if not child.note:
            child.note = parent.note
        if child.examples is None:
            child.examples = parent.examples
        child.attr_id = parent.attr_id
        return child

    def _lookup_attribute(self, attr_id: str) -> Union[SemanticAttribute, None]:
        return next(
            (
                attr
                for model in self.models.values()
                for attr in model.attributes_and_templates
                if attr.fqn == attr_id and attr.ref is None
            ),
            None,
        )

    def attributes(self):
        output = []
        for semconv in self.models.values():
            output.extend(semconv.attributes)
        return output

    def attribute_templates(self):
        output = []
        for semconv in self.models.values():
            output.extend(semconv.attribute_templates)
        return output


CONVENTION_CLS_BY_GROUP_TYPE = {
    cls.GROUP_TYPE_NAME: cls
    for cls in (
        SpanSemanticConvention,
        ResourceSemanticConvention,
        EventSemanticConvention,
        MetricGroupSemanticConvention,
        MetricSemanticConvention,
        UnitSemanticConvention,
        ScopeSemanticConvention,
        AttributeGroupConvention,
    )
}
