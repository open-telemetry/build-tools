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

import glob
import io
import os
import re
import sys
import typing
from pathlib import PurePath

from opentelemetry.semconv.model.constraints import AnyOf, Include
from opentelemetry.semconv.model.semantic_attribute import (
    AttributeType,
    EnumAttributeType,
    EnumMember,
    RequirementLevel,
    SemanticAttribute,
    StabilityLevel,
)
from opentelemetry.semconv.model.semantic_convention import (
    BaseSemanticConvention,
    EventSemanticConvention,
    MetricSemanticConvention,
    SemanticConventionSet,
    UnitSemanticConvention,
)
from opentelemetry.semconv.model.utils import ID_RE
from opentelemetry.semconv.templating.markdown.options import MarkdownOptions

_REQUIREMENT_LEVEL_URL = (
    "https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/"
)


class RenderContext:
    def __init__(self):
        self.is_full = False
        self.is_remove_constraint = False
        self.is_metric_table = False
        self.is_omit_requirement_level = False
        self.group_key = ""
        self.enums = []
        self.notes = []
        self.units = []
        self.current_md = ""
        self.current_semconv = None

    def clear_table_generation(self):
        self.notes = []
        self.enums = []

    def add_note(self, msg: str):
        self.notes.append(msg)

    def add_enum(self, attr: SemanticAttribute):
        self.enums.append(attr)


class MarkdownRenderer:
    p_start = re.compile("<!--\\s*semconv\\s+(.+)-->")
    p_semconv_selector = re.compile(
        rf"(?P<semconv_id>{ID_RE.pattern})(?:\((?P<parameters>.*)\))?"
    )
    p_end = re.compile("<!--\\s*endsemconv\\s*-->")
    default_break_conditional_labels = 50
    valid_parameters = [
        "tag",
        "full",
        "remove_constraints",
        "metric_table",
        "omit_requirement_level",
    ]

    prelude = "<!-- semconv {} -->\n"

    def __init__(
        self, md_folder, semconvset: SemanticConventionSet, options=MarkdownOptions()
    ):
        self.options = options
        self.render_ctx = RenderContext()
        self.semconvset = semconvset
        # We load all markdown files to render
        self.file_names = sorted(
            set(glob.glob(f"{md_folder}/**/*.md", recursive=True))
            - set(options.exclude_files)
        )
        # We build the dict that maps each attribute that has to be rendered to the latest visited file
        # that contains it
        self.filename_for_attr_fqn = self._create_attribute_location_dict()

        req_level = f"[Requirement Level]({_REQUIREMENT_LEVEL_URL})"

        self.table_headers = (
            f"| Attribute  | Type | Description  | Examples  | {req_level} |"
            "\n|---|---|---|---|---|\n"
        )
        self.table_headers_omitting_req_level = (
            "| Attribute  | Type | Description  | Examples  |\n|---|---|---|---|\n"
        )

    def to_markdown_attr(
        self,
        attribute: SemanticAttribute,
        output: io.StringIO,
    ):
        """
        This method renders attributes as markdown table entry
        """
        name = self.render_fqn_for_attribute(attribute)
        attr_type = (
            "enum"
            if isinstance(attribute.attr_type, EnumAttributeType)
            else AttributeType.get_instantiated_type(attribute.attr_type)
        )
        description = (
            self._description_with_badge(attribute.stability, attribute.deprecated)
            + attribute.brief
        )
        if attribute.note:
            self.render_ctx.add_note(attribute.note)
            description += f" [{len(self.render_ctx.notes)}]"
        examples = ""
        if isinstance(attribute.attr_type, EnumAttributeType):
            if self.render_ctx.is_full or (attribute.is_local and not attribute.ref):
                self.render_ctx.add_enum(attribute)
            example_list = attribute.examples if attribute.examples else ()
            examples = (
                "; ".join(f"`{ex}`" for ex in example_list)
                if example_list
                else f"`{attribute.attr_type.members[0].value}`"
            )
            # Add better type info to enum
            if attribute.attr_type.custom_values:
                attr_type = attribute.attr_type.enum_type
            else:
                attr_type = attribute.attr_type.enum_type
        elif attribute.attr_type:
            example_list = attribute.examples if attribute.examples else []
            # check for array types
            if attribute.attr_type.endswith("[]"):
                examples = "`[" + ", ".join(f"{ex}" for ex in example_list) + "]`"
            else:
                examples = "; ".join(f"`{ex}`" for ex in example_list)

        if self.render_ctx.is_omit_requirement_level:
            output.write(f"| {name} | {attr_type} | {description} | {examples} |\n")
        else:
            required = self.derive_requirement_level(attribute)
            output.write(
                f"| {name} | {attr_type} | {description} | {examples} | {required} |\n"
            )

    def derive_requirement_level(self, attribute: SemanticAttribute):
        if attribute.requirement_level == RequirementLevel.REQUIRED:
            required = "`Required`"
        elif attribute.requirement_level == RequirementLevel.CONDITIONALLY_REQUIRED:
            if len(attribute.requirement_level_msg) < self.options.break_count:
                required = "`Conditionally Required` " + attribute.requirement_level_msg
            else:
                # We put the condition in the notes after the table
                self.render_ctx.add_note(attribute.requirement_level_msg)
                required = f"`Conditionally Required` [{len(self.render_ctx.notes)}]"
        elif attribute.requirement_level == RequirementLevel.OPT_IN:
            required = "Opt-In"
        else:  # attribute.requirement_level == Required.RECOMMENDED or None
            # check if there are any notes
            if (
                not self.render_ctx.is_remove_constraint
                and self.render_ctx.current_semconv.has_attribute_constraint(attribute)
            ):
                required = "See below"
            else:
                if not attribute.requirement_level_msg:
                    required = "`Recommended`"
                elif len(attribute.requirement_level_msg) < self.options.break_count:
                    required = "`Recommended` " + attribute.requirement_level_msg
                else:
                    # We put the condition in the notes after the table
                    self.render_ctx.add_note(attribute.requirement_level_msg)
                    required = f"`Recommended` [{len(self.render_ctx.notes)}]"
        return required

    def write_table_header(self, output: io.StringIO):
        if self.render_ctx.is_omit_requirement_level:
            output.write(self.table_headers_omitting_req_level)
        else:
            output.write(self.table_headers)

    def to_markdown_attribute_table(
        self, semconv: BaseSemanticConvention, output: io.StringIO
    ):
        attr_to_print = []
        for attr in semconv.attributes_and_templates:
            if self.render_ctx.group_key is not None:
                if attr.tag == self.render_ctx.group_key:
                    attr_to_print.append(attr)
                continue
            if self.render_ctx.is_full or attr.is_local:
                attr_to_print.append(attr)

        if self.render_ctx.group_key is not None and not attr_to_print:
            raise ValueError(
                f"No attributes retained for '{semconv.semconv_id}' filtering by '{self.render_ctx.group_key}'"
            )
        if attr_to_print:
            self.write_table_header(output)
            for attr in attr_to_print:
                self.to_markdown_attr(attr, output)
        attr_sampling_relevant = [
            attr for attr in attr_to_print if attr.sampling_relevant
        ]
        self.to_markdown_notes(output)
        self.to_creation_time_attributes(attr_sampling_relevant, output)

    def to_markdown_metric_table(
        self, semconv: MetricSemanticConvention, output: io.StringIO
    ):
        """
        This method renders metrics as markdown table entry
        """
        if not isinstance(semconv, MetricSemanticConvention):
            raise ValueError(
                f"semconv `{semconv.semconv_id}` was specified with `metric_table`, but it is not a metric convention"
            )

        instrument = MetricSemanticConvention.canonical_instrument_name_by_yaml_name[
            semconv.instrument
        ]
        output.write(
            "| Name     | Instrument Type | Unit (UCUM) | Description    |\n"
            "| -------- | --------------- | ----------- | -------------- |\n"
        )

        description = self._description_with_badge(semconv.stability, semconv.deprecated) + semconv.brief
        if semconv.note:
            self.render_ctx.add_note(semconv.note)
            description += f" [{len(self.render_ctx.notes)}]"

        output.write(
            f"| `{semconv.metric_name}` | {instrument} | `{semconv.unit}` | {description} |\n"
        )
        self.to_markdown_notes(output)

    def to_markdown_anyof(self, anyof: AnyOf, output: io.StringIO):
        """
        This method renders anyof constraints into markdown lists
        """
        if anyof.inherited and not self.render_ctx.is_full:
            return
        output.write(
            "\n**Additional attribute requirements:** At least one of the following sets of attributes is "
            "required:\n\n"
        )
        for choice in anyof.choice_list_ids:
            output.write("* ")
            list_of_choice = ", ".join(self.render_attribute_id(c) for c in choice)
            output.write(list_of_choice)
            output.write("\n")

    def to_markdown_notes(self, output: io.StringIO):
        """Renders notes after a Semantic Convention Table
        :return:
        """
        counter = 1
        for note in self.render_ctx.notes:
            output.write(f"\n**[{counter}]:** {note}\n")
            counter += 1

    def to_creation_time_attributes(
        self,
        sampling_relevant_attrs: typing.List[SemanticAttribute],
        output: io.StringIO,
    ):
        """Renders list of attributes that MUST be provided at creation time
        :return:
        """
        if sampling_relevant_attrs:
            output.write(
                "\nThe following attributes can be important for making sampling decisions "
                + "and SHOULD be provided **at span creation time** (if provided at all):\n\n"
            )

            for attr in sampling_relevant_attrs:
                output.write("* " + self.render_fqn_for_attribute(attr) + "\n")

    @staticmethod
    def to_markdown_unit_table(members, output: io.StringIO):
        output.write("\n")
        output.write(
            "| Name        | Kind of Quantity         | Unit String   |\n"
            "| ------------| ----------------         | -----------   |"
        )
        for member in members.values():
            output.write(f"\n| {member.id} | {member.brief} | `{member.value}` |")
        output.write("\n")

    def to_markdown_enum(self, output: io.StringIO):
        """Renders enum types after a Semantic Convention Table
        :return:
        """
        attr: SemanticAttribute
        for attr in self.render_ctx.enums:
            enum = typing.cast(EnumAttributeType, attr.attr_type)
            output.write("\n`" + attr.fqn + "` ")
            if enum.custom_values:
                output.write(
                    "has the following list of well-known values."
                    + " If one of them applies, then the respective value MUST be used;"
                    + " otherwise, a custom value MAY be used."
                )
            else:
                output.write("MUST be one of the following:")
            output.write("\n\n")
            output.write("| Value  | Description |\n|---|---|")
            member: EnumMember
            counter = 1
            notes = []
            for member in enum.members:
                description = (
                    self._description_with_badge(member.stability, member.deprecated)
                    + member.brief
                )
                if member.note:
                    description += f" [{counter}]"
                    counter += 1
                    notes.append(member.note)
                output.write(f"\n| `{member.value}` | {description} |")
            counter = 1
            if not notes:
                output.write("\n")
            for note in notes:
                output.write(f"\n\n**[{counter}]:** {note}")
                counter += 1
            if notes:
                output.write("\n")

    def render_fqn_for_attribute(self, attribute):
        rel_path = self.get_attr_reference_relative_path(attribute.fqn)
        name = attribute.fqn
        if AttributeType.is_template_type(attribute.attr_type):
            name = f"{attribute.fqn}.<key>"

        if rel_path is not None:
            return f"[`{name}`]({rel_path})"
        return f"`{name}`"

    def render_attribute_id(self, attribute_id):
        """
        Method to render in markdown an attribute id. If the id points to an attribute in another rendered table, a
        markdown link is introduced.
        """
        rel_path = self.get_attr_reference_relative_path(attribute_id)
        if rel_path is not None:
            return f"[`{attribute_id}`]({rel_path})"
        return f"`{attribute_id}`"

    def get_attr_reference_relative_path(self, attribute_id):
        md_file = self.filename_for_attr_fqn.get(attribute_id)
        if md_file:
            path = PurePath(self.render_ctx.current_md)
            if path.as_posix() != PurePath(md_file).as_posix():
                rel_path = PurePath(
                    os.path.relpath(md_file, start=path.parent)
                ).as_posix()
                if rel_path != ".":
                    return rel_path
        return None

    def to_markdown_constraint(
        self,
        obj: typing.Union[AnyOf, Include],
        output: io.StringIO,
    ):
        """
        Entry method to translate attributes and constraints of a semantic convention into Markdown
        """
        if isinstance(obj, AnyOf):
            self.to_markdown_anyof(obj, output)
        elif not isinstance(obj, Include):
            raise TypeError(f"Trying to generate Markdown for a wrong type {type(obj)}")

    def render_md(self):
        for md_filename in self.file_names:
            with open(md_filename, encoding="utf-8") as md_file:
                content = md_file.read()
                output = io.StringIO()
                self._render_single_file(content, md_filename, output)
            if self.options.check_only:
                if content != output.getvalue():
                    sys.exit(
                        "File "
                        + md_filename
                        + " contains a table that would be reformatted."
                    )
            else:
                with open(md_filename, "w", encoding="utf-8") as md_file:
                    md_file.write(output.getvalue())
        if self.options.check_only:
            print(f"{len(self.file_names)} files left unchanged.")

    def _create_attribute_location_dict(self):
        """
        This method creates a dictionary that associates each attribute with the latest table in which it is rendered.
        This is required by the ref attributes to point to the correct file
        """
        m = {}
        for md in self.file_names:
            with open(md, "r", encoding="utf-8") as markdown:
                self.current_md = md
                content = markdown.read()
                for match in self.p_start.finditer(content):
                    semconv_id, _ = self._parse_semconv_selector(match.group(1).strip())
                    semconv = self.semconvset.models.get(semconv_id)
                    if not semconv:
                        raise ValueError(
                            f"Semantic Convention ID {semconv_id} not found"
                        )
                    valid_attr = (
                        a
                        for a in semconv.attributes_and_templates
                        if a.is_local and not a.ref
                    )
                    for attr in valid_attr:
                        m[attr.fqn] = md
        return m

    def _parse_semconv_selector(self, selector: str):
        semconv_id = selector
        parameters = {}
        m = self.p_semconv_selector.match(selector)
        if m:
            semconv_id = m.group("semconv_id")
            pars = m.group("parameters")
            if pars:
                for par in pars.split(","):
                    key_value = par.split("=")
                    if len(key_value) > 2:
                        raise ValueError(
                            "Wrong syntax in "
                            + m.group(4)
                            + " in "
                            + self.render_ctx.current_md
                        )
                    key = key_value[0].strip()
                    if key not in self.valid_parameters:
                        raise ValueError(
                            "Unexpected parameter `"
                            + key_value[0]
                            + "` in "
                            + self.render_ctx.current_md
                        )
                    if key in parameters:
                        raise ValueError(
                            "Parameter `"
                            + key_value[0]
                            + "` already defined in "
                            + self.render_ctx.current_md
                        )
                    value = key_value[1] if len(key_value) == 2 else ""
                    parameters[key] = value
        return semconv_id, parameters

    def _render_single_file(self, content: str, md: str, output: io.StringIO):
        last_match = 0
        self.render_ctx.current_md = md
        # The current implementation swallows nested semconv tags
        while True:
            match = self.p_start.search(content, last_match)
            if not match:
                break
            semconv_id, parameters = self._parse_semconv_selector(
                match.group(1).strip()
            )
            semconv = self.semconvset.models.get(semconv_id)
            if not semconv:
                # We should not fail here since we would detect this earlier
                # But better be safe than sorry
                raise ValueError(f"Semantic Convention ID {semconv_id} not found")
            output.write(content[last_match : match.start(0)])
            self._render_group(semconv, parameters, output)
            end_match = self.p_end.search(content, last_match)
            if not end_match:
                raise ValueError("Missing ending <!-- endsemconv --> tag")
            last_match = end_match.end()
        output.write(content[last_match:])

    def _render_group(self, semconv, parameters, output):
        header: str
        header = semconv.semconv_id
        if parameters:
            header += "("
            header += ",".join(
                par + "=" + val if val else par for par, val in parameters.items()
            )
            header = header + ")"
        output.write(MarkdownRenderer.prelude.format(header))
        self.render_ctx.clear_table_generation()
        self.render_ctx.current_semconv = semconv
        self.render_ctx.is_remove_constraint = "remove_constraints" in parameters
        self.render_ctx.group_key = parameters.get("tag")
        self.render_ctx.is_full = "full" in parameters
        self.render_ctx.is_metric_table = "metric_table" in parameters
        self.render_ctx.is_omit_requirement_level = (
            "omit_requirement_level" in parameters
        )

        if self.render_ctx.is_metric_table:
            self.to_markdown_metric_table(semconv, output)
        else:
            if isinstance(semconv, EventSemanticConvention):
                output.write(f"The event name MUST be `{semconv.name}`.\n\n")
            self.to_markdown_attribute_table(semconv, output)

        if not self.render_ctx.is_remove_constraint:
            for cnst in semconv.constraints:
                self.to_markdown_constraint(cnst, output)
        self.to_markdown_enum(output)

        if isinstance(semconv, UnitSemanticConvention):
            self.to_markdown_unit_table(semconv.members, output)

        output.write("<!-- endsemconv -->")

    def _description_with_badge(self, stability: StabilityLevel, deprecated: str):
        description = ""
        if deprecated and self.options.enable_deprecated:
            if "deprecated" in deprecated.lower():
                description = f"**{deprecated}**<br>"
            else:
                deprecated_msg = self.options.deprecated_md_snippet().format(deprecated)
                description = f"{deprecated_msg}<br>"
        elif stability == StabilityLevel.STABLE and self.options.enable_stable:
            description = f"{self.options.stable_md_snippet()}<br>"
        elif (
            stability == StabilityLevel.EXPERIMENTAL
            and self.options.enable_experimental
        ):
            description = f"{self.options.experimental_md_snippet()}<br>"

        return description
