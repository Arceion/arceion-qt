from arceion.qt.contrib.enums import BorderStyle, FontWeight
from arceion.qt.contrib.widgets.Attr import Border, Margin
from arceion.qt.util import UI, Style

__all__ = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

h1 = Style("""
QLabel [
	background-color: {backgroundColor};
	font-family: {fontFamily};
	font-weight: {fontWeight};
	font-size: {fontSize}px;
	border: {border};
	color: {color};
	margin: {margin};
]
""", **dict(
	fontFamily="'Inter'",
	fontWeight=FontWeight.Bold,
	fontSize=UI.sp(36),
	border=Border(BorderStyle.NONE).qss,
	color='white',
	margin=Margin(0, 0, 0, 20).qss,
	backgroundColor='transparent',
))

h2 = h1.update(
	fontSize=UI.sp(32),
)

h3 = h1.update(
	fontSize=UI.sp(28),
)

h4 = h1.update(
	fontSize=UI.sp(24),
	fontWeight=FontWeight.SemiBold,
)

h5 = h1.update(
	fontSize=UI.sp(20),
	fontWeight=FontWeight.Medium,
)

h6 = h1.update(
	fontSize=UI.sp(16),
	fontWeight=FontWeight.Normal,
)
