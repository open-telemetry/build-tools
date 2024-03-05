# Semantic Conventions build tools

This document provides information for contributions specific to the `semantic-convention` tooling.

Read the OpenTelemetry project [contributing
guide](https://github.com/open-telemetry/community/blob/main/CONTRIBUTING.md)
for general information about the project.

## Development setup

### Prerequisites

- Python
- Docker (optional)

### Building

Any changes to the build process should be reflected in this repositiory's `.github/workflows/semconvgen.yml` workflow, in addition to this document.

For local development, use an isolated environment ([venv](https://docs.python.org/3/library/venv.html)). Doing so will avoid polluting your system's path with dependencies specific to this project, and allow for more reproducible builds. For detailed instructions setting up python, see [venv setup](#venv-setup).

Ensure dependencies are installed and on your `PATH` before building. If you're using a terminal, you can install your dependencies in your venv by activating it and then running

```bash
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r dev-requirements.txt
pip install --upgrade --editable .
```

### Building Docker Image

Any changes to the deployment process should be reflected in this repositiory's `.github/workflows/semconvgen.yml` workflow, in addition to this document and the [CHANGELOG](CHANGELOG.md).

We use [Docker](https://docs.docker.com/) for deployments. The configuration is specified in `Dockerfile`, and you can build an image named `semconvgen` by running

```bash
# You need to package the code before building the docker image
python -m pip install -U pip && pip install -U setuptools wheel
pip wheel --no-deps . --wheel-dir .

docker build -t semconvgen .
```

### venv setup

_Note:_ `venv` integrations exist for IDEs such as [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env) or [VSCode](https://code.visualstudio.com/docs/python/environments). Below describes how to accomplish this setup in a terminal.

See the offical documents for creating and [using](https://docs.python.org/3/tutorial/venv.html) a [venv environment](https://docs.python.org/3/library/venv.html).  All "python" commands listed in this document should be run in an activated `venv`.

**Note**, ensure the venv you create is using the earliest supported version of python as defined in `setup.cfg`

```bash
# note that it's convention to not store your venv in your working directory, lest build tooling "pick up" venv configuration.
python3.10 -m venv ../semconvgen
source ../semconvgen/bin/activate
# Run your pip/wheel commands as described elsewhere in this documentation here.
# reset your environment by typing 'deactivate' or by exiting your TTY
```

Once you've set up and activated venv, you can use pip as normal to [install dependencies](#building).

## How to Contribute

The normal guidance on creating github issues prior to a PR and writing tests applies.

### Dependencies

We use [`pip`'s `requirements.txt`](https://pip.pypa.io/en/stable/reference/requirements-file-format/) and [`setuptool`'s `setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) for dependency management. Build and Runtime dependencies should be enumerated in the `setup.cfg` file's `install_requires` section. Dependencies exclusive to Development may go in the `dev-requirements.txt` file.

To add a new dependency, add it as a new line in either of the relevant `requirements` files.

### Testing

We use `pytest` for testing, which natively supports python's built in `unittest`. You can write your tests in `src/tests`. See the [pytest](https://docs.pytest.org/en/7.1.x/contents.html) or [unittest](https://docs.python.org/3/library/unittest.html) documentation for implementation and further documentation on our test tooling.

To run your tests and check your code, execute pytest

```bash
pytest -v
```

We use [`mypy`](https://mypy.readthedocs.io/en/latest/) for type checking. `mypy` natively supports python [type hinting](https://docs.python.org/3/library/typing.html), and maintains an excellent [cheat-sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) for their use. `mypy` options are configured in `mypy.ini`.

To validate your typing, run mypy on the relevant directory or file.

```bash
mypy src
```

### Linting

We run a handful of linting procedures. It's easiest to first format your code with `black`, which should have been installed as a dev-dependency during development setup.

To format your code, simply run `black`. This should only change code you've written. Please do not post any PRs reformatting other's code, unless that's exclusively the code contained in the PR.

### Creating a new PR

If there is a `CHANGELOG.md` file in the component you are updating,
please make sure to add an entry for your change in the "Unreleased" section.

Both the top-level [README](../README.md) for this repository and the advice in the [open telemetry community guidelines](https://opentelemetry.io/docs/contribution-guidelines/) still apply for PRs to these build tools.
