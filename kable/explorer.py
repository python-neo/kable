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
    """
    A file explorer widget with Git-aware styling and hidden file filtering.
    """

    class FileClicked (Message) :
        """
        Message posted when a file is selected.
        """

        def __init__ (self, path : Path) -> None :
            """
            Initialize a file selection message.

            :param path: Path of the selected file.
            """
            self.path = path
            super ().__init__ ()

    def __init__ (self, root : Path) :
        """
        Initialize the file explorer.

        :param root: Root directory to display.
        """
        super ().__init__ (root.name)
        self.root_path = root
        self.ignored_cache : set [Path] = set ()
        self.status_cache : dict [Path, str] = {}
        self.hidden_cache : dict [Path, bool] = {}

    def on_mount (self) -> None :
        """
        Load Git metadata and build the file tree.
        """
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
        """
        Recursively populate the tree view.

        :param node: Parent tree node.
        :param path: Directory being traversed.
        :param ignore: Whether descendants should be treated as ignored.
        """
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
        """
        Add a file node to the tree.

        :param node: Parent tree node.
        :param file_path: Path to the file.
        :param is_ignored: Whether the file is Git ignored.
        """
        status = self.get_status (file_path)
        label = get_icon_and_file (file_path)
        label_cut = label if len (label) <= 33 else label [:30] + "..."
        style = COLOR_GREY if is_ignored else self._file_style (status)
        node.add_leaf (Text (label_cut, style = style), data = file_path)

    def _file_style (self, status : str) -> str :
        """
        Determine the display color for a file.

        :param status: Git status code.
        :return: Hex color string.
        """
        if status == "A" :
            return COLOR_GREEN
        if status == "M" :
            return COLOR_MODIFIED
        return COLOR_WHITE

    def is_git_ignored (self, path : Path) -> bool :
        """
        Check whether a path is ignored by Git.

        :param path: Path to check.
        :return: True if the path is ignored.
        """
        if path in self.ignored_cache :
            return True
        if path.is_dir () :
            result = run_git_command ("check-ignore", "-q", str (path), return_process = True)
            return isinstance (result, CompletedProcess) and result.returncode == 0
        return False

    def on_tree_node_selected (self, event : Tree.NodeSelected) -> None :
        """
        Handle tree node selection.

        Directories are expanded or collapsed. Files emit a
        :class:`FileClicked` message.

        :param event: Tree selection event.
        """
        path = event.node.data
        if not isinstance (path, Path) :
            return

        if path.is_dir () :
            event.node.toggle ()
            return

        self.post_message (self.FileClicked (path))

    def _load_git_cache (self) -> None :
        """
        Populate the Git ignore and status caches.
        """
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
                if status_code.strip () :
                    try :
                        path = self.root_path / line.split (" ") [1]
                        status = "A" if "??" in status_code else "M"
                        self.status_cache [path] = status
                    except (ValueError, OSError) :
                        continue

    def ishidden (self, path : Path) -> bool :
        """
        Check whether a file or directory is hidden.

        On Windows this uses the hidden file attribute.

        :param path: Path to check.
        :return: True if the path is hidden.
        """
        if windll is None :
            return False
        if path not in self.hidden_cache :
            attrs = windll.kernel32.GetFileAttributesW (str (path))
            self.hidden_cache [path] = attrs != -1 and (attrs & 2) != 0
        return self.hidden_cache [path]

    def get_status (self, path : Path) -> str :
        """
        Retrieve the cached Git status of a file.

        :param path: File path.
        :return: Git status code or an empty string.
        """
        return self.status_cache.get (path, "")


class Confirm (ModalScreen [bool]) :
    """
    Modal confirmation dialog.
    """

    def __init__ (self, prompt : str) -> None :
        """
        Initialize the confirmation dialog.

        :param prompt: Message displayed to the user.
        """
        self.prompt = prompt
        super ().__init__ ()

    def compose (self) -> ComposeResult :
        """
        Create the dialog layout.

        :return: Widgets that make up the dialog.
        """
        with Vertical (id = "confirm_box") :
            yield Label (self.prompt)
            with Horizontal (id = "confirm_buttons") :
                yield Button ("Yes", id = "yes")
                yield Button ("No", id = "no")

    def on_button_pressed (self, event : Button.Pressed) -> None :
        """
        Handle confirmation button presses.

        Selecting ``Yes`` dismisses the dialog with ``True``.
        Selecting ``No`` dismisses the dialog with ``False``.

        :param event: Button press event.
        """
        self.dismiss (event.button.id == "yes")