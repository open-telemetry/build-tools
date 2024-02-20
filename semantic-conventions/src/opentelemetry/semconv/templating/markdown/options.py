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


@dataclass()
class MarkdownOptions:
    check_only: bool = False
    check_compatibility_with: str = None
    enable_stable: bool = False
    enable_experimental: bool = False
    enable_deprecated: bool = True
    use_badge: bool = False
    break_count: int = 50
    exclude_files: List[str] = field(default_factory=list)

    def stable_md_snippet(self):
        if self.use_badge:
            return "![Stable](https://img.shields.io/badge/-stable-lightgreen)"
        return "**Stable**"

    def experimental_md_snippet(self):
        if self.use_badge:
            return "![Experimental](https://img.shields.io/badge/-experimental-blue)"
        return "**Experimental**"

    def deprecated_md_snippet(self):
        if self.use_badge:
            return "![Deprecated](https://img.shields.io/badge/-deprecated-red)"
        return "**Deprecated: {}**"
