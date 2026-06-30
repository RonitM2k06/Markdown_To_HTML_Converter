from jinja2 import Environment, BaseLoader
from loguru import logger

# Using a basic GitHub-like CSS for layout, and specific classes for themes
TEMPLATE_STR = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --bg-color-light: #ffffff;
            --text-color-light: #24292e;
            --link-color-light: #0366d6;
            --code-bg-light: #f6f8fa;
            --border-color-light: #e1e4e8;
            
            --bg-color-dark: #0d1117;
            --text-color-dark: #c9d1d9;
            --link-color-dark: #58a6ff;
            --code-bg-dark: #161b22;
            --border-color-dark: #30363d;
        }

        body.light {
            background-color: var(--bg-color-light);
            color: var(--text-color-light);
        }
        body.light a { color: var(--link-color-light); }
        body.light pre, body.light code { background-color: var(--code-bg-light); }
        body.light table th, body.light table td { border-color: var(--border-color-light); }

        body.dark {
            background-color: var(--bg-color-dark);
            color: var(--text-color-dark);
        }
        body.dark a { color: var(--link-color-dark); }
        body.dark pre, body.dark code { background-color: var(--code-bg-dark); }
        body.dark table th, body.dark table td { border-color: var(--border-color-dark); }

        body {
            font-family: {{ font_family }}, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: {{ font_size }}px;
            line-height: 1.6;
            padding: 2em;
            max-width: 900px;
            margin: 0 auto;
        }

        table { border-collapse: collapse; width: 100%; margin-bottom: 1em; }
        th, td { border: 1px solid; padding: 8px 12px; }
        
        pre { padding: 16px; overflow: auto; border-radius: 6px; }
        code { padding: 0.2em 0.4em; border-radius: 3px; font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace; }
        pre code { padding: 0; background-color: transparent; }
        
        blockquote { margin: 0; padding: 0 1em; color: #6a737d; border-left: 0.25em solid #dfe2e5; }
        body.dark blockquote { color: #8b949e; border-color: #30363d; }
    </style>

    <!-- KaTeX CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
</head>
<body class="{{ theme }}">
    <div id="content" class="markdown-body">
        {{ content }}
    </div>

    <!-- KaTeX JS for rendering math -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {delimiters:[{left:'$$', right:'$$', display:true}, {left:'$', right:'$', display:false}]});">
    </script>

    <!-- Mermaid JS for diagrams -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: false, theme: '{{ "dark" if theme == "dark" else "default" }}' });
        
        document.addEventListener("DOMContentLoaded", async () => {
            const nodes = document.querySelectorAll("code.language-mermaid");
            nodes.forEach(node => {
                const pre = node.parentElement;
                pre.classList.add("mermaid");
                pre.textContent = node.textContent;
            });
            await mermaid.run({
                nodes: document.querySelectorAll('.mermaid')
            });
        });
    </script>
</body>
</html>"""


class HtmlBuilder:
    def __init__(self) -> None:
        logger.debug("Initializing HtmlBuilder")
        self.env = Environment(loader=BaseLoader())
        self.template = self.env.from_string(TEMPLATE_STR)

    def build_html(
        self,
        html_content: str,
        title: str = "Markdown Document",
        theme: str = "light",
        font_family: str = "sans-serif",
        font_size: int = 14,
    ) -> str:
        """Wraps the HTML content from markdown into a full HTML document."""
        try:
            rendered = self.template.render(
                content=html_content,
                title=title,
                theme=theme,
                font_family=font_family,
                font_size=font_size,
            )
            logger.debug("Successfully built full HTML document.")
            return rendered
        except Exception as e:
            logger.error(f"Error building HTML document: {e}")
            return f"<html><body><h1>Error</h1><p>{e}</p></body></html>"
