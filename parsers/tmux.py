from collections import defaultdict
from pydantic import ValidationError
from utils.core import BaseParser, ShortcutList, Shortcut
import subprocess
from typing import Dict
import json


def process_tmux_line(line: str, tmux_map: dict) -> Shortcut:
    """
    Parse one 'tmux list-keys' line into (description, key_combination, mode).
    Example:
        "bind-key -r -T prefix S-Right refresh-client -R 10"
        → ("refresh-client -R 10", "S-Right", "prefix")
    """
    if not line.strip():
        raise ValidationError

    # Split by whitespace, preserving quoted strings
    parts = line.split()

    mode = "root"  # default mode
    key_combination = ""
    description = ""

    i = 0
    while i < len(parts):
        part = parts[i]

        # Skip 'bind-key'
        if part == "bind-key":
            i += 1
            continue

        # Handle flags
        if part == "-r":  # repeatable flag
            i += 1
            continue

        # Extract table/mode
        if part == "-T":
            i += 1
            if i < len(parts):
                mode = parts[i]
            i += 1
            continue

        # Handle other single-letter flags
        if part.startswith("-") and len(part) == 2:
            i += 1
            # Some flags take arguments
            if part in ["-p", "-I", "-N", "-d", "-h", "-w", "-x", "-y", "-t"]:
                # Skip the argument (might be quoted or a value)
                if i < len(parts) and not parts[i].startswith("-"):
                    i += 1
            continue

        # First non-flag, non-option token is the key combination
        if not key_combination:
            key_combination = part
            i += 1
            continue

        # Everything else is the command/description
        description = " ".join(parts[i:])
        break

    if key_combination.startswith("M-"):
        key_combination = f"Alt+{key_combination[2:]}"
    elif key_combination.startswith("C-"):
        key_combination = f"Ctrl+{key_combination[2:]}"

    return Shortcut(
        key_combination=key_combination,
        name=tmux_map.get(description, description.replace("|", r"\|")),
        description=description.replace("|", r"\|"),
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
        lines = raw_text.strip().split("\n")
        shortcuts = []

        with open("parsers/data/tmux_map.json", "r") as tmux_map_json:
            tmux_map = json.load(tmux_map_json)

        for line in lines:
            if line.strip():  # Skip empty lines
                shortcut = process_tmux_line(line, tmux_map)
                if shortcut:
                    shortcuts.append(shortcut)

        return ShortcutList(shortcuts=shortcuts)

    @classmethod
    def keep_shortcut(cls, shortcut: Shortcut):
        if not shortcut.key_combination or not shortcut.name:
            return False
        desc = (shortcut.description or "").lower()
        key = shortcut.key_combination.lower()
        name = shortcut.name.lower()
        if desc in ["", "no action"]:
            return False
        if any(x in key for x in ["drag", "wheel", "border"]):
            return False
        if any(
            x in desc
            for x in ["cursor-left", "cursor-right", "cursor-up", "cursor-down"]
        ):
            return False
        if "select " in name or "copy-pipe" in desc:
            return False
        if any([x in name for x in ["scroll", "copy", "context menu"]]):
            return False
        return True

    @classmethod
    def group_shortcuts(cls, shortcuts: ShortcutList) -> Dict[str, ShortcutList]:
        groups = defaultdict(lambda: ShortcutList(shortcuts=[]))
        for shortcut in shortcuts.shortcuts:
            key = shortcut.key_combination.lower()
            desc = (shortcut.description or "").lower()
            mode = (shortcut.mode or "").lower()

            if any(
                x in desc
                for x in [
                    "window",
                    "session",
                    "rename",
                    "new-session",
                    "new-window",
                    "switch-client",
                ]
            ):
                groups["Session & Window Management"].add(shortcut)
            elif any(x in desc for x in ["pane", "split", "resize", "swap", "zoom"]):
                groups["Pane Management"].add(shortcut)
            elif any(
                x in desc
                for x in [
                    "select",
                    "move",
                    "next",
                    "previous",
                    "last-window",
                    "last-pane",
                ]
            ):
                groups["Navigation"].add(shortcut)
            elif mode in ["copy-mode", "copy-mode-vi"] or any(
                x in desc for x in ["search", "copy", "paste", "scroll", "selection"]
            ):
                groups["Copy & Scroll Mode"].add(shortcut)
            elif "mouse" in key:
                groups["Mouse Actions"].add(shortcut)
            elif any(
                x in desc
                for x in ["layout", "even-horizontal", "even-vertical", "tiled"]
            ):
                groups["Layout & Zoom"].add(shortcut)
            elif mode == "root":
                groups["Global (Root Mode)"].add(shortcut)
            else:
                groups["Utility & Misc"].add(shortcut)

        return groups
