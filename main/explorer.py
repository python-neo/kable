from pathlib import Path

from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Tree

from .utils import get_icon


class FileExplorer (Tree) :
    def __init__ (self, root : Path) : 
        super ().__init__ (root.name)
        self.root_path = root

    def on_mount (self) :
        self.root.expand ()
        
        try :
            self.build_tree (self.root, self.root_path)
        except PermissionError :
            self.notify (f"Permission denied to access folder {self.root}. Try running Kable with administrative privilages.", 
                         severity = "error")

    def build_tree (self, node, path : Path) :
        items = sorted (path.iterdir (), key = lambda x : (not x.is_dir (), x.name.lower ()))

        for item in items :
            if item.is_dir () :
                child = node.add (f"{get_icon (item)} {item.name}", expand = False, data = item)
                try :
                    self.build_tree (child, item)
                except PermissionError :
                    self.notify (f"Permission denied to access folder {child}. Try running Kable with administrative privilages.", 
                                severity = "error")
            else :
                node.add_leaf (f"{get_icon (item)} {item.name}", data = item)

class Confirm (ModalScreen [bool]) :
    def __init__ (self, prompt : str) :
        self.prompt = prompt
        return super ().__init__ ()
     
    def compose (self) :
        with Vertical (id = "confirm_box") :
            yield Label (self.prompt)
            with Horizontal (id = "confirm_buttons") :
                yield Button ("Yes", id = "yes")
                yield Button ("No", id = "no")

    def on_button_pressed (self, event : Button.Pressed) -> None :
        self.dismiss (event.button.id == "yes")