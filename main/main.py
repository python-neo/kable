import sys
from argparse import ArgumentParser
from datetime import datetime
from json import JSONDecodeError, dump, load
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, TextArea

from .explorer import Confirm, FileExplorer
from .utils import checksum, get_icon

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
        self.initial_text = ""

        if self.current_file is not None :
            try :
                self.initial_text = self.current_file.read_text (encoding = "utf-8")
            except PermissionError :
                sys.exit ("Permission denied. Try running Kable with administrative privilages.")
            except (OSError, UnicodeError) :
                sys.exit ("File not found or cannot be read.")

        if self.config_path.exists () :
            try :
                with self.config_path.open ("r", encoding = "utf-8") as f :
                    loaded = load (f)
                if isinstance (loaded, dict) :
                    self.config = loaded
            except (OSError, JSONDecodeError) :
                self.config = {}

    def on_mount (self) -> None :
        self.theme = self.config.get ("theme", "textual-dark")
        self.update_clock ()
        self.set_interval (1, self.update_clock)

    def action_quit (self) :
        self.config ["theme"] = self.theme
        self.save_config ()
        self.check_saved_app ()

    def save_config (self) -> None :
        with self.config_path.open ("w", encoding = "utf-8") as f :
            dump (self.config, f, indent = 4)

    def action_save (self) -> None :
        if self.current_file is None :
            return
        editor = self.query_one (TextArea)
        try :
            self.current_file.write_text (editor.text, encoding = "utf-8")
        except PermissionError :
            sys.exit ("Permission denied. Try running Kable with administrative privilages.")

    def check_saved_app (self) :
        editor = self.query_one ("#editor", TextArea)
        checksum_mod = checksum (editor.text)
        checksum_file = checksum (self.current_file.read_text (encoding = "utf-8"))
        if checksum_mod == checksum_file :
            self.exit ()
            return
        self.push_screen (
            Confirm ("Do you want to save changes before quitting?"), self.save_and_quit)

    def save_and_quit (self, save : bool | None) -> None :
        if save : self.action_save ()
        self.exit ()

    def action_toggle_explorer (self) -> None :
        explorer = self.query_one ("#explorer", FileExplorer)
        explorer.toggle_class ("hidden")

    def update_clock (self) -> None :
        self.query_one ("#status_clock", Label).update (
            f"🕒 {datetime.now ().strftime ('%H:%M')}"
        )

    def on_text_area_selection_changed (self) -> None :
        editor = self.query_one (TextArea)
        line = editor.cursor_location [0] + 1
        column = editor.cursor_location [1] + 1
        self.query_one ("#location", Label).update (f"{line}:{column}")

    def compose (self) -> ComposeResult :
        with Horizontal (id = "main") :
            fe = FileExplorer (Path ("."))
            fe.id = "explorer"
            yield fe
            yield TextArea (self.initial_text, show_line_numbers = True, id = "editor")
            
        with Horizontal (id = "status_bar") :
            yield Label (str (f"{get_icon (self.current_file)} {self.current_file.name}"), id = "filename")
            yield Label ("", classes = "spacer")
            yield Label ("1:1", id = "location")
            yield Label ("00:00", id = "status_clock")

def main () :
    argparser = ArgumentParser ()
    argparser.add_argument ("filename")
    args = argparser.parse_args ()

    file_path = Path (args.filename).resolve ()
    Kable (file_path = file_path).run ()

if __name__ == "__main__" :
    main ()