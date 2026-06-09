from hashlib import sha256
from json import JSONDecodeError, dump, load
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, run


def get_icon_and_file (file : Path) -> str :
    """
    Get a Nerd Font icon and filename for display.

    :param file: The file or directory to represent.
    :returns: A formatted string containing an icon and filename.
    """
    if file.is_dir () :
        return file.name

    name = file.name
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

    return f"{icons.get (ext, '󰈔')} {name}"


def checksum (text : str | bytes) -> str :
    """
    Calculate a SHA-256 checksum.

    :param text: The text or bytes to hash.
    :returns: The hexadecimal SHA-256 digest.
    """
    hasher = sha256 ()
    data = text.encode ("utf-8") if isinstance (text, str) else text

    for start in range (0, len (data), 8192) :
        hasher.update (data [start : start + 8192])

    return hasher.hexdigest ()


def safe_file_read (file : Path, json : bool = False, exit : bool = True) :
    """
    Read a file safely.

    :param file: The file to read.
    :param json: Whether to parse the file as JSON.
    :param exit: Whether to raise exceptions on failure.
    :returns: The file contents, parsed JSON object, or None on failure when ``exit`` is False.
    :raises Exception: If the file cannot be read and ``exit`` is True.
    """
    if file is not None :
        try :
            if not json :
                return file.read_text (encoding = "utf-8")

            with file.open ("r", encoding = "utf-8") as f :
                return load (f)

        except PermissionError :
            if not exit :
                return None

            raise Exception (
                "Permission denied. Try running Kable with administrative privilages."
            ) from None

        except (OSError, JSONDecodeError, UnicodeError) :
            if not exit :
                return None

            raise Exception (
                f"ERROR: File {file} not found or cannot be read."
            ) from None


def safe_file_write (file : Path, data, json : bool = False) :
    """
    Write data to a file safely.

    :param file: The file to write to.
    :param data: The data to write.
    :param json: Whether to serialize the data as JSON.
    :raises Exception: If the file cannot be written.
    """
    try :
        if json :
            if data is None :
                return

            with file.open ("w", encoding = "utf-8") as handle :
                dump (data, handle, indent = 4)

            return

        file.write_text (data, encoding = "utf-8")

    except PermissionError :
        raise Exception (
            "Permission denied. Try running Kable with administrative privilages."
        ) from None

    except (OSError, JSONDecodeError, UnicodeError) :
        raise Exception (
            f"ERROR: File {file} cannot be written to."
        ) from None


def run_git_command (*args, return_process : bool = False) -> str | CompletedProcess | CalledProcessError :
    """
    Execute a Git command.

    :param args: Arguments to pass to Git.
    :param return_process: Whether to return the process object instead of command output.
    :returns: Command output, a CompletedProcess, or a CalledProcessError depending on the arguments and execution result.
    """
    try :
        result = run (["git", *args], capture_output = True, text = True)
        return result if return_process else result.stdout.strip ()

    except CalledProcessError as exc :
        return exc if return_process else ""