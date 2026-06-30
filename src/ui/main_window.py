from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QToolBar,
    QStatusBar,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from .editor_widget import EditorWidget
from .preview_widget import PreviewWidget
from .sidebar_widget import SidebarWidget

from src.rendering.markdown_engine import MarkdownEngine
from src.rendering.html_builder import HtmlBuilder


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarkdownToHtml - Editor")
        self.resize(1200, 800)
        self.current_theme = "light"

        # Main splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        # Widgets
        self.sidebar = SidebarWidget()
        self.editor = EditorWidget()
        self.preview = PreviewWidget()

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        self.splitter.setSizes([200, 500, 500])

        # Setup menus, toolbar, statusbar
        self.setup_menu()
        self.setup_toolbar()

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # Connections
        self.editor.textChanged.connect(self.update_preview)
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll)

        # Load sample text
        self.editor.setPlainText("# Hello Markdown\n\nWrite your markdown here.")

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        export_action = QAction("Export as HTML", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_html)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        menubar.addMenu("Edit")

        view_menu = menubar.addMenu("View")
        split_view_action = QAction("Split View", self)
        split_view_action.triggered.connect(lambda: self.set_view_mode("split"))
        view_menu.addAction(split_view_action)

        editor_only_action = QAction("Editor Only", self)
        editor_only_action.triggered.connect(lambda: self.set_view_mode("editor"))
        view_menu.addAction(editor_only_action)

        preview_only_action = QAction("Preview Only", self)
        preview_only_action.triggered.connect(lambda: self.set_view_mode("preview"))
        view_menu.addAction(preview_only_action)

        settings_menu = menubar.addMenu("Settings")
        theme_action = QAction("Toggle Dark/Light Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

    def update_preview(self):
        text = self.editor.toPlainText()
        engine = MarkdownEngine()
        builder = HtmlBuilder()
        html_fragment = engine.render(text)
        styled_html = builder.build_html(html_fragment, theme=self.current_theme)
        self.preview.set_html(styled_html)

    def sync_scroll(self, value):
        scrollbar = self.editor.verticalScrollBar()
        max_val = scrollbar.maximum()
        if max_val > 0:
            percentage = value / max_val
            self.preview.sync_scroll(percentage)
        else:
            self.preview.sync_scroll(0)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Markdown", "", "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
                self.status.showMessage(f"Opened {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown", "", "Markdown Files (*.md);;All Files (*)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.editor.toPlainText())
                self.status.showMessage(f"Saved {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    def export_html(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export HTML", "", "HTML Files (*.html);;All Files (*)"
        )
        if path:
            try:
                text = self.editor.toPlainText()
                engine = MarkdownEngine()
                builder = HtmlBuilder()
                html_fragment = engine.render(text)
                styled_html = builder.build_html(
                    html_fragment, theme=self.current_theme
                )
                with open(path, "w", encoding="utf-8") as f:
                    f.write(styled_html)
                self.status.showMessage(f"Exported HTML to {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not export HTML: {e}")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.update_preview()
        self.status.showMessage(f"Theme switched to {self.current_theme.capitalize()}")

    def set_view_mode(self, mode: str):
        if mode == "split":
            self.editor.show()
            self.preview.show()
        elif mode == "editor":
            self.editor.show()
            self.preview.hide()
        elif mode == "preview":
            self.editor.hide()
            self.preview.show()
        self.status.showMessage(f"Switched to {mode.replace('_', ' ').title()} Mode")
