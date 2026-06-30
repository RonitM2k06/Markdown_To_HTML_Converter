from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Document:
    content: str = ""
    file_path: Optional[Path] = None
    is_modified: bool = False

    def update_content(self, new_content: str) -> None:
        if self.content != new_content:
            self.content = new_content
            self.is_modified = True

    def mark_saved(self) -> None:
        self.is_modified = False
