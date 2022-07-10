import io

import pytest

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer


def test_codegen_units(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "units_template")
    renderer = CodeRenderer({}, {})

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "metrics", "expected.java")

    assert result == expected


@pytest.mark.parametrize("trim_blocks, lstrip_blocks", [("True", "True"), ("true", "TRUE"), ("TRUE", "tRuE")])
def test_strip_blocks_enabled(test_file_path, read_test_file, trim_blocks, lstrip_blocks):
    """Tests that Jinja config options are passed to the Jinja environment"""
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "units_template")
    renderer = CodeRenderer({}, {"trim_blocks": trim_blocks, "lstrip_blocks": lstrip_blocks})

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "metrics", "expected_no_whitespace.java")

    assert result == expected
