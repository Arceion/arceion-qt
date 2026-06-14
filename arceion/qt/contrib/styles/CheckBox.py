from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.contrib.widgets.Attr import Border
from arceion.qt.util import UI, Style

__all__ = ["defaultCheckBox"]

defaultCheckBox = Style(
    """
QCheckBox [
	font-size: {fontSize}px;
	spacing: {spacing}px;
	color: {color};
]

QCheckBox::indicator [
	width: {width}px;
	height: {height}px;
	border: {border};
	border-radius: {borderRadius}px;
	background-color: {backgroundColor};
]

QCheckBox::indicator:checked [
	background-color: {checkedColor};
	border: {checkedBorder};
]

QCheckBox::indicator:unchecked [
	background-color: {uncheckedColor};
]

QCheckBox::indicator:hover [
	border: {hoverBorder};
]
""",
    **dict(
        fontSize=UI.sp(12),
        spacing=UI.dp(8),
        width=UI.dp(16),
        height=UI.dp(16),
        color="#ffffff",
        backgroundColor="#2b2b2b",
        border=Border("#666666", BorderStyle.SOLID, 1).qss,
        borderRadius=UI.dp(5),
        checkedColor="#c992d2",
        checkedBorder=Border("transparent", BorderStyle.SOLID, 1).qss,
        uncheckedColor="#2b2b2b",
        hoverBorder=Border("#ffffff", BorderStyle.SOLID, 1).qss,
    ),
)
