from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from loguru import logger


class MarkdownEngine:
    def __init__(self) -> None:
        logger.debug("Initializing MarkdownEngine with GFM and plugins")
        # Initialize markdown-it with GitHub Flavored Markdown equivalent settings
        self.md = (
            MarkdownIt("commonmark", {"breaks": True, "html": True})
            .enable("table")
            .enable("strikethrough")
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .use(tasklists_plugin)
        )

    def render(self, markdown_text: str) -> str:
        """Renders markdown text to HTML snippet."""
        try:
            html = self.md.render(markdown_text)
            logger.debug(f"Rendered markdown to HTML (length: {len(html)})")
            return html
        except Exception as e:
            logger.error(f"Error rendering markdown: {e}")
            return f"<div class='error'>Error rendering markdown: {e}</div>"
