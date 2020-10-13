# Terraform lens

[![pre-commit](https://github.com/neovasili/tflens/workflows/pre-commit/badge.svg)](https://github.com/neovasili/tflens)
[![unit-tests](https://github.com/neovasili/tflens/workflows/unit-tests/badge.svg)](https://github.com/neovasili/tflens)
[![Pypi package](https://img.shields.io/static/v1.svg?label=Pypi&message=1.0.0&color=blue)](https://pypi.python.org/pypi/tflens/)
![coverage](https://img.shields.io/static/v1.svg?label=coverage&message=40%25&color=yellow)
![Supported versions check](https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiNjBlaXhCTElOdFB4a2xnVm9vNmQ3NzlnVFBaZjRlVFI4emdiSnhybVJqWXpxRlgwRTVqV1p0eTJwVXRhZkJFaHF4KytTVVZJcitEWmdpNjNqaGRsSGNzPSIsIml2UGFyYW1ldGVyU3BlYyI6ImdHZHl4S3RnMzJydDFZVjkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

Terraform lens is a CLI tool that enables developers have a summarized view of tfstate resources.

## Description

It will produce a table with the resources in a given terraform tfstate with the following columns:

* provider
* type
* mode
* name
* module

Example:
|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
| provider.aws |  aws_dynamodb_table | managed | dynamodb-terraform-state-lock | (None) |

### Features

Currently, the tool supports read the tfstate file from a **local file** or a **remote state stored in S3**.

Regarding the produced output, there are three possibilities:

* **CLI output**. This will show the table directly in the terminal.
* **Markdown** file. This will creates a file `.tflens/terraform.tfstate.json.md` in the current directory with the table.
* **HTML** file. It's also possible to create an html file `.tflens/terraform.tfstate.json.html` in the current directory with the table.

The tool has been tested with tfstate files for the following terraform versions:

* 0.12.0 - 0.12.29
* 0.13.0 - 0.13.4

## Usage

```bash
➜ tflens --help

usage: tflens [-h] [-f FILE_LOCATION] [-o OUTPUT] [-r REMOTE]

Ask for user specific information

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_LOCATION, --file-location FILE_LOCATION
                        Defines the location of the tfstate file. If empty then use the current_folder/terraform.tfstate.json
  -o OUTPUT, --output OUTPUT
                        Defines output type (markdown|html). If empty outputs in terminal
  -r REMOTE, --remote REMOTE
                        Defines if remote (s3) or local tfstate file. If empty local is used
```
