from PyQt6.QtGui import QColor

from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.util import UI

__all__ = ["Border"]


class Border:
    """
    Border(style: BorderStyle)
    Border(color: QColor | str | None = None, style: BorderStyle | None = None, width: int | None = None)

    A class that represents a border with customizable color, style, and width.

    This class is used to define the appearance of a border in a UI component. It supports
    customization of the border's color, style, and width using appropriate methods. The border's
    representation can be exported as a CSS-style string for direct application in UI styling.

    Properties:
        qss (str): The CSS style string dynamically calculated based on the border's color,
            style, and width.

    Methods:
            setColor(color: QColor): Sets the color of the border.
            setStyle(style: BorderStyle): Sets the border style.
            setWidth(width: int): Sets the width of the border.
    """

    _borderColor: QColor = QColor("black")
    _borderStyle: BorderStyle = BorderStyle.SOLID
    _borderWidth: int = 1  # in px

    def __init__(self, *args, **kwargs):
        """
        Initializes the border style with specified arguments or keyword arguments.

        This constructor allows creating a border style object by either passing a single
        `BorderStyle` object or by providing three positional or keyword arguments for color,
        style, and width.

        Args:
            *args:
                If one argument is provided, it should be an instance of `BorderStyle`.
                If three arguments are provided, they are expected to represent color, style,
                and width in that order.
            **kwargs:
                Optional keyword arguments for:
                - color: Specifies the border color.
                - style: Specifies the border style.
                - width: Specifies the border width.

        Raises:
            TypeError: If the single argument provided in `*args` is not an instance of `BorderStyle`.
            TypeError: If the number of arguments provided in `*args` is not 1 or 3.
        """

        if len(args) == 1:
            if not isinstance(args[0], BorderStyle):
                raise TypeError(f"Invalid type for style: {type(args[0])}")
            self._borderStyle = args[0]
            return
        if len(args) == 3:
            kwargs["color"], kwargs["style"], kwargs["width"] = args
        elif len(args) != 0:
            raise TypeError(f"Invalid number of arguments: {len(args)}")
        self.setColor(kwargs.get("color", self._borderColor))
        self.setStyle(kwargs.get("style", self._borderStyle))
        self.setWidth(kwargs.get("width", self._borderWidth))

    @property
    def qss(self):
        """
        Returns the CSS style string for the border of a UI component.

        The `qss` property dynamically generates a string based on the internal
        border color, style, and width attributes. If the border style is set to
        `BorderStyle.NONE`, it returns the name of the `BorderStyle.NONE` enumeration.

        Returns:
            str: A string representation of the border style in CSS format.
        """

        return (
            (
                f"{self._borderWidth}px {self._borderStyle.value} "
                f"{self._borderColor.name(format=QColor.NameFormat.HexArgb)}"
            )
            if self._borderStyle != BorderStyle.NONE
            else BorderStyle.NONE.name
        )

    def setColor(self, color: QColor):
        """
        Sets the color of the border.

        This method takes a QColor object or a string representing a color. If a string
        is passed, it is converted to a QColor object. The method ensures that the
        input is of the correct type and raises a TypeError if it is not.

        Args:
            color (QColor or str): The color to set for the border. Accepts a QColor
                object or a string representing a color.

        Raises:
            TypeError: If the provided color is not of type QColor or str.
        """

        if isinstance(color, str):
            color = QColor(color)
        if not isinstance(color, QColor):
            raise TypeError(f"Invalid type for color: {type(color)}")
        self._borderColor = color

    def setStyle(self, style: BorderStyle):
        """
        Sets the border style for the object.

        Args:
            style (BorderStyle): The border style to set.

        Raises:
            TypeError: If `style` is not of type `BorderStyle`.
        """

        if not isinstance(style, BorderStyle):
            raise TypeError(f"Invalid type for style: {type(style)}")
        self._borderStyle = style

    def setWidth(self, width: int):
        """
        Sets the width of the border.

        This method assigns the specified width value to the border width attribute of
        the object.

        Args:
            width (int): The desired width for the border.
        """

        if not isinstance(width, int):
            raise TypeError(f"Invalid type for width: {type(width)}")
        self._borderWidth = UI.dp(width)

    def __repr__(self):
        """
        Provides a string representation of the Border object, including its color, style, and width.

        Returns:
            str: A string detailing the color (in ARGB hexadecimal format), style, and width of the border.
        """

        return (
            f"Border(color={self._borderColor.name(format=QColor.NameFormat.HexArgb)}, style={self._borderStyle.value},"
            f" width={self._borderWidth})"
            if self._borderStyle != BorderStyle.NONE
            else f"Border(style={BorderStyle.NONE.value})"
        )

    def __str__(self):
        """
        Provides a string representation of the object instance.

        This method is used to define the behavior of the `str()` function for the
        object and returns a user-friendly string representation.

        Returns:
            str: A string representation of the object instance.
        """

        return self.__repr__()
