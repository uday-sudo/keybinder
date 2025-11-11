from annotated_types import SLOTS
from utils.core import BaseParser, ShortcutList, Shortcut
import shlex
import subprocess
import re


def process_tmux_line(line):
    """
    Parse one 'tmux list-keys' line into (description, key_combination, mode).

    Example:
        "bind-key -r -T prefix S-Right refresh-client -R 10"
        → ("refresh-client -R 10", "S-Right", "prefix")
    """
    # Split line safely (handles quoted args)
    parts = shlex.split(line)

    if not parts or parts[0] != "bind-key":
        raise ValueError("Not a tmux bind-key line")

    mode = None
    key_combination = ""
    description_parts = []

    def strip_consec_spaces(text: str):
        return re.sub(" +", " ", text).strip()

    mode = strip_consec_spaces(line[0:27])
    key_combination = strip_consec_spaces(line[28:51])
    description = strip_consec_spaces(line[51:])

    # Iterate through parts manually
    return Shortcut(
        key_combination=key_combination,
        name=description,
        description=description,
        mode=mode,
    )


class TmuxParser(BaseParser):
    title = "TMUX"

    @classmethod
    def get_application_output(cls) -> str:
        """Retrieve raw output from tmux"""
        buffer_output = subprocess.run(
            ["tmux", "list-keys"], capture_output=True, text=True, check=True
        )
        return buffer_output.stdout

    @classmethod
    def parse_output(cls, raw_text: str) -> ShortcutList:
        """Convert raw text into a validated ShortcutList."""
        lines = raw_text.split("\n")[:-1]
        shortcuts = [process_tmux_line(line) for line in lines]
        return ShortcutList(shortcuts=shortcuts)

    @classmethod
    def filter_shortcuts(cls, shortcuts: ShortcutList) -> ShortcutList:
        """Filter out only the required keymaps"""
        return shortcuts
