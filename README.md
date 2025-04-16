# vidtoolz-compose

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-compose.svg)](https://pypi.org/project/vidtoolz-compose/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-compose?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-compose/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-compose/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-compose/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-compose/blob/main/LICENSE)

Compose video

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-compose
```
## Usage

type ``vid compose --help`` to get help



## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-compose
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
