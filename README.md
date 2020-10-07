# Terraform lens

[![pre-commit](https://github.com/neovasili/tflens/workflows/pre-commit/badge.svg)](https://github.com/neovasili/tflens)
[![unit-tests](https://github.com/neovasili/tflens/workflows/unit-tests/badge.svg)](https://github.com/neovasili/tflens)
[![Pypi package](https://img.shields.io/static/v1.svg?label=Pypi&message=1.0.0&color=blue)](https://pypi.python.org/pypi/tflens/)
![coverage](https://img.shields.io/static/v1.svg?label=coverage&message=40%25&color=yellow)

Terraform lens is a CLI tool that enables developers have a summarized view of tfstate resources.

## Development

For use this project in your local machine it's recommended to create a python virtual environment. To manually create a virtualenv on MacOS and Linux:

```bash
python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
source .env/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
pip3 install -r requirements.txt
```

### Pre-commit

A pre-commit configuration file is provided in this repo to perform some linterns, validations and so on in order to avoid commit code to the repo that later will fail in validations step in the build pipeline.

The first execution can be slower because of installation of dependencies. Further executions will use the pre-commit cache.

#### Pre-commit requirements

In order to use pre-commit with all the hooks declared you need to install the following:

* [Pre-commit](https://pre-commit.com/#install)
* [Markdownlint](https://github.com/markdownlint/markdownlint) (also requires ruby)
* [Shellcheck](https://github.com/koalaman/shellcheck)
* [pylint](https://www.pylint.org/#install)

#### Use pre-commit

Once you have all the requirements achieved, you have to install pre-commit in the local repository:

```bash
pre-commit install
```

And you can test it's working with the following:

```bash
➜ pre-commit run --all-files

Check for added large files..............................................Passed
Check for case conflicts.................................................Passed
Check that executables have shebangs.................(no files to check)Skipped
Check JSON...........................................(no files to check)Skipped
Check for merge conflicts................................................Passed
Trim Trailing Whitespace.................................................Passed
Detect AWS Credentials...................................................Passed
Tabs remover.............................................................Passed
Check markdown files.....................................................Passed
Test shell scripts with shellcheck...................(no files to check)Skipped
Python lintern...........................................................Passed
```

## References

* [Pypi packaging](https://packaging.python.org/tutorials/packaging-projects/)
* [Pypi setup docs](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
* [Pypi classifiers](https://pypi.org/classifiers/)
* [Pypi test register](https://test.pypi.org/account/register/)
* [Pypi test usage](https://packaging.python.org/guides/using-testpypi/)
