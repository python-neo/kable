# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

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

[Unreleased]: https://github.com/python-neo/kable/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/python-neo/kable/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/python-neo/kable/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/python-neo/kable/releases/tag/v0.0.1
