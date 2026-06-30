from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel
from PySide6.QtCore import QDir


class SidebarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))

        # Hide columns other than Name (index 0)
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        self.layout.addWidget(self.tree)
