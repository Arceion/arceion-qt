from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.contrib.widgets.Attr import Border
from arceion.qt.util import Style

__all__ = ["defaultFrame"]

defaultFrame = Style(
    """
QFrame [
	background-color: {backgroundColor};
	border-radius: {borderRadius}px;
	border: {border};
]
""",
    **dict(
        backgroundColor="transparent",
        borderRadius=0,
        border=Border(BorderStyle.NONE).qss,
    ),
)
