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

from opentelemetry.semconv.model.constraints import AnyOf, Include, parse_constraints
from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_attribute import (
    AttributeType,
    SemanticAttribute,
)
from opentelemetry.semconv.model.unit_member import UnitMember
from opentelemetry.semconv.model.utils import ValidatableYamlNode, validate_id


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


def parse_semantic_convention_groups(yaml_file):
    yaml = YAML().load(yaml_file)
    models = []
    for group in yaml["groups"]:
        models.append(SemanticConvention(group))
    return models


def SemanticConvention(group):
    type_value = group.get("type")
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
        raise ValidationError.from_yaml_pos(position, msg)

    # First, validate that the correct fields are available in the yaml
    convention_type.validate_keys(group)
    model = convention_type(group)
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
        "constraints",
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

        return sorted(
            [
                attr
                for attr in self.attrs_by_name.values()
                if templates is None
                or templates == AttributeType.is_template_type(attr.attr_type)
            ],
            key=lambda attr: attr.fqn,
        )

    def __init__(self, group):
        super().__init__(group)

        self.semconv_id = self.id
        self.note = group.get("note", "").strip()
        self.prefix = group.get("prefix", "").strip()
        stability = group.get("stability")
        deprecated = group.get("deprecated")
        position_data = group.lc.data
        self.stability, self.deprecated = SemanticAttribute.parse_stability_deprecated(
            stability, deprecated, position_data
        )
        self.extends = group.get("extends", "").strip()
        self.events = group.get("events", ())
        self.constraints = parse_constraints(group.get("constraints", ()))
        self.attrs_by_name = SemanticAttribute.parse(
            self.prefix, self.stability, group.get("attributes")
        )

    def contains_attribute(self, attr: "SemanticAttribute"):
        for local_attr in self.attributes_and_templates:
            if local_attr.attr_id is not None:
                if local_attr.fqn == attr.fqn:
                    return True
            if local_attr == attr:
                return True
        return False

    def has_attribute_constraint(self, attr):
        return any(
            attribute.equivalent_to(attr)
            for constraint in self.constraints
            if isinstance(constraint, AnyOf)
            for attr_list in constraint.choice_list_attributes
            for attribute in attr_list
        )

    def validate_values(self):
        super().validate_values()
        if self.prefix:
            validate_id(self.prefix, self._position)


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

    def __init__(self, group):
        super().__init__(group)
        self.span_kind = SpanKind.parse(group.get("span_kind"))
        if self.span_kind is None:
            position = group.lc.data["span_kind"]
            msg = f"Invalid value for span_kind: {group.get('span_kind')}"
            raise ValidationError.from_yaml_pos(position, msg)


class EventSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "event"

    allowed_keys = BaseSemanticConvention.allowed_keys + ("name",)

    def __init__(self, group):
        super().__init__(group)
        self.name = group.get("name", self.prefix)
        if not self.name:
            raise ValidationError.from_yaml_pos(
                self._position, "Event must define at least one of name or prefix"
            )


class UnitSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "units"

    allowed_keys = (  # We completely override base semantic keys here.
        "id",
        "type",
        "brief",
        "members",
    )

    def __init__(self, group):
        super().__init__(group)
        self.members = UnitMember.parse(group.get("members"))


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

    def __init__(self, group):
        super().__init__(group)
        self.metric_name = group.get("metric_name")
        self.unit = group.get("unit")
        self.instrument = group.get("instrument")
        self.validate()

    def validate(self):
        val_tuple = (self.metric_name, self.unit, self.instrument)
        if not all(val_tuple):
            raise ValidationError.from_yaml_pos(
                self._position,
                "All of metric_name, units, and instrument must be defined",
            )

        if self.instrument not in self.allowed_instruments:
            raise ValidationError.from_yaml_pos(
                self._position,
                f"Instrument '{self.instrument}' is not a valid instrument name",
            )


@dataclass
class SemanticConventionSet:
    """Contains the list of models.
    From this structure we will generate md/constants/etc with a pretty print of the structure.
    """

    debug: bool
    models: typing.Dict[str, BaseSemanticConvention] = field(default_factory=dict)
    errors: bool = False

    def parse(self, file):
        with open(file, "r", encoding="utf-8") as yaml_file:
            try:
                semconv_models = parse_semantic_convention_groups(yaml_file)
                for model in semconv_models:
                    if model.semconv_id in self.models:
                        self.errors = True
                        print(f"Error parsing {file}\n", file=sys.stderr)
                        print(
                            f"Semantic convention '{model.semconv_id}' is already defined.",
                            file=sys.stderr,
                        )
                    self.models[model.semconv_id] = model
            except ValidationError as e:
                self.errors = True
                print(f"Error parsing {file}\n", file=sys.stderr)
                print(e, file=sys.stderr)

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
                # Ref first, extends and includes after!
                fixpoint_ref = self.resolve_ref(semconv)
                fixpoint_inc = self.resolve_include(semconv)
                fixpoint = fixpoint and fixpoint_ref and fixpoint_inc
            index += 1
        self.debug = tmp_debug
        # After we resolve any local dependency, we can resolve parent/child relationship
        self._populate_extends()
        # From string containing attribute ids to SemanticAttribute objects
        self._populate_anyof_attributes()
        # From strings containing Semantic Conventions for Events ids to SemanticConvention objects
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
        :param semconvs: The list of remaining semantic conventions to process.
        :return: A list of remaining semantic convention to process.
        """
        # Resolve parent of current Semantic Convention
        if semconv.extends:
            extended = self.models.get(semconv.extends)
            if extended is None:
                raise ValidationError.from_yaml_pos(
                    semconv._position,
                    f"Semantic Convention {semconv.semconv_id} extends "
                    f"{semconv.extends} but the latter cannot be found!",
                )

            # Process hierarchy chain
            not_yet_processed = extended.extends in unprocessed
            if extended.extends and not_yet_processed:
                # Recursion on parent if was not already processed
                parent_extended = self.models.get(extended.extends)
                self._populate_extends_single(parent_extended, unprocessed)

            # inherit prefix and constraints
            if not semconv.prefix:
                semconv.prefix = extended.prefix
            # Constraints
            for constraint in extended.constraints:
                if constraint not in semconv.constraints and isinstance(
                    constraint, AnyOf
                ):
                    semconv.constraints += (constraint.inherit_anyof(),)
            # Attributes
            parent_attributes = {}
            for ext_attr in extended.attributes_and_templates:
                parent_attributes[ext_attr.fqn] = ext_attr.inherit_attribute()

            parent_attributes.update(semconv.attrs_by_name)
            semconv.attrs_by_name = parent_attributes

        # delete from remaining semantic conventions to process
        del unprocessed[semconv.semconv_id]

    def _populate_anyof_attributes(self):
        any_of: AnyOf
        for semconv in self.models.values():
            for any_of in semconv.constraints:
                if not isinstance(any_of, AnyOf):
                    continue
                for index, attr_ids in enumerate(any_of.choice_list_ids):
                    constraint_attrs = []
                    for attr_id in attr_ids:
                        ref_attr = self._lookup_attribute(attr_id)
                        if ref_attr is None:
                            raise ValidationError.from_yaml_pos(
                                any_of._yaml_src_position[index],
                                f"Any_of attribute '{attr_id}' of semantic convention "
                                "{semconv.semconv_id} does not exists!",
                            )
                        constraint_attrs.append(ref_attr)
                    if constraint_attrs:
                        any_of.add_attributes(constraint_attrs)

    def _populate_events(self):
        for semconv in self.models.values():
            events: typing.List[EventSemanticConvention] = []
            for event_id in semconv.events:
                event = self.models.get(event_id)
                if event is None:
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} has "
                        "{event_id} as event but the latter cannot be found!",
                    )
                if not isinstance(event, EventSemanticConvention):
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} has {event_id} as event but"
                        " the latter is not a semantic convention for events!",
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
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} reference `{attr.ref}` but it cannot be found!",
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

    def resolve_include(self, semconv):
        fixpoint_inc = True
        for constraint in semconv.constraints:
            if isinstance(constraint, Include):
                include_semconv = self.models.get(constraint.semconv_id)
                # include required attributes and constraints
                if include_semconv is None:
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        f"Semantic Convention {semconv.semconv_id} includes "
                        "{constraint.semconv_id} but the latter cannot be found!",
                    )
                # We resolve the parent/child relationship of the included semantic convention, if any
                self._populate_extends_single(
                    include_semconv, {include_semconv.semconv_id: include_semconv}
                )
                attr: SemanticAttribute
                for attr in include_semconv.attributes_and_templates:
                    if semconv.contains_attribute(attr):
                        if self.debug:
                            print(
                                f"[Includes] {semconv.semconv_id} already contains attribute {attr}"
                            )
                        continue
                    # There are changes
                    fixpoint_inc = False
                    semconv.attrs_by_name[attr.fqn] = attr.import_attribute()
                for inc_constraint in include_semconv.constraints:
                    if (
                        isinstance(inc_constraint, Include)
                        or inc_constraint in semconv.constraints
                    ):
                        # We do not include "include" constraint or the constraint was already imported
                        continue
                    # We know the type of the constraint
                    inc_constraint: AnyOf
                    # There are changes
                    fixpoint_inc = False
                    semconv.constraints += (inc_constraint.inherit_anyof(),)
        return fixpoint_inc

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
