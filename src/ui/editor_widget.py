import re
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QSyntaxHighlighter, QTextCharFormat, QFont


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightingRules = []

        # Heading
        header_format = QTextCharFormat()
        header_format.setFontWeight(QFont.Bold)
        header_format.setForeground(QColor("#569CD6"))  # Blue
        self.highlightingRules.append((r"^(#+)(.*)", header_format))

        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        bold_format.setForeground(QColor("#DCDCAA"))
        self.highlightingRules.append((r"\*\*(.*?)\*\*", bold_format))
        self.highlightingRules.append((r"__(.*?)__", bold_format))

        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        italic_format.setForeground(QColor("#C586C0"))
        self.highlightingRules.append((r"\*(.*?)\*", italic_format))
        self.highlightingRules.append((r"_(.*?)_", italic_format))

        # Code
        code_format = QTextCharFormat()
        code_format.setFontFamily("Consolas")
        code_format.setForeground(QColor("#CE9178"))
        self.highlightingRules.append((r"`(.*?)`", code_format))

        # Blockquote
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor("#608B4E"))
        self.highlightingRules.append((r"^> (.*)", quote_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)


class EditorWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        self.highlighter = MarkdownHighlighter(self.document())

        self.setStyleSheet(
            "font-family: Consolas, 'Courier New', monospace; font-size: 11pt;"
        )

    def lineNumberAreaWidth(self):
        digits = 1
        m = max(1, self.blockCount())
        while m >= 10:
            m /= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height()
            )
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            # Dark theme active line background
            selection.format.setBackground(QColor("#2a2d2e"))
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#1e1e1e"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#858585"))
                painter.drawText(
                    0,
                    int(top),
                    self.lineNumberArea.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignRight | Qt.AlignVCenter,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            current_line = cursor.block().text()
            indent = len(current_line) - len(current_line.lstrip())
            super().keyPressEvent(event)
            if indent > 0:
                self.insertPlainText(" " * indent)
            return
        super().keyPressEvent(event)
