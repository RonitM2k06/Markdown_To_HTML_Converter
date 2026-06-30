import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Set a dark theme stylesheet
    dark_stylesheet = """
    QMainWindow {
        background-color: #2b2b2b;
    }
    QWidget {
        color: #b1b1b1;
        background-color: #2b2b2b;
    }
    QPlainTextEdit {
        background-color: #1e1e1e;
        color: #d4d4d4;
        border: 1px solid #333333;
    }
    QTreeView {
        background-color: #252526;
        color: #cccccc;
        border: none;
    }
    QSplitter::handle {
        background-color: #333333;
    }
    QMenuBar {
        background-color: #2d2d2d;
        color: #cccccc;
    }
    QMenuBar::item:selected {
        background-color: #3d3d3d;
    }
    QMenu {
        background-color: #2d2d2d;
        color: #cccccc;
        border: 1px solid #333333;
    }
    QMenu::item:selected {
        background-color: #3d3d3d;
    }
    QToolBar {
        background-color: #2d2d2d;
        border: none;
    }
    QStatusBar {
        background-color: #007acc;
        color: white;
    }
    """
    app.setStyleSheet(dark_stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
