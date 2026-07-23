from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.util import UI, Style

__all__ = ["defaultDatePicker"]
defaultDatePicker = Style(
    """
QFrame [
    background-color: {backgroundColor};
    border: {border};
    border-radius: {radius}px;
    padding: {padding};
]
QCalendarWidget QWidget [
    background-color: {backgroundColor};
    color: {color};
]
QCalendarWidget QAbstractItemView:enabled [
    color: {color};
    selection-background-color: {selectedColor};
    selection-color: {selectedTextColor};
]
QCalendarWidget QAbstractItemView:enabled:hover [
    background-color: {hoverColor};
]
QCalendarWidget QToolButton [
    color: {color};
    background-color: transparent;
]
""",
    **dict(
        backgroundColor="#18181B",
        border="1px solid #27272A",
        radius=UI.dp(6),
        padding=Padding(UI.dp(8)).qss,
        color="#FAFAFA",           # text color — hint: same as defaultButton
        selectedColor="#27272A",   # selected date bg — hint: use a zinc highlight
        selectedTextColor="#FAFAFA",
        hoverColor="#27272A",      # same as defaultButton's hoverColor
    )
)
