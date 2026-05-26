# Kable

> An early-stage terminal IDE written in Python.

Kable is a terminal IDE project published at
<https://github.com/python-neo/kable>.

## Table of Contents

- [Background](#background)
- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [Repository Layout](#repository-layout)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

Kable is at the beginning of development. The initial application code
currently lives in `main`.

The project direction is a Python terminal UI application built around
editor workflows that feel familiar to VS Code users.

Kable is currently planned around:

- `Textual` for terminal UI layout, panels, input handling, and app
  structure
- Python-first application logic in `main`

## Requirements

- [Python 3.12+](https://www.python.org/downloads/release/python-31210/)
- [A Nerd Font](https://www.nerdfonts.com/font-downloads)
- [pip or uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2)

## Install

Install the current dependency set:

```bash
uv venv
.venv/Scripts/Activate
uv pip install -r pyproject.toml
```

or with pip:

```bash
python -m venv venv
venv/Scripts/Activate/
pip install -r pyproject.toml
```

## Usage

Run the current Textual app scaffold from the project root:

```text
python -m main.main
```

## Repository Layout

```text
..
+-- main/
+-- .gitignore
+-- .python-version
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- LICENSE
+-- pyproject.toml
+-- README.md
+-- uv.lock
```

## Maintainers

[@python-neo](https://github.com/python-neo)

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines.

Release notes are tracked in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) (c) 2026 python-neo
