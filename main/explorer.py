try :
    from ctypes import windll
except ImportError :
    windll = None

from pathlib import Path
from subprocess import CompletedProcess

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Tree
from textual.widgets.tree import TreeNode

from .utils import get_icon_and_file, run_git_command

COLOR_GREY = "#a7a8a9"
COLOR_WHITE = "#FFFFFF"
COLOR_GREEN = "#56976d"
COLOR_MODIFIED = "#d68e34"


class FileExplorer (Tree) :
    class FileClicked (Message) :
        def __init__ (self, path : Path) -> None :
            self.path = path
            super ().__init__ ()

    def __init__ (self, root : Path) :
        super ().__init__ (root.name)
        self.root_path = root
        self.ignored_cache : set [Path] = set ()
        self.status_cache : dict [Path, str] = {}
        self.hidden_cache : dict [Path, bool] = {}

    def on_mount (self) -> None :
        self.show_root = False
        try :
            self._load_git_cache ()
            self.build_tree (self.root, self.root_path)
        except PermissionError :
            self.notify (
                f"Permission denied to access folder {self.root}. Try running Kable with administrative privilages.",
                severity = "error",
            )

    def build_tree (self, node : TreeNode, path : Path, ignore : bool = False) -> None :
        items = sorted (path.iterdir (), key = lambda item : (not item.is_dir (), item.name.lower ()))

        for item in items :
            if self.ishidden (item) :
                continue

            is_ignored = bool (ignore if ignore else self.is_git_ignored (item))

            if item.is_dir () :
                label_text = get_icon_and_file (item)
                style = COLOR_GREY if is_ignored else COLOR_WHITE
                child = node.add (Text (label_text, style = style), expand = not is_ignored, data = item)
                try :
                    self.build_tree (child, item, ignore = is_ignored)
                except PermissionError :
                    self.notify (
                        f"Permission denied to access folder {child}. Try running Kable with administrative privilages.",
                        severity = "error",
                    )
            else :
                self.add_file_node (node, item, is_ignored)

    def add_file_node (self, node : TreeNode, file_path : Path, is_ignored : bool = False) -> None :
        status = self.get_status (file_path)
        label = get_icon_and_file (file_path)
        label_cut = label if len (label) <= 33 else label [:30] + "..."
        style = COLOR_GREY if is_ignored else self._file_style (status)
        node.add_leaf (Text (label_cut, style = style), data = file_path)

    def _file_style (self, status : str) -> str :
        if status == "A" :
            return COLOR_GREEN
        if status == "M" :
            return COLOR_MODIFIED
        return COLOR_WHITE

    def is_git_ignored (self, path : Path) -> bool :
        if path in self.ignored_cache :
            return True
        if path.is_dir () :
            result = run_git_command ("check-ignore", "-q", str (path), return_process = True)
            return isinstance (result, CompletedProcess) and result.returncode == 0
        return False

    def on_tree_node_selected (self, event : Tree.NodeSelected) -> None :
        path = event.node.data
        if not isinstance (path, Path) :
            return

        if path.is_dir () :
            event.node.toggle ()
            return

        self.post_message (self.FileClicked (path))

    def _load_git_cache (self) -> None :
        ignored_output = run_git_command ("ls-files", "--others", "--exclude-standard", "--ignored")
        if isinstance (ignored_output, str) and ignored_output :
            for line in ignored_output.splitlines () :
                try :
                    path = self.root_path / line
                    self.ignored_cache.add (path)
                except (ValueError, OSError) :
                    pass

        status_output = run_git_command ("status", "--short")
        if isinstance (status_output, str) and status_output :
            for line in status_output.splitlines () :
                line = line.strip ()
                status_code = line.split (" ") [0]
                if status_code.strip ():
                    try :
                        path = self.root_path / line.split (" ") [1]
                        status = "A" if "??" in status_code else "M"
                        self.status_cache [path] = status
                    except (ValueError, OSError) :
                        continue

    def ishidden (self, path : Path) -> bool :
        if windll is None :
            return False
        if path not in self.hidden_cache :
            attrs = windll.kernel32.GetFileAttributesW (str (path))
            self.hidden_cache [path] = attrs != -1 and (attrs & 2) != 0
        return self.hidden_cache [path]

    def get_status (self, path : Path) -> str :
        return self.status_cache.get (path, "")

class Confirm (ModalScreen [bool]) :
    def __init__ (self, prompt : str) -> None :
        self.prompt = prompt
        super ().__init__ ()

    def compose (self) -> ComposeResult :
        with Vertical (id = "confirm_box") :
            yield Label (self.prompt)
            with Horizontal (id = "confirm_buttons") :
                yield Button ("Yes", id = "yes")
                yield Button ("No", id = "no")

    def on_button_pressed (self, event : Button.Pressed) -> None :
        self.dismiss (event.button.id == "yes")