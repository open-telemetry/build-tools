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

import datetime
import os.path
import re
import typing

import mistune
from jinja2 import Environment, FileSystemLoader, select_autoescape

from opentelemetry.semconv.model.semantic_attribute import (
    AttributeType,
    RequirementLevel,
    SemanticAttribute,
    StabilityLevel,
    TextWithLinks,
)
from opentelemetry.semconv.model.semantic_convention import (
    BaseSemanticConvention,
    MetricSemanticConvention,
    SemanticConventionSet,
)
from opentelemetry.semconv.model.utils import ID_RE


def render_markdown(
    txt: str,
    html=True,
    link=None,
    image=None,
    emphasis=None,
    strong=None,
    inline_html=None,
    paragraph=None,
    heading=None,
    block_code=None,
    block_quote=None,
    list=None,  # pylint:disable=redefined-builtin
    list_item=None,
    code=None,
):
    class CustomRender(mistune.HTMLRenderer):
        def link(self, url, text=None, title=None):  # pylint:disable=arguments-renamed
            if link:
                return link.format(url, text, title)
            return super().link(url, text, title) if html else url

        def image(self, src, alt="", title=None):
            if image:
                return image.format(src, alt, title)
            return super().image(src, alt, title) if html else src

        def emphasis(self, text):
            if emphasis:
                return emphasis.format(text)
            return super().emphasis(text) if html else text

        def strong(self, text):
            if strong:
                return strong.format(text)
            return super().strong(text) if html else text

        def inline_html(self, html_text):  # pylint:disable=arguments-renamed
            if inline_html:
                return inline_html.format(html_text)
            return super().inline_html(html_text) if html else html_text

        def paragraph(self, text):
            if paragraph:
                return paragraph.format(text)
            return super().paragraph(text) if html else text

        def heading(self, text, level):
            if heading:
                return heading.format(text, level)
            return super().heading(text, level) if html else text

        def block_code(self, code, info=None):
            if block_code:
                return block_code.format(code)
            return super().block_code(code, info) if html else code

        def block_quote(self, text):
            if block_quote:
                return block_quote.format(text)
            return super().block_quote(text)

        def list(self, text, ordered, level, start=None):
            if list:
                return list.format(text)
            return super().list(text, ordered, level, start) if html else text

        def list_item(self, text, level):
            if list_item:
                return list_item.format(text)
            return super().list_item(text, level) if html else text

        def codespan(self, text):
            if code:
                return code.format(text)
            return super().codespan(text) if html else text

    markdown = mistune.create_markdown(renderer=CustomRender())
    return markdown(txt)


def to_doc_brief(doc_string: typing.Optional[str]) -> str:
    if doc_string is None:
        return ""
    doc_string = doc_string.strip()
    if doc_string.endswith("."):
        return doc_string[:-1]
    return doc_string


def to_html_links(doc_string: typing.Optional[typing.Union[str, TextWithLinks]]) -> str:
    if doc_string is None:
        return ""
    if isinstance(doc_string, TextWithLinks):
        str_list = []
        for elm in doc_string.parts:
            if isinstance(elm, str):
                str_list.append(elm)
            else:
                str_list.append(f'<a href="{elm.url}">{elm.text}</a>')
        doc_string = "".join(str_list)
    doc_string = doc_string.strip()
    if doc_string.endswith("."):
        return doc_string[:-1]
    return doc_string


def regex_replace(text: str, pattern: str, replace: str):
    # convert standard dollar notation to python
    replace = re.sub(r"\$", r"\\", replace)  # TODO This is *very* surprising behavior
    return re.sub(pattern, replace, text, 0, re.U)


def merge(elems: typing.List, elm):
    return elems.extend(elm)


def to_const_name(name: str) -> str:
    return name.upper().replace(".", "_").replace("-", "_")


def to_camelcase(name: str, first_upper=False) -> str:
    first, *rest = name.replace("_", ".").split(".")
    if first_upper:
        first = first.capitalize()
    return first + "".join(word.capitalize() for word in rest)


def first_up(name: str) -> str:
    return name[0].upper() + name[1:]


def is_stable(obj: typing.Union[SemanticAttribute, BaseSemanticConvention]) -> bool:
    return obj.stability == StabilityLevel.STABLE


def is_deprecated(obj: typing.Union[SemanticAttribute, BaseSemanticConvention]) -> bool:
    return obj.stability == StabilityLevel.DEPRECATED


def is_experimental(
    obj: typing.Union[SemanticAttribute, BaseSemanticConvention]
) -> bool:
    return obj.stability is None or obj.stability == StabilityLevel.EXPERIMENTAL


def is_definition(attribute: SemanticAttribute) -> bool:
    return attribute.is_local and attribute.ref is None


def is_template(attribute: SemanticAttribute) -> bool:
    return AttributeType.is_template_type(str(attribute.attr_type))


def is_metric(semconv: BaseSemanticConvention) -> bool:
    return isinstance(semconv, MetricSemanticConvention)


class CodeRenderer:
    pattern = f"{{{ID_RE.pattern}}}"

    parameters: typing.Dict[str, str]
    trim_whitespace: bool

    @staticmethod
    def from_commandline_params(parameters=None, trim_whitespace=False):
        if parameters is None:
            parameters = []
        params = {}
        if parameters:
            for elm in parameters:
                pairs = elm.split(",")
                for pair in pairs:
                    (k, v) = pair.split("=")
                    params[k] = v
        return CodeRenderer(params, trim_whitespace)

    def __init__(self, parameters: typing.Dict[str, str], trim_whitespace: bool):
        self.parameters = parameters
        self.trim_whitespace = trim_whitespace

    def get_data_single_file(
        self, semconvset: SemanticConventionSet, template_path: str
    ) -> dict:
        """Returns a dictionary that contains all SemanticConventions to fill the template."""
        data = {
            "template": template_path,
            "semconvs": semconvset.models,
            "attributes": semconvset.attributes(),
            "attribute_templates": semconvset.attribute_templates(),
            "attributes_and_templates": self._grouped_attribute_definitions(semconvset),
        }
        data.update(self.parameters)
        return data

    def get_data_multiple_files(
        self, semconv, template_path
    ) -> typing.Dict[str, typing.Any]:
        """Returns a dictionary with the data from a single SemanticConvention to fill the template."""
        data = {"template": template_path, "semconv": semconv}
        data.update(self.parameters)
        return data

    @staticmethod
    def setup_environment(env: Environment, trim_whitespace: bool):
        env.filters["to_doc_brief"] = to_doc_brief
        env.filters["to_const_name"] = to_const_name
        env.filters["merge"] = merge
        env.filters["to_camelcase"] = to_camelcase
        env.filters["first_up"] = first_up
        env.filters["to_html_links"] = to_html_links
        env.filters["regex_replace"] = regex_replace
        env.filters["render_markdown"] = render_markdown
        env.filters["is_deprecated"] = is_deprecated
        env.filters["is_definition"] = is_definition
        env.filters["is_stable"] = is_stable
        env.filters["is_experimental"] = is_experimental
        env.filters["is_template"] = is_template
        env.filters["is_metric"] = is_metric
        env.tests["is_stable"] = is_stable
        env.tests["is_experimental"] = is_experimental
        env.tests["is_deprecated"] = is_deprecated
        env.tests["is_definition"] = is_definition
        env.tests["is_template"] = is_template
        env.tests["is_metric"] = is_metric
        env.trim_blocks = trim_whitespace
        env.lstrip_blocks = trim_whitespace

    @staticmethod
    def prefix_output_file(env, file_name, prefix):
        # TODO - We treat incoming file names as a pattern.
        # We allow will give them access to the same jinja model as file creation
        # and we'll make sure a few things are available there, specifically:
        # camelcase_file_name, raw_file_name, ...
        data={
            "prefix": prefix,
            "camelcase_prefix": to_camelcase(prefix, True),
            # TODO Pascal version
            # TODO snake_case
        }
        print("[JOSH] Creating filename [", file_name, "] with data: ", data, "\n")
        template = env.from_string(file_name)
        full_name = template.render(data)
        dirname = os.path.dirname(full_name)
        basename = os.path.basename(full_name)
        print("[JOSH] Writing to file: ", os.path.join(dirname, basename), "\n")
        return os.path.join(dirname, basename)

    def render(
        self,
        semconvset: SemanticConventionSet,
        template_path: str,
        output_file,
        pattern: str,
    ):
        file_name = os.path.basename(template_path)
        folder = os.path.dirname(template_path)
        env = Environment(
            loader=FileSystemLoader(searchpath=folder),
            autoescape=select_autoescape([""]),
        )
        self.setup_environment(env, self.trim_whitespace)
        if pattern == "root_namespace":
            self._render_group_by_root_namespace(
                semconvset, template_path, file_name, output_file, env
            )
        elif pattern is not None:
            self._render_by_pattern(
                semconvset, template_path, file_name, output_file, pattern, env
            )
        else:
            data = self.get_data_single_file(semconvset, template_path)
            template = env.get_template(file_name, globals=data)
            self._write_template_to_file(template, data, output_file)

    def _render_by_pattern(
        self,
        semconvset: SemanticConventionSet,
        template_path: str,
        file_name: str,
        output_file: str,
        pattern: str,
        env: Environment,
    ):
        for semconv in semconvset.models.values():
            prefix = getattr(semconv, pattern)
            output_name = self.prefix_output_file(env, output_file, prefix)
            data = self.get_data_multiple_files(semconv, template_path)
            template = env.get_template(file_name, globals=data)
            self._write_template_to_file(template, data, output_name)

    def _render_group_by_root_namespace(
        self,
        semconvset: SemanticConventionSet,
        template_path: str,
        file_name: str,
        output_file: str,
        env: Environment,
    ):
        attribute_and_templates = self._grouped_attribute_definitions(semconvset)
        metrics = self._grouped_metric_definitions(semconvset)
        for ns, attribute_and_templates in attribute_and_templates.items():
            sanitized_ns = ns if ns != "" else "other"
            output_name = self.prefix_output_file(env, output_file, sanitized_ns)

            data = {
                "template": template_path,
                "attributes_and_templates": attribute_and_templates,
                "metrics": metrics.get(ns) or [],
                "root_namespace": sanitized_ns,
            }
            data.update(self.parameters)

            template = env.get_template(file_name, globals=data)
            self._write_template_to_file(template, data, output_name)

    def _grouped_attribute_definitions(self, semconvset):
        grouped_attributes = {}
        for semconv in semconvset.models.values():
            for attr in semconv.attributes_and_templates:
                if not is_definition(attr):  # skip references
                    continue
                if attr.root_namespace not in grouped_attributes:
                    grouped_attributes[attr.root_namespace] = []
                grouped_attributes[attr.root_namespace].append(attr)

        for ns in grouped_attributes:
            grouped_attributes[ns] = sorted(grouped_attributes[ns], key=lambda a: a.fqn)
        return grouped_attributes

    def _grouped_metric_definitions(self, semconvset):
        grouped_metrics = {}
        for semconv in semconvset.models.values():
            if not is_metric(semconv):
                continue

            if semconv.root_namespace not in grouped_metrics:
                grouped_metrics[semconv.root_namespace] = []

            grouped_metrics[semconv.root_namespace].append(semconv)

        for ns in grouped_metrics:
            grouped_metrics[ns] = sorted(
                grouped_metrics[ns], key=lambda a: a.metric_name
            )
        return grouped_metrics

    def _write_template_to_file(self, template, data, output_name):
        template.globals["now"] = datetime.datetime.utcnow()
        template.globals["version"] = os.environ.get("ARTIFACT_VERSION", "dev")
        template.globals["RequirementLevel"] = RequirementLevel

        content = template.render(data)
        if content != "":
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(content)
