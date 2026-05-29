# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [0.3.1] - 2026-05-29

### Added

- `Ctrl+E` explorer toggle for showing and hiding the file explorer.
- Save-before-quit confirmation modal for modified files.
- Shared `utils.py` helpers for file icons and text checksums.
- Overlay styling for confirmation dialogs.

### Changed

- Moved file icon lookup out of `explorer.py` and into `utils.py`.
- Updated `README` install and usage instructions for the `kable`
  command.
- Updated Ruff formatting configuration to use CRLF line endings.
- Updated `uv.lock` project metadata for the editable `0.3.0` package.

## [0.3.0] - 2026-05-26

### Added

- `explorer.py` for explorer widget.
- Icon to filename in status bar.

### Changed

- `pyproject.toml` to include project data.
- Dependencies section in the `README`.

### Fixed

- Possible `PermissionDenied` bug in `explorer.py`.

## [0.2.1] - 2026-05-24

### Added

- Line numbers in main editor widget.
- Modern uv based dependency workflow

### Changed

- Status bar to include the name of the current file and your location in it.
- README

### Fixed

- PermissionDenied errors when opening or editing files that need admin access.

## [0.2.0] - 2026-05-22

### Added

- Required command-line filename loading with absolute-path resolution
  and initial file contents loaded into the editor.
- `Ctrl+S` save binding for writing the current buffer back to disk.
- Custom bottom status bar with a live 24-hour clock display.
- External `main/styles.txt` stylesheet for Textual UI styling.

### Changed

- Replaced the built-in Textual footer with a custom status bar layout.
- Updated `.gitignore` for the Textual project shape and removed stale
  Qt-specific ignore rules.

## [0.1.0] - 2026-05-21

### Added

- Initial Textual app scaffold with a header, footer, and central text
  area.
- Theme persistence through `main/config.json`.

## [0.0.1] - 2026-05-19

### Added

- Initial project documentation.
- Repository published at <https://github.com/python-neo/kable>.

[Unreleased]: https://github.com/python-neo/kable/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/python-neo/kable/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/python-neo/kable/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/python-neo/kable/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/python-neo/kable/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/python-neo/kable/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/python-neo/kable/releases/tag/v0.0.1
