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
    RequirementLevel,
    TextWithLinks,
)
from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
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
                str_list.append('<a href="{}">{}</a>'.format(elm.url, elm.text))
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


class CodeRenderer:
    pattern = "{{{}}}".format(ID_RE.pattern)
    matcher = re.compile(pattern)

    parameters: typing.Dict[str, str]

    @staticmethod
    def from_commandline_params(parameters=None):
        if parameters is None:
            parameters = []
        params = {}
        if parameters:
            for elm in parameters:
                pairs = elm.split(",")
                for pair in pairs:
                    (k, v) = pair.split("=")
                    params[k] = v
        return CodeRenderer(params)

    def __init__(self, parameters: typing.Dict[str, str]):
        self.parameters = parameters

    def get_data_single_file(
        self, semconvset: SemanticConventionSet, template_path: str
    ) -> dict:
        """Returns a dictionary that contains all SemanticConventions to fill the template."""
        data = {
            "template": template_path,
            "semconvs": semconvset.models,
            "attributes": semconvset.attributes(),
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
    def setup_environment(env: Environment):
        env.filters["to_doc_brief"] = to_doc_brief
        env.filters["to_const_name"] = to_const_name
        env.filters["merge"] = merge
        env.filters["to_camelcase"] = to_camelcase
        env.filters["to_html_links"] = to_html_links
        env.filters["regex_replace"] = regex_replace
        env.filters["render_markdown"] = render_markdown

    @staticmethod
    def prefix_output_file(file_name, pattern, semconv):
        basename = os.path.basename(file_name)
        dirname = os.path.dirname(file_name)
        value = getattr(semconv, pattern)
        return os.path.join(dirname, to_camelcase(value, True), basename)

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
        self.setup_environment(env)
        if pattern:
            for semconv in semconvset.models.values():
                output_name = self.prefix_output_file(output_file, pattern, semconv)
                data = self.get_data_multiple_files(semconv, template_path)
                template = env.get_template(file_name, globals=data)
                template.globals["now"] = datetime.datetime.utcnow()
                template.globals["version"] = os.environ.get("ARTIFACT_VERSION", "dev")
                template.globals["RequirementLevel"] = RequirementLevel
                template.stream(data).dump(output_name)
        else:
            data = self.get_data_single_file(semconvset, template_path)
            template = env.get_template(file_name, globals=data)
            template.globals["now"] = datetime.datetime.utcnow()
            template.globals["version"] = os.environ.get("ARTIFACT_VERSION", "dev")
            template.globals["RequirementLevel"] = RequirementLevel
            template.stream(data).dump(output_file)
