from arceion.qt.util import UI, Style

__all__ = ["defaultCalendarGrid"]

# NOTE: dayCellRadius should stay at half of DayCell's fixed size (see
# CalendarGrid.py DayCell.setFixedSize) so selected/today cells render as
# true circles, not rounded squares. 36dp cell -> 18dp radius.

defaultCalendarGrid = Style(
    """
QWidget#CalendarGrid [
    background-color: transparent;
    border: none;
]
QLabel#CalendarGridMonthLabel [
    background: transparent;
    color: {color};
    font-weight: 600;
    font-size: {monthLabelSize}px;
]
QLabel#CalendarGridWeekday [
    background: transparent;
    color: {weekdayColor};
    font-size: {weekdayLabelSize}px;
    font-weight: 500;
]
QPushButton#DayCell [
    background: transparent;
    color: {color};
    border: none;
    border-radius: {dayCellRadius}px;
    font-size: {dayCellFontSize}px;
    padding: 0px;
]
QPushButton#DayCell:hover [
    background-color: {hoverColor};
]
QPushButton#DayCell:disabled [
    color: {disabledColor};
]
QPushButton#DayCellOutside [
    background: transparent;
    color: {outsideColor};
    border: none;
    border-radius: {dayCellRadius}px;
    font-size: {dayCellFontSize}px;
    padding: 0px;
]
QPushButton#DayCellOutside:hover [
    background-color: {hoverColor};
]
QPushButton#DayCellOutside:disabled [
    color: {disabledColor};
]
QPushButton#DayCellToday [
    background: transparent;
    color: {color};
    border: 1px solid {todayBorderColor};
    border-radius: {dayCellRadius}px;
    font-size: {dayCellFontSize}px;
    padding: 0px;
]
QPushButton#DayCellToday:hover [
    background-color: {hoverColor};
]
QPushButton#DayCellSelected [
    background-color: {selectedColor};
    color: {selectedTextColor};
    border: none;
    border-radius: {dayCellRadius}px;
    font-size: {dayCellFontSize}px;
    font-weight: 600;
    padding: 0px;
]
QPushButton#DayCellSelected:hover [
    background-color: {selectedHoverColor};
]
QPushButton#DayCellRangeStart [
    background-color: {rangeEdgeColor};
    color: {rangeEdgeTextColor};
    border: none;
    border-top-left-radius: {dayCellRadius}px;
    border-bottom-left-radius: {dayCellRadius}px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
    font-size: {dayCellFontSize}px;
    font-weight: 600;
    padding: 0px;
]
QPushButton#DayCellRangeStart:hover [
    background-color: {selectedHoverColor};
]
QPushButton#DayCellRangeEnd [
    background-color: {rangeEdgeColor};
    color: {rangeEdgeTextColor};
    border: none;
    border-top-right-radius: {dayCellRadius}px;
    border-bottom-right-radius: {dayCellRadius}px;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    font-size: {dayCellFontSize}px;
    font-weight: 600;
    padding: 0px;
]
QPushButton#DayCellRangeEnd:hover [
    background-color: {selectedHoverColor};
]
QPushButton#DayCellRangeMiddle [
    background-color: {rangeMiddleColor};
    color: {color};
    border: none;
    border-radius: 0px;
    font-size: {dayCellFontSize}px;
    padding: 0px;
]
QPushButton#DayCellRangeMiddle:hover [
    background-color: {rangeMiddleHoverColor};
]
QPushButton#CalendarNavButton [
    background: transparent;
    border: none;
    color: {buttonColor};
    border-radius: {buttonRadius}px;
]
QPushButton#CalendarNavButton:hover [
    background-color: {hoverColor};
]
""",
    **dict(
        color="#FAFAFA",  # foreground
        weekdayColor="#A1A1AA",  # muted-foreground
        monthLabelSize=UI.dp(14),
        weekdayLabelSize=UI.dp(12),
        dayCellRadius=UI.dp(18),
        dayCellFontSize=UI.dp(13),
        hoverColor="#27272A",  # accent
        outsideColor="#52525B",  # dimmer muted text for prev/next month days
        todayBorderColor="#3F3F46",  # ring, subtle outline only
        selectedColor="#FAFAFA",  # primary (dark mode: inverted to light/silver)
        selectedTextColor="#18181B",  # primary-foreground
        selectedHoverColor="#E4E4E7",
        rangeEdgeColor="#FAFAFA",  # same as selectedColor — range endpoints look identical to a single selection
        rangeEdgeTextColor="#18181B",
        rangeMiddleColor="#27272A",  # accent — persistent, not just on hover, unlike DayCell's hoverColor
        rangeMiddleHoverColor="#3F3F46",
        disabledColor="#3F3F46",
        buttonColor="#A1A1AA",  # muted-foreground
        buttonRadius=UI.dp(6),
    ),
)
