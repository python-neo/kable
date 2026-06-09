from pathlib import Path

from textual.widgets import Label, TextArea

from .utils import checksum, safe_file_read, safe_file_write


class Editor (TextArea) :
    """
    The editor widget for Kable.
    :param initial_text: The text to be displayed in the TextArea.
    :example: Editor (initial_text = 'hello')
    """

    def __init__ (self, initial_text : str = "", **kwargs) -> None :
        """
        The __init__ function for this widget.
        :param initial_text: The text to be displayed in the TextArea.
        """
        super ().__init__ (initial_text, show_line_numbers = True, **kwargs)
        self.initial_text = initial_text

    def save_file (self, file_path : Path) -> None :
        """
        Saves the contents of the editor to the specified file.
        :param file_path: The path of the file to save to.
        :raises Exception: Upon a file write error.
        """
        try :
            safe_file_write (file_path, self.text)
        except Exception as e :
            raise Exception (f"Failed to save file: {e}") from None

    def load_file (self, file_path : Path) -> None :
        """
        Loads a file into the editor.
        :param file_path: The path of the file to load.
        :raises Exception: Upon file read error.
        """
        try :
            content = safe_file_read (file_path)
            self.text = content if isinstance (content, str) and content else ""
        except Exception as e :
            raise Exception (f"Failed to load file: {e}") from None

    def update_location_label (self, location_label : Label) -> None :
        """
        Updates the location of the cursor in the editor.
        :param location_label: The Label to update.
        """
        line, column = self.cursor_location
        location_label.update (f"{line + 1}:{column + 1}")

    def has_unsaved_changes (self, file_path : Path) -> bool :
        """
        Check whether the editor contents differ from the file on disk.

        :param file_path: The path of the file to compare against.
        :returns: True if the editor contains unsaved changes, otherwise False.
        """
        try :
            disk_text = safe_file_read (file_path)
            disk_checksum = checksum (disk_text or "")
            editor_checksum = checksum (self.text)
            return disk_checksum != editor_checksum
        except Exception :
            return True

    def get_text (self) -> str :
        """
        Get the current editor contents.

        :returns: The text currently contained in the editor.
        """
        return self.text

    def set_text (self, text : str) -> None :
        """
        Set the editor contents.

        :param text: The text to place in the editor.
        """
        self.text = text