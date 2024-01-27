import io

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer

def fail(msg=None):
    """Fail immediately, with the given message."""
    raise AssertionError(msg)

def test_codegen_units(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("yaml", "metrics", "units.yaml"))
    semconv.finish()

    template_path = test_file_path("jinja", "metrics", "units_template")
    renderer = CodeRenderer({}, trim_whitespace=False)

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

    template_path = test_file_path(
        "jinja", "metrics", "units_template_trim_whitespace_enabled"
    )
    renderer = CodeRenderer({}, trim_whitespace=True)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file(
        "jinja", "metrics", "expected_trim_whitespace_enabled.java"
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

def test_codegen_log_event_attributes_templates(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("yaml", "attr_templates_code", "attribute_templates.yml")
    )
    # This yaml file should not cause the global attributes to be polluted
    semconv.parse(
        test_file_path("yaml", "log_events", "client_exception.yaml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "log_event", "attributes_template")
    renderer = CodeRenderer({}, trim_whitespace=False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "log_event", "attributes_expected.java")

    if result != expected:
        fail("Result:" + result)

    assert result == expected

def test_codegen_log_event_templates(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("yaml", "attr_templates_code", "attribute_templates.yml")
    )
    # This yaml file should not cause the global attributes to be polluted
    semconv.parse(
        test_file_path("yaml", "log_events", "client_exception.yaml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "log_event", "log_events_template")
    renderer = CodeRenderer({}, trim_whitespace=False)

    output = io.StringIO()
    renderer.render(semconv, template_path, output, None)
    result = output.getvalue()

    expected = read_test_file("jinja", "log_event", "log_events_expected.java")

    if result != expected:
        fail("Result:" + result)

    assert result == expected
