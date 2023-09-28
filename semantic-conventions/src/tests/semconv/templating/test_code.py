import io

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer


def test_codegen_units(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "units", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "units", "units_template")
    renderer = CodeRenderer({}, trim_whitespace=False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "units", "expected.java")

    assert result == expected


def test_codegen_metrics(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "metrics.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "metrics_template")
    renderer = CodeRenderer({}, trim_whitespace=False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "metrics", "expected.java")

    assert result == expected

def test_strip_blocks_enabled(test_file_path, read_test_file):
    """Tests that the Jinja whitespace control params are fed to the Jinja environment"""
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "units", "units.yaml"))
    semconv.finish()

    template_path = test_file_path(
        "jinja", "units", "units_template_trim_whitespace_enabled"
    )
    renderer = CodeRenderer({}, trim_whitespace=True)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file(
        "jinja", "units", "expected_trim_whitespace_enabled.java"
    )

    assert result == expected


def test_codegen_attribute_templates(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("yaml", "attr_templates_code", "attribute_templates.yml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "attribute_templates", "template")
    renderer = CodeRenderer({}, trim_whitespace=False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "attribute_templates", "expected.java")

    assert result == expected
