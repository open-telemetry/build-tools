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
from typing import Tuple, Union

from ruamel.yaml import YAML

from opentelemetry.semconv.model.constraints import AnyOf, Include, parse_constraints
from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_attribute import (
    Required,
    SemanticAttribute,
    unique_attributes,
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
        line = group.lc.data["id"][1] + 1
        print(
            "Using default SPAN type for semantic convention '{}' @ line {}".format(
                group["id"], line
            ),
            file=sys.stderr,
        )

    convention_type = parse_semantic_convention_type(type_value)
    if convention_type is None:
        position = group.lc.data["type"] if "type" in group else group.lc.data["id"]
        msg = "Invalid value for semantic convention type: {}".format(group.get("type"))
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
        if not hasattr(self, "attrs_by_name"):
            return []

        return list(self.attrs_by_name.values())

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
        for local_attr in self.attributes:
            if local_attr.attr_id is not None:
                if local_attr.fqn == attr.fqn:
                    return True
            if local_attr == attr:
                return True
        return False

    def all_attributes(self):
        return unique_attributes(self.attributes + self.conditional_attributes())

    def sampling_attributes(self):
        return unique_attributes(
            [attr for attr in self.attributes if attr.sampling_relevant]
        )

    def required_attributes(self):
        return unique_attributes(
            [attr for attr in self.attributes if attr.required == Required.ALWAYS]
        )

    def conditional_attributes(self):
        return unique_attributes(
            [attr for attr in self.attributes if attr.required == Required.CONDITIONAL]
        )

    def any_of(self):
        result = []
        for constraint in self.constraints:
            if isinstance(constraint, AnyOf):
                result.append(constraint)
        return result

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
            msg = "Invalid value for span_kind: {}".format(group.get("span_kind"))
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


class MetricSemanticConvention(BaseSemanticConvention):
    GROUP_TYPE_NAME = "metric"

    allowed_keys: Tuple[str, ...] = BaseSemanticConvention.allowed_keys + ("metrics",)

    class Metric:
        allowed_instruments: Tuple[str, ...] = (
            "Counter",
            "UpDownCounter",
            "Histogram",
            "Gauge",
        )

        def __init__(self, metric, parent_prefix, position):
            self.id: str = metric.get("id")
            self.fqn = "{}.{}".format(parent_prefix, self.id)
            self._position = position
            self.units: str = metric.get("units")
            self.brief: str = metric.get("brief")
            self.instrument: str = metric.get("instrument")

            if self.instrument not in self.allowed_instruments:
                raise ValidationError.from_yaml_pos(
                    self._position,
                    "Instrument '{}' is not a valid instrument name".format(
                        self.instrument
                    ),
                )
            if None in [self.instrument, self.id, self.units, self.brief]:
                raise ValidationError.from_yaml_pos(
                    self._position,
                    "id, instrument, units, and brief must all be defined for concrete metrics",
                )

    def __init__(self, group):
        super().__init__(group)
        self.metrics = ()
        if group.get("metrics"):
            self.metrics: Tuple[MetricSemanticConvention.Metric, ...] = tuple(
                map(
                    lambda m: MetricSemanticConvention.Metric(
                        m, self.prefix, self._position
                    ),
                    group.get("metrics"),
                )
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
                        print("Error parsing {}\n".format(file), file=sys.stderr)
                        print(
                            "Semantic convention '{}' is already defined.".format(
                                model.semconv_id
                            ),
                            file=sys.stderr,
                        )
                    self.models[model.semconv_id] = model
            except ValidationError as e:
                self.errors = True
                print("Error parsing {}\n".format(file), file=sys.stderr)
                print(e, file=sys.stderr)

    def has_error(self):
        return self.errors

    def check_unique_fqns(self):
        group_by_fqn: typing.Dict[str, str] = {}
        for model in self.models.values():
            for attr in model.attributes:
                if not attr.ref:
                    if attr.fqn in group_by_fqn:
                        self.errors = True
                        print(
                            "Attribute {} of Semantic convention '{}' is already defined in {}.".format(
                                attr.fqn, model.semconv_id, group_by_fqn.get(attr.fqn)
                            ),
                            file=sys.stderr,
                        )
                    group_by_fqn[attr.fqn] = model.semconv_id

    def finish(self):
        """Resolves values referenced from other models using `ref` and `extends` attributes AFTER all models were parsed.
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
                    "Semantic Convention {} extends {} but the latter cannot be found!".format(
                        semconv.semconv_id, semconv.extends
                    ),
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
            for ext_attr in extended.attributes:
                parent_attributes[ext_attr.fqn] = ext_attr.inherit_attribute()
            # By induction, parent semconv is already correctly sorted
            parent_attributes.update(
                SemanticConventionSet._sort_attributes_dict(semconv.attrs_by_name)
            )
            if parent_attributes or semconv.attributes:
                semconv.attrs_by_name = parent_attributes
        elif semconv.attributes:  # No parent, sort of current attributes
            semconv.attrs_by_name = SemanticConventionSet._sort_attributes_dict(
                semconv.attrs_by_name
            )
        # delete from remaining semantic conventions to process
        del unprocessed[semconv.semconv_id]

    @staticmethod
    def _sort_attributes_dict(
        attributes: typing.Dict[str, SemanticAttribute]
    ) -> typing.Dict[str, SemanticAttribute]:
        """
        First  imported, and then defined attributes.
        :param attributes: Dictionary of attributes to sort
        :return: A sorted dictionary of attributes
        """
        return dict(
            sorted(attributes.items(), key=lambda kv: 0 if kv[1].imported else 1)
        )

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
                                "Any_of attribute '{}' of semantic convention {} does not exists!".format(
                                    attr_id, semconv.semconv_id
                                ),
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
                        "Semantic Convention {} has {} as event but the latter cannot be found!".format(
                            semconv.semconv_id, event_id
                        ),
                    )
                if not isinstance(event, EventSemanticConvention):
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        "Semantic Convention {} has {} as event but"
                        " the latter is not a semantic convention for events!".format(
                            semconv.semconv_id, event_id
                        ),
                    )
                events.append(event)
            semconv.events = events

    def resolve_ref(self, semconv):
        fixpoint_ref = True
        attr: SemanticAttribute
        for attr in semconv.attributes:
            if attr.ref is not None and attr.attr_id is None:
                # There are changes
                fixpoint_ref = False
                ref_attr = self._lookup_attribute(attr.ref)
                if not ref_attr:
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        "Semantic Convention {} reference `{}` but it cannot be found!".format(
                            semconv.semconv_id, attr.ref
                        ),
                    )
                attr.attr_type = ref_attr.attr_type
                if not attr.brief:
                    attr.brief = ref_attr.brief
                if not attr.note:
                    attr.note = ref_attr.note
                if attr.examples is None:
                    attr.examples = ref_attr.examples
                attr.attr_id = attr.ref
        return fixpoint_ref

    def resolve_include(self, semconv):
        fixpoint_inc = True
        for constraint in semconv.constraints:
            if isinstance(constraint, Include):
                include_semconv = self.models.get(constraint.semconv_id)
                # include required attributes and constraints
                if include_semconv is None:
                    raise ValidationError.from_yaml_pos(
                        semconv._position,
                        "Semantic Convention {} includes {} but the latter cannot be found!".format(
                            semconv.semconv_id, constraint.semconv_id
                        ),
                    )
                # We resolve the parent/child relationship of the included semantic convention, if any
                self._populate_extends_single(
                    include_semconv, {include_semconv.semconv_id: include_semconv}
                )
                attr: SemanticAttribute
                for attr in include_semconv.attributes:
                    if semconv.contains_attribute(attr):
                        if self.debug:
                            print(
                                "[Includes] {} already contains attribute {}".format(
                                    semconv.semconv_id, attr
                                )
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
                for attr in model.attributes
                if attr.fqn == attr_id and attr.ref is None
            ),
            None,
        )

    def attributes(self):
        output = []
        for semconv in self.models.values():
            output.extend(semconv.attributes)
        return output


CONVENTION_CLS_BY_GROUP_TYPE = {
    cls.GROUP_TYPE_NAME: cls
    for cls in (
        SpanSemanticConvention,
        ResourceSemanticConvention,
        EventSemanticConvention,
        MetricSemanticConvention,
        UnitSemanticConvention,
    )
}
