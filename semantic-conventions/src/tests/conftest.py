import os
import pytest

from ruamel.yaml import YAML


_TEST_DIR = os.path.dirname(__file__)


@pytest.fixture
def test_file_path():
    def loader(filename):
        return os.path.join(_TEST_DIR, "data", filename)

    return loader


@pytest.fixture
def open_test_file(test_file_path):
    def loader(filename):
        return open(test_file_path(filename), "r", encoding="utf-8")

    return loader


@pytest.fixture
def load_yaml(open_test_file):
    def loader(filename):
        with open_test_file(os.path.join("yaml", filename)) as yaml_file:
            return YAML().load(yaml_file)

    return loader
