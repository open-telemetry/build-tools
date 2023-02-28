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

import re
from collections.abc import Iterable
from dataclasses import dataclass, replace
from enum import Enum
from typing import Dict, List, Optional, Union

from ruamel.yaml.comments import CommentedMap, CommentedSeq

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.utils import (
    check_no_missing_keys,
    validate_id,
    validate_values,
)


class RequirementLevel(Enum):
    REQUIRED = 1
    CONDITIONALLY_REQUIRED = 2
    RECOMMENDED = 3
    OPT_IN = 4


class StabilityLevel(Enum):
    STABLE = 1
    EXPERIMENTAL = 2
    DEPRECATED = 3


def unique_attributes(attributes):
    output = []
    for x in attributes:
        if x.fqn not in [attr.fqn for attr in output]:
            output.append(x)
    return output


@dataclass
class SemanticAttribute:
    fqn: str
    attr_id: str
    ref: str
    attr_type: Union[str, "EnumAttributeType"]
    brief: str
    examples: List[Union[str, int, bool]]
    tag: str
    stability: StabilityLevel
    deprecated: str
    requirement_level: Optional[RequirementLevel]
    requirement_level_msg: str
    sampling_relevant: bool
    note: str
    position: List[int]
    inherited: bool = False
    imported: bool = False

    def import_attribute(self):
        return replace(self, imported=True)

    def inherit_attribute(self):
        return replace(self, inherited=True)

    @property
    def is_local(self):
        return not self.imported and not self.inherited

    @property
    def is_enum(self):
        return isinstance(self.attr_type, EnumAttributeType)

    @staticmethod
    def parse(
        prefix, semconv_stability, yaml_attributes
    ) -> "Dict[str, SemanticAttribute]":
        """This method parses the yaml representation for semantic attributes
        creating the respective SemanticAttribute objects.
        """
        attributes = {}  # type: Dict[str, SemanticAttribute]
        allowed_keys = (
            "id",
            "type",
            "brief",
            "examples",
            "ref",
            "tag",
            "deprecated",
            "stability",
            "requirement_level",
            "sampling_relevant",
            "note",
        )
        if not yaml_attributes:
            return attributes

        for attribute in yaml_attributes:
            validate_values(attribute, allowed_keys)
            attr_id = attribute.get("id")
            ref = attribute.get("ref")
            position_data = attribute.lc.data
            position = position_data[next(iter(attribute))]
            if attr_id is None and ref is None:
                msg = "At least one of id or ref is required."
                raise ValidationError.from_yaml_pos(position, msg)
            if attr_id is not None:
                validate_id(attr_id, position_data["id"])
                attr_type, brief, examples = SemanticAttribute.parse_id(attribute)
                if prefix:
                    fqn = f"{prefix}.{attr_id}"
                else:
                    fqn = attr_id
            else:
                # Ref
                attr_type = None
                if "type" in attribute:
                    msg = f"Ref attribute '{ref}' must not declare a type"
                    raise ValidationError.from_yaml_pos(position, msg)
                brief = attribute.get("brief")
                examples = attribute.get("examples")
                ref = ref.strip()
                fqn = ref

            required_value_map = {
                "required": RequirementLevel.REQUIRED,
                "conditionally_required": RequirementLevel.CONDITIONALLY_REQUIRED,
                "recommended": RequirementLevel.RECOMMENDED,
                "opt_in": RequirementLevel.OPT_IN,
            }
            requirement_level_msg = ""
            requirement_level_val = attribute.get("requirement_level", "")
            requirement_level: Optional[RequirementLevel]
            if isinstance(requirement_level_val, CommentedMap):

                if len(requirement_level_val) != 1:
                    position = position_data["requirement_level"]
                    msg = "Multiple requirement_level values are not allowed!"
                    raise ValidationError.from_yaml_pos(position, msg)

                recommended_msg = requirement_level_val.get("recommended", None)
                condition_msg = requirement_level_val.get(
                    "conditionally_required", None
                )
                if condition_msg is not None:
                    requirement_level = RequirementLevel.CONDITIONALLY_REQUIRED
                    requirement_level_msg = condition_msg
                elif recommended_msg is not None:
                    requirement_level = RequirementLevel.RECOMMENDED
                    requirement_level_msg = recommended_msg
            else:
                requirement_level = required_value_map.get(requirement_level_val)

            if requirement_level_val and requirement_level is None:
                position = position_data["requirement_level"]
                msg = (
                    f"Value '{requirement_level_val}' for required field is not allowed"
                )
                raise ValidationError.from_yaml_pos(position, msg)

            if (
                requirement_level == RequirementLevel.CONDITIONALLY_REQUIRED
                and not requirement_level_msg
            ):
                position = position_data["requirement_level"]
                msg = "Missing message for conditionally required field!"
                raise ValidationError.from_yaml_pos(position, msg)

            tag = attribute.get("tag", "").strip()
            stability, deprecated = SemanticAttribute.parse_stability_deprecated(
                attribute.get("stability"), attribute.get("deprecated"), position_data
            )
            if (
                semconv_stability == StabilityLevel.DEPRECATED
                and stability is not StabilityLevel.DEPRECATED
            ):
                position = (
                    position_data["stability"]
                    if "stability" in position_data
                    else position_data["deprecated"]
                )
                msg = f"Semantic convention stability set to deprecated but attribute '{attr_id}' is {stability}"
                raise ValidationError.from_yaml_pos(position, msg)
            stability = stability or semconv_stability or StabilityLevel.STABLE
            sampling_relevant = (
                AttributeType.to_bool("sampling_relevant", attribute)
                if attribute.get("sampling_relevant")
                else False
            )
            note = attribute.get("note", "")
            fqn = fqn.strip()
            parsed_brief = TextWithLinks(brief.strip() if brief else "")
            parsed_note = TextWithLinks(note.strip())
            attr = SemanticAttribute(
                fqn=fqn,
                attr_id=attr_id,
                ref=ref,
                attr_type=attr_type,
                brief=parsed_brief,
                examples=examples,
                tag=tag,
                deprecated=deprecated,
                stability=stability,
                requirement_level=requirement_level,
                requirement_level_msg=str(requirement_level_msg).strip(),
                sampling_relevant=sampling_relevant,
                note=parsed_note,
                position=position,
            )
            if attr.fqn in attributes:
                position = position_data[list(attribute)[0]]
                msg = (
                    "Attribute id "
                    + fqn
                    + " is already present at line "
                    + str(attributes[fqn].position[0] + 1)
                )
                raise ValidationError.from_yaml_pos(position, msg)
            attributes[fqn] = attr
        return attributes

    @staticmethod
    def parse_id(attribute):
        check_no_missing_keys(attribute, ["type", "brief"])
        attr_val = attribute["type"]
        try:
            attr_type = EnumAttributeType.parse(attr_val)
        except ValidationError as e:
            if e.line != 0:  # Does the error already have a position?
                raise
            position = attribute.lc.data["type"]
            raise ValidationError.from_yaml_pos(position, e.message) from e
        brief = attribute["brief"]
        zlass = (
            AttributeType.type_mapper(attr_type)
            if isinstance(attr_type, str)
            else "enum"
        )

        examples = attribute.get("examples")
        is_simple_type = AttributeType.is_simple_type(attr_type)
        # if we are an array, examples must already be an array
        if (
            is_simple_type
            and attr_type.endswith("[]")
            and not isinstance(examples, CommentedSeq)
        ):
            position = attribute.lc.data[list(attribute)[0]]
            msg = f"Non array examples for {attr_type} are not allowed"
            raise ValidationError.from_yaml_pos(position, msg)
        if not isinstance(examples, CommentedSeq) and examples is not None:
            # TODO: If validation fails later, this will crash when trying to access position data
            # since a list, contrary to a CommentedSeq, does not have position data
            examples = [examples]
        if is_simple_type and attr_type not in (
            "boolean",
            "boolean[]",
            "int",
            "int[]",
            "double",
            "double[]",
        ):
            if not examples:
                position = attribute.lc.data[list(attribute)[0]]
                msg = f"Empty examples for {attr_type} are not allowed"
                raise ValidationError.from_yaml_pos(position, msg)

        # TODO: Implement type check for enum examples or forbid them
        if examples is not None and is_simple_type:
            AttributeType.check_examples_type(attr_type, examples, zlass)
        return attr_type, str(brief), examples

    @staticmethod
    def parse_stability_deprecated(stability, deprecated, position_data):
        if deprecated is not None and stability is None:
            stability = "deprecated"
        if deprecated is not None:
            if stability is not None and stability != "deprecated":
                position = position_data["deprecated"]
                msg = f"There is a deprecation message but the stability is set to '{stability}'"
                raise ValidationError.from_yaml_pos(position, msg)
            if AttributeType.get_type(deprecated) != "string" or deprecated == "":
                position = position_data["deprecated"]
                msg = (
                    "Deprecated field expects a string that specifies why the attribute is deprecated and/or what"
                    " to use instead! "
                )
                raise ValidationError.from_yaml_pos(position, msg)
            deprecated = deprecated.strip()
        if stability is not None:
            stability = SemanticAttribute.check_stability(
                stability,
                position_data["stability"]
                if "stability" in position_data
                else position_data["deprecated"],
            )
        return stability, deprecated

    @staticmethod
    def check_stability(stability_value, position):

        stability_value_map = {
            "deprecated": StabilityLevel.DEPRECATED,
            "experimental": StabilityLevel.EXPERIMENTAL,
            "stable": StabilityLevel.STABLE,
        }
        val = stability_value_map.get(stability_value)
        if val is not None:
            return val
        msg = f"Value '{stability_value}' is not allowed as a stability marker"
        raise ValidationError.from_yaml_pos(position, msg)

    def equivalent_to(self, other: "SemanticAttribute"):
        if self.attr_id is not None:
            if self.fqn == other.fqn:
                return True
        elif self == other:
            return True
        return False


class AttributeType:

    # https://yaml.org/type/bool.html
    bool_type_true = re.compile("y|Y|yes|Yes|YES|true|True|TRUE|on|On|ON")
    bool_type_false = re.compile("n|N|no|No|NO|false|False|FALSE|off|Off|OFF")
    bool_type = re.compile(bool_type_true.pattern + "|" + bool_type_false.pattern)

    @staticmethod
    def get_type(t):
        if isinstance(t, int):
            return "int"
        if AttributeType.bool_type.fullmatch(t):
            return "boolean"
        return "string"

    @staticmethod
    def is_simple_type(attr_type: str):
        return attr_type in (
            "string",
            "string[]",
            "int",
            "int[]",
            "double",
            "double[]",
            "boolean",
            "boolean[]",
        )

    @staticmethod
    def type_mapper(attr_type: str):
        type_mapper = {
            "int": int,
            "int[]": int,
            "double": float,
            "double[]": float,
            "string": str,
            "string[]": str,
            "boolean": bool,
            "boolean[]": bool,
        }
        return type_mapper.get(attr_type)

    @staticmethod
    def check_examples_type(attr_type, examples, zlass):
        """This method checks example are correctly typed"""
        index = -1
        for example in examples:
            index += 1
            if attr_type.endswith("[]") and isinstance(example, Iterable):
                # Multi array example
                for element in example:
                    if not isinstance(element, zlass):
                        position = examples.lc.data[index]
                        msg = f"Example with wrong type. Expected {attr_type} examples but is was {type(element)}."
                        raise ValidationError.from_yaml_pos(position, msg)
            else:  # Single value example or array example with a single example array
                if not isinstance(example, zlass):
                    position = examples.lc.data[index]
                    msg = f"Example with wrong type. Expected {attr_type} examples but is was {type(example)}."
                    raise ValidationError.from_yaml_pos(position, msg)

    @staticmethod
    def to_bool(key, parent_object):
        """This method translate yaml boolean values to python boolean values"""
        yaml_value = parent_object.get(key)
        if isinstance(yaml_value, bool):
            return yaml_value
        if isinstance(yaml_value, str):
            if AttributeType.bool_type_true.fullmatch(yaml_value):
                return True
            if AttributeType.bool_type_false.fullmatch(yaml_value):
                return False
        position = parent_object.lc.data[key]
        msg = f"Value '{yaml_value}' for {key} field is not allowed"
        raise ValidationError.from_yaml_pos(position, msg)


@dataclass
class EnumAttributeType:
    custom_values: bool
    members: "List[EnumMember]"
    enum_type: str

    def __init__(self, custom_values, members, enum_type):
        self.custom_values = custom_values
        self.members = members
        self.enum_type = enum_type

    def __str__(self):
        return self.enum_type

    @staticmethod
    def is_valid_enum_value(val):
        return isinstance(val, (int, str))

    @staticmethod
    def parse(attribute_type):
        """This method parses the yaml representation for semantic attribute types.
        If the type is an enumeration, it generated the EnumAttributeType object,
        otherwise it returns the basic type as string.
        """
        if isinstance(attribute_type, str):
            if AttributeType.is_simple_type(attribute_type):
                return attribute_type
            # Wrong type used - raise the exception and fill the missing data in the parent
            raise ValidationError(
                0, 0, f"Invalid type: {attribute_type} is not allowed"
            )
        allowed_keys = ["allow_custom_values", "members"]
        mandatory_keys = ["members"]
        validate_values(attribute_type, allowed_keys, mandatory_keys)
        custom_values = (
            bool(attribute_type.get("allow_custom_values"))
            if "allow_custom_values" in attribute_type
            else False
        )
        members = []
        if (
            not isinstance(attribute_type["members"], CommentedSeq)
            or len(attribute_type["members"]) < 1
        ):
            raise ValidationError.from_yaml_pos(
                attribute_type.lc.data["members"], "Enumeration without members!"
            )

        allowed_keys = ["id", "value", "brief", "note"]
        mandatory_keys = ["id", "value"]
        for member in attribute_type["members"]:
            validate_values(member, allowed_keys, mandatory_keys)
            if not EnumAttributeType.is_valid_enum_value(member["value"]):
                raise ValidationError.from_yaml_pos(
                    member.lc.data["value"][:2],
                    f"Invalid value used in enum: <{member['value']}>",
                )
            validate_id(member["id"], member.lc.data["id"])
            members.append(
                EnumMember(
                    member_id=member["id"],
                    value=member["value"],
                    brief=member.get("brief", member["id"]).strip(),
                    note=member.get("note", "").strip(),
                )
            )
        enum_type = AttributeType.get_type(members[0].value)
        for myaml, m in zip(attribute_type["members"], members):
            if enum_type != AttributeType.get_type(m.value):
                raise ValidationError.from_yaml_pos(
                    myaml.lc.data["value"],
                    f"Enumeration member does not have type {enum_type}!",
                )
        return EnumAttributeType(custom_values, members, enum_type)


@dataclass
class EnumMember:
    member_id: str
    value: str
    brief: str
    note: str


class MdLink:
    text: str
    url: str

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def __str__(self):
        return f"[{self.text}]({self.url})"


class TextWithLinks(str):
    parts: List[Union[str, MdLink]]
    raw_text: str
    md_link = re.compile(r"\[([^\[\]]+)\]\(([^)]+)")

    def __init__(self, text):
        super().__init__()
        self.raw_text = text
        self.parts = []
        last_position = 0
        for match in self.md_link.finditer(text):
            prev_text = text[last_position : match.start()]
            link = MdLink(match.group(1), match.group(2))
            if prev_text:
                self.parts.append(prev_text)
            self.parts.append(link)
            last_position = match.end() + 1
        last_part = text[last_position:]
        if last_part:
            self.parts.append(last_part)

    def __str__(self):
        str_list = []
        for elm in self.parts:
            str_list.append(elm.__str__())
        return "".join(str_list)
