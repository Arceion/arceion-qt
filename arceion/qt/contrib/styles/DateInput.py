"""Default style tokens for the date input widget."""

from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.util import UI, Style

__all__ = ["defaultDateInput"]

defaultDateInput = Style(
    """
QFrame#DateInputContainer [
    border: {border};
    border-radius: {radius}px;
    background-color: {backgroundColor};
]
QFrame#DateInputContainer:focus-within [
    border: 1px solid {focusColor};
    box-shadow: 0 0 0 2px {focusGlow};
]
QLineEdit [
    border: none;
    background: transparent;
    color: {color};
    padding: {inputPadding};
]
QToolButton, QPushButton [
    background: transparent;
    border: none;
    color: {buttonColor};
    padding: {buttonPadding};
    border-radius: {buttonRadius}px;
]
QToolButton:hover, QPushButton:hover [
    background-color: {hoverColor};
]
""",
    **dict(
        border="1px solid #E4E4E7",
        radius=UI.dp(10),
        backgroundColor="#171717",
        color="#F4F4FA",
        inputPadding=Padding(UI.dp(4), UI.dp(8)).qss,
        buttonColor="#71717A",
        buttonPadding=Padding(UI.dp(4), UI.dp(6)).qss,
        buttonRadius=UI.dp(6),
        hoverColor="#F4F4F5",
        focusColor="#2563EB",
        focusGlow="#DBEAFE",
    ),
)
