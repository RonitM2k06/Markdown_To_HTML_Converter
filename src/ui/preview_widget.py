from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView


class PreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.view = QWebEngineView()
        self.layout.addWidget(self.view)

    def set_html(self, html):
        self.view.setHtml(html)

    def sync_scroll(self, percentage):
        script = f"window.scrollTo(0, (document.body.scrollHeight - window.innerHeight) * {percentage});"
        self.view.page().runJavaScript(script)
