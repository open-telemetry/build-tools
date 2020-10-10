import os
import pytest

from ruamel.yaml import YAML


_TEST_DIR = os.path.dirname(__file__)


@pytest.fixture
def load_yaml():
    def loader(filename):
        full_path = os.path.join(_TEST_DIR, "data", filename)
        with open(full_path, "r", encoding="utf-8") as yaml_file:
            return YAML().load(yaml_file)

    return loader
