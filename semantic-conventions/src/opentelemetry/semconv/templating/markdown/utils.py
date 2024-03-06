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

import difflib
import os


class VisualDiffer:
    """Colorize differential outputs, which can be useful in development of
    semantic conventions
    """

    @staticmethod
    def colorize_text(r: int, g: int, b: int, text: str):
        """
        Colorize text according to ANSI standards
        The way this works is we send out a control character,
        then send the color information (the r,g,b parts),
        then the normal text, then an escape char to end the coloring

        ## Breakdown of magic values
        33 (octal) == 1b (hexadecimal) == ESC control character

        ESC[38 => This sets foreground color
        https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

        ESC[38;2; => Set foreground color with 24-bit color mode
        https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit

        ESC[0m => Resets foreground color (basically turn off "coloring mode")

        {r};{g};{b};m => Sets the color mode.  "m" denotes the end of the escape sequence prefix

        For more information and colors, see
        https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
        """
        escape_color_24bitmode = "\x1b[38;2"
        reset_color = "\x1b[0m"
        return f"{escape_color_24bitmode};{r};{g};{b}m{text}{reset_color}"

    @classmethod
    def removed(cls, text: str) -> str:
        return cls.colorize_text(255, 0, 0, text)

    @classmethod
    def added(cls, text: str) -> str:
        return cls.colorize_text(0, 255, 0, text)

    @classmethod
    def visual_diff(cls, a: str, b: str):
        """
        Prints git-like colored diff using ANSI terminal coloring.
        Diff is "from a to b", that is, red text is text deleted in `a`
        while green text is new to `b`
        """
        if "true" != os.environ.get("COLORED_DIFF", "false").lower():
            return "".join(difflib.context_diff(a, b))

        colored_diff = []
        diff_partitions = difflib.SequenceMatcher(None, a, b)
        for operation, a_start, a_end, b_start, b_end in diff_partitions.get_opcodes():
            if operation == "equal":
                colored_diff.append(a[a_start:a_end])
            elif operation == "insert":
                colored_diff.append(cls.added(b[b_start:b_end]))
            elif operation == "delete":
                colored_diff.append(cls.removed(a[a_start:a_end]))
            elif operation == "replace":
                colored_diff.append(cls.added(b[b_start:b_end]))
                colored_diff.append(cls.removed(a[a_start:a_end]))
            else:
                # Log.warn would be best here
                raise ValueError(
                    f"Unhandled opcode from difflib in semantic conversion markdown renderer: {operation}"
                )
        return "".join(colored_diff)
