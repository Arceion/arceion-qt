from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.contrib.widgets.Attr import Border
from arceion.qt.util import UI, Style

__all__ = ["defaultCard", "defaultScrollArea", "defaultScrollAreaFrame"]

defaultCard = Style(
    """
QFrame [
	background-color: {backgroundColor};
	border-radius: {borderRadius}px;
	border: {border};
]
""",
    **dict(
        backgroundColor="#FAFAFA",
        borderRadius=UI.dp(4),
        border=Border("#D9D9D9", BorderStyle.SOLID, 1).qss,
    ),
)

defaultScrollArea = Style(
    """
QScrollArea [
	border: {border};
	background: {backgroundColor};
]

QScrollBar:vertical [

]

QScrollBar::handle:vertical [

]

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical [

]

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical [

]
""",
    **dict(
        border=Border(BorderStyle.NONE).qss,
        backgroundColor="transparent",
        scrollBarBorder=Border(BorderStyle.NONE).qss,
    ),
)

defaultScrollAreaFrame = Style(
    """
QFrame [
	background-color: {backgroundColor};
	border-radius: {borderRadius}px;
	border: {border};
]
""",
    **dict(
        backgroundColor="#FAFAFA",
        borderRadius=UI.dp(4),
        border=Border("#D9D9D9", BorderStyle.SOLID, 1).qss,
    ),
)
