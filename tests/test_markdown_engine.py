import pytest
from src.rendering.markdown_engine import MarkdownEngine

def test_markdown_basic_rendering():
    engine = MarkdownEngine()
    md = "# Hello World\nThis is a test."
    html = engine.render(md)
    assert "<h1>Hello World</h1>" in html
    assert "<p>This is a test.</p>" in html

def test_markdown_tables():
    engine = MarkdownEngine()
    md = "| Header 1 | Header 2 |\n| -------- | -------- |\n| Cell 1 | Cell 2 |"
    html = engine.render(md)
    assert "<table>" in html
    assert "<th>Header 1</th>" in html
    assert "<td>Cell 1</td>" in html

def test_markdown_task_lists():
    engine = MarkdownEngine()
    md = "- [ ] Task 1\n- [x] Task 2"
    html = engine.render(md)
    assert "Task 1" in html
    assert "Task 2" in html
