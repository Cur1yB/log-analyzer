# Log analyzer

This script analyze file or several files `*.log`, where each line is JSON object.

# Install

Your system must have installed `uv` [Documetation astral-uv](https://docs.astral.sh/uv/)

```
pipx install uv
```

## Install environment

You can install all dependencies from `uv.lock` by command:

```
uv sync
```

Also you can use command from Makefile:

```
make install
```

Done!

## Usage
```bash
uv run analyze [-h] --file FILE [--report REPORT] [--date DATE]

Log Analyzer for processing *.log files, where each line is JSON object.

options:
  -h, --help       show this help message and exit
  --file FILE      Path to file | files separated by space
  --report REPORT  Report type
  --date DATE      Date in format YYYY-MM-DD
```
# Demo version

You can run demo-verson **Asciinema powered** by command:

```
make demo_version
```

## Tests

You can run tests by command:

```
make test
```

You can watch test coverage by command

```
make coverage
```