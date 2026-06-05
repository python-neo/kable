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
CONFIG_FILE = BASE_DIR / "config.json"

class Kable (App) :
    CSS = (BASE_DIR / "styles.txt").read_text ()
    BINDINGS = [
        Binding ("ctrl+s", "save", "Save"),
        Binding ("ctrl+e", "toggle_explorer", "Toggle Explorer", priority = True),
        Binding ("ctrl+q", "quit", "Quit"),
    ]

    def __init__ (self, file_path : Path) -> None :
        super ().__init__ ()
        self.current_file = file_path
        try :
            self.initial_text = safe_file_read (self.current_file)
        except Exception as e : return self.notify (str (e), severity = "error")
        self.current_branch = run_git_command ("branch", "--show-current") or ""
        self.config : dict = self._load_config ()

    def _load_config (self) -> dict :
        try :
            loaded = safe_file_read (CONFIG_FILE, json = True, exit = False)
        except Exception as e : 
            self.notify (str (e), severity = "error")
            return {}
        return loaded if isinstance (loaded, dict) else {}

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
        try :
            self.config = {
                "theme" : self.theme,
                "explorer.hidden" : self.query_one ("#sidebar", Vertical).has_class ("hidden"),
            }
            safe_file_write (CONFIG_FILE, self.config, json = True)
        except Exception as e :
            return self.notify (str (e), severity = "error")

    def action_save (self) -> None :
        try :
            editor = self.query_one (TextArea)
            safe_file_write (self.current_file, editor.text)
        except Exception as e :
            return self.notify (str (e), severity = "error")

    def check_saved_app (self, should_exit : bool) -> None :
        editor = self.query_one ("#editor", TextArea)
        try :
            disk_text = safe_file_read (self.current_file)
        except Exception as e : 
            return self.notify (str (e), severity = "error")
        checksum_mod = checksum (editor.text)
        checksum_file = checksum (disk_text or "")

        if checksum_mod == checksum_file :
            if should_exit :
                self.exit ()
            return

        self.push_screen (
            Confirm ("Do you want to save changes before quitting?"),
            callback = lambda save : self.handle_save_choice (save, should_exit),
        )

    def handle_save_choice (self, save : bool | None, should_exit : bool) -> None :
        if save :
            self.action_save ()
        if should_exit :
            self.exit ()

    def action_toggle_explorer (self) -> None :
        self.query_one ("#sidebar", Vertical).toggle_class ("hidden")

    def on_text_area_selection_changed (self) -> None :
        editor = self.query_one (TextArea)
        line, column = editor.cursor_location
        self.query_one ("#location", Label).update (f"{line + 1}:{column + 1}")

    def compose (self) -> ComposeResult :
        with Horizontal (id = "main") :
            with Vertical (id = "sidebar") :
                file_explorer = FileExplorer (Path ("."))
                file_explorer.id = "explorer"
                yield file_explorer

            yield TextArea (self.initial_text or "", show_line_numbers = True, id = "editor")

        with Horizontal (id = "status_bar") :
            if self.current_branch :
                yield Label (" main", id = "branch")
                yield Label ("  ", id = "divider")
            yield Label (get_icon_and_file (self.current_file), id = "filename")
            yield Label ("", classes = "spacer")
            yield Label ("1:1", id = "location")
            yield Label ("󱑂 00:00", id = "clock")

    def update_status_bar (self) -> None :
        self.current_branch = run_git_command ("branch", "--show-current")
        self.query_one ("#filename", Label).update (get_icon_and_file (self.current_file))

        if not isinstance (self.current_branch, str) : return

        if self.current_branch.strip () :
            self.query_one ("#branch", Label).update (" " + self.current_branch)

        self.query_one ("#location", Label).update ("1:1")
        self.on_text_area_selection_changed ()

    def on_file_explorer_file_clicked (self, event : FileExplorer.FileClicked) -> None :
        self.action_quit (should_exit = False)
        self.current_file = cast (Path, event.path)
        self.update_status_bar ()
        try :
            file = safe_file_read (self.current_file)
        except Exception as e : 
            return self.notify (str (e), severity = "error")
            return
        self.query_one ("#editor", TextArea).text = file if isinstance (file, str) and file else ""

def main () -> None :
    argparser = ArgumentParser ()
    argparser.add_argument ("filename", help = "Path to file to open")
    args = argparser.parse_args ()

    try :
        file_path = Path (args.filename).resolve ()
        if not file_path.exists () :
            raise FileNotFoundError (f"File not found: {file_path}")
        Kable (file_path = file_path).run ()
    except FileNotFoundError as e :
        import sys
        sys.exit (f"ERROR: {e}")

if __name__ == "__main__" :
    main ()