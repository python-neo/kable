from ctypes import windll
from pathlib import Path

from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Tree
from textual.widgets.tree import TreeNode

from .utils import get_icon_and_file


class FileExplorer (Tree) :
    class FileClicked (Message) :
        def __init__ (self, path : Path) -> None :
            self.path = path
            super ().__init__ ()

    def __init__ (self, root : Path) : 
        super ().__init__ (root.name)
        self.root_path = root

    def on_mount (self) :
        self.show_root = False
        
        try :
            self.build_tree (self.root, self.root_path)
        except PermissionError :
            self.notify (f"Permission denied to access folder {self.root}. Try running Kable with administrative privilages.", 
                         severity = "error")

    def build_tree (self, node : TreeNode, path : Path) :
        items = sorted (path.iterdir (), key = lambda x : (not x.is_dir (), x.name.lower ()))

        for item in items :
            if self.ishidden (item) : continue
            if item.is_dir () :
                child = node.add (get_icon_and_file (item), expand = False, data = item)
                try :
                    self.build_tree (child, item)
                except PermissionError :
                    self.notify (f"Permission denied to access folder {child}. Try running Kable with administrative privilages.", 
                                severity = "error")
            else :
                node.add_leaf (get_icon_and_file (item), data = item)

    def on_tree_node_selected (self, event : Tree.NodeSelected) :
        path = event.node.data
        if not isinstance (path, Path) : return

        if path.is_dir () :
            event.node.toggle ()
            return
        self.post_message (self.FileClicked (path))

    def ishidden (self, path : Path) :
        attrs = windll.kernel32.GetFileAttributesW (str (path))
        return attrs != -1 and (attrs & 2) != 0

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