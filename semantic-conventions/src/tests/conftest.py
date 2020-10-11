import os
import pytest

from ruamel.yaml import YAML


_TEST_DIR = os.path.dirname(__file__)


@pytest.fixture
def open_test_file():
    def loader(filename):
        full_path = os.path.join(_TEST_DIR, "data", filename)
        return open(full_path, "r", encoding="utf-8")

    return loader


@pytest.fixture
def load_yaml(open_test_file):
    def loader(filename):
        with open_test_file(filename) as yaml_file:
            return YAML().load(yaml_file)

    return loader
