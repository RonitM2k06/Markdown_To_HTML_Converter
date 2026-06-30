# MarkdownToHtml

A modern, production-ready desktop application that converts Markdown into HTML with a beautiful live preview, syntax highlighting, and an unparalleled professional editing experience.

## ✨ Features
- **Live HTML Preview:** Real-time rendering with WebEngine and synchronized scrolling.
- **Robust Markdown Engine:** Supports GFM, tables, footnotes, task lists, strikethrough, Math (KaTeX), and Mermaid diagrams.
- **Advanced Code Editor:** Syntax highlighting, line numbers, auto-indentation, and powerful search/replace.
- **Project Explorer:** Integrated sidebar to browse directories and manage files.
- **Customizable Themes:** Switch between premium Dark and Light UI themes.
- **Export Options:** Export your documents to styled HTML, plain HTML, or PDF.
- **Session Management:** Auto-saving and settings persistence.

## 📸 Screenshots
*(Coming soon)*

## 🛠️ Tech Stack
- **Python 3.13+**
- **UI Framework:** PySide6
- **Markdown Engine:** markdown-it-py (with mdit-py-plugins)
- **Code Highlighting:** Pygments
- **HTML Templating:** Jinja2 + BeautifulSoup4
- **Testing & Tooling:** pytest, black, ruff, mypy, loguru

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/MarkdownToHtml.git
   cd MarkdownToHtml
   ```
2. **Set up a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Launch the application:**
   ```bash
   python src/main.py
   ```

## 📐 Architecture
MarkdownToHtml follows SOLID principles and Clean Architecture. See our [Architecture Documentation](docs/Architecture.md) for more details.

## 🤝 Contributing
Please see our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
