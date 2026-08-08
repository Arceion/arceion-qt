from arceion.qt.contrib.widgets.Attr import Padding
from arceion.qt.util import UI, Style

__all__ = ["defaultDatePicker"]
defaultDatePicker = Style(
    """
QFrame#DatePickerContainer, QFrame#DateInputContainer, QFrame#DateRangePicker [
    background-color: {backgroundColor};
    border: {border};
    border-radius: {radius}px;
    padding: {padding};
]
QFrame#DatePickerContainer:focus-within, QFrame#DateInputContainer:focus-within [
    border: 1px solid {focusColor};
]
QFrame#DatePickerPopup, QFrame#DateInputPopup, QFrame#DateRangePopup [
    background-color: {popupBackground};
    border: 1px solid {popupBorder};
    border-radius: {popupRadius}px;
    padding: {popupPadding};
]
QLineEdit [
    background: transparent;
    border: none;
    color: {color};
    padding: {inputPadding};
]
QToolButton, QPushButton [
    background: transparent;
    border: none;
    color: {buttonColor};
    padding: {buttonPadding};
    border-radius: {buttonRadius}px;
]
QToolButton:hover, QPushButton:hover [
    background-color: {hoverColor};
]
QCalendarWidget [
    background-color: transparent;
    border: none;
]
QCalendarWidget QWidget [
    background-color: transparent;
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
    border-radius: 999px;
]
QCalendarWidget QToolButton:hover [
    background-color: {hoverColor};
]
QPushButton#DatePickerTrigger [
    background-color: {backgroundColor};
    border: {border};
    border-radius: {radius}px;
    padding: {padding};
    color: {buttonColor};
    text-align: left;
]
QPushButton#DatePickerTrigger:hover [
    background-color: {hoverColor};
]
QPushButton#DatePickerTrigger:focus [
    border: 1px solid {focusColor};
]
""",
    **dict(
        backgroundColor="#171717",
        border="1px solid #E4E4E7",
        radius=UI.dp(10),
        padding=Padding(UI.dp(8)).qss,
        popupBackground="#171717",
        popupBorder="#27272A",
        popupRadius=UI.dp(12),
        popupPadding=Padding(UI.dp(10)).qss,
        inputPadding=Padding(UI.dp(4), UI.dp(8)).qss,
        color="#FAFAFA",
        selectedColor="#FAFAFA",
        selectedTextColor="#171717",
        hoverColor="#27272A",
        buttonColor="#A1A1AA" ,
        buttonPadding=Padding(UI.dp(4), UI.dp(6)).qss,
        buttonRadius=UI.dp(6),
        focusColor="#2563EB",
        focusGlow="#DBEAFE",
    ),
)
