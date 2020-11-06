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

from jinja2 import Environment, FileSystemLoader, select_autoescape

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.model.utils import ID_RE


def to_doc_brief(doc_string: typing.Optional[str]) -> str:
    if doc_string is None:
        return ""
    doc_string = doc_string.strip()
    if doc_string.endswith("."):
        return doc_string[:-1]
    return doc_string


def merge(list: typing.List, elm):
    return list.extend(elm)


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

    def get_data_multiple_files(self, semconv, template_path) -> dict:
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

    @staticmethod
    def prefix_output_file(file_name, pattern, semconv):
        base = os.path.basename(file_name)
        dir = os.path.dirname(file_name)
        value = getattr(semconv, pattern)
        return os.path.join(dir, to_camelcase(value, True), base)

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
                template = env.get_template(file_name, data)
                template.globals["now"] = datetime.datetime.utcnow()
                template.globals["version"] = os.environ.get("ARTIFACT_VERSION", "dev")
                template.stream(data).dump(output_name)
        else:
            data = self.get_data_single_file(semconvset, template_path)
            template = env.get_template(file_name, data)
            template.globals["now"] = datetime.datetime.utcnow()
            template.globals["version"] = os.environ.get("ARTIFACT_VERSION", "dev")
            template.stream(data).dump(output_file)
