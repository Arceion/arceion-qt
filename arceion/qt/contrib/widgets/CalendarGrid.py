from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from arceion.qt.contrib.styles.CalendarGrid import defaultCalendarGrid
from arceion.qt.contrib.widgets.Button import Button
from arceion.qt.util import UI, Style

__all__ = ["CalendarGrid", "DayCell"]


class DayCell(QPushButton):
    """A single selectable day cell inside a CalendarGrid."""

    def __init__(self, day: int, date: QDate, parent: QWidget | None = None):
        super().__init__(str(day), parent)
        self.date = date
        self.setObjectName("DayCell")
        self.setCheckable(True)
        self.setFixedSize(UI.dp(36), UI.dp(36))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._setState("default")

    def _setState(self, state: str) -> None:
        self.setProperty("state", state)  # kept for introspection only, not used by QSS
        # NOTE: state is expressed via objectName, not a `[state="..."]` attribute
        # selector — square-bracket attribute selectors collide with the Style
        # class's own bracket-delimited block syntax and get mangled during the
        # bracket->brace conversion. ObjectName-based IDs avoid that entirely.
        objectName = {
            "today": "DayCellToday",
            "selected": "DayCellSelected",
            "outside": "DayCellOutside",
            "range-start": "DayCellRangeStart",
            "range-middle": "DayCellRangeMiddle",
            "range-end": "DayCellRangeEnd",
        }.get(state, "DayCell")
        self.setObjectName(objectName)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class CalendarGrid(QWidget):
    """
    A shadcn-style calendar: month nav header, weekday row, and a
    6x7 grid of DayCell buttons. Fully QSS-styleable, unlike QCalendarWidget
    whose internal QTableView/QCalendarView painting can't be fully reached.
    """

    dateSelected = pyqtSignal(QDate)

    def __init__(
        self,
        selectedDate: QDate | None = None,
        minimumDate: QDate | None = None,
        maximumDate: QDate | None = None,
        isDateDisabled: Callable[[QDate], bool] | None = None,
        firstDayOfWeek: Qt.DayOfWeek = Qt.DayOfWeek.Sunday,
        selectionMode: str = "single",  # "single" or "range"
        style: str | Style = defaultCalendarGrid,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self._selectionMode = selectionMode
        self._selectedDate = selectedDate
        self._rangeStart: QDate | None = None
        self._rangeEnd: QDate | None = None
        self._minimumDate = minimumDate
        self._maximumDate = maximumDate
        self._isDateDisabled = isDateDisabled
        self._firstDayOfWeek = firstDayOfWeek
        self._style = style

        today = QDate.currentDate()
        base = selectedDate if selectedDate is not None else today
        self._viewMonth = QDate(base.year(), base.month(), 1)

        self.setObjectName("CalendarGrid")
        self.setStyleSheet(self._style if isinstance(self._style, str) else self._style.qss)

        self._dayCells: list[DayCell] = []
        self._buildUi()
        self._renderMonth()

    # ---- UI construction ---------------------------------------------------

    def _buildUi(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(UI.dp(12), UI.dp(12), UI.dp(12), UI.dp(12))
        layout.setSpacing(UI.dp(8))

        header = QHBoxLayout()
        header.setSpacing(0)

        self._prevButton = Button(text="\u2039", onClick=lambda: self._shiftMonth(-1))
        self._prevButton.setObjectName("CalendarNavButton")
        self._prevButton.setFixedSize(UI.dp(28), UI.dp(28))
        self._prevButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self._nextButton = Button(text="\u203a", onClick=lambda: self._shiftMonth(1))
        self._nextButton.setObjectName("CalendarNavButton")
        self._nextButton.setFixedSize(UI.dp(28), UI.dp(28))
        self._nextButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self._monthLabel = QLabel()
        self._monthLabel.setObjectName("CalendarGridMonthLabel")
        self._monthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(self._prevButton)
        header.addWidget(self._monthLabel, stretch=1)
        header.addWidget(self._nextButton)
        layout.addLayout(header)

        self._grid = QGridLayout()
        self._grid.setSpacing(UI.dp(2))
        layout.addLayout(self._grid)

        for col, name in enumerate(self._weekdayLabels()):
            label = QLabel(name)
            label.setObjectName("CalendarGridWeekday")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(UI.dp(36), UI.dp(20))
            self._grid.addWidget(label, 0, col)

    def _weekdayLabels(self) -> list[str]:
        names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        if self._firstDayOfWeek == Qt.DayOfWeek.Monday:
            return names[1:] + names[:1]
        return names

    def _weekdayColumn(self, dayOfWeek: int) -> int:
        # Qt.DayOfWeek: Monday=1 ... Sunday=7
        if self._firstDayOfWeek == Qt.DayOfWeek.Monday:
            return dayOfWeek - 1
        return dayOfWeek % 7  # Sunday(7)->0, Monday(1)->1 ... Saturday(6)->6

    # ---- rendering ----------------------------------------------------------

    def _renderMonth(self) -> None:
        for cell in self._dayCells:
            self._grid.removeWidget(cell)
            cell.deleteLater()
        self._dayCells.clear()

        self._monthLabel.setText(self._viewMonth.toString("MMMM yyyy"))

        firstOfMonth = self._viewMonth
        firstColumn = self._weekdayColumn(firstOfMonth.dayOfWeek())
        gridStart = firstOfMonth.addDays(-firstColumn)

        today = QDate.currentDate()
        cursor = QDate(gridStart)
        for row in range(6):
            for col in range(7):
                cellDate = QDate(cursor)
                cell = DayCell(cellDate.day(), cellDate, self)

                isCurrentMonth = (
                    cellDate.month() == self._viewMonth.month() and cellDate.year() == self._viewMonth.year()
                )
                isToday = cellDate == today
                isDisabled = self._isDateOutOfRange(cellDate) or (
                    self._isDateDisabled is not None and self._isDateDisabled(cellDate)
                )

                if self._selectionMode == "range":
                    isRangeStart = self._rangeStart is not None and cellDate == self._rangeStart
                    isRangeEnd = self._rangeEnd is not None and cellDate == self._rangeEnd
                    isInRange = (
                        self._rangeStart is not None
                        and self._rangeEnd is not None
                        and self._rangeStart < cellDate < self._rangeEnd
                    )

                    if isDisabled:
                        cell.setEnabled(False)
                        cell._setState("disabled")
                    elif isRangeStart and isRangeEnd:
                        cell._setState("selected")  # single-day range: a plain pill, not a flat-sided segment
                    elif isRangeStart:
                        cell._setState("range-start")
                    elif isRangeEnd:
                        cell._setState("range-end")
                    elif isInRange:
                        cell._setState("range-middle")
                    elif isToday:
                        cell._setState("today")
                    elif not isCurrentMonth:
                        cell._setState("outside")
                    else:
                        cell._setState("default")
                else:
                    isSelected = self._selectedDate is not None and cellDate == self._selectedDate
                    if isDisabled:
                        cell.setEnabled(False)
                        cell._setState("disabled")
                    elif isSelected:
                        cell.setChecked(True)
                        cell._setState("selected")
                    elif isToday:
                        cell._setState("today")
                    elif not isCurrentMonth:
                        cell._setState("outside")
                    else:
                        cell._setState("default")

                cell.clicked.connect(lambda _checked, d=cellDate: self._onDayClicked(d))
                self._grid.addWidget(cell, row + 1, col)
                self._dayCells.append(cell)
                cursor = cursor.addDays(1)

    def _isDateOutOfRange(self, d: QDate) -> bool:
        if self._minimumDate is not None and d < self._minimumDate:
            return True
        if self._maximumDate is not None and d > self._maximumDate:
            return True
        return False

    # ---- interaction ---------------------------------------------------------

    def _onDayClicked(self, d: QDate) -> None:
        if self._selectionMode == "single":
            self._selectedDate = d
        if d.month() != self._viewMonth.month() or d.year() != self._viewMonth.year():
            self._viewMonth = QDate(d.year(), d.month(), 1)
        self._renderMonth()
        self.dateSelected.emit(d)

    def _shiftMonth(self, delta: int) -> None:
        self._viewMonth = self._viewMonth.addMonths(delta)
        self._renderMonth()

    # ---- keyboard navigation ---------------------------------------------------

    def keyPressEvent(self, event) -> None:
        focused = self.focusWidget()
        if not isinstance(focused, DayCell):
            super().keyPressEvent(event)
            return

        index = self._dayCells.index(focused)
        key = event.key()

        if key == Qt.Key.Key_Right:
            target = index + 1
        elif key == Qt.Key.Key_Left:
            target = index - 1
        elif key == Qt.Key.Key_Down:
            target = index + 7
        elif key == Qt.Key.Key_Up:
            target = index - 7
        elif key == Qt.Key.Key_PageDown:
            self._shiftMonth(1)
            return
        elif key == Qt.Key.Key_PageUp:
            self._shiftMonth(-1)
            return
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            focused.click()
            return
        else:
            super().keyPressEvent(event)
            return

        if 0 <= target < len(self._dayCells):
            self._dayCells[target].setFocus()

    # ---- public API -------------------------------------------------------------

    def setSelectedDate(self, d: QDate) -> None:
        self._selectedDate = d
        self._viewMonth = QDate(d.year(), d.month(), 1)
        self._renderMonth()

    def setViewDate(self, d: QDate) -> None:
        """Move the visible month to contain `d` without selecting any date."""
        self._viewMonth = QDate(d.year(), d.month(), 1)
        self._renderMonth()

    def setRange(self, start: QDate | None, end: QDate | None) -> None:
        """Set the range anchors (range mode only) and re-render highlighting."""
        self._rangeStart = start
        self._rangeEnd = end
        if start is not None:
            self._viewMonth = QDate(start.year(), start.month(), 1)
        self._renderMonth()

    def selectedRange(self) -> tuple[QDate | None, QDate | None]:
        return (self._rangeStart, self._rangeEnd)

    def selectedDate(self) -> QDate | None:
        return self._selectedDate
