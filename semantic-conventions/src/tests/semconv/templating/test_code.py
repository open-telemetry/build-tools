import io
import os
import tempfile

from opentelemetry.semconv.model.semantic_convention import SemanticConventionSet
from opentelemetry.semconv.templating.code import CodeRenderer


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


def test_codegen_attribute_v2_experimental(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("jinja", "attributesv2", "attributes.yml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "attributesv2", "template")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.renderv2(semconv, template_path, os.path.join(tmppath, "Attributes.java"), stable=False)
    with open(os.path.join(tmppath, "FirstAttributes.java")) as first:
        data = first.read()
        print(data)
        expected = read_test_file("jinja", "attributesv2", "FirstAttributes.java")
        assert data == expected

    with open(os.path.join(tmppath, "SecondAttributes.java")) as second:
        data = second.read()
        expected = read_test_file("jinja", "attributesv2", "SecondAttributes.java")
        assert data == expected

    assert not os.path.isfile(os.path.join(tmppath, "ThirdAttributes.java"))

def test_codegen_attribute_v2_stable(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("jinja", "attributesv2", "attributes.yml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "attributesv2", "template")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.renderv2(semconv, template_path, os.path.join(tmppath, "Attributes.java"), stable=True)

    with open(os.path.join(tmppath, "ThirdAttributes.java")) as second:
        data = second.read()
        expected = read_test_file("jinja", "attributesv2", "ThirdAttributes.java")
        assert data == expected

    assert not os.path.isfile(os.path.join(tmppath, "FirstAttributes.java"))
    assert not os.path.isfile(os.path.join(tmppath, "SecondAttributes.java"))

def test_codegen_attribute_v2_no_group_prefix(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(
        test_file_path("jinja", "attributesv2", "attributes_no_group_prefix.yml")
    )
    semconv.finish()

    template_path = test_file_path("jinja", "attributesv2", "template")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.renderv2(semconv, template_path, os.path.join(tmppath, "Attributes.java"), stable=False)
    with open(os.path.join(tmppath, "FooAttributes.java")) as foo:
        data = foo.read()
        expected = read_test_file("jinja", "attributesv2", "FooAttributes.java")
        assert data == expected

    with open(os.path.join(tmppath, "OtherAttributes.java")) as other:
        data = other.read()
        expected = read_test_file("jinja", "attributesv2", "OtherAttributes.java")
        assert data == expected
