# Kable

> A terminal IDE built in python.

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

Kable currently includes a text editor, file explorer, and configurable
terminal interface built with Textual.

The project is a terminal application built around
editor workflows similar to those of VS Code and Neovim (LazyVim).

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
.venv\Scripts\Activate
uv pip install -r pyproject.toml
uv pip install -e . --system
```

or with pip:

```bash
python -m venv venv
venv\Scripts\Activate
pip install -r pyproject.toml
pip install -e .
```

Note: If using uv, run as administrator.

## Usage

```bash
kable <filename>
```

### Key Binds

| Key    | Action          |
| ------ | --------------- |
| Ctrl+S | Save file       |
| Ctrl+E | Toggle explorer |
| Ctrl+Q | Quit            |

## Repository Layout

```text
.
├── .github/
│   └── workflows/
├── docs/
│   ├── source/
│   │   ├── _static/
│   │   ├── _templates/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── kable.rst
│   │   └── modules.rst
│   ├── Makefile
│   └── make.bat
├── kable/
│   ├── editor.py
│   ├── explorer.py
│   ├── main.py
│   ├── utils.py
│   ├── config.json
│   ├── styles.txt
│   └── __init__.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE.md
├── pyproject.toml
├── README.md
├── uv.lock
└── .python-version
```

## Maintainers

[@python-neo](https://github.com/python-neo)

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines.

Release notes are tracked in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE.md) (c) 2026 python-neo
