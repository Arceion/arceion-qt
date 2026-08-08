from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from arceion.qt.contrib.widgets.Attr import Margin

from .Frame import Frame

__all__ = ["HBoxFrame"]


class HBoxFrame(Frame):
    """
    HBoxWidget(parent: type[QWidget] | QWidget | None = None, spacing: int = 0, margin: Margin | None = None,
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft, **kwargs)

    HBoxWidget is a subclass of Widget designed for creating horizontal box layouts.

    This class provides a streamlined way to set up a horizontal box layout using
    `QHBoxLayout`. It allows you to control layout properties such as spacing,
    margin, and alignment while supporting additional customization through
    keyword arguments. This is ideal for organizing child widgets horizontally
    within a parent widget.
    """

    def __init__(
        self,
        parent: type[QWidget] | QWidget | None = None,
        spacing: int = 0,
        margin: Margin | None = None,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
        **kwargs,
    ):
        """
        Initializes an instance of the class with the specified layout and alignment
        parameters.

        The constructor sets up the widget using an `QHBoxLayout`. It allows specifying
        a parent widget, spacing, margin, and alignment for the layout, along with other
        optional keyword arguments.

        Args:
            parent (type[QWidget] | QWidget | None): The parent widget for this
                instance. Defaults to None.
            spacing (int): The spacing to use between layout elements. Defaults to 0.
            margin (Margin | None): The margin to set around the layout. Defaults to
                None.
            alignment (Qt.AlignmentFlag): The alignment of the layout within the widget.
                Defaults to `Qt.AlignmentFlag.AlignLeft`.
            **kwargs: Additional arguments to be passed to the superclass constructor.
        """

        super().__init__(
            parent=parent,
            layout=QHBoxLayout,
            spacing=spacing,
            margin=margin,
            alignment=alignment,
            **kwargs,
        )
