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
from typing import Tuple  # noqa: F401

from opentelemetry.semconv.model.exceptions import ValidationError

ID_RE = re.compile("([a-z](\\.?[a-z0-9_-]+)+)")
"""Identifiers must start with a lowercase ASCII letter and
contain only lowercase, digits 0-9, underscore, dash (not recommended) and dots.
Each dot must be followed by at least one allowed non-dot character."""


def validate_id(semconv_id, position, validation_ctx):
    if not ID_RE.fullmatch(semconv_id):
        validation_ctx.raise_or_warn(
            position,
            f"Invalid id {semconv_id}. Semantic Convention ids MUST match {ID_RE.pattern}",
            semconv_id,
        )


def validate_values(yaml, keys, validation_ctx, mandatory=()):
    """This method checks only valid keywords and value types are used"""
    id = yaml.get("id")
    unwanted = [k for k in yaml.keys() if k not in keys]
    if unwanted:
        position = yaml.lc.data[unwanted[0]]
        msg = f"Invalid keys: {unwanted}"
        validation_ctx.raise_or_warn(position, msg, id)
    if mandatory:
        check_no_missing_keys(yaml, mandatory, validation_ctx)


def check_no_missing_keys(yaml, mandatory, validation_ctx):
    missing = list(set(mandatory) - set(yaml))
    if missing:
        position = (yaml.lc.line, yaml.lc.col)
        msg = f"Missing keys: {missing}"
        validation_ctx.raise_or_warn(position, msg, yaml.get("id"))


class ValidatableYamlNode:

    allowed_keys = ()  # type: Tuple[str, ...]
    mandatory_keys = ("id", "brief")  # type: Tuple[str, ...]

    def __init__(self, yaml_node, validation_ctx):
        self.id = yaml_node.get("id").strip()
        self.brief = str(yaml_node.get("brief")).strip()
        self.validation_ctx = validation_ctx

        self._position = (yaml_node.lc.line, yaml_node.lc.col)

    @classmethod
    def validate_keys(cls, node, validation_ctx):
        unwanted = [key for key in node.keys() if key not in cls.allowed_keys]
        if unwanted:
            position = node.lc.data[unwanted[0]]
            msg = f"Invalid keys: {unwanted}"
            validation_ctx.raise_or_warn(position, msg, node.get("id"))

        if cls.mandatory_keys:
            check_no_missing_keys(node, cls.mandatory_keys, validation_ctx)

    def validate_values(self):
        """
        Subclasses may provide additional validation.
        This method should raise an exception with a descriptive
        message if the semantic convention is not valid.
        """
        validate_id(self.id, self._position, self.validation_ctx)


class ValidationContext:
    def __init__(self, file_name: str, strict_validation: bool):
        self.strict_validation = strict_validation
        self.file_name = file_name

    def raise_or_warn(self, pos, msg, fqn):
        # the yaml parser starts counting from 0
        # while in document is usually reported starting from 1
        error = ValidationError(pos[0] + 1, pos[1] + 1, msg, fqn)
        if self.strict_validation:
            raise error
        else:
            print(f"[Warning] {self.file_name}: {error}\n")
