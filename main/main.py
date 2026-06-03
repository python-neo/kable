from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, TextArea

from .explorer import Confirm, FileExplorer
from .utils import (
    checksum,
    get_icon_and_file,
    run_git_command,
    safe_file_read,
    safe_file_write,
)

BASE_DIR = Path (__file__).resolve ().parent

class Kable (App) :
    CSS = (BASE_DIR / "styles.txt").read_text ()
    BINDINGS = [
        Binding  ("ctrl+s", "save", "Save"),
        Binding ("ctrl+e", "toggle_explorer", "Toggle Explorer", priority = True),
        Binding ("ctrl+q", "quit", "Quit")
    ]

    def __init__ (self, file_path : Path) -> None :
        super ().__init__ ()
        self.config_path = (BASE_DIR / "config.json")
        self.config : dict = {}
        self.current_file = file_path
        self.initial_text = safe_file_read (self.current_file)
        self.current_branch = run_git_command ("branch", "--show-current")

        loaded = safe_file_read (self.config_path, json = True)
        self.config = loaded if isinstance (loaded, dict) else {}

    def on_mount (self) -> None :
        self.theme = "textual-dark"
        self.update_status_bar ()
        self.update_clock ()
        self.query_one ("#clock", Label).set_interval (1, self.update_clock)
        if self.config.get ("explorer.hidden") :
            self.query_one ("#sidebar", Vertical).add_class ("hidden")

    def update_clock (self) -> None :
        now = datetime.now ()
        self.query_one ("#clock", Label).update (f"󱑂 {now.strftime ('%H:%M')}")

    def action_quit (self, should_exit : bool = True) -> None :
        self.save_config ()
        self.check_saved_app (should_exit)

    def save_config (self) -> None :
        self.config = {
            "theme" : self.theme,
            "explorer.hidden" : self.query_one ("#sidebar", Vertical).has_class ("hidden")
        }
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
        explorer = self.query_one ("#sidebar", Vertical)
        explorer.toggle_class ("hidden")

    def on_text_area_selection_changed (self) -> None :
        editor = self.query_one (TextArea)
        line = editor.cursor_location [0] + 1
        column = editor.cursor_location [1] + 1
        self.query_one ("#location", Label).update (f"{line}:{column}")

    def compose (self) -> ComposeResult :
        with Horizontal (id = "main") :
            with Vertical (id = "sidebar") :
                fe = FileExplorer (Path ("."))
                fe.id = "explorer"
                yield fe

            yield TextArea (self.initial_text, show_line_numbers = True, id = "editor")
            
        with Horizontal (id = "status_bar") :
            if self.current_branch :
                yield Label (" main", id = "branch")
                yield Label (" ", id = "divider")
            yield Label (get_icon_and_file (self.current_file), id = "filename")
            yield Label ("", classes = "spacer")
            yield Label ("1:1", id = "location")
            yield Label ("󱑂 00:00", id = "clock")
    
    def update_status_bar (self) -> None :
        self.current_branch = run_git_command ("branch", "--show-current")
        self.query_one ("#filename", Label).update (get_icon_and_file (self.current_file))
        if self.current_branch.strip ():
            self.query_one ("#branch", Label).update (" " + self.current_branch + " ")
        self.query_one ("#location", Label).update ("1:1")
        self.on_text_area_selection_changed ()

    def on_file_explorer_file_clicked (self, event : FileExplorer.FileClicked) -> None :
        self.action_quit (should_exit = False)
        self.current_file = cast (Path, event.path)
        self.update_status_bar ()

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