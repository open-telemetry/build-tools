import io

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer


def test_codegen_units(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "units_template")
    renderer = CodeRenderer({}, False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "metrics", "expected.java")

    assert result == expected


def test_strip_blocks_enabled(test_file_path, read_test_file):
    """Tests that the Jinja whitespace control params are fed to the Jinja environment"""
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "units_template")
    renderer = CodeRenderer({}, True)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "metrics", "expected_no_whitespace.java")

    assert result == expected
