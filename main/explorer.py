from pathlib import Path

from textual.widgets import Tree


def get_icon (file : Path) -> str :
    if file.is_dir () :
        return "󰉋"

    name = file.name.lower ()
    ext = file.suffix.lower ()

    special = {
        ".gitignore" : "󰊢",
        ".gitkeep" : "󰊢",
        "readme.md" : "󰍔",
        "license" : "󰿃",
        ".env" : "󰌆",
        "package.json" : "󰎙",
        "tsconfig.json" : "󰛦",
    }

    if name in special :
        return special [name]

    icons = {
        ".py" : "󰌠",
        ".js" : "󰌞",
        ".ts" : "󰛦",
        ".json" : "󰘦",
        ".md" : "󰍔",
        ".txt" : "󰈙",
        ".html" : "󰌝",
        ".css" : "󰌜",
        ".scss" : "󰌜",
        ".yaml" : "󰈙",
        ".yml" : "󰈙",
        ".toml" : "󰈙",
        ".sh" : "󱆃",
        ".bat" : "󰆍",
        ".c" : "",
        ".cpp" : "",
        ".rs" : "󱘗",
        ".go" : "󰟓",
        ".java" : "󰬷",
        ".php" : "󰌟",
        ".png" : "󰋩",
        ".jpg" : "󰋩",
        ".jpeg" : "󰋩",
        ".svg" : "󰜡",
        ".zip" : "󰗄",
    }

    return icons.get (ext, "󰈔")

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