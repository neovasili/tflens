# Terraform lens

[![pre-commit](https://github.com/neovasili/tflens/workflows/pre-commit/badge.svg)](https://github.com/neovasili/tflens)
[![unit-tests](https://github.com/neovasili/tflens/workflows/unit-tests/badge.svg)](https://github.com/neovasili/tflens)
[![Pypi package](https://img.shields.io/static/v1.svg?label=Pypi&message=1.3.0&color=blue)](https://pypi.python.org/pypi/tflens/)
![coverage](https://img.shields.io/static/v1.svg?label=coverage&message=40%25&color=yellow)
![Supported versions check](https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiNjBlaXhCTElOdFB4a2xnVm9vNmQ3NzlnVFBaZjRlVFI4emdiSnhybVJqWXpxRlgwRTVqV1p0eTJwVXRhZkJFaHF4KytTVVZJcitEWmdpNjNqaGRsSGNzPSIsIml2UGFyYW1ldGVyU3BlYyI6ImdHZHl4S3RnMzJydDFZVjkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=neovasili_tflens&metric=alert_status)](https://sonarcloud.io/dashboard?id=neovasili_tflens)

Terraform lens is a CLI tool that enables developers have a summarized view of tfstate resources.

## Description

It will produce a table with the resources in a given terraform tfstate with the following columns:

* provider
* type
* mode
* name
* module

Example:

```txt
|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
| provider.aws |  aws_dynamodb_table | managed | dynamodb-terraform-state-lock |   -    |
```

### Features

Currently, the tool supports read the tfstate file from a **local file** or a **remote state stored in S3**.

Regarding the produced output, there are three possibilities:

* **CLI output**. This will show the table directly in the terminal.
* **Markdown** file. This will creates a file `.tflens/terraform.tfstate.json.md` in the current directory with the table.
* **HTML** file. It's also possible to create an html file `.tflens/terraform.tfstate.json.html` in the current directory with the table.

The tool has been tested with tfstate files for the following terraform versions:

* 0.12.0 - 0.12.29
* 0.13.0 - 0.13.5

## Install

As the content of this repo is a Pypi package, you can easily install it using pip:

```bash
pip install tflens
```

## Usage

```bash
➜ tflens --help

usage: tflens [-h] [-f FILE_LOCATION] [-o OUTPUT] [-r REMOTE] [-m FILTER_MODULE] [-n FILTER_NAME] [-t FILTER_TYPE] [-p FILTER_PROVIDER] [-d FILTER_MODE] [-u HTTP_USER] [-w HTTP_PASSWORD] [-v]

Terraform lens is a CLI tool that enables developers have a summarized view of tfstate resources.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_LOCATION, --file-location FILE_LOCATION
        Defines the location (remote or local) of the tfstate file.
        Mandatory if remote tfstate is selected.
        If empty then use the current_folder/terraform.tfstate
  -o OUTPUT, --output OUTPUT
        Defines output type (markdown|html).
        If empty outputs in terminal
  -r REMOTE, --remote REMOTE
        Defines if remote (s3|http) or local tfstate file.
        If empty local is used.
        When remote is defined, you also need to specify --file-location with the tfstate location
        according to the following pattern: bucket-name/tfstate-key
  -m FILTER_MODULE, --filter-module FILTER_MODULE
        Applies a regular expression to the module field in order to filter the resources list to output
  -n FILTER_NAME, --filter-name FILTER_NAME
        Applies a regular expression to the name field in order to filter the resources list to output
  -t FILTER_TYPE, --filter-type FILTER_TYPE
        Applies a regular expression to the type field in order to filter the resources list to output
  -p FILTER_PROVIDER, --filter-provider FILTER_PROVIDER
        Applies a regular expression to the provider field in order to filter the resources list to output
  -d FILTER_MODE, --filter-mode FILTER_MODE
        Applies a regular expression to the mode field in order to filter the resources list to output
  -u HTTP_USER, --http-user HTTP_USER
        User for http remote backend basic auth
  -w HTTP_PASSWORD, --http-password HTTP_PASSWORD
        Password for http remote backend basic auth
  -v, --version
        Show program version
```

### Examples

View table of resources for a tfstate located in the file system in the directory:

```bash
➜ tflens

|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
| provider.aws |  aws_dynamodb_table | managed | dynamodb-terraform-state-lock |   -    |
```

View filtered table of resources for a tfstate located in the file system in the directory:

```bash
➜ tflens --filter-name "current"

|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
```

Or:

```bash
➜ tflens --filter-module "test"

|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
```

Or:

```bash
➜ tflens --filter-name "current" --filter-module "test"

|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
```

View table of resources for a tfstate located in the file system in the `dev/terraform.tfstate.json` path:

```bash
➜ tflens --file-location dev/terraform.tfstate.json

|   provider   |        type         |   mode  |           name                | module |
|--------------|---------------------|---------|-------------------------------|--------|
| provider.aws | aws_caller_identity |   data  |        current_user           |  test  |
| provider.aws |  aws_dynamodb_table | managed | dynamodb-terraform-state-lock |   -    |
```

Create markdown file with table of resources for a tfstate located in the file system in the directory:

```bash
➜ tflens --output markdown
```

View table of resources for a tfstate located in a S3 bucket called `tflens-test-tfstate-bucket`:

```bash
➜ tflens --file-location tflens-test-tfstate-bucket/common/terraform.tfstate --remote s3
```
