# Semantic Conventions build tools

This document provides information for contributions specific to the `semantic-convention` tooling.

Read the OpenTelemetry project [contributing
guide](https://github.com/open-telemetry/community/blob/master/CONTRIBUTING.md)
for general information about the project.

## Development setup

### Prerequisites

- Python
- Docker (optional)

### Building

Any changes to the build process should be reflected in this repositiory's `.github/workflows/semconvgen.yml` workflow, in addition to this document and the [CHANGELOG](CHANGELOG.md).

For local development, it may be helpful to use an isolated environment such as [venv](https://docs.python.org/3/library/venv.html), or whatever your preferred IDE may offer. Doing so will avoid polluting your system's path with dependencies specific to this project, and allow for more reproducible builds. For detailed instructions setting up python, see [venv setup](#venv-setup)

Ensure dependencies are installed and on your `PATH` before building. If you're using a terminal, you can install your dependencies by running

```bash
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install --requirement dev-requirements.txt
pip install --upgrade --editable .
```

### Deployment

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

Creating a [venv environment](https://docs.python.org/3/library/venv.html) is incredibly simple for newer versions of python. Basically, you run a script, and then you install whatever you want as you normally would with pip.

To create a venv named `semconvgen`, you can simply run

```bash
# venv will create a directory with the same name as the given path.
# Tooling such as mypy or black may conflict with this directory in
# some scenerios. Storing them
mkdir -p ~/.venvs/semconvgen
python3 -m venv ~/.venvs/semconvgen
```

To "activate" your `venv` for the current tty, source your `VENVNAME/bin/activate` script

```bash
# you may want to make an alias for this
source ~/.venvs/semconvgen/bin/activate
```

_Note: If that doesn't work, please check the [official documentation](https://docs.python.org/3/tutorial/venv.html). `venv` comes bundled with python since version 3.3._

You can validate your path by inspecting the output of

```bash
# This should point to the python venv installed
which python
# These two should have venv on their paths
python -c 'import sys; print(sys.path)'
echo $PATH
```

If something is missing on your path, ensure you've `source`'d the venv dependency script or manually add them.

Once you've verified your shell environment looks correct, you can use pip as normal to [install dependencies](#building).
_**Note:** If you have trouble running or importing a newly installed dependency, try `deactivate`ing and `activate`ing venv_

If you wish to restore your original shell environment, you can run the `deactivate` shell function that `venv` automatically registers upon activation, or simply acquire a new shell.

If you want to "reset" your `venv`, simply deactivate, delete, recreate, and activate it.

```bash
deactivate
rm -Rf ~/.venvs/semconvgen
python -m venv ~/.venvs/semconvgen
source ~/.venvs/semconvgen/bin/activate
```

## How to Contribute

The normal guidance on creating github issues prior to a PR and writing tests applies.

### Dependencies

We use [`pip`'s `requirements.txt`](https://pip.pypa.io/en/stable/reference/requirements-file-format/) and [`setuptool`'s `setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) for dependency management. Build and Runtime dependencies should be enumerated in the `setup.cfg` file's `install_requires` section. Dependencies exclusive to Development may go in the `dev-requirements.txt` file.

To add a new dependency, add it as a new line in either of the relevant `requirements` files

### Testing

We use `pytest` for testing, which natively supports python's built in `unittest`. You can write your tests in `src/tests`. See the [pytest](https://docs.pytest.org/en/7.1.x/contents.html) or [unittest](https://docs.python.org/3/library/unittest.html) documentation for implementation and further documentation on our test tooling.

To run your tests and check your code, execute pytest

```bash
pytest -v
```

We use [`mypy`](https://mypy.readthedocs.io/en/latest/) for type checking. `mypy` natively supports python [type hinting](https://docs.python.org/3/library/typing.html), and maintains an excellent [cheat-sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) for their use. `mypy` options are configured in `mypy.ini`

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
