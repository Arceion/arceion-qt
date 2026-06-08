from arceion.qt.contrib.enums import BorderStyle, FontWeight
from arceion.qt.contrib.widgets.Attr import Border, Padding
from arceion.qt.util import UI, Style

__all__ = ["label", "successBg", "errorBg", "transparentBg"]

label = Style(
    """
QLabel [
	background-color: {backgroundColor};
	color: {color};
	border: {border};
	border-radius: {radius}px;
	padding: {padding};
	font-size: {fontSize}px;
	text-align: {textAlign};
	font-weight: {fontWeight};
]
""",
    **dict(
        color="black",
        fontSize=UI.sp(12),
        textAlign="center",
        border=Border(BorderStyle.NONE).qss,
        backgroundColor="transparent",
        padding=Padding(0).qss,
        radius=0,
        fontWeight=FontWeight.Normal,
    ),
)

successBg = label.update(**dict(backgroundColor="#4CAF50", color="#FFFFFF"))

errorBg = label.update(**dict(backgroundColor="#F44336", color="#FFFFFF"))

transparentBg = label.update(**dict(backgroundColor="transparent", color="black"))
