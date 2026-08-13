from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from arceion.qt.util import Style

__all__ = ["Label"]


class Label(QLabel):
    _onClick: Callable | None = NotImplemented

    def __init__(
        self, text: str | None = None, style: Style | None = None, parent=None, onClick: Callable | None = None
    ):
        super().__init__(parent=parent)
        self._text = text
        self._style = style
        self.onClick(onClick)

        self.setText(text)
        self.updateStyle()

    def setStyle(self, style: Style):
        self._style = style
        self.updateStyle()

    def updateStyle(self):
        if self._style:
            self.setStyleSheet(self._style.qss)

    def mousePressEvent(self, ev):
        if self._onClick:
            self._onClick()

    def onClick(self, action: Callable):
        self._onClick = action
        self.setCursor(Qt.CursorShape.PointingHandCursor if action else Qt.CursorShape.ArrowCursor)
