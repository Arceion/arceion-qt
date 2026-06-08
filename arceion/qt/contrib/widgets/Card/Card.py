from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget

from arceion.qt.contrib.styles.Card import defaultCard
from arceion.qt.contrib.widgets.Attr import Margin
from arceion.qt.util import Style

__all__ = ["Card"]


class Card(QFrame):
    """
    Represents a customized frame widget with a vertical layout, margin, and style.

    This class provides a QFrame-based widget that allows for customization of its layout
    using a vertical box layout (QVBoxLayout). It supports applying margin settings to its
    content and applying custom stylesheets or style objects. It is designed for use as a
    reusable component in Qt-based UI applications.

    Attributes:
        parent (QWidget | None): The parent widget associated with this widget. Defaults to None.
    """

    parent: QWidget | None

    def __init__(
        self,
        parent: QWidget | None = None,
        margin: Margin | None = None,
        style: str | Style = defaultCard,
    ):
        """
        Initializes the class with a parent widget, margin, and style.

        This constructor sets up the layout for the widget using a QVBoxLayout,
        applies the given margin to the layout, applies the provided style, and
        associates the widget with its optional parent.

        Args:
            parent (QWidget | None): The parent widget, if any, to which this widget belongs.
            margin (Margin | None): The margin settings for the layout content. If not provided,
                defaults to a Margin instance initialized with 0.
            style (str | Style): The stylesheet or style object to be applied to the widget.
                If a `Style` object is provided, its `qss` property is applied as the stylesheet.
        """

        super().__init__(parent)
        self.parent = parent

        if margin is None:
            margin = Margin(0)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(margin)
        self.setLayout(self.layout)

        self.setStyleSheet(style if isinstance(style, str) else style.qss)
