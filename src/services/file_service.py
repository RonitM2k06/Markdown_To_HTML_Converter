from pathlib import Path
from typing import Optional
from loguru import logger
from ..models.document import Document


class FileService:
    @staticmethod
    def open_markdown(file_path: Path) -> Optional[Document]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            doc = Document(content=content, file_path=file_path, is_modified=False)
            logger.info(f"Opened markdown file: {file_path}")
            return doc
        except Exception as e:
            logger.error(f"Error opening markdown file {file_path}: {e}")
            return None

    @staticmethod
    def save_markdown(document: Document, file_path: Optional[Path] = None) -> bool:
        target_path = file_path or document.file_path
        if not target_path:
            logger.error("No file path provided for saving markdown.")
            return False

        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(document.content)
            document.file_path = target_path
            document.mark_saved()
            logger.info(f"Saved markdown to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving markdown to {target_path}: {e}")
            return False

    @staticmethod
    def export_html(html_content: str, file_path: Path) -> bool:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"Exported HTML to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting HTML to {file_path}: {e}")
            return False
