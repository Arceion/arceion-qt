from PyQt6.QtWidgets import QCheckBox

from arceion.qt.contrib.styles.CheckBox import defaultCheckBox
from arceion.qt.util import UI, Style

__all__ = ["CheckBox"]


class CheckBox(QCheckBox):
    """
    This class is a custom checkbox widget that can be styled using a Style object. It inherits from QCheckBox and
    provides additional functionality to set the height of the checkbox indicator and to apply custom styles.
    The checkbox can be styled using a Style object that defines the appearance of the checkbox.

    Methods:
            setHeight(height: int) -> None: Sets the height of the checkbox indicator.
            setStyle(style: Style) -> None: Sets the style of the checkbox.
            updateStyle(self) -> None: Updates the style of the checkbox.
    """

    _height: int = NotImplemented
    _style: Style = defaultCheckBox

    def __init__(self, parent=None, text: str | None = None, height: int | None = None):
        """
        This class is a custom checkbox widget that can be styled using a Style object.

        Args:
                parent: The parent widget of the checkbox. Default is None.
                text: The text to be displayed next to the checkbox. Default is None.
                height: The height of the checkbox indicator. Default is None, which uses the default height from the style.
        """

        super().__init__(parent=parent, text=text)

        self._height = self.size().height()
        if height is not None:
            self.setHeight(height)

    def setHeight(self, height: int) -> None:
        """
        This method sets the height of the checkbox indicator.

        Args:
                height: The height of the checkbox indicator.

        Returns: None
        """

        if not isinstance(height, int) or not height > 0:
            raise ValueError("Height must be a positive integer")
        self._height = height
        self.setFixedHeight(UI.dp(height))
        self.updateStyle()

    def setStyle(self, style: Style) -> None:
        """
        This method sets the style of the checkbox.

        Args:
                style: The style to be applied to the checkbox.

        Returns: None
        """

        self._style = style
        self.updateStyle()

    def updateStyle(self) -> None:
        """
        This method updates the style of the checkbox.

        Returns: None
        """

        if not self._style:
            return
        self._style.update(
            width=self._height - UI.dp(2),
            height=self._height - UI.dp(2),
        ).apply(self)
