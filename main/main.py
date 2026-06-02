import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import cast

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Label, TextArea

from .explorer import Confirm, FileExplorer
from .utils import checksum, safe_file_read, safe_file_write, get_icon_and_file

BASE_DIR = Path (__file__).resolve ().parent

class Kable (App) :
    CSS = (BASE_DIR / "styles.txt").read_text ()
    BINDINGS = [
        ("ctrl+s", "save", "Save"),
        ("ctrl+e", "toggle_explorer", "Toggle Explorer"),
        ("ctrl+q", "quit", "Quit")
    ]

    def __init__ (self, file_path : Path) -> None :
        super ().__init__ ()
        self.config_path = (BASE_DIR / "config.json")
        self.config : dict = {}
        self.current_file = file_path
        self.initial_text = safe_file_read (self.current_file)

        loaded = safe_file_read (self.config_path)
        self.config = loaded if isinstance (loaded, dict) else {}

    def on_mount (self) -> None :
        self.theme = self.config.get ("theme", "textual-dark")

    def action_quit (self, should_exit : bool = True) -> None :
        self.config ["theme"] = self.theme
        self.save_config ()
        self.check_saved_app (should_exit)

    def save_config (self) -> None :
        safe_file_write (self.config_path, self.config, json = True)

    def action_save (self) -> None :
        if self.current_file is None :
            return
        editor = self.query_one (TextArea)
        safe_file_write (self.current_file, editor.text)

    def check_saved_app (self, should_exit : bool) -> None :
        editor = self.query_one ("#editor", TextArea)
        checksum_mod = checksum (editor.text)
        checksum_file = checksum (safe_file_read (self.current_file))
        if checksum_mod == checksum_file :
            if should_exit :
                self.exit ()
            return
        self.push_screen (
            Confirm ("Do you want to save changes before quitting?"),
            callback = lambda save : self.handle_save_choice (save, should_exit),
        )

    def handle_save_choice (self, save : bool | None, should_exit : bool) -> None :
        if save : self.action_save ()
        if should_exit : self.exit ()

    def action_toggle_explorer (self) -> None :
        explorer = self.query_one ("#explorer", FileExplorer)
        explorer.toggle_class ("hidden")

    def on_text_area_selection_changed (self) -> None :
        editor = self.query_one (TextArea)
        line = editor.cursor_location [0] + 1
        column = editor.cursor_location [1] + 1
        self.query_one ("#location", Label).update (f"{line}:{column}")

    def compose (self) -> ComposeResult :
        yield Header (show_clock = True, time_format = "%H:%M", icon = "󰆍")

        with Horizontal (id = "main") :
            with Vertical (id = "sidebar") :
                fe = FileExplorer (Path ("."))
                fe.id = "explorer"
                yield fe

            yield TextArea (self.initial_text, show_line_numbers = True, id = "editor")
            
        with Horizontal (id = "status_bar") :
            yield Label (get_icon_and_file (self.current_file), id = "filename")
            yield Label ("", classes = "spacer")
            yield Label ("1:1", id = "location")

    def on_file_explorer_file_clicked (self, event : FileExplorer.FileClicked) -> None :
        self.action_quit (should_exit = False)
        self.current_file = cast (Path, event.path)
        self.query_one ("#filename", Label).update (get_icon_and_file (self.current_file))
        editor = self.query_one ("#editor", TextArea)
        editor.text = self.current_file.read_text (encoding = "utf-8")

def main () :
    argparser = ArgumentParser ()
    argparser.add_argument ("filename")
    args = argparser.parse_args ()

    file_path = Path (args.filename).resolve ()
    Kable (file_path = file_path).run ()

if __name__ == "__main__" :
    main ()