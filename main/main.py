from json import dump, load
from json import JSONDecodeError
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea

class Kable (App) :
    CSS = """
    TextArea {
        height: 1fr;
    }
    """

    def __init__ (self) -> None :
        super ().__init__ ()
        self.config_path = Path (__file__).resolve ().parent / "config.json"
        self.config : dict = {}

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

    def _on_exit_app (self) :
        self.config ["theme"] = self.theme
        self.save_config ()
        return super ()._on_exit_app ()

    def save_config (self) -> None :
        with self.config_path.open ("w", encoding = "utf-8") as f :
            dump (self.config, f, indent = 4)

    def compose (self) -> ComposeResult :
        yield Header ()
        yield TextArea ()
        yield Footer ()

if __name__ == "__main__" :
    Kable ().run ()
