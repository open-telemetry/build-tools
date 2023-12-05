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

    filename = os.path.join(tempfile.mkdtemp(), "Attributes.java")
    renderer.render(semconv, template_path, filename, None)
    with open(filename) as f:
        result = f.read()

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

    filename = os.path.join(tempfile.mkdtemp(), "Attributes.java")
    renderer.render(semconv, template_path, filename, None)
    with open(filename) as f:
        result = f.read()

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

    filename = os.path.join(tempfile.mkdtemp(), "Attributes.java")
    renderer.render(semconv, template_path, filename, None)
    with open(filename) as f:
        result = f.read()
    expected = read_test_file("jinja", "attribute_templates", "expected.java")

    assert result == expected


def test_codegen_attribute_root_ns(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)

    semconv.parse(test_file_path("jinja", "group_by_root_namespace", "attributes.yml"))
    semconv.finish()

    template_path = test_file_path("jinja", "group_by_root_namespace", "template_all")
    renderer = CodeRenderer({}, trim_whitespace=True)

    test_path = os.path.join("group_by_root_namespace", "all")
    tmppath = tempfile.mkdtemp()
    renderer.render(
        semconv,
        template_path,
        os.path.join(tmppath, "Attributes.java"),
        "root_namespace",
    )

    first = read_test_file("jinja", test_path, "FirstAttributes.java")
    check_file(tmppath, "FirstAttributes.java", first)

    second = read_test_file("jinja", test_path, "SecondAttributes.java")
    check_file(tmppath, "SecondAttributes.java", second)

    third = read_test_file("jinja", test_path, "ThirdAttributes.java")
    check_file(tmppath, "ThirdAttributes.java", third)


def test_codegen_attribute_root_ns_stable(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)
    semconv.parse(test_file_path("jinja", "group_by_root_namespace", "attributes.yml"))
    semconv.finish()

    test_path = os.path.join("group_by_root_namespace", "stable")
    template_path = test_file_path("jinja", test_path, "template_only_stable")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.render(
        semconv,
        template_path,
        os.path.join(tmppath, "Attributes.java"),
        "root_namespace",
    )

    thirdStable = read_test_file("jinja", test_path, "ThirdAttributesStable.java")
    check_file(tmppath, "ThirdAttributes.java", thirdStable)
    assert not os.path.isfile(os.path.join(tmppath, "FirstAttributes.java"))
    assert not os.path.isfile(os.path.join(tmppath, "SecondAttributes.java"))


def test_codegen_attribute_root_ns_no_group_prefix(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)

    test_path = os.path.join("group_by_root_namespace", "no_group_prefix")
    semconv.parse(test_file_path("jinja", test_path, "attributes_no_group_prefix.yml"))
    semconv.finish()

    template_path = test_file_path("jinja", "group_by_root_namespace", "template_all")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.render(
        semconv,
        template_path,
        os.path.join(tmppath, "Attributes.java"),
        "root_namespace",
    )

    foo = read_test_file("jinja", test_path, "FooAttributes.java")
    check_file(tmppath, "FooAttributes.java", foo)

    other = read_test_file("jinja", test_path, "OtherAttributes.java")
    check_file(tmppath, "OtherAttributes.java", other)


def test_codegen_attribute_root_ns_single_file(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)

    test_path = os.path.join("group_by_root_namespace", "single_file")
    semconv.parse(test_file_path("jinja", test_path, "semconv.yml"))
    semconv.finish()

    template_path = test_file_path("jinja", test_path, "template_single_file")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.render(semconv, template_path, os.path.join(tmppath, "All.java"), None)

    all = read_test_file("jinja", test_path, "All.java")
    check_file(tmppath, "All.java", all)


def test_codegen_attribute_root_ns_metrics(test_file_path, read_test_file):
    semconv = SemanticConventionSet(debug=False)

    test_path = os.path.join("group_by_root_namespace", "attributes_and_metrics")
    semconv.parse(test_file_path("jinja", test_path, "semconv.yml"))
    semconv.finish()

    template_path = test_file_path("jinja", test_path, "template")
    renderer = CodeRenderer({}, trim_whitespace=True)

    tmppath = tempfile.mkdtemp()
    renderer.render(
        semconv, template_path, os.path.join(tmppath, ".java"), "root_namespace"
    )

    first = read_test_file("jinja", test_path, "First.java")
    check_file(tmppath, "First.java", first)

    second = read_test_file("jinja", test_path, "Second.java")
    check_file(tmppath, "Second.java", second)


def check_file(tmppath, actual_filename, expected_content):
    with open(os.path.join(tmppath, actual_filename)) as f:
        actual = f.read()
        print(actual)
        assert actual == expected_content
