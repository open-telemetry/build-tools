import os
import pytest

from ruamel.yaml import YAML


_TEST_DIR = os.path.dirname(__file__)

# Fixtures in pytest work with reused outer names, so shut up pylint here.
# pylint:disable=redefined-outer-name


@pytest.fixture
def test_file_path():
    def loader(*path):
        return os.path.join(_TEST_DIR, "data", *path)

    return loader


@pytest.fixture
def open_test_file(test_file_path):
    def loader(*path):
        return open(test_file_path(*path), "r", encoding="utf-8")

    return loader


@pytest.fixture
def load_yaml(open_test_file):
    def loader(filename):
        with open_test_file(os.path.join("yaml", filename)) as yaml_file:
            return YAML().load(yaml_file)

    return loader


@pytest.fixture
def read_test_file(open_test_file):
    def reader(*path):
        with open_test_file(*path) as test_file:
            return test_file.read()

    return reader
