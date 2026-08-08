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
	background-color: {backgroundColor};
]

QScrollArea > QWidget > QWidget [
    background-color: {backgroundColor};
]

QScrollArea QWidget [
    background-color: {backgroundColor};
]

QScrollBar [
    background-color: transparent;
]

QScrollBar:vertical [
	border: {scrollBarBorder};
	background-color: transparent;
	border-radius: 8px;
	width: 18px;
	margin-left: 10px;
]

QScrollBar::handle:vertical [
	background: #287DC5;
	border-radius: 3px;
]

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical [
	border: none;
	height: 0px;
]

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical [
	background: transparent;
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
