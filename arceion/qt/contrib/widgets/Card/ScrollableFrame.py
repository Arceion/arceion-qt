from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

from arceion.qt.contrib.styles.Card import defaultScrollArea
from arceion.qt.contrib.styles.Frame import defaultFrame
from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.contrib.widgets.Card import ScrollArea
from arceion.qt.contrib.widgets.Frame import VBoxFrame

__all__ = ["ScrollableFrame"]


class ScrollableFrame(ScrollArea):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setContentsMargins(Margin(0))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setStyleSheet(defaultScrollArea.qss)

        self.layout = VBoxFrame(self, *args, **kwargs)
        self.layout.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setContentsMargins(Margin(0))
        self.layout.setStyleSheet(defaultFrame.qss)

        self.setWidget(self.layout)
