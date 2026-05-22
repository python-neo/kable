from argparse import ArgumentParser
from datetime import datetime
from json import dump, load
from json import JSONDecodeError
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Label, TextArea
import sys

BASE_DIR = Path (__file__).resolve ().parent

class Kable (App) :
    CSS = (BASE_DIR / "styles.txt").read_text ()
    BINDINGS = [("ctrl+s", "save", "Save")]

    def __init__ (self, file_path : Path | None = None) -> None :
        super ().__init__ ()
        self.config_path = (BASE_DIR / "config.json")
        self.config : dict = {}
        self.current_file = file_path
        self.initial_text = ""

        if self.current_file is not None :
            try :
                self.initial_text = self.current_file.read_text (encoding = "utf-8")
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

    def _on_exit_app (self) :
        self.config ["theme"] = self.theme
        self.save_config ()
        return super ()._on_exit_app ()

    def save_config (self) -> None :
        with self.config_path.open ("w", encoding = "utf-8") as f :
            dump (self.config, f, indent = 4)

    def action_save (self) -> None :
        if self.current_file is None :
            return
        editor = self.query_one (TextArea)
        self.current_file.write_text (editor.text, encoding = "utf-8")

    def update_clock (self) -> None :
        self.query_one ("#status_clock", Label).update (
            f"🕒 {datetime.now ().strftime ('%H:%M')}"
        )

    def compose (self) -> ComposeResult :
        yield Header ()
        yield TextArea (self.initial_text)
        with Horizontal (id = "status_bar") :
            yield Label ("", classes = "spacer")
            yield Label ("00:00", id = "status_clock")

if __name__ == "__main__" :
    argparser = ArgumentParser ()
    argparser.add_argument ("filename")
    args = argparser.parse_args ()

    file_path = Path (args.filename).resolve ()
    Kable (file_path = file_path).run ()
