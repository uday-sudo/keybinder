from utils.core import BaseParser, ShortcutList
import subprocess


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
        raise NotImplementedError("This parser is not yet implemented")

    @classmethod
    def filter_shortcuts(cls, Shortcuts: ShortcutList) -> ShortcutList:
        """Filter out only the required keymaps"""
        raise NotImplementedError("This parser is not yet implemented")
