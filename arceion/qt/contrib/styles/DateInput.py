from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.util import UI, Style

__all__ = ["defaultDateInput"]

defaultDateInput = Style(
    """
QFrame [
    border: {border};
    border-radius: {radius}px;
    background-color: {backgroundColor};
]
QLineEdit [
    border: none;
    background: transparent;
    color: {color};
    padding: {inputPadding};
]
""",
    **dict(
        border="1px solid #27272A",
        radius=UI.dp(6),
        backgroundColor="#18181B",
        color="#FAFAFA",
        inputPadding=Padding(UI.dp(4), UI.dp(8)).qss,
    )
)
