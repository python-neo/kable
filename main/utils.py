import sys
from hashlib import sha256
from json import JSONDecodeError, dump, load
from pathlib import Path
from subprocess import CalledProcessError, run


def get_icon_and_file (file : Path) -> str :
    if file.is_dir () : return file.name

    name, ext = file.name, file.suffix.lower ()

    special = {
        ".gitignore" : "󰊢",
        ".gitkeep" : "󰊢",
        "readme.md" : "󰍔",
        "license" : "󰿃",
        ".env" : "󰌆",
        "package.json" : "󰎙",
        "tsconfig.json" : "󰛦",
    }

    if name.lower () in special :
        return f"{special [name.lower ()]} {name}"

    icons = {
        ".py" : "󰌠", ".js" : "󰌞", ".ts" : "󰛦", ".json" : "󰘦",
        ".md" : "󰍔", ".txt" : "󰈙", ".html" : "󰌝", ".css" : "󰌜",
        ".scss" : "󰌜", ".yaml" : "󰈙", ".yml" : "󰈙", ".toml" : "󰈙",
        ".sh" : "󱆃", ".bat" : "󰆍", ".c" : "", ".cpp" : "",
        ".rs" : "󱘗", ".go" : "󰟓", ".java" : "󰬷", ".php" : "󰌟",
        ".png" : "󰋩", ".jpg" : "󰋩", ".jpeg" : "󰋩", ".svg" : "󰜡",
        ".zip" : "󰗄",
    }

    return f"{icons.get (ext, "󰈔")} {name}"

def checksum (text : str | bytes) -> str :
    hasher, data = sha256 (), text.encode ("utf-8") if isinstance (text, str) else text

    for start in range (0, len (data), 8192) :
        hasher.update (data [start:start + 8192])
        
    return hasher.hexdigest ()

def safe_file_read (file : Path, json : bool = False) :
    if file is not None :
        try :
            if not json : return file.read_text (encoding = "utf-8")
            with file.open ("r", encoding = "utf-8") as f : return load (f)

        except PermissionError :
            sys.exit ("Permission denied. Try running Kable with administrative privilages.")

        except (OSError, JSONDecodeError, UnicodeError) :
            sys.exit (f"ERROR: File {file} not found or cannot be read.") 

    else :
        return ""

def safe_file_write (file : Path, data, json : bool = False) :
    try :
        if not json :
            file.write_text (data, encoding = "utf-8")
            return
        with file.open ("w", encoding = "utf-8") as f : return dump (data, f, indent = 4)

    except PermissionError :
        sys.exit ("Permission denied. Try running Kable with administrative privilages.")
    except (OSError, JSONDecodeError, UnicodeError) :
        sys.exit (f"ERROR: File {file} cannot be written to.")

def run_git_command (*args) -> str :
    try :
        result = run (["git", *args], capture_output = True, text = True, check = True)
        return result.stdout.strip ()
    except CalledProcessError :
        return ""