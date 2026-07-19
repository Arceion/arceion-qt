from arceion.qt.contrib.enums import BorderStyle
from arceion.qt.contrib.widgets.Attr import Border, Margin, Padding
from arceion.qt.util import UI, Style

__all__ = [
    "defaultButton",
    "destructiveButton",
    "outlineButton",
    "secondaryButton",
    "ghostButton",
    "linkButton",
    "pill",
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
	border-radius: {radius}px;
	padding: {padding};
	text-align: {textAlign};
	text-decoration: {textDecoration};
]
QToolButton:hover [
	background-color: {hoverColor};
	text-decoration: {hoverTextDecoration};
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
        fontWeight="500",
        fontFamily="'Inter'",
        margin=Margin(0).qss,
        iconMargin=Margin(0).qss,
        radius=UI.dp(6),
        padding=Padding(UI.dp(8)).qss,
        textAlign="center",
        textDecoration="none",
        hoverTextDecoration="none",
        border=Border(BorderStyle.NONE).qss,
        backgroundColor="#18181B",
        hoverColor="#27272A",
        color="#FAFAFA",
        disabledColor="#F4F4F5",
        disabledTextColor="#A1A1AA",
    ),
)

destructiveButton = defaultButton.update(
    **dict(
        backgroundColor="#EF4444",
        hoverColor="#DC2626",
        color="#FAFAFA",
    )
)

secondaryButton = defaultButton.update(
    **dict(
        backgroundColor="#F4F4F5",
        hoverColor="#E4E4E7",
        color="#18181B",
    )
)

outlineButton = defaultButton.update(
    **dict(
        backgroundColor="transparent",        # no fill
        hoverColor="#272729",                 # subtle tint on hover
        color="#FFFFFF",                      # text color
        border="1px solid #3B82F6",           # primary color border
    )
)

ghostButton = defaultButton.update(
    **dict(
        backgroundColor="transparent",
        hoverColor="#272729",
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


def pill(style: Style) -> Style:
    """
    Wrap any variant Style to get shadcn's `rounded-full` pill shape.
    Usage: Button(text="Save", style=pill(defaultButton))
    """
    return style.update(radius=UI.dp(20))