from pydantic import BaseModel, Field, field_validator
from abc import ABC, abstractmethod
from typing import Optional, List


class Shortcut(BaseModel):
    key_combination: str = Field(..., description="Key combination, e.g. Ctrl+S")
    name: str = Field(..., description="Name of the shortcut action")
    description: Optional[str] = Field(
        None, description="Detailed description of what the shortcut does"
    )
    mode: Optional[str] = Field(
        None, description="Editor mode or context, if applicable"
    )

    @field_validator("key_combination")
    def normalize_key(cls, v: str) -> str:
        """Ensure key combinations are normalized and readable."""
        return v.strip().replace(" +", "+").replace("+ ", "+").replace(" ", "")

    def to_markdown_row(self) -> str:
        """Convert one shortcut to a Markdown table row."""
        return f"| `{self.key_combination}` | {self.name} | {self.description or ''} | {self.mode or ''} |"


class ShortcutList(BaseModel):
    """Wrapper model to ensure list-wide validation or post-processing."""

    shortcuts: List[Shortcut]

    def to_markdown(self, title: str = "Shortcuts") -> str:
        """Render the whole list to Markdown."""
        if not self.shortcuts:
            return f"# {title}\n\n_No shortcuts found._"

        header = "| Key | Action | Description | Mode |\n|-----|---------|-------------|------|"
        rows = "\n".join(shortcut.to_markdown_row() for shortcut in self.shortcuts)
        return f"# {title}\n\n{header}\n{rows}\n"


class BaseParser(ABC):
    """Defines the standard interface for all parsers.
    Can be used directly from subclasses without creating objects.
    """

    title = None

    @classmethod
    @abstractmethod
    def get_application_output(cls) -> str:
        """Retrieve raw output from the target application."""
        raise NotImplementedError("This parser is not yet implemented")

    @classmethod
    @abstractmethod
    def parse_output(cls, raw_text: str) -> ShortcutList:
        """Convert raw text into a validated ShortcutList."""
        raise NotImplementedError("This parser is not yet implemented")

    @classmethod
    def filter_shortcuts(cls, Shortcuts: ShortcutList) -> ShortcutList:
        """Filter out only the required keymaps"""
        raise NotImplementedError("This parser is not yet implemented")

    @classmethod
    def convert_to_markdown(cls) -> str:
        """High-level API: fetch → parse → render."""
        if not cls.title:
            raise NotImplementedError("This class title is not defined")
        raw_text = cls.get_application_output()
        shortcuts = cls.parse_output(raw_text)
        filtered_shortcuts = cls.filter_shortcuts(shortcuts)
        return filtered_shortcuts.to_markdown(f"{cls.title} Shortcuts")
