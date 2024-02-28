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
import os
import sys
import tempfile
import zipfile
from typing import List

import requests

from opentelemetry.semconv.model.semantic_convention import (
    CONVENTION_CLS_BY_GROUP_TYPE,
    SemanticConventionSet,
)
from opentelemetry.semconv.templating.code import CodeRenderer
from opentelemetry.semconv.templating.compatibility import CompatibilityChecker
from opentelemetry.semconv.templating.markdown import MarkdownRenderer
from opentelemetry.semconv.templating.markdown.options import MarkdownOptions


def parse_semconv(
    yaml_root: str, exclude: str, debug: bool, parser
) -> SemanticConventionSet:
    semconv = SemanticConventionSet(debug)
    files = find_yaml(yaml_root, exclude)
    for file in sorted(files):
        if not file.endswith(".yaml") and not file.endswith(".yml"):
            parser.error(f"{file} is not a yaml file.")
        semconv.parse(file, False)
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


def filter_semconv(semconv, types):
    if types:
        semconv.models = {
            id: model
            for id, model in semconv.models.items()
            if model.GROUP_TYPE_NAME in types
        }


def main():
    parser = setup_parser()
    args = parser.parse_args()
    check_args(args, parser)
    semconv = parse_semconv(args.yaml_root, args.exclude, args.debug, parser)
    semconv_filter = parse_only_filter(args.only, parser)
    filter_semconv(semconv, semconv_filter)
    if len(semconv.models) == 0:
        parser.error("No semantic convention model found!")
    if args.flavor == "code":
        renderer = CodeRenderer.from_commandline_params(
            args.parameters, args.trim_whitespace
        )
        renderer.render(semconv, args.template, args.output, args.pattern)
    elif args.flavor == "markdown":
        process_markdown(semconv, args)
    elif args.flavor == "compatibility":
        check_compatibility(semconv, args, parser)


def process_markdown(semconv, args):
    options = MarkdownOptions(
        check_only=args.md_check,
        disable_stable_badge=args.md_disable_stable,
        disable_experimental_badge=args.md_disable_experimental,
        disable_deprecated_badge=args.md_disable_deprecated,
        break_count=args.md_break_conditional,
        exclude_files=exclude_file_list(args.markdown_root, args.exclude),
    )
    md_renderer = MarkdownRenderer(args.markdown_root, semconv, options)
    md_renderer.render_md()


def check_compatibility(semconv, args, parser):
    prev_semconv_path = download_previous_version(args.previous_version)
    prev_semconv = parse_semconv(prev_semconv_path, args.exclude, args.debug, parser)
    compatibility_checker = CompatibilityChecker(semconv, prev_semconv)
    problems = compatibility_checker.check()

    if any(problems):
        print(f"Found {len(problems)} compatibility issues:")
        for problem in sorted(str(p) for p in problems):
            print(f"\t{problem}")

        if not args.ignore_warnings or (
            args.ignore_warnings and any(problem.critical for problem in problems)
        ):
            sys.exit(1)


def find_yaml(yaml_root: str, exclude: str) -> List[str]:
    if yaml_root is not None:
        excluded_files = set(exclude_file_list(yaml_root if yaml_root else "", exclude))
        yaml_files = set(glob.glob(f"{yaml_root}/**/*.yaml", recursive=True)).union(
            set(glob.glob(f"{yaml_root}/**/*.yml", recursive=True))
        )
        return list(yaml_files - excluded_files)

    return []


def check_args(arguments, parser):
    files = arguments.yaml_root is None and len(arguments.files) == 0
    if files:
        parser.error("Either --yaml-root or YAML_FILE must be present")


def parse_only_filter(only: str, parser) -> List[str]:
    if not only:
        return []

    types = [t.strip() for t in only.split(",")]
    unknown_types = [t for t in types if t not in CONVENTION_CLS_BY_GROUP_TYPE.keys()]
    if unknown_types:
        parser.error(
            f"Unknown semconv names in `--only` option: '{', '.join(unknown_types)}'"
        )
        sys.exit(1)
    return types


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
    parser.add_argument(
        "--trim-whitespace",
        help="Allow customising whitespace control in Jinja templates."
        " Providing the flag will enable both `lstrip_blocks` and `trim_blocks`",
        required=False,
        action="store_true",
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
    parser.add_argument(
        "--check-compat",
        help="Check backward compatibility with previous version of semantic conventions.",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--md-disable-stable",
        help="Removes badges from attributes marked as stable.",
        required=False,
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--md-disable-experimental-badge",
        help="Removes badges from attributes marked as experimental.",
        required=False,
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--md-disable-deprecated-badge",
        help="Removes badges from attributes marked as deprecated.",
        required=False,
        default=False,
        action="store_true",
    )


def add_compat_check_parser(subparsers):
    parser = subparsers.add_parser("compatibility")
    parser.add_argument(
        "--previous-version",
        help="Check backward compatibility with specified older version of semantic conventions.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--ignore-warnings",
        help="Ignore non-critical compatibility problems.",
        required=False,
        default=False,
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
        "--only",
        type=str,
        help=f"""Generates semantic conventions of the specified types only
        ({", ".join(CONVENTION_CLS_BY_GROUP_TYPE.keys())}).

        To generate multiple conventions at once, pass comma-separated list of
        convention names, e.g. '--only span,event'.

        The `--only` flag filters the output and does not apply to input.
        Resolution of referenced attributes (using `ref`), or semantic conventions
        (using `exclude` or `include`) is done against all semantic convention
        files provided as input using `--yaml-root` or `YAML_FILE` options.
        """,
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
    add_compat_check_parser(subparsers)

    return parser


def download_previous_version(version: str) -> str:
    filename = f"v{version}.zip"
    tmppath = tempfile.mkdtemp()
    path_to_zip = os.path.join(tmppath, filename)
    path_to_semconv = os.path.join(tmppath, f"v{version}")

    semconv_vprev = (
        f"https://github.com/open-telemetry/semantic-conventions/archive/{filename}"
    )

    response = requests.get(semconv_vprev, allow_redirects=True, timeout=30)
    response.raise_for_status()

    with open(path_to_zip, "wb") as zip_file:
        zip_file.write(response.content)

    with zipfile.ZipFile(path_to_zip, "r") as zip_ref:
        zip_ref.extractall(path_to_semconv)

    return os.path.join(path_to_semconv, f"semantic-conventions-{version}", "model")


if __name__ == "__main__":
    main()
