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

from dataclasses import dataclass, field
from typing import List

from opentelemetry.semconv.model.semantic_attribute import StabilityLevel


@dataclass()
class MarkdownOptions:

    _badge_map = {
        StabilityLevel.DEPRECATED: "![Deprecated](https://img.shields.io/badge/-deprecated-red)",
        StabilityLevel.EXPERIMENTAL: "![Experimental](https://img.shields.io/badge/-experimental-blue)",
        StabilityLevel.STABLE: "![Stable](https://img.shields.io/badge/-stable-lightgreen)",
    }

    _label_map = {
        StabilityLevel.DEPRECATED: "**Deprecated: {}**",
        StabilityLevel.EXPERIMENTAL: "**Experimental**",
        StabilityLevel.STABLE: "**Stable**",
    }

    check_only: bool = False
    enable_stable: bool = False
    enable_experimental: bool = False
    enable_deprecated: bool = True
    use_badge: bool = False
    break_count: int = 50
    exclude_files: List[str] = field(default_factory=list)

    @property
    def md_snippet_by_stability_level(self):
        if self.use_badge:
            return self._badge_map
        return self._label_map
