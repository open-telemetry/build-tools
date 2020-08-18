#!/usr/bin/env python3

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

import argparse
import glob
import sys
from typing import List

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer

from opentelemetry.semconv.templating.markdown import MarkdownRenderer


def parse_semconv(args, parser) -> SemanticConventionSet:
    semconv = SemanticConventionSet(args.debug)
    find_yaml(args)
    for file in sorted(args.files):
        if not file.endswith(".yaml") and not file.endswith(".yml"):
            parser.error("{} is not a yaml file.".format(file))
        semconv.parse(file)
    semconv.finish()
    if semconv.has_error():
        sys.exit(1)
    return semconv


def exclude_file_list(folder: str, pattern: str) -> List[str]:
    if not pattern:
        return []
    sep = "/"
    if folder.endswith("/"):
        sep = ""
    file_names = glob.glob(folder + sep + pattern, recursive=True)
    return file_names


def main():
    parser = setup_parser()
    args = parser.parse_args()
    check_args(args, parser)
    semconv = parse_semconv(args, parser)

    if args.flavor == "code":
        renderer = CodeRenderer.from_commandline_params(args.parameters)
        renderer.render(semconv, args.template, args.output, args.pattern)
    elif args.flavor == "markdown":
        process_markdown(semconv, args)


def process_markdown(semconv, args):
    exclude = exclude_file_list(args.markdown_root, args.exclude)
    md_renderer = MarkdownRenderer(
        args.markdown_root, semconv, exclude, args.md_break_conditional, args.md_check
    )
    md_renderer.render_md()


def find_yaml(args):
    if args.yaml_root is not None:
        exclude = set(
            exclude_file_list(args.yaml_root if args.yaml_root else "", args.exclude)
        )
        yaml_files = set(
            glob.glob("{}/**/*.yaml".format(args.yaml_root), recursive=True)
        ).union(set(glob.glob("{}/**/*.yml".format(args.yaml_root), recursive=True)))
        file_names = yaml_files - exclude
        args.files.extend(file_names)


def check_args(arguments, parser):
    files = arguments.yaml_root is None and len(arguments.files) == 0
    if files:
        parser.error("Either --yaml-root or YAML_FILE must be present")


def add_code_parser(subparsers):
    parser = subparsers.add_parser("code")
    parser.add_argument(
        "--output",
        "-o",
        help="Specify the output file for the code generation.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--template",
        "-t",
        help="Specify the template to use for code generation",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--file-per-group",
        dest="pattern",
        help="Each Semantic Convention is processed by the template and store in a different file. PATTERN is expected "
        "to be the name of a SemanticConvention field and is prepended as a prefix to the output argument",
        type=str,
    )
    parser.add_argument(
        "--parameters",
        "-D",
        dest="parameters",
        action="append",
        help="List of key=value pairs separated by comma. These values are fed into the template as is.",
        type=str,
    )


def add_md_parser(subparsers):
    parser = subparsers.add_parser("markdown")
    parser.add_argument(
        "--markdown-root",
        "-md",
        help="Specify folder of the markdown files",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--md-break-conditional",
        "-bc",
        help="Set the number of chars before moving conditional causes of attributes to footnotes",
        type=str,
        required=False,
        default=MarkdownRenderer.default_break_conditional_labels,
    )
    parser.add_argument(
        "--md-check",
        help="Don't write the files back, just return the status. Return code 0 means nothing would change. Return "
        "code 1 means some files would change.",
        required=False,
        action="store_true",
    )


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Process Semantic Conventions yaml files."
    )
    parser.add_argument(
        "--debug", "-d", help="Enable debug output", action="store_true"
    )
    parser.add_argument(
        "--yaml-root",
        "-f",
        metavar="folder",
        help="Read all YAML files from a folder",
        type=str,
    )
    parser.add_argument(
        "--exclude", "-e", help="Exclude the matching files using GLOB syntax", type=str
    )
    parser.add_argument(
        "files",
        metavar="YAML_FILE",
        type=str,
        nargs="*",
        help="YAML file containing a Semantic Convention",
    )
    subparsers = parser.add_subparsers(dest="flavor")
    add_code_parser(subparsers)
    add_md_parser(subparsers)

    return parser


if __name__ == "__main__":
    main()
