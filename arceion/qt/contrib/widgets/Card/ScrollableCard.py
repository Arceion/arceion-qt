from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget

from arceion.qt.contrib.styles import Card
from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.util import UI

from .ScrollArea import ScrollArea

__all__ = ["ScrollableCard"]


class ScrollableCard(QFrame):
    """
    Represents a custom scrollable card widget with a border and configurable margins.

    This widget is designed to provide a scrollable area enclosed within a bordered frame,
    intended for hosting additional child widgets. It includes a custom layout for managing
    child widgets, a vertical scroll bar with configurable behavior, and supports customizable
    layout margins. The scrollable card is particularly useful for creating dynamic, scrollable
    containers with a polished visual appearance.

    Attributes:
        scrollBarVisibilityChanged (pyqtSignal): Signal emitted when the visibility state of
            the vertical scrollbar changes. Emits a boolean indicating the scroll bar visibility.
        parent (QWidget | None): The parent widget of this scrollable card. Can be None if no parent
            is assigned.

    Methods:
            onScrollAreaResized(self, state: bool) -> None: Handles the resizing event of the scroll area.
            setScrollAreaStyleSheet(self, styleSheet: str) -> None: Sets the stylesheet for the scroll area.
            setScrollAreaLayout(self, layout: QLayout) -> None: Sets the layout for the scroll area.
    """

    scrollBarVisibilityChanged: pyqtSignal = pyqtSignal(bool)
    parent: QWidget | None

    def __init__(self, parent: QWidget | None = None, margin: Margin | None = None):
        """
        Initializes an instance of a custom widget with a border, scrollable area, and defined
        layout margins.

        The widget consists of a scrollable area and a custom layout to host additional child
        widgets. The scroll area and its contents are styled appropriately and are configured with
        the provided or default margins.

        Args:
            parent (QWidget | None): The parent widget of the custom widget. Can be None, meaning
                the widget has no parent.
            margin (Margin | None): The margins to apply to the widget's layout. If None is provided,
                default margins will be set to zero.
        """

        super().__init__(parent)

        self.parent = parent

        if margin is None:
            margin = Margin(0)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(margin)
        self.setLayout(self.mainLayout)

        self.scrollArea = ScrollArea(self)
        self.scrollArea.setContentsMargins(Margin(0))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.verticalScrollBarStateChanged.connect(self.onScrollAreaResized)

        self.scrollAreaWidget = QWidget(self)
        self.scrollAreaWidget.setStyleSheet("background-color: transparent;")
        self.scrollAreaWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.layout = QVBoxLayout(self.scrollAreaWidget)
        self.layout.setContentsMargins(Margin(0, 0, UI.dp(24), 0))
        self.scrollAreaWidget.setLayout(self.layout)

        self.mainLayout.addWidget(self.scrollArea)

        self.setScrollAreaStyleSheet(Card.defaultScrollArea)
        self.setStyleSheet(Card.defaultScrollAreaFrame.qss)

    def onScrollAreaResized(self, state):
        """
        Handles the resizing event of the scroll area and updates layout margins
        and scrollbar visibility accordingly.

        Args:
            state (bool): Indicates whether the scroll area has been resized.
                True if resized, False otherwise.
        """

        if state:
            self.layout.setContentsMargins(Margin(0, 0, UI.dp(24), 0))
        else:
            self.layout.setContentsMargins(Margin(0))
        self.scrollBarVisibilityChanged.emit(state)

    def setScrollAreaStyleSheet(self, styleSheet):
        """
        Sets the stylesheet for the scroll area widget.

        This method applies the provided stylesheet to the scroll area to
        customize its appearance.

        Args:
            styleSheet: A string representing the CSS stylesheet to set
                for the scroll area.
        """

        self.scrollArea.setStyleSheet(styleSheet if isinstance(styleSheet, str) else styleSheet.qss)

    def setScrollAreaLayout(self, layout):
        """
        Sets the layout for the scroll area widget.

        This method applies the given layout to the scroll area's internal
        widget. It is used to manage the positioning and arrangement of
        child widgets within the scroll area.

        Args:
            layout: The layout to be set for the scroll area widget.
        """

        self.scrollAreaWidget.setLayout(layout)
