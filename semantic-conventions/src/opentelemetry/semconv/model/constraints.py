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

from dataclasses import dataclass, replace
from typing import List, Tuple

from ruamel.yaml.comments import CommentedSeq

from opentelemetry.semconv.model.exceptions import ValidationError
from opentelemetry.semconv.model.semantic_attribute import SemanticAttribute
from opentelemetry.semconv.model.utils import validate_values


# We cannot frozen due to later evaluation of the attributes
@dataclass
class AnyOf:
    """Defines a constraint where at least one of the list of attributes must be set.
    The implementation of this class is evaluated in two times. At parsing time, the choice_list_ids field is
    populated. After all yaml files are parsed, the choice_list_attributes field is populated with the object
    representation of the attribute ids of choice_list_ids.

    Attributes:
        choice_list_ids             Contains the lists of attributes ids that must be set.
        inherited                   True if it is inherited by another semantic convention, i.e. by include or extends.
        choice_list_attributes      Contains the list of attributes objects. This list contains the same lists of
                                    attributes of choice_list_ids but instead of the ids, it contains the respective
                                    objects representations.
        _yaml_src_position          Contains the position in the YAML file of the AnyOf attribute
    """

    choice_list_ids: Tuple[Tuple[str, ...], ...]
    inherited: bool = False
    choice_list_attributes: Tuple[Tuple[SemanticAttribute, ...], ...] = ()
    _yaml_src_position: int = 0

    def __eq__(self, other):
        if not isinstance(other, AnyOf):
            return False
        return self.choice_list_ids == other.choice_list_ids

    def __hash__(self):
        return hash(self.choice_list_ids)

    def add_attributes(self, attr: List[SemanticAttribute]):
        self.choice_list_attributes += (attr,)

    def inherit_anyof(self):
        return replace(self, inherited=True)


@dataclass(frozen=True)
class Include:
    semconv_id: str


def parse_constraints(yaml_constraints):
    """This method parses the yaml representation for semantic convention attributes
    creating a list of Constraint objects.
    """
    constraints = ()
    allowed_keys = ("include", "any_of")
    for constraint in yaml_constraints:
        validate_values(constraint, allowed_keys)
        if len(constraint.keys()) > 1:
            position = constraint.lc.data[list(constraint)[1]]
            msg = (
                "Invalid entry in constraint array - multiple top-level keys in entry."
            )
            raise ValidationError.from_yaml_pos(position, msg)
        if "include" in constraint:
            constraints += (Include(constraint.get("include")),)
        elif "any_of" in constraint:
            choice_sets = ()
            for constraint_list in constraint.get("any_of"):
                inner_id_list = ()
                if isinstance(constraint_list, CommentedSeq):
                    inner_id_list = tuple(
                        attr_constraint for attr_constraint in constraint_list
                    )
                else:
                    inner_id_list += (constraint_list,)
                choice_sets += (inner_id_list,)
            any_of = AnyOf(choice_sets)
            any_of._yaml_src_position = constraint.get("any_of").lc.data
            constraints += (any_of,)
    return constraints

def populate_anyof_attributes(parent_id, constraints, lookup_attribute):
    any_of: AnyOf
    for any_of in constraints:
        if isinstance(any_of, AnyOf):
            for index, attr_ids in enumerate(any_of.choice_list_ids):
                constraint_attrs = []
                for attr_id in attr_ids:
                    ref_attr = lookup_attribute(attr_id)
                    if ref_attr is None:
                        raise ValidationError.from_yaml_pos(
                            any_of._yaml_src_position[index],
                            f"Any_of attribute '{attr_id}' of semantic convention "
                            f"{parent_id} does not exists!",
                        )
                    constraint_attrs.append(ref_attr)
                if constraint_attrs:
                    any_of.add_attributes(constraint_attrs)
