[![PyPI](https://img.shields.io/pypi/v/vidtoolz-compose.svg)](https://pypi.org/project/vidtoolz-compose/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-compose?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-compose/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-compose/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-compose/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-compose/blob/main/LICENSE)

# vidtoolz-compose

A **vidtoolz** plugin that reads a markdown-style `compose_vid` file and composes videos from multiple source files.

It parses comments defining compositions (e.g. `# continous, howmany=3,audfile="...",prefix=kotilingestwar`) followed by video file entries, then executes the resulting commands to produce a composed video.

## What it does

- **Parse** a compose_vid file with inline comments that specify per-group parameters (`howmany`, `audio`, `prefix`, `startat`, etc.) and list of input videos.
- **Generate** intermediate files (`.txt`) for each command group and a consolidated `cmds.txt`.
- **Execute** the commands sequentially, tracking which ones succeed vs. fail.

## Key options

| Flag | Description |
|------|-------------|
| ``-d, --debug`` | Create all files but skip executing commands (useful for dry runs). |
| ``-v, --valid`` | Validate each command by running it with `--help` before execution. |
| ``-s, --skip N`` | Skip the first N entries / create vids after this many lines. |

## Recent improvements

- **Error tracking** — which commands fail vs. succeed is now printed clearly.
- **Smoke testing** — each command is verified to start without error before running (with a timeout).
- **Timeout protection** — subprocess calls are wrapped in try/except and killed if they exceed the allowed duration.



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

```bash
usage: vid compose [-h] [-d] [-v] input

Compose Videos using the supplied compose_vid file

positional arguments:
  input        
               Input file which contains the composition of the videos.
               
               Example file content
               
               # vid shorts, howmany=3,audfile="path/to/audio.mp3",prefix=kotilingestwar
               IMG_2494.MOV
               IMG_9122.MOV
               IMG_9123.MOV
               # mconcat
               IMG_2585.MOV
               # vid concat, howmany=4,audio=19FLOOR,prefix=Markendeshwar
               IMG_7476.MOV
               IMG_7520.MOV
               IMG_7552.MOV
               # vid stitch, howmany=5,audfile="path/t/audio.mp3",prefix=Markendeshwar,startat=30
               IMG_2664.MOV
               IMG_2665.MOV

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Will create all the files but will not run the cmds
  -v, --valid  Will validate the cmds

```

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
