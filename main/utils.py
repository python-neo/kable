from hashlib import sha256
from pathlib import Path


def get_icon (file : Path) -> str :
    if file.is_dir () : return "󰉋"

    name, ext = file.name.lower (), file.suffix.lower ()

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
        ".py" : "󰌠", ".js" : "󰌞", ".ts" : "󰛦", ".json" : "󰘦",
        ".md" : "󰍔", ".txt" : "󰈙", ".html" : "󰌝", ".css" : "󰌜",
        ".scss" : "󰌜", ".yaml" : "󰈙", ".yml" : "󰈙", ".toml" : "󰈙",
        ".sh" : "󱆃", ".bat" : "󰆍", ".c" : "", ".cpp" : "",
        ".rs" : "󱘗", ".go" : "󰟓", ".java" : "󰬷", ".php" : "󰌟",
        ".png" : "󰋩", ".jpg" : "󰋩", ".jpeg" : "󰋩", ".svg" : "󰜡",
        ".zip" : "󰗄",
    }

    return icons.get (ext, "󰈔")

def checksum (text : str | bytes) -> str :
    hasher, data = sha256 (), text.encode ("utf-8") if isinstance (text, str) else text

    for start in range (0, len (data), 8192) :
        hasher.update (data [start:start + 8192])
        
    return hasher.hexdigest ()