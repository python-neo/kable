import sys
from pathlib import Path

project = "Kable"
copyright = "2026, Aarav Agarwal"
author = "Aarav Agarwal"
release = "0.5.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autosummary_generate = True

autodoc_default_options = {
    "inherited-members": False,
    "undoc-members": False,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))