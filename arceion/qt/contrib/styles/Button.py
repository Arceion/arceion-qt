from arceion.qt.contrib.enums import BorderStyle, FontWeight
from arceion.qt.contrib.widgets.Attr import Border, Margin, Padding
from arceion.qt.util import UI, Style

__all__ = [
    "defaultButton",
    "destructiveButton",
    "outlineButton",
    "secondaryButton",
    "ghostButton",
    "linkButton",
]


defaultButton = Style(
    """
QToolButton [
	background-color: {backgroundColor};
	color: {color};
	border: {border};
	font-family: {fontFamily};
	font-size: {fontSize}px;
	font-weight: {fontWeight};
	margin: {margin};
	border-radius: {borderRadius}px;
	padding: {padding};
	text-align: {textAlign};
	text-decoration: {textDecoration};
]
QToolButton:hover [
	background-color: {hoverColor};
	text-decoration: {hoverTextDecoration};
	border: {hoverBorder};
]
QToolButton:disabled [
	background-color: {disabledColor};
	color: {disabledTextColor};
]
QToolButton::icon [
	margin: {iconMargin};
]
""",
    **dict(
        fontSize=UI.sp(14),
        fontWeight=FontWeight.Medium,
        fontFamily="'Inter'",
        margin=Margin(0).qss,
        iconMargin=Margin(0).qss,
        borderRadius=UI.dp(10),
        padding=Padding(UI.dp(8), UI.dp(4)).qss,
        textAlign="center",
        textDecoration="none",
        hoverTextDecoration="none",
        border=Border(BorderStyle.NONE).qss,
        hoverBorder=Border(BorderStyle.NONE).qss,
        backgroundColor="#18181B",
        hoverColor="#27272A",
        color="#FAFAFA",
        disabledColor="#F4F4F5",
        disabledTextColor="#A1A1AA",
    ),
)

destructiveButton = defaultButton.update(**dict(backgroundColor="#ff6467", hoverColor="#26ff6467", color="#FF6467"))

secondaryButton = defaultButton.update(
    **dict(
        backgroundColor="#F5F5F5",
        hoverColor="#E5E5E5",
    )
)

outlineButton = defaultButton.update(
    **dict(
        backgroundColor="#0BFFFFFF",
        border=Border("#26FFFFFF", BorderStyle.SOLID, 1).qss,
        hoverColor="#26FFFFFF",
        hoverBorder=Border("#26FFFFFF", BorderStyle.SOLID, 1).qss,
        color="#FFFFFF",
    )
)

ghostButton = defaultButton.update(
    **dict(
        backgroundColor="transparent",
        hoverColor="#26FFFFFF",
        color="#FFFFFF",
    )
)

linkButton = defaultButton.update(
    **dict(
        backgroundColor="transparent",
        hoverColor="transparent",
        color="#FFFFFF",
        hoverTextDecoration="underline",
    )
)
